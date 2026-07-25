# [21] CRYSTALS-Dilithium - A Lattice-Based Digital Signature Scheme

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 31
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-21"
derived_asset_id: "PCM-DFA-REF-21-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[21] CRYSTALS-Dilithium - A Lattice-Based Digital Signature Scheme.pdf"
source_sha256: "b95e5d87562661c645236cc8e347d4c2060c17a401f813d650a59c824e6e2116"
pages: 31
bbox_words: 18511
consumed_bbox_words: 18511
numeric_tokens: 2134
consumed_numeric_tokens: 2134
source_blocks: 605
consumed_source_blocks: 605
emitted_blocks: 555
embedded_raster_images: 0
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 31
glyph_chars_removed: 8
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

Léo Ducas 1 , Eike Kiltz 2 , Tancrède Lepoint 3 , Vadim Lyubashevsky 4 , Peter Schwabe 5 , Gregor Seiler 6 and Damien Stehlé 7

2

1 CWI, Netherlands Ruhr Universität Bochum, Germany 3 SRI International, USA 4 IBM Research – Zurich, Switzerland 5 Radboud University, Netherlands 6 IBM Research – Zurich, Switzerland 7 ENS de Lyon, France

Abstract. In this paper, we present the lattice-based signature scheme Dilithium, which is a component of the CRYSTALS (Cryptographic Suite for Algebraic Lattices) suite that was submitted to NIST’s call for post-quantum cryptographic standards. The design of the scheme avoids all uses of discrete Gaussian sampling and is easily implementable in constant-time. For the same security levels, our scheme has a public key that is 2.5X smaller than the previously most efficient lattice-based schemes that did not use Gaussians, while having essentially the same signature size. In addition to the new design, we significantly improve the running time of the main component of many lattice-based constructions – the number theoretic transform. Our AVX2-based implementation results in a speed-up of roughly a factor of 2 over the previously best algorithms that appear in the literature. The techniques for obtaining this speed-up also have applications to other lattice-based schemes. Keywords: Lattice Cryptography · Digital Signatures · Constant-Time Implementa- tion · AVX2

1 Introduction

Cryptography based on the hardness of lattice problems is seen as a very promising replacement of traditional cryptography after the eventual coming of quantum computers. In this paper, we present a new digital signature scheme Dilithium, whose security is based on the hardness of finding short vectors in lattices. We also present its complete optimized implementation, as well as a detailed security analysis of the underlying problems upon which it is based. Our scheme was designed with the following criteria in mind:

Simple to implement securely. The most compact lattice-based signature schemes [DDLL13, DLP14] crucially require the generation of secret randomness from the dis- crete Gaussian distribution. Generating such samples in a way that is secure against side-channel attacks is highly non-trivial and can easily lead to insecure implementations, as demonstrated in [BHLY16, EFGT17, PBY17]. While it may be possible that a very careful implementation can prevent such attacks, it is unreasonable to assume that a universally- deployed scheme containing many subtleties will always be expertly implemented. Dilithium therefore only uses uniform sampling, as was originally proposed in [Lyu09, GLP12, BG14]. Furthermore all other operations (such as polynomial multiplication and rounding) are easily implemented in constant time.

Licensed under Creative Commons License CC-BY 4.0. IACR Transactions on Cryptographic Hardware and Embedded Systems ISSN 2569-2925, Vol. 2018, No. 1, pp. 238–268 DOI:10.13154/tches.v2018.i1.238-268

<!-- PDF_PAGE: 2 -->

## PDF page 2

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

Gen 01 A ← R q k×` 02 (s 1 , s 2 ) ← S η ` × S η k 03 t := As 1 + s 2 04 return (pk = (A, t), sk = (A, t, s 1 , s 2 ))

Sign(sk, M )

239

05 z := ⊥ 06 while z = ⊥ do 07 y ← S γ ` 1 −1 08 w 1 := HighBits(Ay, 2γ 2 ) 09 c ∈ B 60 := H(M k w 1 ) 10 z := y + cs 1 11 if kzk ∞ ≥ γ 1 − β or kLowBits(Ay − cs 2 , 2γ 2 )k ∞ ≥ γ 2 − β, then z := ⊥ 12 return σ = (z, c)

Verify(pk, M , σ = (z, c)) 13 w 1 0 := HighBits(Az − ct, 2γ 2 ) 14 if return Jkzk ∞ &lt; γ 1 − βK and Jc = H (M k w 1 0 )K

Figure 1: Template for our signature scheme.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 2]

Be conservative with parameters. Since we are aiming for long-term security, we have analyzed the applicability of lattice attacks from a very favorable, to the attacker, viewpoint. In particular, we are considering quantum algorithms that require virtually as much space as time. Such algorithms are currently unrealistic, and there seem to be serious obstacles in removing the space requirement, but we are allowing for the possibility that improvements may occur in the future.

Minimize the size of public key + signature. Since many applications require the transmission of both the public key and the signature (e.g. certificate chains), we designed our scheme to minimize the sum of these parameters. Under the restriction that we avoid discrete Gaussian sampling, to the best of our knowledge, Dilithium has the smallest combination of signature and public key sizes of any post-quantum signature scheme.

Be modular – easy to vary security. The two operations that constitute nearly the entirety of the signing and verification procedures are expansion of an XOF (we use SHAKE-128 and SHAKE-256), and multiplication in the polynomial ring Z q [X ]/(X n + 1). Highly efficient implementations of our algorithm will therefore need to optimize these operations and make sure that they run in constant time. For all security levels, our scheme uses the same ring with q = 2 23 − 2 13 + 1 and n = 256. Varying security simply involves doing more/less operations over this ring and doing more/less expansion of the XOF. In other words, once an optimized implementation is obtained for some security level, it is almost trivial to obtain an optimized implementation for a higher/lower level.

### 1.1 Overview of the Basic Approach

The design of the scheme is based on the “Fiat-Shamir with Aborts” approach [Lyu09] and bears most resemblance to the schemes proposed in [GLP12, BG14]. For readers who are unfamiliar with the general framework of such signature schemes, we present a simplified (and less efficient) version of our scheme in Fig. 1. This version is essentially a slightly modified version of the scheme from [BG14]. We will now go through each of its components to give the reader an idea of how such schemes work.

<!-- PDF_PAGE: 3 -->

## PDF page 3

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

240

Key Generation. The key generation algorithm generates a k × ` matrix A each of whose entries is a polynomial in the ring R q = Z q [X ]/(X n + 1). As previously mentioned, we will always have q = 2 23 − 2 13 + 1 and n = 256. Afterwards, the algorithm samples random secret key vectors s 1 and s 2 . Each coefficient of these vectors is an element of R q with small coefficients – of size at most η. Finally, the second part of the public key is computed as t = As 1 + s 2 . All algebraic operations in this scheme are assumed to be over the polynomial ring R q .

Signing Procedure. The signing algorithm generates a masking vector of polynomials y with coefficients less than γ 1 . The parameter γ 1 is set strategically – it is large enough that the eventual signature does not reveal the secret key (i.e. the signing algorithm is zero-knowledge), yet small enough so that the signature is not easily forged. The signer then computes Ay and sets w 1 to be the “high-order” bits of the coefficients in this vector. In particular, every coefficient w in Ay can be written in a canonical way as w = w 1 · 2γ 2 + w 0 where |w 0 | ≤ γ 2 ; w 1 is then the vector comprising all the w 1 ’s. The challenge c is then created as the hash of the message and w 1 . The output c is a polynomial in R q with exactly 60 ±1’s and the rest 0’s. The reason for this distribution is that c has small norm and comes from a domain of size &gt; 2 256 . The potential signature is then computed as z = y + cs 1 . If z were directly output at this point, then the signature scheme would be insecure due to the fact that the secret key would be leaked. To avoid the dependency of z on the secret key, we use rejection sampling. The parameter β is set to be the maximum possible coefficient of cs i . Since c has 60 ±1’s and the maximum coefficient in s i is η, it’s easy to see that β ≤ 60η. If any coefficient of z is larger than γ 1 − β, then we reject and restart the signing procedure. Also, if any coefficient of the low-order bits of Az − ct is greater than γ 2 − β, we restart. The first check is necessary for security, while the second is necessary for both security and correctness. The while loop in the signing procedure keeps being repeated until the preceding two conditions are satisfied. The parameters are set such that the expected number of repetitions is between 4 and 7.

Verification. The verifier first computes w 1 0 to be the high-order bits of Az − ct, and then accepts if all the coefficients of z are less than γ 1 − β and if c is the hash of the message and w 1 0 . Let us look at why verification works, in particular as to why HighBits(Az − ct, 2γ 2 ) = HighBits(Ay, 2γ 2 ). The first thing to notice is that Az − ct = Ay − cs 2 . So all we really need to show is that

(1)

HighBits(Ay, 2γ 2 ) = HighBits(Ay − cs 2 , 2γ 2 ).

The reason for this is that a valid signature will have kLowBits(Ay − cs 2 , 2γ 2 )k ∞ &lt; γ 2 − β. And since we know that the coefficients of cs 2 are smaller than β, we know that adding cs 2 is not enough to cause any carries by increasing any low-order coefficient to have magnitude at least γ 2 . Thus Eq. (1) is true and the signature verifies correctly.

### 1.2 Dilithium

