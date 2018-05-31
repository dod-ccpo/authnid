#! /bin/bash

DAYS=$((365 * 1000))

key() {
    local key=$1; shift

    if [ ! -f "${key}.pem" ]; then
    	openssl genpkey 2>/dev/null \
	    -paramfile <(openssl ecparam -name prime256v1) \
	    -out "${key}.pem"
    fi
}

req() {
    local key=$1; shift
    local cn=$1; shift

    key "$key"
    openssl req -new -sha256 -key "${key}.pem" 2>/dev/null \
	-config <(printf "[req]\n%s\n%s\n[dn]\nCN=%s\n" \
		   "prompt = no" "distinguished_name = dn" "${cn}")
}

req_nocn() {
    local key=$1; shift

    key "$key"
    openssl req -new -sha256 -subj / -key "${key}.pem" 2>/dev/null \
	-config <(printf "[req]\n%s\n[dn]\nCN_default =\n" \
		   "distinguished_name = dn")
}

cert() {
    local cert=$1; shift
    local exts=$1; shift

    openssl x509 -req -sha256 -out "${cert}.pem" 2>/dev/null \
	-extfile <(printf "%s\n" "$exts") "$@"
}

genroot() {
    local cn=$1; shift
    local key=$1; shift
    local cert=$1; shift
    local skid="subjectKeyIdentifier = hash"
    local akid="authorityKeyIdentifier = keyid"

    exts=$(printf "%s\n%s\n%s\n" "$skid" "$akid" "basicConstraints = CA:true")
    csr=$(req "$key" "$cn")
    echo "$csr" | cert "$cert" "$exts" -signkey "${key}.pem" -set_serial 1 -days "${DAYS}"
}

genca() {
    local cn=$1; shift
    local key=$1; shift
    local cert=$1; shift
    local cakey=$1; shift
    local ca=$1; shift
    local skid="subjectKeyIdentifier = hash"
    local akid="authorityKeyIdentifier = keyid"

    exts=$(printf "%s\n%s\n%s\n" "$skid" "$akid" "basicConstraints = CA:true")
    csr=$(req "$key" "$cn")
    echo "$csr" | cert "$cert" "$exts" -CA "${ca}.pem" -CAkey "${cakey}.pem" \
	    -set_serial 2 -days "${DAYS}" "$@"
}

genee() {
    local cn=$1; shift
    local key=$1; shift
    local cert=$1; shift
    local cakey=$1; shift
    local ca=$1; shift

    exts=$(printf "%s\n%s\n%s\n%s\n%s\n[alts]\n%s\n" \
	    "subjectKeyIdentifier = hash" \
	    "authorityKeyIdentifier = keyid, issuer" \
	    "basicConstraints = CA:false" \
	    "extendedKeyUsage = serverAuth" \
	    "subjectAltName = @alts" "DNS=${cn}")
    csr=$(req "$key" "$cn")
    echo "$csr" |
	cert "$cert" "$exts" -CA "${ca}.pem" -CAkey "${cakey}.pem" \
	    -set_serial 2 -days "${DAYS}" "$@"
}

genss() {
    local cn=$1; shift
    local key=$1; shift
    local cert=$1; shift

    exts=$(printf "%s\n%s\n%s\n%s\n%s\n[alts]\n%s\n" \
	    "subjectKeyIdentifier   = hash" \
	    "authorityKeyIdentifier = keyid, issuer" \
	    "basicConstraints = CA:true" \
	    "extendedKeyUsage = serverAuth" \
	    "subjectAltName = @alts" "DNS=${cn}")
    csr=$(req "$key" "$cn")
    echo "$csr" | cert "$cert" "$exts" -set_serial 1 -days "${DAYS}" -signkey "${key}.pem" "$@"
}

gennocn() {
    local key=$1; shift
    local cert=$1; shift

    csr=$(req_nocn "$key")
    echo "$csr" |
	cert "$cert" "" -signkey "${key}.pem" -set_serial 1 -days -1 "$@"
}

"$@"
