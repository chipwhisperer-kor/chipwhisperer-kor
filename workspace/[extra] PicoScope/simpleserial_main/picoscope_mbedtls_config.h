#ifndef PICOSCOPE_MBEDTLS_CONFIG_H
#define PICOSCOPE_MBEDTLS_CONFIG_H

/*
 * This target compiles only mbedTLS SHA-256. Using the repository-wide
 * mbedTLS config would also enable platform and self-test modules that this
 * bare-metal firmware neither calls nor links.
 */
#define MBEDTLS_SHA256_C

#endif