The basic template in Fig. 1 is rather inefficient, as is. The most glaring (but easily fixed) inefficiency is that the public key consists of a matrix of k · ` polynomials, which could have a rather large representation. The obvious fix is to have A generated from some seed ρ using SHAKE-128, and this is a standard technique. The novelty of Dilithium over the previous schemes is that we also shrink the size of the public key by a factor of 2.5 at the expense of increasing the signature by around 150 bytes. For the recommended security level, the scheme has 2.7KB signatures and 1.5KB public keys.

<!-- PDF_PAGE: 4 -->

## PDF page 4

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

241

The main observation for obtaining this very favorable trade-off is that when the verifier computes w 1 0 in Line 13, the high-order bits of Az − ct do not depend too much on the low order bits of t because t is being multiplied by a very low-weight polynomial c. In our scheme, some low-order bits of t are not included in the public key, and so the verifier cannot always correctly compute the high-order bits of Az − ct. To make up for this, the signer includes some “hints” as part of the signature, which are essentially the carries caused by adding in the product of c with the missing low-order bits of t. With this hint, the verifier is able to correctly compute w 1 0 . Additionally, we make our scheme deterministic using the standard technique of adding a seed to the secret key and using this seed together with the message to produce the randomness y in Line 07. Our full scheme in Fig. 4 also makes use of basic optimizations such as pre-hashing the message M so as to not rehash it with every signing attempt.

Implementation Considerations. The main algebraic operation performed in the scheme is a multiplication of a matrix A, whose elements are polynomials in Z q [X ]/(X 256 + 1) by a vector of such polynomials. In our recommended parameter setting, A is a 5 × 4 matrix, and thus the multiplication Av involves 20 polynomial multiplications. As in most lattice-based schemes that are based on operations over polynomial rings, we have chosen our ring so that the multiplication operation has a very efficient implementation via the Number Theoretic Transform (NTT), which is just a version of FFT that works over the finite field Z q rather than over the complex numbers. To enable the NTT, we needed to choose a prime q so that the group Z ∗ q has an element of order 2n = 512; or equivalently q ≡ 1(mod 512). If r is such an element, then X 256 + 1 = (X − r)(X − r 3 ) · · · (X − r 511 ) and thus one can equivalently represent any polynomial a ∈ Z q [X ]/(X 256 + 1) in its CRT (Chinese Remainder Theorem) form as (a(r), a(r 3 ), . . . , a(r 2n−1 )). The advantage of this representation is that the product of two polynomials is coordinate-wise. Therefore the most expensive parts of polynomial multiplication are the transformations a → â and the inverse â → a – these are the NTT and inverse NTT operations. The other major time-consuming operation is the expansion of a seed ρ into the polynomial matrix A. The matrix A is needed for both signing and verification, therefore a good implementation of SHAKE-128 is important for the efficiency of the scheme. The fastest NTT-implementation used in cryptography prior to this work is, to our knowledge, the AVX2 optimized NTT of NewHope [ADPS16] which uses floating point arithmetic. In our implementation, we resort to the more natural choice of using integer arithmetic, as for example also in [LN16]. Although we pack only 4 coefficients into one vector register of 256 bits, which is the same density that is also used by floating point implementations, we can improve on the multiplication speed by about a factor of 2 compared to the NewHope NTT adapted to the prime and degree used in Dilithium, see Table 1.2. We achieved this speed-up by carefully scheduling the instructions and interleaving the multiplications and reductions during the NTT so that parts of the multiplication latencies are hidden. 1 The effect of our fast NTT on the entire Dilithium scheme is a speed-up of 25% for signing and 15% for verification compared to the same implementation with the adapted floating point NTT from NewHope. We point out that in this implementation only the NTT and SHAKE are vectorized. By vectorizing other parts of the implementation like sampling and vector addition, a faster NTT would result in an even greater speed-up. Similarly, if one uses a faster algorithm for seed expansion of ρ into A (or perhaps has A already stored in memory if speed is truly of the essence), then the effect on the signing and (especially) verification algorithms will also be magnified.

1 When the prime in the NTT is smaller than in Dilithium, additional improvements to the current algorithm produce a bigger speed-up (see Table 1.2 and [Sei18]).

<!-- PDF_PAGE: 5 -->

## PDF page 5

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

242

Table 1: Haswell cycle counts on an Intel i7-4770 CPU in terms of 10 3 cycles of different AVX2 optimized NTT implementations for Dilithium and NewHope. Dilithium uses the ring Z q [X ]/(X 256 + 1) with q = 2 23 − 2 13 + 1 and NewHope Z q [X ]/(X 1024 + 1) with q = 2 13 + 2 12 + 1. The cycle count for the forward NTT given in [ADPS16] is smaller than the cycle count of the inverse NTT because it is measured without the bitreversal operation. This operation can be left out if the input polynomial is randomly sampled with independent coefficients. In Dilithium this is not always the case, and so we compare the cycle counts including the bitreversal. The ADPS implementation for Dilithium is the floating point AVX2 implementation from NewHope [ADPS16] adapted to the Dilithium prime and degree. The LN implementation is the integer AVX2 implementation from [LN16]. Finally, the implementation for NewHope in the last row is similar to the one from this work but with major additional improvements that are not applicable to Dilithium, see [Sei18].

Dilithium

ADPS 3.2

LN -

This work 1.5

### 1.3 Related Work

NewHope

9.5

9.7

### 2.2 [Sei18]

The first asymptotically-efficient lattice-based signature scheme using the “Fiat-Shamir with Aborts” approach was constructed in [Lyu09] based on the Ring-SIS problem. The efficiency of the scheme was improved in [Lyu12] by basing the scheme on the combination of (Ring)-LWE and (Ring)-SIS problems. These schemes were further improved upon in [GLP12, BG14] by reducing the size of the signature. All the previous works had security proofs in the classical random oracle model. Schemes based on the hardness of (Ring)-LWE in the quantum random oracle model were instantiated from “lossy identification” schemes [AFLT12] in [ABB + 17] and [KLS17]. The latter work also showed that one could base the quantum security of all the schemes listed in the previous paragraph (as well as the scheme in this paper) on a non-interactive problem that’s a convolution of a lattice problem with a cryptographic hash function. The main disadvantage of schemes based only on (Ring)-LWE is that they are less efficient – they have substantially larger public key / signature sizes and also need to be instantiated over rings in which one cannot do NTT.

2 Basic Operations

### 2.1 Ring Operations

We let R and R q respectively denote the rings Z[X ]/(X n + 1) and Z q [X ]/(X n + 1), for q an integer. Throughout this paper, the value of n will always be 256 and q will be the prime 8380417 = 2 23 − 2 13 + 1. Regular font letters denote elements in R or R q (which includes elements in Z and Z q ) and bold lower-case letters represent column vectors with coefficients in R or R q . By default, all vectors will be column vectors. Bold upper-case letters are matrices. For a vector v, we denote by v T its transpose. The boolean operator JstatementK evaluates to 1 if statement is true, and to 0 otherwise.

<!-- PDF_PAGE: 6 -->

## PDF page 6

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

243

Modular reductions. For an even (resp. odd) positive integer α, we define r 0 = r mod ± α α−1 0 to be the unique element r 0 in the range − α 2 &lt; r 0 ≤ α 2 (resp. − α−1 2 ≤ r ≤ 2 ) such 0 that r ≡ r mod α. We will sometimes refer to this as a centered reduction modulo q. For any positive integer α, we define r 0 = r mod + α to be the unique element r 0 in the range 0 ≤ r 0 &lt; α such that r 0 ≡ r mod α. When the exact representation is not important, we simply write r mod α.

Sizes of elements. For an element w ∈ Z q , we write kwk ∞ to mean |w mod ± q|. We define the ` ∞ and ` 2 norms for w = w 0 + w 1 X + . . . + w n−1 X n−1 ∈ R: p kwk ∞ = max kw i k ∞ , kwk = kw 0 k 2 ∞ + . . . + kw n−1 k 2 ∞ .

i

Similarly, for w = (w 1 , . . . , w k ) ∈ R k , we define

kwk ∞ = max kw i k ∞ , kwk =

i

p

kw 1 k 2 + . . . + kw k k 2 .

We will write S η to denote all elements w ∈ R such that kwk ∞ ≤ η.

### 2.2 NTT domain representation

Our modulus q is chosen such that there exists a 512-th root of unity r modulo q. Concretely, we always work with r = 1753. This implies that the cyclotomic polynomial X 256 + 1 splits into linear factors X − r i modulo q with i = 1, 3, 5, . . . , 511. By the Chinese remainder theorem our cyclotomic ring R q is thus isomorphic to the product of the rings Z q [X ]/(X − r i ) ∼ = Z q . In this product of rings it is easy to multiply elements since the multiplication is pointwise there. The isomorphism Y a 7→ a(r), a(r 3 ), . . . , a(r 511 ) : R q → Z q [X ]/(X − r i )

i

can be computed quickly with the help of the Fast Fourier Transform. Since X 256 + 1 = X 256 − r 256 = (X 128 − r 128 )(X 128 + r 128 ) one can first compute the map

Z q [X ]/(X 256 + 1) → Z q [X ]/(X 128 − r 128 ) × Z q [X ]/(X 128 + r 128 )

and then continue separately with the two reduced polynomials of degree less than 128 noting that X 128 + r 128 = X 128 − r 384 . We give further detail about our NTT implementations in Section 5.1.

### 2.3 Hashing

Our scheme uses several different algorithms that hash strings in {0, 1} ∗ onto domains of various forms. Below we give the high level descriptions of these functions and defer the details of how exactly they are used in our signature scheme to Section 5.2.

Hashing to a Ball. Let B h denote the set of elements of R that have h coefficients that are either −1 or 1 and the rest are 0. We have |B h | = 2 h · nh . For our signature scheme, we will need a cryptographic hash function that hashes onto B 60 (which has more than 2 256 elements). The algorithm we will use to create a random element in B 60 is sometimes referred to as an “inside-out” version of the Fisher-Yates shuffle, and its high-level description is in Fig. 2. 2

2 Normally, the algorithm should begin at i = 0, but since there are 196 0’s, the first 195 iterations would just be setting components of c to 0.

<!-- PDF_PAGE: 7 -->

## PDF page 7

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

244

SampleInBall 01 Initialize c = c 0 c 1 . . . c 255 = 00 . . . 0 02 for i := 196 to 255 03 j ← {0, 1, . . . , i} 04 s ← {0, 1} 05 c i := c j 06 c j := (−1) s 07 return c

Figure 2: Create a random 256-element array with 60 ±1’s and 196 0 0 s

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 7]

Expanding the Matrix A. The function ExpandA maps a uniform seed ρ ∈ {0, 1} 256 to a matrix A ∈ R q k×l in CRT representation.

Sampling the vectors y. The function ExpandMask, used for deterministically generating the randomness of the signature scheme, maps K k µ k κ to y ∈ S γ l 1 −1 .

Collision resistant hash. The function CRH used in our signature scheme is a collision resistant hash function mapping to {0, 1} 384 .

### 2.4 High/Low Order Bits and Hints

To reduce the size of the public key, we will need some simple algorithms that extract “higher-order” and “lower-order” bits of elements in Z q . The goal is that when given an arbitrary element r ∈ Z q and another small element z ∈ Z q , we would like to be able to recover the higher order bits of r + z without needing to store z. We therefore define algorithms that take r, z and produce a 1-bit hint h that allows one to compute the higher order bits of r + z just using r and h. This hint is essentially the “carry” caused by z in the addition. There are two different ways in which we will break up elements in Z q into their “high- order” bits and “low-order” bits. The first algorithm, Power2Round q , is the straightforward bit-wise way to break up an element r = r 1 · 2 d + r 0 where r 0 = r mod ± 2 d and r 1 = (r − r 0 )/2 d . Notice that if we choose the representatives of r 1 to be non-negative integers between 0 and bq/2 d c, then the distance (modulo q) between any two r 1 · 2 d and r 1 0 · 2 d is usually ≥ 2 d , except for the border case. In particular, the distance modulo q between bq/2 d c · 2 d and 0 could be very small. This is problematic in the case that we would like to produce a 1-bit hint, as adding a small number to r can actually cause the high-order bits of r to change by more than 1. We avoid having the high-order bits change by more than 1 with a simple tweak. We select an α that is a divisor of q − 1 and write r = r 1 · α + r 0 in the same way as before. For the sake of simplicity, we assume that α is even (which is possible, as q is odd). The possible r 1 · α’s are now {0, α, 2α, . . . , q − 1}. Note that the distance between q − 1 and 0 is 1, and so we remove q − 1 from the set of possible r 1 · α’s, and simply round the corresponding r’s to 0. Because q − 1 and 0 differ by 1, all this does is possibly increase the magnitude of the remainder r 0 by 1. This procedure is called Decompose q . Using this procedure as a sub-routine, we can define the MakeHint q and UseHint q routines that produce a hint and, respectively, use the hint to recover the high-order bits of the sum. For notational convenience, we also define HighBits q and LowBits q routines that simply extract r 1 and r 0 , respectively, from the output of Decompose q . The below Lemmas state the crucial properties of these supporting algorithms that are necessary for the correctness and security of our scheme. Their proofs can be found in

<!-- PDF_PAGE: 8 -->

## PDF page 8

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

Power2Round q (r, d) 08 r := r mod + q 09 r 0 := r mod ± 2 d 10 return (r − r 0 )/2 d , r 0

MakeHint q (z, r, α)

11 r 1 := HighBits q (r, α) 12 v 1 := HighBits q (r + z, α) 13 return Jr 1 6 = v 1 K

UseHint q (h, r, α) 14 m := (q − 1)/α 15 (r 1 , r 0 ) := Decompose q (r, α) 16 if h = 1 and r 0 &gt; 0 return (r 1 + 1) mod + m 17 if h = 1 and r 0 ≤ 0 return (r 1 − 1) mod + m 18 return r 1

245

Decompose q (r, α)

19 r := r mod + q 20 r 0 := r mod ± α 21 if r − r 0 = q − 1 22 then r 1 := 0; r 0 := r 0 − 1 23 else r 1 := (r − r 0 )/α 24 return (r 1 , r 0 )

HighBits q (r, α) 25 (r 1 , r 0 ) := Decompose q (r, α) 26 return r 1

LowBits q (r, α)

27 (r 1 , r 0 ) := Decompose q (r, α) 28 return r 0

Figure 3: Supporting algorithms for Dilithium.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 8]

Appendix A.

Lemma 1. Suppose that q and α are positive integers satisfying q &gt; 2α, q ≡ 1 (mod α) and α even. Let r and z be vectors of elements in R q where kzk ∞ ≤ α/2, and let h, h 0 be vectors of bits. Then the HighBits q , MakeHint q , and UseHint q algorithms satisfy the following properties:

1. UseHint q (MakeHint q (z, r, α), r, α) = HighBits q (r + z, α).

2. Let v 1 = UseHint q (h, r, α). Then kr − v 1 · αk ∞ ≤ α + 1. Furthermore, if the number of 1’s in h is ω, then all except at most ω coefficients of r − v 1 · α will have magnitude at most α/2 after centered reduction modulo q.

3. For any h, h 0 , if UseHint q (h, r, α) = UseHint q (h 0 , r, α), then h = h 0 .

Lemma 2. If ksk ∞ ≤ β and kLowBits q (r, α)k ∞ &lt; α/2 − β, then

HighBits q (r, α) = HighBits q (r + s, α).

3 Signature

The Key Generation, Signing, and Verification algorithms for our signature scheme are presented in Fig. 4. We present the deterministic version of the scheme in which the ran- domness used in the signing procedure is generated (using SHAKE-256) as a deterministic function of the message and a small secret key. Since our signing procedure may need to be repeated several times until a signature is produced, we also append a counter in order to make the SHAKE-256 output differ with each signing attempt of the same message. Also due to the fact that each message may require several iterations to sign, we compute an initial digest of the message using a collision-resistant hash function, and use this digest in place of the message throughout the signing procedure. As discussed in Section 1.2, the main design improvement of Dilithium over the scheme in Fig. 1 is that the public key size is reduced by a factor of around 2.5 at the expense of an additional hundred bytes in the signature. To accomplish the size reduction, the key generation algorithm outputs t 1 := Power2Round q (t, d) as the public key instead of t as

<!-- PDF_PAGE: 9 -->

## PDF page 9

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

246

Gen 01 ρ ← {0, 1} 256 02 K ← {0, 1} 256 03 (s 1 , s 2 ) ← S η ` × S η k 04 A ∈ R q k×` := ExpandA(ρ) A is stored in NTT Domain Representation 05 t := As 1 + s 2 06 (t 1 , t 0 ) := Power2Round q (t, d) 07 tr ∈ {0, 1} 384 := CRH(ρ k t 1 ) 08 return (pk = (ρ, t 1 ), sk = (ρ, K , tr, s 1 , s 2 , t 0 ))

Sign(sk, M ) 09 A ∈ R q k×` := ExpandA(ρ) A is stored in NTT Domain Representation 10 µ ∈ {0, 1} 384 := CRH(tr k M ) 11 κ := 0, (z, h) := ⊥ 12 while (z, h) = ⊥ do 13 y ∈ S γ ` 1 −1 := ExpandMask(K k µ k κ) 14 w := Ay 15 w 1 := HighBits q (w, 2γ 2 ) 16 c ∈ B 60 := H(µ k w 1 ) 17 z := y + cs 1 18 (r 1 , r 0 ) := Decompose q (w − cs 2 , 2γ 2 ) 19 if kzk ∞ ≥ γ 1 − β or kr 0 k ∞ ≥ γ 2 − β or r 1 6 = w 1 , then (z, h) := ⊥ 20 else 21 h := MakeHint q (−ct 0 , w − cs 2 + ct 0 , 2γ 2 ) 22 if kct 0 k ∞ ≥ γ 2 or the # of 1’s in h is greater than ω, then (z, h) := ⊥ 23 κ := κ + 1 24 return σ = (z, h, c)

Verify(pk, M , σ = (z, h, c)) 25 A ∈ R q k×` := ExpandA(ρ) A is stored in NTT Domain Representation 26 µ ∈ {0, 1} 384 := CRH(CRH(ρ k t 1 ) k M ) 27 w 1 0 := UseHint q (h, Az − ct 1 · 2 d , 2γ 2 ) 28 return Jkzk ∞ &lt; γ 1 − βK and Jc = H (µ k w 1 0 )K and J# of 1’s in h is ≤ ωK

Figure 4: Our signature scheme Dilithium.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 9]

in Fig. 1. This means that instead of dlog qe bits per coefficient, the public key requires dlog qe − d bits. In our instantiation, q ≈ 2 23 and d = 14, which means that instead of 23 bits in each public key coefficient, there are instead 9. The main problem with not having the entire t in the public key is that the verification algorithm is no longer able to exactly compute w 1 0 in Line 13 in Fig. 1. In order to do this, the verification algorithm will need the high order bits of Az − ct, but it can only compute Az − ct 1 · 2 d = Az − ct + ct 0 . But since the product ct 0 consists of only small numbers, and we only care about the high order bits, we really only need to know the carries that each coefficient ct 0 causes. These are the carries that the signer sends as a hint to the verifier. Heuristically, based on our parameter choices, there should not be more than ω positions in which a carry is caused. The signer therefore simply sends the positions in which these carries occur (this is the extra bytes in the signature), which allows the verifier to compute the high order bits of Az − ct.

### 3.1 Correctness

In this section, we prove the correctness of the signature scheme.

<!-- PDF_PAGE: 10 -->

## PDF page 10

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

247

Table 2: Parameters for Dilithium.

q d weight of c γ 1 = (q − 1)/16 γ 2 = γ 1 /2 (k, `) η β ω

pk size (bytes) sig size (bytes) Exp. reps (from Eq. (5))

BKZ block-size b to break SIS Best Known Classical bit-cost Best Known Quantum bit-cost Best Plausible bit-cost

BKZ block-size b to break LWE Best Known Classical bit-cost Best Known Quantum bit-cost Best Plausible bit-cost

Gen median cycles (Haswell) Sign median cycles (Haswell) Sign average cycles (Haswell) Verify median cycles (Haswell)

Gen median cycles (AVX2, Haswell) Sign median cycles (AVX2, Haswell) Sign average cycles (AVX2, Haswell) Verify median cycles (AVX2, Haswell)

If kct 0 k ∞ &lt; γ 2 , then by Lemma 1 we know that

weak medium recommended very high

8380417 14 60 523776 261888 (3, 2) 7 375 64

8380417 14 60 523776 261888 (4, 3) 6 325 80

8380417 14 60 523776 261888 (5, 4) 5 275 96

8380417 14 60 523776 261888 (6, 5) 3 175 120

896 1387 4.3

1184 2044 5.9

1472 2701 6.6

1760 3366 4.3

235 68 62 48

355 103 94 73

475 138 125 98

605 176 160 125

200 58 53 41

340 100 91 71

485 141 128 100

595 174 158 124

157, 596 736, 564 917, 585 188, 628

260, 468 1, 252, 496 1, 597, 555 293, 068

386, 268 1, 804, 738 2, 326, 829 409, 904

507, 616 1, 677, 924 2, 152, 901 551, 452

91, 940 359, 462 450, 438 102, 820

144, 662 567, 614 722, 372 148, 096

218, 724 789, 926 1, 035, 284 209, 292

280, 448 749, 148 947, 865 284, 284

UseHint q (h, w − cs 2 + ct 0 , 2γ 2 ) = HighBits q (w − cs 2 , 2γ 2 ) .

Since w = Ay and t = As 1 + s 2 , we have that

(2)

w − cs 2 = Ay − cs 2 = A(z − cs 1 ) − cs 2 = Az − ct,

and w − cs 2 + ct 0 = Az − ct 1 · 2 d . Therefore the verifier computes

UseHint q (h, Az − ct 1 · 2 d , 2γ 2 ) = HighBits q (w − cs 2 , 2γ 2 ) .

Furthermore, because the signer also checks in Line 19 that r 1 = w 1 , this is equivalent

to

(3)

HighBits q (w − cs 2 , 2γ 2 ) = HighBits q (w, 2γ 2 ).

Therefore, the w 1 computed by the verifier is the same as that of the signer, and the verification procedure will always accept.

<!-- PDF_PAGE: 11 -->

## PDF page 11

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

248

### 3.2 Number of Iterations

We now want to compute the probability that Step 19 will set (z, h) to ⊥. The probability that kzk ∞ &lt; γ 1 − β can be computed by considering each coefficient separately. For each coefficient σ of cs 1 , the corresponding coefficient of z will be between −γ 1 + β + 1 and γ 1 − β − 1 (inclusively) whenever the corresponding coefficient of y i is between −γ 1 + β + 1 − σ and γ 1 − β − 1 − σ. The size of this range is 2(γ 1 − β) − 1, and the coefficients of y have 2γ 1 − 1 possibilities. Thus the probability that every coefficient of y is in the good range is

256·`

2(γ 1 − β) − 1 2γ 1 − 1

= 1 −

`n

β γ 1 − 1/2

≈ e −256·β`/γ 1 ,

(4)

where we used the fact that our values of γ 1 are large compared to 1/2. We now move to computing the probability that we have

kr 0 k ∞ = kLowBits q (w − cs 2 , 2γ 2 )k ∞ &lt; γ 2 − β .

If we (heuristically) assume that the low order bits are uniformly distributed modulo 2γ 2 , then there is a 256·k 2(γ 2 − β) − 1 ≈ e −256·βk/γ 2 2γ 2

probability that all the coefficients are in the good range (using the fact that our values of β are large compared to 1/2). As we already mentioned, if kcs 2 k ∞ ≤ β, then kr 0 k ∞ &lt; γ 2 − β implies that r 1 = w 1 . Thus the last check should succeed with overwhelming probability when the previous check passed. Therefore, the probability that Step 19 passes is

≈ e −256·β(`/γ 1 +k/γ 2 ) .

(5)

It is more difficult to formally compute the probability that Step 22 results in a restart. The parameters were set such that heuristically (z, h) = ⊥ with probability less than 1%. Therefore the vast majority of the loop repetitions will be caused by Step 19.

4 Security

The standard security notion for digital signatures is UF-CMA security, which is security under chosen message attacks. In this security model, the adversary gets the public key and has access to a signing oracle to sign messages of his choice. The adversary’s goal is to come up with a valid signature of a new message. A slightly stronger security requirement that is sometimes useful is SUF-CMA (Strong Unforgeability under Chosen Message Attacks), which also allows the adversary to win by producing a different signature of a message that he has already seen. It can be shown that in the (classical) random oracle model, Dilithium is SUF-CMA secure based on the hardness of the standard MLWE and MSIS lattice problems. The reduction, however, is not tight. Furthermore, since we also care about quantum attackers, we need to consider the security of the scheme when the adversary can query the hash function on a superposition of inputs (i.e. security in the quantum random oracle model – QROM). Since the classical security proof uses the “forking lemma” (which is essentially rewinding), the reduction does not transfer over to the quantum setting. There are no counter-examples of schemes whose security is actually affected by the non-tightness of the reduction. For example, schemes like Schnorr signatures [Sch89], GQ signatures [GQ88], etc. all set their parameters ignoring the non-tightness of the reduction.

<!-- PDF_PAGE: 12 -->

## PDF page 12

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

249

Furthermore, the only known uses of the additional power of quantum algorithms against schemes whose security is based on quantum-resistant problems under a classical reduction involve “Grover-type” algorithms that improve exhaustive search (although it has been shown that there cannot be a “black-box” proof that the Fiat-Shamir transform is secure in the QROM [ARU14]). The reason that there haven’t been any attacks taking advantage of the non-tightness of the reduction is because there is an intermediate problem which is tightly equivalent, even under quantum reductions, to the UF-CMA security of the signature scheme. This problem is essentially a “convolution” of the underlying mathematical problem (such as MSIS or discrete log) with a cryptographic hash function H. It would appear that as long as there is no relationship between the structure of the math problem and H, solving this intermediate problem is not easier than solving the mathematical problem. 3 Below, we will introduce the hardness assumptions upon whose hardness the SUF-CMA security of our scheme is based. The first two assumptions, MLWE and MSIS, are standard lattice problems which are a generalization of LWE, Ring-LWE, SIS, and Ring-SIS. The third problem, SelfTargetMSIS is the aforementioned problem that’s based on the combined hardness of MSIS and the hash function H. In the classical ROM, there is a (non-tight) reduction from MSIS to SelfTargetMSIS.

### 4.1 Assumptions

The MLWE Problem. For integers m, k, and a probability distribution D : R q → [0, 1], we say that the advantage of algorithm A in solving the decisional MLWE m,k,D problem over the ring R q is

m×k Adv MLWE ; t ← R q m ; b ← A(A, t)] m,k,D := Pr[b = 1 | A ← R q

− Pr[b = 1 | A ← R q m×k ; s 1 ← D k ; s 2 ← D m ; b ← A(A, As 1 + s 2 )] .

The MSIS Problem. To an algorithm A we associate the advantage function Adv MSIS m,k,γ to solve the (Hermite Normal Form) MSIS m,k,γ problem over the ring R q as m×k Adv MSIS ; y ← A(A) . m,k,γ (A) := Pr 0 &lt; kyk ∞ ≤ γ ∧ [ I | A ] · y = 0 | A ← R q

The SelfTargetMSIS Problem. Suppose that H : {0, 1} ∗ → B 60 is a cryptographic hash function. To an algorithm A we associate the advantage function

Adv SelfTargetMSIS (A) := H,m,k,γ r 0 ≤ kyk ∞ ≤ γ m×k |H(·)i Pr A ← R q ; y := , M ← A (A) . c ∧ H([ I | A ] · y k M ) = c

### 4.2 Signature Scheme Security

The concrete security of Dilithium was analyzed in [KLS17], where it was shown that if H is a quantum random oracle (i.e., a quantum-accessible perfect hash function), the advantage of an adversary A breaking the SUF-CMA security of the signature scheme is

SelfTargetMSIS - CMA MLWE −254 4 Adv SUF (C) + Adv MSIS , Dilithium (A) ≤ Adv k,`,D (B) + Adv H,k,`+1,ζ k,`,ζ 0 (D) + 2

(6)

3 In the ROM, there is indeed a (non-tight) reduction using the forking lemma that states that solving this problem is as hard as solving the underlying mathematical problem. 4 To simplify the concrete security bound, we assume that ExpandA produces a uniform matrix A ∈ R k×` , q ExpandMask(K , ·) is a perfect pseudo-random function, and CRH is a perfect collision-resistant hash function.

<!-- PDF_PAGE: 13 -->

## PDF page 13

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

250

for D a uniform distribution over S η , and

ζ = max{γ 1 − β, 2γ 2 + 1 + 2 d−1 · 60} ≤ 4γ 2 ,

(7)

ζ 0 = max{2(γ 1 − β), 4γ 2 + 2} ≤ 4γ 2 + 2.

(8)

Furthermore, if the running times and success probabilities (i.e. advantages) of A, B, C, D are t A , t B , t C , t D , A , B , C , D , then the lower bound on t A / A is within a small multiplicative factor of min t i / i for i ∈ {B, C, D}. Intuitively, the MLWE assumption is needed to protect against key-recovery, the SelfTargetMSIS is the assumption upon which new message forgery is based, and the MSIS assumption is needed for strong unforgeability. We will now sketch some parts of the security proof that are relevant to the concrete parameter setting.

### 4.2.1 UF-CMA Security Sketch

It was shown in [KLS17] that for zero-knowledge deterministic signature schemes, if an adversary having quantum access to H and classical access to a signing oracle can produce a forgery of a new message, then there is also an adversary who can produce a forgery without access to the signing oracle (so he only gets the public key). 5 The latter security model is called UF-NMA – unforgeability under no-message attack. By the MLWE assumption, the public key (A, t = As 1 + s 2 ) is indistinguishable from (A, t) where t is chosen uniformly at random. The proof that our signature scheme is zero-knowledge is fairly standard and follows the framework from [Lyu09, Lyu12, BG14]. It is formally proved in [KLS17] 6 and we sketch the proof in Appendix B. If we thus assume that the MLWE k,`,D problem is hard, where D is the distribution that samples a uniform integer in the range [−η, η], then to prove UF-NMA security, we only need to analyze the hardness of the experiment where the adversary receives a random (A, t) and then needs to output a valid message/signature pair M , (z, h, c) such that

• kzk ∞ &lt; γ 1 − β

• H(UseHint q (h, Az − ct 1 · 2 d , 2γ 2 )kM ) = c

• # of 1’s in h is ≤ ω

Lemma 1 implies that one can rewrite

UseHint q (h, Az − ct 1 · 2 d , 2γ 2 ) = Az − ct 1 · 2 d + u,

(9)

where kuk ∞ ≤ 2γ 2 + 1. Furthermore, only ω coefficients of u will have magnitude greater than γ 2 . If we write t = t 1 · 2 d + t 0 where kt 0 k ∞ ≤ 2 d−1 , then we can rewrite Eq. (9) as

Az − ct 1 · 2 d + u = Az − c(t − t 0 ) + u = Az − ct + (ct 0 + u) = Az − ct + u 0 .

Note that the worst-case upper-bound for u 0 is

(10)

ku 0 k ∞ ≤ kct 0 k ∞ + kuk ∞ ≤ kck 1 · kt 0 k ∞ + kuk ∞ ≤ 60 · 2 d−1 + 2γ 2 + 1 &lt; 4γ 2 .

5 It was also shown in [KLS17] that the “deterministic” part of the requirement can be relaxed. The security proof simply loses a factor of the number of different signatures produced per message in its tightness. Thus, for example, if one were to implement the signature scheme (with the same secret key) on several devices with different random-number generators, the security of the scheme would not be affected much. 6 In that paper, it is actually proved that the underlying zero-knowledge proof is zero-knowledge and then the security of the signature scheme follows via black box transformations.

<!-- PDF_PAGE: 14 -->

## PDF page 14

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

251

Thus a (quantum) adversary who is successful at creating a forgery of a new message is able to find z, c, u 0 , M such that kzk ∞ &lt; γ 1 − β, kck ∞ = 1, ku 0 k ∞ &lt; 4γ 2 , and M ∈ {0, 1} ∗ such that     z H  [ A | t | I k ] ·  c  k M  = c. (11) u 0

Since (A, t) is completely random, this is exactly the definition of the SelfTargetMSIS problem from above. A standard forking lemma argument can be used to show that an adversary solving the above problem in the (standard) random oracle model can be used to solve the MSIS problem. While giving a reduction using the forking lemma is a good “sanity check”, it is not particularly useful for setting parameters due to its lack of tightness. So how does one set parameters? The Fiat-Shamir transform has been used for over 3 decades (and we have been aware of the non-tightness of the forking lemma for two of them), yet the parameter settings for schemes employing it have ignored this loss in tightness. Implicitly, therefore, these schemes rely on the exact hardness of analogues (based on various assumptions such as discrete log [Sch89], one-wayness of RSA [GQ88], etc.) of the problem in Eq. (11). The intuition for the security of the problem in Eq. (11) (and its discrete log, RSA, etc. analogues) is as follows: since H is a cryptographic hash function whose structure is completely independent of the algebraic structure of its inputs, choosing some M “strategically” should not help – so the problem would be equally hard if the M were fixed. Then, again relying on the independence of H and the algebraic structure of its inputs, the only approach for obtaining a solution appears to be picking some w, computing H( w k M ) = c, and then finding z, u 0 such that Az + u 0 = w + ct. 7 The hardness of finding such z, u 0 with ` ∞ -norms less than 4γ 2 such that

Az + u 0 = t 0

(12)

for some t 0 is the problem whose concrete security we will be analyzing. Note that this is conservative because in Eq. (11) kzk ∞ &lt; γ 1 − β ≈ 2γ 2 . Furthermore, only ω coefficients of u 0 can be larger than 2γ 2 .

The Addition of the Strong Unforgeabilty Property

4.2.2

To handle the strong-unforgeability requirement, one needs to handle an additional case. Intuitively, the reduction from UF-CMA to UF-NMA used the fact that a forgery of a new message will necessarily require the use of a challenge c for which the adversary has never seen a valid signature (i.e., (z, h, c) was never an output by the signing oracle). To prove strong-unforgeability, we also have to consider the case where the adversary sees a signature (z, h, c) for M and then only changes (z, h). In other words, the adversary ends up with two valid signatures such that

UseHint q (h, Az − ct 1 · 2 d , 2γ 2 ) = UseHint q (h 0 , Az 0 − ct 1 · 2 d , 2γ 2 ).

By Lemma 1, the above equality can be shown to imply that there exist kzk ∞ ≤ 2(γ 1 − β) and kuk ∞ ≤ 4γ 2 + 2 such that Az + u = 0.

### 4.3 Concrete Security Analysis

In Appendix C, we describe the best known lattice attacks against the problems in Eq. (6) upon which the security of our signature scheme is based. The best attacks involve finding short vectors in some lattice. The main difference between the MLWE and MSIS

7 This is indeed the (non-tight) proof sketch in the classical random oracle model.

<!-- PDF_PAGE: 15 -->

## PDF page 15

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

252

problems is that the MLWE problem involves finding a short vector in a lattice in which an “unusually short” vector exists. The MSIS problem, on the other hand, involves just finding a short vector in a random lattice. In knapsack terminology, the MLWE problem is a low-density knapsack, while MSIS is a high-density knapsack instance. The analysis for the two instances is slightly different and we analyze the MLWE problem in Appendix C.2 and the MSIS problem (as well as SelfTargetMSIS) in Appendix C.3. We follow the general methodology from [ADPS16, BCD + 16] to analyze the security of our signature scheme, with minor adaptations. This methodology is significantly more conservative than prior ones used in lattice-based cryptography. In particular, we assume the adversary can run the asymptotically best algorithms known, with no overhead compared to the asymptotic run-times. In particular, we assume the adversary can cheaply handle huge amounts of (possibly quantum) memory. This conservatism is in line with the goal of long-term post-quantum security. We note that despite this security analysis methodology, our schemes remain competitive in practice. While the MLWE and MSIS problems are defined over polynomial rings, we do not currently have any way of exploiting this ring structure, and therefore the best attacks are mounted by simply viewing these problems as LWE and SIS problems. The LWE and SIS problems are exactly as in the definitions of MLWE and MSIS in Section 4.1 with the ring R q being replaced by Z q .

5 Implementation Details

### 5.1 NTT domain representation

Natural fast NTT implementations do not output vectors with coefficients in the order a(r), a(r 3 ), . . . , a(r 511 ). Therefore we define the NTT domain representation â ∈ Z 256 of q a polynomial a ∈ R q to have coefficients in the order as output by our reference NTT. Concretely, â = (a(r 0 ), a(−r 0 ), . . . , a(r 127 ), a(−r 127 ))

where r i = r brv(128+i) with brv(k) the bitreversal of the 8 bit number k. This is important for sampling the matrix A. The matrix A is only needed for multiplication. Hence, for the sake of faster implementations, the expansion function ExpandA does not output A ∈ R q k×l . Instead it outputs a matrix with coefficients in Z 256 q , which is interpreted as the NTT domain representation of A. As A needs to be sampled uniformly and the NTT is an isomorphism, ExpandA also needs to sample uniformly in this representation. To be compatible to Dilithium, an implementation whose NTT produces differently ordered vectors than our reference NTT needs to sample coefficients in a non-consecutive order.

### 5.2 Hashing

Hashing to a Ball. We now precisely describe the operation of the function H : µ k w 1 7→ c ∈ B 60 described in Fig. 2 as it is used in our signature scheme. The vector w 1 consists of k polynomials w 1,0 , . . . , w 1,k−1 in R q with coefficients in {0, . . . , 15}. This allows w 1 to be packed in a string of k · 256 · 4/8 = k · 128 bytes. Concretely, the bytes numbers 128i to 128i + 127, i = 0, . . . , k − 1, encode the coefficients of w 1,i in increasing order, where each byte encodes two consecutive coefficients of w 1,i in its low 4 bits and high 4 bits, respectively. For example, the first two coefficients c 0 and c 1 of w 1,i are encoded in the 128i th byte of the bit-packed string of w 1 as c 1 · 16 + c 0 . H then absorbs the 384-bit string µ immediately followed by the k · 128 bytes for w 1 into SHAKE-256. Throughout its operations the function squeezes SHAKE-256 in order to obtain a stream of random bytes of variable length. The first 60 bits in the first 8 bytes

<!-- PDF_PAGE: 16 -->

## PDF page 16

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

253

of this random stream are interpreted as 60 random sign bits s i ∈ {0, 1}. The remaining 4 bits are discarded. Then H uses Algorithm 2 to compute c where in each iteration of the for loop it uses rejection sampling on elements from {0, . . . , 255} until it gets a j ∈ {0, . . . , i}. An element in {0, . . . , 255} is obtained by interpreting the next byte of the random stream from SHAKE-256 as a number in this set. For the sign s the corresponding s i−196 is used.

Expanding the Matrix A. The function ExpandA maps a uniform seed ρ ∈ {0, 1} 256 to a matrix A ∈ R q k×l in NTT domain representation. It computes each coefficient â i,j ∈ Z 256 q of A separately. For the coefficient â i,j it absorbs the 32 bytes of ρ immediately followed by one byte representing 0 ≤ 16 · j + i &lt; 255 into SHAKE-128. Next it uses consecutive blocks of 3 bytes of the variable-length output string in order to obtain a sequence of integers between 0 and 2 23 − 1. This is done by setting the highest bit of the third byte in each block to zero and interpreting the blocks in little endian byte order. So for example the three bytes b 0 , b 1 and b 2 from SHAKE-128 are used to get the integer 0 ≤ b 2 0 · 2 16 + b 1 · 2 8 + b 0 ≤ 2 23 − 1 where b 2 0 is the logical AND of b 2 and 2 128 − 1. Finally, ExpandA performs rejection sampling on these 23-bit integers to sample the 256 coefficients a i,j (r 0 ), a i,j (−r 0 ), . . . , a i,j (r 127 )a i,j (−r 127 ) of â i,j uniformly from the set {0, . . . , q − 1} in the order of our NTT domain representation.

Sampling the vectors y. The function ExpandMask maps K k µ k κ to y ∈ S γ l 1 −1 , where κ ≥ 0, and works as follows. It computes each of the l coefficients of y, which are polynomials in S γ 1 −1 , independently. For the i-th polynomial, 0 ≤ i &lt; l, it absorbs 32 bytes of K concatenated with the 48 bytes of µ and two bytes representing lκ + i in little endian byte order into SHAKE-256. Then each block of 5 consecutive output bytes is used to get two 20 bit integers between 0 and 2 20 − 1. For this the first two bytes of each output block together with a third byte having as lower 4 bits the lower 4 bits of the third output byte and 4 high zero bits is interpreted in little endian order. Then the high 4 bits of the third output byte followed by the 16 bits of the fourth and and fifth byte are interpreted as the second 20 bit integer. As an example assume we have received the five bytes b 0 , . . . , b 4 from SHAKE-128. Then ExpandMask computes the two integers 0 ≤ b 2 0 · 2 16 + b 1 · 2 8 + b 0 ≤ 2 20 − 1 and 0 ≤ b 4 · 2 12 + b 3 · 2 4 + b 2 00 ≤ 2 20 − 1 where b 2 0 is the AND of b 2 and 15 and b 2 0 = [b 2 /16]. On the resulting sequence of 20 bit integers rejection sampling is performed to get 256 values v j ∈ {0, . . . , 2γ 1 − 2}. From these the polynomial coefficients are computed in increasing order as q + γ 1 − 1 − v j .

Collision resistant hash. The function CRH in Figure 4 is a collision resistant hash function. For this purpose 384 bits of the output of SHAKE-256 are used. CRH is called with two different sets of inputs. First it is called with ρ k t 1 . The function then absorbs the 32 bytes of ρ followed by the k · 256 · 9/8 bytes for the bit-packed representation of t 1 into SHAKE-256 and takes the first 48 bytes of the first output block of SHAKE-256 as the output hash. The bit-packing for t 1 is done in the same way as described above for w 1 . As always integers are read in little endian byte order. The second input is µ k M . Here the concatenation of the hash µ and the message string are absorbed into SHAKE-256 and the first 48 output bytes are used as the resulting hash.

### 5.3 Data layout of keys and signature

Public key. The public key, containing ρ and t 1 , is stored as the concatenation of the bit-packed representations of ρ and t 1 in this order. Therefore, it has a size of 32 + 288k bytes.

<!-- PDF_PAGE: 17 -->

## PDF page 17

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

254

Secret key. The secret key contains ρ, K , tr, s 1 , s 2 and t 0 and is also stored as a bit- packed representation of these quantities in the given order. We explain the bit-packing of s 1 , s 2 and t 0 . The polynomials inside s 1 and s 2 have coefficients with infinity norm at most η. So every coefficient c ∈ Z q of these polynomials can be represented by c = q + η − v with some v ∈ {0, . . . , 2η}. In the bit packing the values v are stored so that each polynomial needs 256 · 4/8 bytes for the weak, medium and recommended security levels, and 256 · 3/8 bytes for the very high security level. The coefficients of the polynomials of t 0 can be written in the form q + 2 d−1 − v with v ∈ {0, . . . , 2 d − 1} and the representation by these v is used in the bit packing. Hence, this results in 256 · d/8 bytes per polynomial. Consequently, a secret key requires 64 + 48 + 32((k + l) · dlog (2η + 1)e + 14k) bytes. For the weak, medium and high security level this is equal to 112 + 576k + 128l bytes. With the very high security parameters one needs 112 + 544k + 96l = 3856 bytes.

Signature. The signature bit string is the concatenation of a bit packed representation of z and encodings of h and c in this order. The coefficients of the polynomials of z are written in the form q + γ 1 − 1 − v with v ∈ {0, . . . , 2γ 1 − 2} and these values v are bit packed resulting in 256 · 20/8 bytes per polynomial. Next we describe the encoding of h, which needs ω + K bytes. Together all the polynomials in the vector h have at most ω non-zero coefficients. It is sufficient to store the locations of these non-zero coefficients. Each of the first ω bytes of the bit string representing h is the index i of the next non-zero coefficient in its polynomial, i.e. 0 ≤ i ≤ 255, or zero if there are no more non-zero coefficients. The bytes numbers ω up to ω + k − 1 record the k positions j of the polynomial boundaries in the string of ω coefficient indices, where 0 ≤ j ≤ ω. In the encoding of the challenge c, the first 256 bits are 0 or 1 when the corresponding coefficient of c is zero or non-zero, respectively. The next 60 bits are 0 or 1 if the corresponding non-zero coefficient is 1 or −1, respectively. Note that there are precisely 60 non-zero coefficients. The 4 bits up to the next byte boundary are zero. Therefore, a signature requires 640l + ω + k + 40 bytes.

### 5.4 Constant time implementation

Our reference implementation does not branch depending on secret data and does not access memory locations that depend on secret data. For the modular reductions that are needed for the arithmetic in R q we never use the ’%’ operator of the C programming language. Instead we use Montgomery reductions without the correction steps and special reduction routines that are specific to our modulus q. For computing the rounding functions described in Section 2.4, we have implemented branching-free algorithms. On the other hand, when it is safe to reveal information, we have not tried to make the code constant-time. This includes the computation of the challenges and the rejection conditions in the signing algorithm. When performing rejection sampling, our code reveals which of the conditions was the reason for the rejection, and in case of the norm checks, which coefficient violated the bound. This is safe since the rejection probabilities for each coefficient are independent of secret data. The challenges reveal information about CRH(µ k w 1 ) also in the case of rejected y, but this does not reveal any information about the secret key when CRH is modeled as a random oracle and w 1 has high min-entropy.

### 5.5 Reference implementation

Our reference NTT is a natural iterative implementation for 32 bit unsigned integers that uses Cooley-Tukey butterflies in the forward transform and Gentleman-Sande butterflies in the inverse transform. For modular reductions after multiplying with a precomputed root of unity we use the Montgomery algorithm as was already done before in e.g. [ADPS16]. In order that the reduced values are correct representatives, the precomputed roots contain the Montgomery factor 2 32 mod q. We also use Montgomery reductions after the pointwise

<!-- PDF_PAGE: 18 -->

## PDF page 18

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

255

product of the polynomials in the NTT domain representations. Since we cannot get the Montgomery factor in at this point, these products are in fact Hensel remainders r 0 ≡ r2 32 (mod q). We then make use of the fact that the NTT transform is linear and multiply by an additional Montgomery factor after the inverse NTT when we divide out the factor 256. The implementations of the functions ExpandA and ExpandMask initially squeeze a number of output blocks of SHAKE-256 and SHAKE-128 that gives enough randomness with high probability. In the case of ExpandA, which samples uniform polynomials and hence needs at least 3 · 256 = 768 random bytes per polynomial, 5 blocks from SHAKE-128 of 168 bytes each are needed at least for one polynomial. They suffice with probability greater than 1 − 2 −132 . ExpandMask initially retrieves 5 blocks from SHAKE-256 that have 136 bytes. This is the minimum number of blocks and suffices with probability greater than 1 − 2 −81 . As mentioned in the introduction our reference implementation is protected against timing attacks. For this reason the centralized remainders in the rounding functions given in Figure 3 are not computed with branchings. Instead we use the following well-known trick to compute the centralized remainder r 0 = r mod ± α where 0 ≤ r ≤ 3α/2. Subtracting α/2 + 1 from r yields a negative result if and only if r ≤ α/2. Therefore, shifting this result arithmetically to the right by 31 bits gives −1, i.e. the integer with all bits equal to 1, if r ≤ α/2 and 0 otherwise. Then the logical AND of the shifted value and α is added to r and α/2 − 1 subtracted. This results in r − α if r &gt; α/2 and r if r ≤ α/2, i.e. the centralized remainder. We make heavy use of lazy reduction in our implementation. In the NTT we do not reduce the results of additions and subtractions at all. For rounding and norm checking it is important to map to standard representatives. This freezing of the coefficients is achieved in constant-time by conditionally subtracting q with another instance of the arithmetic right shift trick.

### 5.6 AVX2 optimized implementation

We have written an optimized implementation of Dilithium for CPUs that supports the AVX2 instruction set. Since the two most time-consuming operations are polynomial multiplication and the expansion of the matrix and vectors, the optimized implementation speeds up these two operations. For polynomial multiplication, we have implemented a vectorized version of the NTT. This NTT achieves a full multiplication of two polynomials including three NTTs and the pointwise multiplication in less than 5000 Haswell cycles and is about a factor of 4.5 faster than the reference C code compiled using gcc with full machine-specific optimizations turned on. We do not use floating point instructions, where modular reductions are easily done by multiplying with a floating point inverse of q and rounding to get the quotient from which the remainder can be computed with another multiplication and a subtraction. Instead, we use integer instructions only and the same Montgomery reduction methodology as in the reference C code. At any time our AVX2 optimized NTT has 32 unsigned integer coefficients, of 32 bits each, loaded into 8 AVX2 vector registers. Each of these vector registers then contains 4 extended 64 bit coefficients. So after three levels of NTT the reduced polynomials fit completely into these 8 registers and we can transform them to linear factors without further loads and stores. In the second last and last level the polynomials have degree less than 4. This means that every polynomial fits into one register but only half of the coefficients need to be multiplied by roots. For this reason we shuffle the vectors in order to group together coefficients that need to be multiplied. The instruction that we use for this task are perm2i128 in the second last level and a combination of vpshufd and vpblendd in the last level. The multiplications with the constant roots of unity are performed using the vpmuludq instruction. This instruction computes a full 64 bit product

<!-- PDF_PAGE: 19 -->

## PDF page 19

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

256

of two 32 bit integers. It has a latency of 5 cycles on both Haswell and Skylake. In each level of the NTT half of the coefficients need to be multiplied. Therefore we can do four vector multiplications and Montgomery reductions in parallel. This hides some of the latency of the multiplication instructions. For faster matrix and vector expansion, we use a vectorized SHAKE implementation that operates on 4 parallel sponges and hence can absorb and squeeze blocks in and out of these 4 sponges at the same time. For sampling this means that up to four coefficients can be sampled simultaneously.

### 5.7 Computational Efficiency

We have performed timing experiments with our reference implementation on a Haswell CPU. The results are presented in Table 2. They include the number of CPU cycles needed by the three operations key generation, signing and signature verification. These numbers are the medians of 10000 executions each. For the signing operation we also give the average number of cycles because the use of rejection sampling during signing has the effect that sometimes more time is needed than is indicated by the median cycle counts. Signing was performed with a message size of 32 bytes. The computer we have used is equipped with an Intel Core i7-4770K CPU running at the constant clock frequency of 3500 Mhz. Hyperthreading and Turbo Boost are switched off. The system runs Debian stable with Linux Kernel version 3.16.0 and the code was compiled with gcc 6.3.0.

6 Comparisons

There are three major approaches for post-quantum signatures: hash-based signatures, multivariate signatures, and lattice-based signatures. Applications that can securely maintain a state (i.e., a constantly changing secret key) will certainly want to adopt stateful hash-based signatures like XMSS [BDH11], which is currently being standardized by the crypto forum research group (CFRG) of IETF. However, many applications are unlikely to migrate to a signature scheme that becomes insecure if, for example, the secret key is part of a backup and is restored to an older state. In their call for proposals, NIST therefore explicitly asks for stateless signature proposals. We present a comparison of our digital signature to other lattice-based and non-lattice-based schemes in Table 3.

Non-Lattice-Based Signatures. Arguably the most conservative approach to digital signature construction is using stateless hash-based signatures that come with tight reductions in the standard model to standard properties of a cryptographic hash function, like collision resistance or second-preimage resistance. Unfortunately, stateless hash-based signatures are rather inefficient in terms of signature size and signing speed. For example, the SPHINCS signature scheme has signatures of about 40 KB and takes about 50 million cycles to sign even on large Intel processors with the AVX2 vector instruction set. Applications that need small signatures may want to turn their attention to multivariate signature schemes like Rainbox or HFEv-. These small signatures, however, come at the expense of rather large public keys. Many applications, for instance TLS, need to transmit public keys almost as much as signatures, so what becomes important is the sum of the public-key size and signature size. Also, efficient multivariate signature schemes do not enjoy a reduction from the MQ problem. Instead these schemes require a hidden structure in the instance of the MQ problem, which was a weakness exploited by many attacks on prior protocols (c.f. [KS98, DFSS07, FGP + 15, TW12]). At Asiacrypt 2016, Chen, Hülsing, Rijneveld, Samardjiska, and Schwabe presented MQDSS [CHR + 16], a multivariate signature scheme that does have a reduction from MQ, but this reduction comes at the price of signatures that are not shorter than SPHINCS signatures.

<!-- PDF_PAGE: 20 -->

## PDF page 20

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

257

Lattice-Based Signatures. The most efficient (in terms of key and signature sizes) lattice- based schemes are those based on the hardness of the NTRU problem. The one with the smallest key/signature combination [DLP14] uses the key-generation of [HHGP + 03] to create lattices which are optimal for using the secure signing algorithm in [GPV08]. The “Fiat-Shamir with Aborts” based scheme BLISS [DDLL13] is also based on the hardness of finding short vectors in NTRU lattices and has slightly larger parameters. While the above schemes have the smallest outputs of all lattice-based schemes, they contain several downsides. The most important one is that the schemes crucially require sampling from the discrete Gaussian distribution, and to the best of our knowledge no constant-time implementations of these schemes exist due to this “feature”. 8 A second downside is that the security of these schemes is based on NTRU rather than Ring/Module- LWE. The geometric structure of NTRU lattices has been recently exploited [KF17] to produce significantly better attacks against large-modulus/small-secret version of the problem (these attacks, though, currently do not extend to the parameters used in digital signatures). The final downside is that increasing/decreasing the security levels would require a complete re-implementation of the schemes. In particular, it is not possible to efficiently instantiate them in a way that constructs the public key out of small blocks, as in this paper. At the other extreme of lattice constructions are digital signatures based on the hardness of standard lattice problems without any algebraic structure. The main downside of these schemes (c.f. [Lyu12, ABB + 17]) is that they have extremely large public keys, and are not suitable for many practical applications. Carefully optimized signatures based on the hardness of ideal or module lattice problems sit in the sweet spot that offers reasonably small signatures and public keys, good signing and verification speeds, and simple constant-time implementations. In particular, the combined size of the public key and signature of the scheme in the current paper is smaller than in all the non-lattice-based schemes that we are aware of. Starting from [Lyu09], there have been many improvements and implementations of this type of scheme (e.g. [Lyu12, GLP12, GOPS13, BG14]). The most practical one of these that existed prior to the current work is [BG14], which is essentially the scheme in Fig. 1. Since Dilithium reduces the public key of that scheme by a factor ≈ 2.5 (saving over 2KB) at the expense of an additional 100 bytes in the signature, it is the most efficient of all those contained in this line of work. We should mention that it is also possible to produce slightly-shorter parameters (around 10 - 15% saving in the signature size) if one samples from the Gaussian distribution, but we believe that this saving does not justify the added complexity of securely implementing the scheme.

8 A recent work [MW17] addresses some issues, but their implementation still uses lookup tables which are not protected against side-channel attacks.

<!-- PDF_PAGE: 21 -->

## PDF page 21

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

258

Table 3: Comparison of post-quantum signature schemes. Benchmarks were performed on an Intel Core i7-4770K (Haswell) if not indicated otherwise. The “sec” column states the security as reported by the authors of the respective papers. Cycles are stated for signing (S) and verification (V). Bytes are given for public keys (pk), and signatures (s). The column “ct?” indicates whether the software is protected against timing attacks.

Scheme

sec

ct? Cycles Bytes

NTRU-based lattice signature schemes

NTRU-GPV [DLP14] (adapted to a 1024-dim instance) a

128

128

BLISS [DDLL13] (adapted to a 1024-dim instance) a

no

S: V:

?? ??

pk: s:

1 792 ≈ 1 200

no

S: V:

?? ??

pk: s:

1 792 ≈ 1 700

Ring/Module-lattice-Based signature schemes

Dilithium, recomm. param. (this paper)

125

yes

S: V:

789K 209K

pk: s:

1 472 2 701

Standard-lattice-based signature schemes

+

TESLA-I [ABB 17]

98 yes

S: V:

143 402K 19 284K

pk: s:

12MB 2 444

Stateless hash-based signature schemes

+

SPHINCS [BHH 15]

128

51 636K b 1 451K b

yes

S: V:

pk: s:

1 056 41 000

Multivariate signature schemes

HmFEv(256,15,3,16) [CLP + 17] 128

Rainbow(16,32,32,32) [CLP + 17] 128

MQDSS [CHR + 16]

128

1 497K c 15K c

yes

S: V:

pk: s:

83 100 61

68K c 22K c

yes

S: V:

pk: s:

145 500 48

yes

S: V:

8 510K 5 752K

pk: s:

72 40 952

a The scheme in the paper used a different security analysis and therefore considered instances of

dimensions (i.e. 512) that are not secure enough using the security analysis in the current paper. Doubling the dimension to 1024 makes these schemes well over 128-bit quantum-secure. We adjusted the approximate parameters to match this increase in the instance size. We should point out that it might also be possible to increase the dimension to less than 1024 by not using a ring of the form Z[X]/(X N + 1). This may reduce the parameters of the schemes. b Benchmarked on an Intel Xeon E3-1275 (Haswell) c Benchmarked on an Intel Xeon E3-1245 v3 (Haswell)

<!-- PDF_PAGE: 22 -->

## PDF page 22

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

Acknowledgements

259

We are very thankful to the referees for their useful suggestions. This work is supported by the European Commission through the ICT program under contracts ICT-645622 (PQCRYPTO), ICT-644729 (SAFEcrypto), and through the ERC Starting Grant ERC- 2013-StG-335086 (LATTAC). It is also supported by the Swiss National Science Foundation through the 2014 transfer ERC Starting Grant CRETP2-166734 (FELICITY) and by the Netherlands Organization for Scientific Research (NWO) through Veni grant 639.021.645 (Cryptanalysis of Lattice-based Cryptography).

### References

[ABB + 17]

Erdem Alkim, Nina Bindel, Johannes A. Buchmann, Özgür Dagdelen, Edward Eaton, Gus Gutoski, Juliane Krämer, and Filip Pawlega. Revisiting TESLA in the quantum random oracle model. In PQCrypto, pages 143–162, 2017. 242, 257, 258

[ADPS16]

Erdem Alkim, Léo Ducas, Thomas Pöppelmann, and Peter Schwabe. Post- quantum key exchange – a new hope. In Proceedings of the 25th USENIX Security Symposium, pages 327–343. USENIX Association, 2016. http: //cryptojedi.org/papers/#newhope. 241, 242, 252, 254, 266

[AFLT12]

Michel Abdalla, Pierre-Alain Fouque, Vadim Lyubashevsky, and Mehdi Ti- bouchi. Tightly-secure signatures from lossy identification schemes. In EUROCRYPT, pages 572–590, 2012. 242

[AG11]

Sanjeev Arora and Rong Ge. New algorithms for learning in presence of errors. In Luca Aceto, Monika Henzinger, and Jiri Sgall, editors, ICALP 2011, Part I, volume 6755 of LNCS, pages 403–415. Springer, Heidelberg, July 2011. 267

[ARU14]

Andris Ambainis, Ansis Rosmanis, and Dominique Unruh. Quantum attacks on classical proof systems: The hardness of quantum rewinding. In FOCS, pages 474–483, 2014. 249

[BCD + 16]

Joppe W. Bos, Craig Costello, Léo Ducas, Ilya Mironov, Michael Naehrig, Valeria Nikolaenko, Ananth Raghunathan, and Douglas Stebila. Frodo: Take off the ring! Practical, quantum-secure key exchange from LWE. In Edgar R. Weippl, Stefan Katzenbeisser, Christopher Kruegel, Andrew C. Myers, and Shai Halevi, editors, ACM CCS 16, pages 1006–1018. ACM Press, October 2016. 252

[BDGL16]

Anja Becker, Léo Ducas, Nicolas Gama, and Thijs Laarhoven. New directions in nearest neighbor searching with applications to lattice sieving. In Robert Krauthgamer, editor, 27th SODA, pages 10–24. ACM-SIAM, January 2016. 264

[BDH11]

Johannes A. Buchmann, Erik Dahmen, and Andreas Hülsing. XMSS - A prac- tical forward secure signature scheme based on minimal security assumptions. In PQCrypto, pages 117–129, 2011. 256

[BG14]

Shi Bai and Steven D. Galbraith. An improved compression technique for signatures based on learning with errors. In CT-RSA, pages 28–47, 2014. 238, 239, 242, 250, 257, 264

<!-- PDF_PAGE: 23 -->

## PDF page 23

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

260

[BHH + 15]

Daniel J. Bernstein, Daira Hopwood, Andreas Hülsing, Tanja Lange, Ruben Niederhagen, Louiza Papachristodoulou, Michael Schneider, Peter Schwabe, and Zooko Wilcox-O’Hearn. SPHINCS: practical stateless hash-based signa- tures. In Marc Fischlin and Elisabeth Oswald, editors, Advances in Cryptology – EUROCRYPT 2015, volume 9056 of LNCS, pages 368–397. Springer, 2015. http://cryptojedi.org/papers/#sphincs. 258

[BHLY16]

Leon Groot Bruinderink, Andreas Hülsing, Tanja Lange, and Yuval Yarom. Flush, gauss, and reload - A cache attack on the BLISS lattice-based signature scheme. In CHES, pages 323–345, 2016. 238

[BKW03]

Avrim Blum, Adam Kalai, and Hal Wasserman. Noise-tolerant learning, the parity problem, and the statistical query model. J. ACM, 50(4):506–519, 2003. 267

[BS16]

Jean-François Biasse and Fang Song. Efficient quantum algorithms for com- puting class groups and solving the principal ideal problem in arbitrary degree number fields. In Robert Krauthgamer, editor, 27th SODA, pages 893–902. ACM-SIAM, January 2016. 267

[CDPR16]

Ronald Cramer, Léo Ducas, Chris Peikert, and Oded Regev. Recovering short generators of principal ideals in cyclotomic rings. In Marc Fischlin and Jean-Sébastien Coron, editors, EUROCRYPT 2016, Part II, volume 9666 of LNCS, pages 559–585. Springer, Heidelberg, May 2016. 267

[CDW17]

Ronald Cramer, Léo Ducas, and Benjamin Wesolowski. Short Stickelberger class relations and application to ideal-SVP. In EUROCRYPT (1), volume 10210 of Lecture Notes in Computer Science, pages 324–348, 2017. 267

[CGS14]

Peter Campbell, Michael Groves, and Dan Shepherd. Soliloquy: A cautionary tale. In ETSI 2nd Quantum-Safe Crypto Workshop, pages 1–9, 2014. 267

[CHR + 16]

Ming-Shing Cheng, Andreas Hülsing, Joost Rijneveld, Simona Samardjiska, and Peter Schwabe. From 5-pass MQ-based identification to MQ-based signatures. In Jung Hee Cheon and Tsuyoshi Takagi, editors, Advances in Cryptology – ASIACRYPT 2016, volume 10032 of LNCS, page 135–165. Springer, 2016. http://cryptojedi.org/papers/#mqdss. 256, 258

[CLP + 17]

Ming-Shing Chen, Wen-Ding Li, Bo-Yuan Peng, Bo-Yin Yang, and Chen-Mou Cheng. Implementing 128-bit secure mpkc signatures. Cryptology ePrint Archive, Report 2017/636, 2017. http://eprint.iacr.org/2017/636/. 258

[CN11]

Yuanmi Chen and Phong Q. Nguyen. BKZ 2.0: Better lattice security estimates. In Dong Hoon Lee and Xiaoyun Wang, editors, ASIACRYPT 2011, volume 7073 of LNCS, pages 1–20. Springer, Heidelberg, December 2011. 264

[DDLL13]

Léo Ducas, Alain Durmus, Tancrède Lepoint, and Vadim Lyubashevsky. Lattice signatures and bimodal gaussians. In CRYPTO (1), pages 40–56, 2013. 238, 257, 258

[DFSS07]

Vivien Dubois, Pierre-Alain Fouque, Adi Shamir, and Jacques Stern. Practical cryptanalysis of SFLASH. In Alfred Menezes, editor, Advances in Cryptology – CRYPTO 2007, volume 4622 of LNCS, pages 1–12. Springer, 2007. https: //eprint.iacr.org/2007/14. 256

[DLP14]

Léo Ducas, Vadim Lyubashevsky, and Thomas Prest. Efficient identity-based encryption over NTRU lattices. In ASIACRYPT, pages 22–41, 2014. 238, 257, 258

<!-- PDF_PAGE: 24 -->

## PDF page 24

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

[EFGT17]

261

Thomas Espitau, Pierre-Alain Fouque, Benoit Gerard, and Mehdi Ti- bouchi. Side-channel attacks on bliss lattice-based signatures – exploit- ing branch tracing against strongswan and electromagnetic emanations in microcontrollers. Cryptology ePrint Archive, Report 2017/505, 2017. http://eprint.iacr.org/2017/505 To appear in CCS 2017. 238

[FGP + 15]

Jean-Charles Faugère, Danilo Gligoroski, Ludovic Perret, , Simona Samard- jiska, and Enrico Thomae. A polynomial-time key-recovery attack on MQQ cryptosystems. In Jonathan Katz, editor, Public-Key Cryptogra- phy – PKC 2015, volume 9020 of LNCS, pages 150–174. Springer, 2015. https://eprint.iacr.org/2014/811. 256

[GLP12]

Tim Güneysu, Vadim Lyubashevsky, and Thomas Pöppelmann. Practical lattice-based cryptography: A signature scheme for embedded systems. In CHES, pages 530–547, 2012. 238, 239, 242, 257

[GOPS13]

Tim Güneysu, Tobias Oder, Thomas Pöppelmann, and Peter Schwabe. Soft- ware speed records for lattice-based signatures. In PQCrypto, volume 7932 of Lecture Notes in Computer Science, pages 67–82. Springer, 2013. 257

[GPV08]

Craig Gentry, Chris Peikert, and Vinod Vaikuntanathan. Trapdoors for hard lattices and new cryptographic constructions. In STOC, pages 197–206, 2008. 257

[GQ88]

Louis C. Guillou and Jean-Jacques Quisquater. A "paradoxical" indentity- based signature scheme resulting from zero-knowledge. In CRYPTO, pages 216–231, 1988. 248, 251

[HHGP + 03] Jeffrey Hoffstein, Nick Howgrave-Graham, Jill Pipher, Joseph H. Silverman, and William Whyte. Ntrusign: Digital signatures using the ntru lattice. In CT-RSA, pages 122–140, 2003. 257

[HPS11]

Guillaume Hanrot, Xavier Pujol, and Damien Stehlé. Analyzing blockwise lattice algorithms using dynamical systems. In Phillip Rogaway, editor, CRYPTO 2011, volume 6841 of LNCS, pages 447–464. Springer, Heidelberg, August 2011. 264

[KF17]

Paul Kirchner and Pierre-Alain Fouque. Revisiting lattice attacks on over- stretched NTRU parameters. In EUROCRYPT (1), volume 10210 of Lecture Notes in Computer Science, pages 3–26, 2017. 257, 267

[KLS17]

Eike Kiltz, Vadim Lyubashevsky, and Christian Schaffner. A concrete treat- ment of fiat-shamir signatures in the quantum random-oracle model. Cryp- tology ePrint Archive, Report 2017/916, 2017. http://eprint.iacr.org/ 2017/916. To appear in Eurocrypt 2018. 242, 249, 250, 264

[KS98]

Aviad Kipnis and Adi Shamir. Cryptanalysis of the Oil &amp; Vinegar signature scheme. In Hugo Krawczyk, editor, Advances in Cryptology – CRYPTO ’98, volume 1462 of LNCS, pages 257–266. Springer, 1998. 256

[Laa15]

Thijs Laarhoven. Search problems in cryptography. PhD thesis, Eindhoven University of Technology, 2015. 264

[LN16]

Patrick Longa and Michael Naehrig. Speeding up the number theoretic transform for faster ideal lattice-based cryptography. In Cryptology and Network Security - 15th International Conference, CANS 2016, Milan, Italy, November 14-16, 2016, Proceedings, pages 124–139, 2016. 241, 242

<!-- PDF_PAGE: 25 -->

## PDF page 25

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

262

[Lyu09]

Vadim Lyubashevsky. Fiat-Shamir with aborts: Applications to lattice and factoring-based signatures. In ASIACRYPT, pages 598–616, 2009. 238, 239, 242, 250, 257

[Lyu12]

Vadim Lyubashevsky. Lattice signatures without trapdoors. In EUROCRYPT, pages 738–755, 2012. 242, 250, 257, 264

[MW17]

Daniele Micciancio and Michael Walter. Gaussian sampling over the integers: Efficient, generic, constant-time. In CRYPTO, pages 455–485, 2017. 257

[PBY17]

Peter Pessl, Leon Groot Bruinderink, and Yuval Yarom. To bliss-b or not to be - attacking strongswan’s implementation of post-quantum signatures. Cryptology ePrint Archive, Report 2017/490, 2017. http://eprint.iacr. org/2017/490. To appear in CCS 2017. 238

[Sch89]

Claus-Peter Schnorr. Efficient identification and signatures for smart cards. In CRYPTO, pages 239–252, 1989. 248, 251

[SE94]

Claus-Peter Schnorr and M. Euchner. Lattice basis reduction: Improved practical algorithms and solving subset sum problems. Math. Program., 66:181–199, 1994. 264

[Sei18]

Gregor Seiler. Faster avx2 optimized ntt multiplication for ring-lwe lattice cryptography. Cryptology ePrint Archive, Report 2018/039, 2018. https: //eprint.iacr.org/2018/039. 241, 242

[TW12]

Enrico Thomae and Christopher Wolf. Cryptanalysis of enhanced TTS, STS and all its variants, or: Why cross-terms are important. In Aika- terini Mitrokotsa and Serge Vaudenay, editors, Progress in Cryptology – AFRICACRYPT 2012, volume 7374 of LNCS, pages 188–202. Springer, 2012. 256

Proofs for Rounding Algorithm Properties

A

The three lemmas below prove each of the three parts of Lemma 1.

Lemma 3. Let r, z ∈ Z q with kzk ∞ ≤ α/2. Then

UseHint q (MakeHint q (z, r, α), r, α) = HighBits q (r + z, α).

Proof. The output of Decompose q is an integer r 1 such that 0 ≤ r 1 &lt; (q − 1)/α and another integer r 0 such that kr 0 k ∞ ≤ α/2. Because kzk ∞ ≤ α/2, the integer v 1 := HighBits q (r + z, α) either stays the same as r 1 or becomes r 1 ± 1 modulo m = (q − 1)/α. More precisely, if r 0 &gt; 0, then −α/2 &lt; r 0 + z ≤ α. This implies that v 1 is either r 1 or r 1 + 1 mod m. If r 0 ≤ 0, then we have −α ≤ r 0 + z ≤ α/2. In this case, we have v 1 = r 1 or r 1 − 1 mod m. The MakeHint q routine checks whether r 1 = v 1 and outputs 0 if this is so, and 1 if r 1 6 = v 1 . The UseHint q routine uses the “hint” h to either output r 1 (if y = 0) or, depending on whether r 0 &gt; 0 or not, output either r 1 + 1 mod + m or r 1 − 1 mod + m.

The lemma below shows that r is not too far away from the output of the UseHint q algorithm. This will be necessary for the security of the scheme.

Lemma 4. Let (h, r) ∈ {0, 1} × Z q and let v 1 = UseHint q (h, r, α). If h = 0, then kr − v 1 · αk ∞ ≤ α/2; else kr − v 1 · αk ∞ ≤ α + 1.

<!-- PDF_PAGE: 26 -->

## PDF page 26

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

263

Proof. Let (r 1 , r 0 ) := Decompose q (r, α). We go through all three cases of the UseHint q procedure.

Case 1 (h = 0): We have v 1 = r 1 and

r − v 1 · α = r 1 · α + r 0 − r 1 · α = r 0 ,

which by definition has absolute value at most α/2.

Case 2 (h = 1 and r 0 &gt; 0): We have v 1 = r 1 + 1 − κ · (q − 1)/α for κ = 0 or 1. Thus

r − v 1 · α = r 1 · α + r 0 − (r 1 + 1 − κ · (q − 1)/α) · α

= −α + r 0 + κ · (q − 1).

After centered reduction modulo q, the latter has magnitude ≤ α.

Case 3 (h = 1 and r 0 ≤ 0): We have v 1 = r 1 − 1 + κ · (q − 1)/α for κ = 0 or 1. Thus

r − v 1 · α = r 1 · α + r 0 − (r 1 − 1 + κ · (q − 1)/α) · α

= α + r 0 − κ · (q − 1).

After centered reduction modulo q, the latter quantity has magnitude ≤ α + 1.

The next lemma will play a role in proving the strong existential unforgeability of our signature scheme. It states that two different h, h 0 cannot lead to UseHint q (h, r, α) = UseHint q (h 0 , r, α).

Lemma 5. Let r ∈ Z q and h, h 0 ∈ {0, 1}. If UseHint q (h, r, α) = UseHint q (h 0 , r, α), then h = h 0 .

Proof. Note that UseHint q (0, r, α) = r 1 and UseHint q (1, r, α) is equal to (r 1 ± 1) mod + (q − 1)/α. Since (q − 1)/α ≥ 2, we have that r 1 6 = (r 1 ± 1) mod + (q − 1)/α.

We now prove Lemma 2.

Proof. (Of Lemma 2) We prove the lemma for integers, rather than vectors of polynomials, since the HighBits function works independently on each coefficient. If kLowBits q (r, α)k ∞ &lt; α/2 − β, then r = r 1 · α + r 0 where −α/2 + β &lt; r 0 ≤ α/2 + β. Then r + s = r 1 · α + (r 0 + s) and −α/2 &lt; r 0 + s ≤ α/2. Therefore r + s mod ± α = r 0 + s, and thus

(r + s) − ((r + s) mod ± α) = r 1 · α = r − (r mod ± α),

and the claim in the Lemma follows.

B Zero-Knowledge Proof

The security of our scheme does not rely on the part of the public key t 0 being secret and so we will be assuming that the public key is t rather than t 1 . We want to first compute the probability that some particular (z, c) is generated in Step 17 taken over the randomness of y and the random oracle H which is modeled as a random function. We have

Pr[z, c] = Pr[c] · Pr[y = z − cs 1 | c].

Whenever z has all its coefficients less than γ 1 − β then the above probability is exactly the same for every such tuple (z, c). This is because kcs i k ∞ ≤ β (with overwhelming probability), and thus kz − cs 1 k ∞ ≤ γ 1 − 1, which is a valid value of y. Therefore, if we

<!-- PDF_PAGE: 27 -->

## PDF page 27

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

264

only output z when all its coefficients have magnitudes less than γ 1 − β, then the resulting distribution will be uniformly random over S γ ` 1 −β−1 × B 60 . The simulation of the signature follows [Lyu12, BG14]. The simulator picks a uniformly random (z, c) in S γ ` 1 −β−1 × B 60 , after which it also makes sure that

kr 0 k ∞ = kLowBits q (w − cs 2 , 2γ 2 )k ∞ &lt; γ 2 − β.

By Equation (2), we know that w − cs 2 = Az − ct, and therefore the simulator can perfectly simulate this as well. If z does indeed satisfy kLowBits q (w−cs 2 , 2γ 2 )k ∞ &lt; γ 2 −β, then as long as kcs 2 k ∞ ≤ β, we will have

r 1 = HighBits q (w − cs 2 , 2γ 2 ) = HighBits q (w, 2γ 2 ) = w 1 .

Since our β was chosen such that the probability (over the choice of c, s 2 ) that kcs 2 k ∞ &lt; β is &gt; 1 − 2 −128 , the simulator does not need to perform the check that r 1 = w 1 and can always assume that it passes. We can then program H(µ k w 1 ) ← c .

Unless we have already set the value of H(µ k w 1 ) to something else, the resulting pair (z, c) has the same distribution as in a genuine signature of µ. It was shown in [KLS17] that the probability, over the random choice of A and y, that we already set the value of H(µ k w 1 ) is less than 2 −255 . All the other steps (after Step 19) of the signing algorithm are performed using public information and are therefore simulatable.

C Concrete Security

Lattice Reduction and Core-SVP Hardness

C.1

The best known algorithm for finding very short non-zero vectors in Euclidean lattices is the Block–Korkine–Zolotarev algorithm (BKZ) [SE94], proposed by Schnorr and Euchner in 1991. More recently, it was proven to quickly converge to its fix-point [HPS11] and improved in practice [CN11]. Yet, what it achieves asymptotically remains unchallenged. BKZ with block-size b makes calls to an algorithm that solves the Shortest lattice Vector Problem (SVP) in dimension b. The security of our scheme relies on the necessity to run BKZ with a large block-size b and the fact that the cost of solving SVP is exponential in p b. The best known classical SVP solver [BDGL16] runs in time ≈ 2 c C ·b with c C = log 2 3/2 ≈ 0.292. The best p known quantum SVP solver [Laa15, Sec. 14.2.10] runs in time ≈ 2 c Q ·b with c Q = log 2 13/9 ≈ 0.265. One may hope to improve these run- p c P ·b times, but going below ≈ 2 with c P = log 2 4/3 ≈ 0.2075 would require a theoretical breakthrough. Indeed, the best known SVP solvers rely on covering the b-dimensional sphere with cones of center-to-edge angle π/3: this requires 2 c P ·b cones. The subscripts C, Q, P respectively stand for Classical, Quantum and Paranoid. The strength of BKZ increases with b. More concretely, given as input a basis (c 1 , . . . , c n ) of an n-dimensional lattice, BKZ repeatedly uses the b-dimensional SVP-solver on lattices of the form (c i+1 (i), . . . , c j (i)) where i ≤ n, j = min(n, i + b) and where c k (i) denotes the projection of c k orthogonally to the vectors (c 1 , . . . , c i ). The effect of these calls is to flatten the curve of the ` i = log 2 kc i (i − 1)k’s (for i = 1, . . . , n). At the start of the execution, the ` i ’s typically decrease fast, at least locally. As BKZ preserves the determinant of the c i ’s, the sum of the ` i ’s remains constant throughout the execution, and after a (small) polynomial number of SVP calls, BKZ has made the ` i ’s decrease less.

<!-- PDF_PAGE: 28 -->

## PDF page 28

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

` i

log 2 q

Zone 1 Zone 3

0

0

i

Before reduction

` i

log 2 q

Zone 2 Zone 3

0

0

i

After b-BKZ with med. b

265

` i

log 2 q

Zone 1 Zone 2 Zone 3

0

0

i

After b-BKZ with small b

` i

log 2 q

Zone 2

0

0

i

After b-BKZ with large b

Figure 5: Evolution of Gram-Schmidt length in log-scale under BKZ reduction for various blocksizes. The area under the curves remains constant, and the slope in Zone 2 decrease with the blocksize. Note that Zone 3 may disappear before Zone 1, depending on the shape of the input basis.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 28]

It can be heuristically estimated that for sufficiently large b, the local slope of the ` i ’s converges to 1 b 1/b slope(b) = log 2 (π · b) , b − 1 2πe

unless the local input ` i ’s are already too small or too large. The quantity slope(b) decreases with b, implying that the larger b the flatter the output ` i ’s. In our case, the input ` i ’s are of the following form (cf. Fig. 5). The first ones are all equal to log 2 q and the last ones are all equal to 0. BKZ will flatten the jump, decreasing ` i ’s with small i’s and increasing ` i ’s with large i’s. However, the local slope slope(b) may not be sufficiently small to make the very first ` i ’s decrease and the very last ` i ’s increase. Indeed, BKZ will not increase (resp. increase) some ` i ’s if these are already smaller (resp. larger) than ensured by the local slope guarantee. In our case, the ` i ’s are always of the following form at the end of the execution:

• The first ` i ’s are constant equal to log 2 q (this is the possibly empty Zone 1).

• Then they decrease linearly, with slope slope(b) (this is the never-empty Zone 2).

• The last ` i ’s are constant equal to 0 (this is the possibly empty Zone 3).

The graph is continuous, i.e., if Zone 1 (resp. Zone 3) is not empty, then Zone 2 starts with ` i = log 2 q (resp. ends with ` i = 0).

C.2 Solving MLWE

Any MLWE `,k,D instance for some distribution D can be viewed as an LWE instance of dimensions 256·` and 256·k. Indeed, the above can be rewritten as finding vec(s 1 ), vec(s 2 ) ∈ Z 256·` × Z 256·k from (rot(A), vec(t)), where vec(·) maps a vector of ring elements to the vector obtained by concatenating the coefficients of its coordinates, and rot(A) ∈ Z 256·k×256·` is obtained by replacing all entries a ij ∈ R q of A by the 256 × 256 matrix q whose z-th column is vec x z−1 · a ij .

<!-- PDF_PAGE: 29 -->

## PDF page 29

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

266

Given an LWE instance, there are two lattice-based attacks. The primal attack and the dual attack. Here, the primal attack consists in finding a short non-zero vector in the lattice Λ = {x ∈ Z d : Mx = 0 mod q} where M = (rot(A) [1:m] |I m |vec(t) [1:m] ) is an m × d matrix where d = 256 · ` + m + 1 and m ≤ 256 · k. Indeed, it is sometime not optimal to use all the given equations in lattice attacks. We tried all possible number m of rows, and, for each trial, we increased the blocksize of b until the value ` d−b obtained as explained above was deemed sufficiently large. As explained in [ADPS16, Sec. 6.3], if 2 ` d−b is greater than the expected norm of (vec(s 1 ), vec(s 2 )) after projection orthogonally to the first d − b vectors, it is likely that the Module-LWE solution can be easily extracted from the BKZ output. The dual attack consists in finding a short non-zero vector in the lattice Λ 0 = {(x, y) ∈ m Z × Z d : M T x + y = 0 mod q)}, M = (rot(A) [1:m] ) is an m × d matrix where d = 256 · ` and m ≤ 256 · k. Again, for each value of m, we increased the value of b until the value ` 1 obtained as explained above was deemed sufficiently small according the analysis of [ADPS16, Sec. 6.3].

C.3 Solving MSIS and SelfTargetMSIS

As per the discussion in Section 4.2.1, the best known attack against the SelfTargetMSIS problem involves either breaking the security of H or solving the problem in Eq. (12). The latter amounts to solving the MSIS k,`+1,ζ problem for the matrix [ A | t 0 ]. 9 Note that the MSIS instance can be mapped to a SIS 256·k,256·(`+1),ζ instance by consid-

256·k×256·(`+1)

ering the matrix rot(A|t 0 ) ∈ Z q . The attack against the MSIS k,`,ζ 0 instance in Eq. (6) can similarly be mapped to a SIS 256·k,256·`,ζ 0 instance by considering the matrix rot(A) ∈ Z q 256·k×256·` . The attacker may consider a subset of w columns, and let the solution coefficients corresponding to the dismissed columns be zero.

Remark 1. An unusual aspect here is that we are considering the infinity norm, rather than the Euclidean norm. Further, for our specific parameters, the Euclidean norms of the solutions are above q. In particular, the vector (q, 0, . . . , 0) T belongs to the lattice, has Euclidean norm below that of the solution, but its infinity norm above the requirement. This raises difficulties in analyzing the strength of BKZ towards solving our infinity norm SIS instances: indeed, even with small values of b, the first ` i ’s are short (they correspond to q-vectors), even though they are not solutions.

For each number w of selected columns and for each value of b, we compute the estimated BKZ output ` i ’s, as explained above. We then consider the smallest i such that ` i is below log 2 q and the largest j such that ` j above 0. These correspond to the vectors that were modified by BKZ, with smallest and largest indices, respectively. In fact, for p b the same cost as a call to the SVP-solver, we can obtain 4/3 vectors with Euclidean norm ≈ 2 ` i after projection orthogonally to the first i − 1 basis vectors. Now, let us look closely at the shape of such a vector. As the first i − 1 basis vectors are the first i − 1 canonical unit vectors multiplied by q, projecting orthogonally to these consists in zeroing the first i − 1 coordinates. The remaining w − i + 1 coordinates have total Euclidean norm ≈ 2 ` i ≈ q, and the last w − j coordinates √ are 0. We heuristically assume that these coordinates have similar magnitudes σ ≈ 2 ` i / j − i + 1; we model each such coordinate p b as a Gaussian of standard deviation σ. We assume that each one of our 4/3 vectors has its first i − 1 coordinates independently uniformly distributed modulo q, and finally compute the probability that all coordinates in both ranges [0, i − 1] and [i, j] are less than B in absolute value. Our cost estimate is the inverse of that probability multiplied by the run-time of our b-dimensional SVP-solver.

9 Note that a solution to Eq. (12) would require the coefficient in from of t 0 to be ±1, while we’re allowing any small polynomial. Furthermore, as discussed after Eq. (12), some parts of the real solution are smaller than the bound ζ, but we’re ignoring this for the sake of being conservative with our analysis.

<!-- PDF_PAGE: 30 -->

## PDF page 30

### L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé

` i

log 2 q

Zone 1 Zone 2 Zone 3

0

0

i

Keeping q-vectors

267

` i

Zone 2 Zone 3

0

0

i

Forgetting q-vectors

Figure 6: Effect of forgetting q-vectors by randomization, under the same BKZ-blocksize b.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 30]

Forgetting q-vectors. For all the parameter sets proposed in this paper, the best parametrization of the attack above kept the basis in a shape with a non-trivial Zone 1. We note that the coordinates in this range have a quite lower probability of passing the ` ∞ constraint than coordinates in Zone 2. We therefore considered a strategy consisting of “forgetting” the q-vectors, by re-randomizing the input basis before running the BKZ algorithm. For the same blocksize b, this makes Zone 1 of the output basis disappear (BKZ does not find the q-vectors), at the cost of producing a basis with first vectors of larger Euclidean norms. This is depicted in Fig. 6. It turns out that this strategy always improves over the previous strategy for the parameter ranges considered in this paper. We therefore used this strategy for our security estimates.

C.4 On Other Attacks

For our parameters, the BKW [BKW03] and Arora–Ge [AG11] families of algorithms are far from competitive.

Algebraic attacks. One specificity of our LWE and SIS instances is that they are inherited from Module-LWE and Module-SIS instances. One may wonder whether the extra algebraic structure of the resulting lattices can be exploited by an attacker. The line of work of [CGS14, BS16, CDPR16, CDW17] did indeed find new cryptanalytic results on certain algebraic lattices, but [CDW17] mentions serious obstacles towards breaking cryptographic instances of Ring-LWE. By switching from Ring-LWE to Module-LWE, we get even further away from those weak algebraic lattice problems.

Dense sublattice attacks. Kirchner and Fouque [KF17] showed that the existence of many linearly independent and unexpectedly short lattice vectors (much shorter than Minkowski’s bound) helps BKZ run better than expected in some cases. This could happen for our primal LWE attack, by extending M = (rot(A) [1:m] |I m |vec(t) [1:m] ) to (rot(A) [1:m] |I m |rot(t) [1:m] ): the associated lattice now has 256 linearly independent short vectors rather than a single one. The Kirchner-Fouque analysis of BKZ works best if both q and the ratio between the number of unexpectedly short vectors and the lattice dimension are high. In the NTRU case, for example, the ratio is 1/2, and, for some schemes derived from NTRU, the modulus q is also large. We considered this refined analysis of BKZ in our setup, but, to become relevant for our parameters, it requires a parameter b which is higher than needed with the usual analysis of BKZ. Note that [KF17] also arrived to the conclusion that this attack is irrelevant in the small modulus regime, and is mostly a threat to fully homomorphic encryption schemes and cryptographic multilinear maps. Note that, once again, the switch from Ring-LWE to MLWE takes us further away from lattices admitting unconventional attacks. Indeed, the dimension ratio of the dense

<!-- PDF_PAGE: 31 -->

## PDF page 31

CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme

268

sub-lattice is 1/2 in NTRU, at most 1/3 in lattices derived from Ring-LWE, and at most 1/(` + 2) in lattices derived from MLWE.

Specialized attack against ` ∞ -SIS. At last, we would like to mention that it is not clear whether the attack sketched in Appendix C.3 above for SIS in infinity norm is optimal. Indeed, as we have seen, this approach produces many vectors, with some rather large uniform coordinates (at indices 1, . . . , i), and smaller Gaussian ones (at indices i, . . . , j). In our current analysis, we simply hope that one of the vector satisfies the ` ∞ bound. Instead, one could combine them in ways that decrease the size of the first (large) coefficients, while letting the other (small) coefficients grow a little bit. This situation created by the use of ` ∞ -SIS (see Remark 1) has — to the best of our knowledge — not been studied in detail. After a preliminary analysis, we do not consider such an improved attack a serious threat to our concrete security claims, especially in the light of the approximations already made in the favor of the adversary. Nevertheless, we believe this question deserves a detailed study, which we leave to future work.
