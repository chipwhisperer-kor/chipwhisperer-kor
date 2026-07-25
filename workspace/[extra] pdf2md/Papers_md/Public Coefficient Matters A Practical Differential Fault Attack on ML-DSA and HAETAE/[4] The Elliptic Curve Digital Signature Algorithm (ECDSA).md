# [4] The Elliptic Curve Digital Signature Algorithm (ECDSA)

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 28
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-04"
derived_asset_id: "PCM-DFA-REF-04-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[4] The Elliptic Curve Digital Signature Algorithm (ECDSA).pdf"
source_sha256: "0ce5cff6d9adf76c71419cbe6aad689f1cf6ea1e1c3c3f80f79ae7cea51f860c"
pages: 28
bbox_words: 23653
consumed_bbox_words: 23653
numeric_tokens: 2866
consumed_numeric_tokens: 2866
source_blocks: 433
consumed_source_blocks: 433
emitted_blocks: 426
embedded_raster_images: 10656
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 28
glyph_chars_removed: 10
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

IJIS (2001) 1: 36–63 / Digital Object Identiﬁer (DOI) 10.1007/s102070100002

The Elliptic Curve Digital Signature Algorithm (ECDSA)

Don Johnson 1 , Alfred Menezes 1,2 , Scott Vanstone 1,2

1

2

Certicom Research, Canada Department of Combinatorics and Optimization, University of Waterloo, Canada E-mails: {djohnson,amenezes,svanstone}@certicom.com

Published online: 27 July 2001 –  Springer-Verlag 2001

Abstract. The Elliptic Curve Digital Signature Algo- rithm (ECDSA) is the elliptic curve analogue of the Dig- ital Signature Algorithm (DSA). It was accepted in 1999 as an ANSI standard and in 2000 as IEEE and NIST standards. It was also accepted in 1998 as an ISO stan- dard and is under consideration for inclusion in some other ISO standards. Unlike the ordinary discrete loga- rithm problem and the integer factorization problem, no subexponential-time algorithm is known for the elliptic curve discrete logarithm problem. For this reason, the strength-per-key-bit is substantially greater in an algo- rithm that uses elliptic curves. This paper describes the ANSI X9.62 ECDSA, and discusses related security, im- plementation, and interoperability issues.

Keywords: Signature schemes – Elliptic curve cryptog- raphy – DSA – ECDSA

1 Introduction

The Digital Signature Algorithm (DSA) was speciﬁed in a U.S. Government Federal Information Processing Standard (FIPS) called the Digital Signature Standard (DSS [70]). Its security is based on the computational in- tractability of the discrete logarithm problem (DLP) in prime-order subgroups of Z p ∗ . Elliptic curve cryptosystems (ECC) were invented by Neal Koblitz [49] and Victor Miller [67] in 1985. They can be viewed as elliptic curve analogues of the older discrete logarithm (DL) cryptosystems in which the subgroup of Z p ∗ is replaced by the group of points on an elliptic curve over a ﬁnite ﬁeld. The mathematical basis for the security of elliptic curve cryptosystems is the computational in- tractability of the elliptic curve discrete logarithm prob- lem (ECDLP).

Since the ECDLP appears to be signiﬁcantly harder than the DLP, the strength-per-key-bit is substantially greater in elliptic curve systems than in conventional discrete logarithm systems. Thus, smaller parameters, but with equivalent levels of security, can be used with ECC than with DL systems. The advantages that can be gained from smaller parameters include speed (faster computations) and smaller keys and certiﬁcates. These advantages are especially important in environments where processing power, storage space, bandwidth, or power consumption is constrained. The Elliptic Curve Digital Signature Algorithm (ECDSA) is the elliptic curve analogue of the DSA. ECDSA was ﬁrst proposed in 1992 by Scott Vanstone [108] in response to NIST’s (National Institute of Standards and Technology) request for public comments on their ﬁrst proposal for DSS. It was accepted in 1998 as an ISO (International Standards Organization) standard (ISO 14888-3), accepted in 1999 as an ANSI (American Na- tional Standards Institute) standard (ANSI X9.62), and accepted in 2000 as an IEEE (Institute of Electrical and Electronics Engineers) standard (IEEE 1363-2000) and a FIPS standard (FIPS 186-2). It is also under consid- eration for inclusion in some other ISO standards. In this paper, we describe the ANSI X9.62 ECDSA, present rationale for some of the design decisions, and discuss related security, implementation, and interoperability issues. The remainder of this paper is organized as follows. In Sect. 2, we review digital signature schemes and the DSA. A brief tutorial on ﬁnite ﬁelds and elliptic curves is pro- vided in Sects. 3 and 4, respectively. In Sect. 5, methods for domain parameter generation and validation are con- sidered, while Sect. 6 discusses methods for key pair gen- eration and public key validation. The ECDSA signature and veriﬁcation algorithms are presented in Sect. 7. The security of ECDSA is studied in Sect. 8. Finally, some im-

<!-- PDF_PAGE: 2 -->

## PDF page 2

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

plementation and interoperability issues are considered in Sects. 9 and 10.

2 Digital signature schemes

### 2.1 Background

Digital signature schemes are designed to provide the dig- ital counterpart to handwritten signatures (and more). A digital signature is a number dependent on some se- cret known only to the signer (the signer’s private key), and, additionally, on the contents of the message being signed. Signatures must be veriﬁable – if a dispute arises as to whether an entity signed a document, an unbiased third party should be able to resolve the matter equi- tably, without requiring access to the signer’s private key. Disputes may arise when a signer tries to repudiate a sig- nature it did create, or when a forger makes a fraudulent claim. This paper is concerned with asymmetric digital sig- natures schemes with an appendix. “Asymmetric” means that each entity selects a key pair consisting of a private key and a related public key. The entity maintains the se- crecy of the private key that it uses for signing messages, and makes authentic copies of its public key available to other entities which use it to verify signatures. “Ap- pendix” means that a cryptographic hash function is used to create a message digest of the message, and the sign- ing transformation is applied to the message digest rather than to the message itself.

Security. Ideally, a digital signature scheme should be existentially unforgeable under chosen-message attack. This notion of security was introduced by Goldwasser et al. [33]. Informally, it asserts that an adversary who is able to obtain entity A’s signatures for any message of its choice is unable to successfully forge A’s signature on a single other message.

Applications. Digital signature schemes can be used to provide the following basic cryptographic services: data integrity (the assurance that data has not been altered by unauthorized or unknown means), data ori- gin authentication (the assurance that the source of data is as claimed), and non-repudiation (the assur- ance that an entity cannot deny previous actions or commitments). Digital signature schemes are commonly used as primitives in cryptographic protocols that pro- vide other services including entity authentication (e.g., FIPS 196 [72], ISO/IEC 9798-3 [40], and Blake-Wilson and Menezes [10]), authenticated key transport (e.g., Blake-Wilson and Menezes [10], ANSI X9.63 [4], and ISO/IEC 11770-3 [41]), and authenticated key agreement (e.g., ISO/IEC 11770-3 [41], Diﬃe et al. [21], and Bellare et al. [8]).

Classiﬁcation. The digital signature schemes in use to- day can be classiﬁed according to the hard underlying

37

mathematical problem which provides the basis for their security: 1. Integer factorization (IF) schemes, which base their security on the intractability of the integer factoriza- tion problem. Examples of these include the RSA [85] and Rabin [84] signature schemes. 2. Discrete logarithm (DL) schemes, which base their se- curity on the intractability of the (ordinary) discrete logarithm problem in a ﬁnite ﬁeld. Examples of these include the ElGamal [23], Schnorr [90], DSA [70], and Nyberg-Rueppel [78, 79] signature schemes. 3. Elliptic curve (EC) schemes, which base their security on the intractability of the elliptic curve discrete loga- rithm problem.

### 2.2 The Digital Signature Algorithm (DSA)

The DSA was proposed in August 1991 by the U.S. Na- tional Institute of Standards and Technology (NIST) and was speciﬁed in a U.S. Government Federal Information Processing Standard (FIPS 186 [70]) called the Digital Signature Standard (DSS). The DSA can be viewed as a variant of the ElGamal signature scheme [23]. Its secu- rity is based on the intractability of the discrete logarithm problem in prime-order subgroups of Z p ∗ .

DSA domain parameter generation. Domain parameters are generated for each entity in a particular security do- main. (See also the note below on the secure generation of parameters.) 1. Select a 160-bit prime q and a 1024-bit prime p with the property that q | p − 1. 2. (Select a generator g of the unique cyclic group of order q in Z p ∗ .) Select an element h ∈ Z p ∗ and compute g = h (p−1)/q mod p. (Repeat until g = 1.) 3. Domain parameters are p, q, and g.

DSA key pair generation. Each entity A in the domain with domain parameters (p, q, g) does the following: 1. Select a random or pseudorandom integer x such that 1 ≤ x ≤ q − 1. 2. Compute y = g x mod p. 3. A’s public key is y; A’s private key is x.

DSA signature generation. To sign a message m, A does the following: 1. Select a random or pseudorandom integer k, 1 ≤ k ≤ q − 1. 2. Compute X = g k mod p and r = X mod q. If r = 0 then go to step 1. 3. Compute k −1 mod q. 4. Compute e = SHA-1(m). 5. Compute s = k −1 {e + xr} mod q. If s = 0 then go to step 1. 6. A’s signature for the message m is (r, s).

<!-- PDF_PAGE: 3 -->

## PDF page 3

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

38

DSA signature veriﬁcation. To verify A’s signature (r, s) on m, B obtains authentic copies of A’s domain parame- ters (p, q, g) and public key y and does the following: 1. Verify that r and s are integers in the interval [1, q − 1]. 2. Compute e = SHA-1(m). 3. Compute w = s −1 mod q. 4. Compute u 1 = ew mod q and u 2 = rw mod q. 5. Compute X = g u 1 y u 2 mod p and v = X mod q. 6. Accept the signature if and only if v = r.

Security analysis. Since r and s are each integers less than q, DSA signatures are 320 bits in size. The security of the DSA relies on two distinct but related discrete log- arithm problems. One is the discrete logarithm problem in Z p ∗ where the number ﬁeld sieve algorithm (see Gor- don [35] and Schirokauer [89]) applies; this algorithm has a subexponential running time. More precisely, the ex- pected running time of the algorithm is (1) O exp (c + o(1))(ln p) 1/3 (ln ln p) 2/3 ,

where c ≈ 1.923, and ln n denotes the natural logarithm function. If p is a 1024-bit prime, then the expression (1) represents an infeasible amount of computation; thus the DSA using a 1024-bit prime p is currently not vulnera- ble to this attack. The second discrete logarithm problem works to the base g in the subgroup of order q in Z p ∗ : given p, q, g, and y, ﬁnd x such that y ≡ g x (mod p). For large p (e.g., 1024 bits), the best algorithm known for this prob- lem is Pollard’s rho method [83], and takes about πq/2 (2)

steps. If q ≈ 2 160 , then the expression (2) represents an infeasible amount of computation; thus the DSA is not vulnerable to this attack. However, note that there are two primary security parameters for DSA: the size of p and the size of q. Increasing one without a corresponding increase in the other will not result in an eﬀective increase in security. Furthermore, an advance in algorithms for either one of the two discrete logarithm problems could weaken DSA.

Secure generation of parameters. In response to some criticisms received on the ﬁrst draft (see Rueppel et al. [86] and Smid and Branstad [99]), FIPS 186 spec- iﬁed a method for generating primes p and q “ver- iﬁably at random”. This feature prevents an entity (e.g., a central authority generating domain parame- ters to be shared by a network of entities) from in- tentionally constructing “weak” primes p and q for which the discrete logarithm problem is relatively easy. For a further discussion of this issue, see Gordon [34]. FIPS 186 also speciﬁes two methods, based on DES and SHA-1, for pseudorandomly generating private keys x and per-message secrets k. FIPS 186 mandates the use of these algorithms or any other FIPS-approved security methods.

3 Finite ﬁelds

We provide a brief introduction to ﬁnite ﬁelds. For further information, see Chapt. 3 of Koblitz [52], or the books by McEliece [61] and Lidl and Niederreitter [59]. A ﬁnite ﬁeld consists of a ﬁnite set of elements F together with two binary operations on F , called add- ition and multiplication, that satisfy certain arithmetic properties. The order of a ﬁnite ﬁeld is the number of elements in the ﬁeld. There exists a ﬁnite ﬁeld of order q if and only if q is a prime power. If q is a prime power, then there is essentially only one ﬁnite ﬁeld of order q; this ﬁeld is denoted by F q . There are, how- ever, many ways of representing the elements of F q . Some representations may lead to more eﬃcient imple- mentations of the ﬁeld arithmetic in hardware or in software. If q = p m where p is a prime and m is a positive integer, then p is called the characteristic of F q and m is called the extension degree of F q . Most standards which specify the elliptic curve cryptographic tech- niques restrict the order of the underlying ﬁnite ﬁeld to be an odd prime (q = p) or a power of 2 (q = 2 m ). In Sect. 3.1, we describe the elements and operations of the ﬁnite ﬁeld F p . In Sect. 3.2, elements and the operations of the ﬁnite ﬁeld F 2 m are described, to- gether with two methods for representing the ﬁeld elem- ents: polynomial basis representations and normal basis representations.

### 3.1 The ﬁnite ﬁeld F p

Let p be a prime number. The ﬁnite ﬁeld F p , called a prime ﬁeld, is comprised of the set of integers {0, 1, 2, . . . , p − 1} with the following arithmetic operations: – Addition: If a, b ∈ F p , then a + b = r, where r is the re- mainder when a + b is divided by p and 0 ≤ r ≤ p − 1. This is known as addition modulo p. – Multiplication: If a, b ∈ F p , then a · b = s, where s is the remainder when a · b is divided by p and 0 ≤ s ≤ p − 1. This is known as multiplication modulo p. – Inversion: If a is a non-zero element in F p , the inverse of a modulo p, denoted a −1 , is the unique integer c ∈ F p for which a · c = 1.

Example 1. (The ﬁnite ﬁeld F 23 ) The elements of F 23 are {0, 1, 2, . . . , 22}. Examples of the arithmetic opera- tions in F 23 are: (1) 12 + 20 = 9; (2) 8 · 9 = 3; and (3) 8 −1 = 3.

### 3.2 The ﬁnite ﬁeld F 2 m

The ﬁeld F 2 m , called a characteristic two ﬁnite ﬁeld or a binary ﬁnite ﬁeld , can be viewed as a vector space of dimension m over the ﬁeld F 2 , which consists of the two elements 0 and 1. That is, there exist m elements

<!-- PDF_PAGE: 4 -->

## PDF page 4

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

α 0 , α 1 , . . . , α m−1 in F 2 m such that each element α ∈ F 2 m can be uniquely written in the form:

α = a 0 α 0 + a 1 α 1 + · · · + a m−1 α m−1 , where a i ∈ {0, 1}.

Such a set {α 0 , α 1 , . . . , α m−1 } is called a basis of F 2 m over F 2 . Given such a basis, a ﬁeld element α can be repre- sented as the bit string (a 0 a 1 . . . a m−1 ). Addition of ﬁeld elements is performed by bitwise XOR-ing the vector rep- resentations. The multiplication rule depends on the basis selected. There are many diﬀerent bases of F 2 m over F 2 . Some bases lead to more eﬃcient software or hardware imple- mentations of the arithmetic in F 2 m than other bases. ANSI X9.62 permits two kinds of bases: polynomial bases and normal bases.

### 3.2.1 Polynomial basis representations

Let f (x) = x m + f m−1 x m−1 + · · ·+ f 2 x 2 + f 1 x + f 0 (where f i ∈ {0, 1} for i = 0, 1, . . . , m − 1) be an irreducible poly- nomial of degree m over F 2 . That is, f (x) cannot be factored as a product of two polynomials over F 2 , each of degree less than m. Each such polynomial f (x) de- ﬁnes a polynomial basis representation of F 2 m , which is described next. f (x) is called the reduction polynomial.

Field elements. The ﬁnite ﬁeld F 2 m is comprised of all polynomials over F 2 of degree less than m:

F 2 m = {a m−1 x m−1 + · · · + a 1 x + a 0 : a i ∈ {0, 1}}.

The ﬁeld element a m−1 x m−1 + · · · + a 1 x + a 0 is usually denoted by the bit string (a m−1 . . . a 1 a 0 ) of length m, so that

F 2 m = {(a m−1 . . . a 1 a 0 ) : a i ∈ {0, 1}}.

Thus the elements of F 2 m can be represented by the set of all binary strings of length m. The multiplicative iden- tity element (1) is represented by the bit string (00 . . . 01), while the additive identity element (0) is represented by the bit string of all 0’s.

Field operations. The following arithmetic operations are deﬁned on the elements of F 2 m when using a polynomial basis representation with reduction polynomial f (x): – Addition: If a = (a m−1 . . . a 1 a 0 ) and b = (b m−1 . . . b 1 b 0 ) are elements of F 2 m , then a + b = c = (c m−1 . . . c 1 c 0 ), where c i = (a i + b i ) mod 2. That is, ﬁeld addition is performed bitwise. – Multiplication: If a = (a m−1 . . . a 1 a 0 ) and b = (b m−1 . . . b 1 b 0 ) are elements of F 2 m , then a · b = r = (r m−1 . . . r 1 r 0 ), where the polynomial r m−1 x m−1 + · · · + r 1 x + r 0 is the remainder when the polynomial

(a m−1 x m−1 + · · · + a 1 x + a 0 ) ·

(b m−1 x m−1 + · · · + b 1 x + b 0 )

39

is divided by f (x) over F 2 . – Inversion: If a is a non-zero element in F 2 m , the in- verse of a, denoted a −1 , is the unique element c ∈ F 2 m for which a · c = 1.

Example 2. (A polynomial basis representation of the ﬁ- nite ﬁeld F 2 4 ) Let f (x) = x 4 + x + 1 be the reduction poly- nomial. Then the 16 elements of F 2 4 are: 0(0000) x 3 (1000) 3 1(0001) x + 1(1001) x(0010) x 3 + x(1010) x + 1(0011) x 3 + x + 1(1011)

x 2 (0100) x 3 + x 2 (1100) x 3 + x 2 + 1(1101) x 2 + 1(0101) x 2 + x(0110) x 3 + x 2 + x(1110) x 2 + x + 1(0111) x 3 + x 2 + x + 1(1111). Examples of the arithmetic operations in F 2 4 are:

– (1101) + (1001) = (0100). – (1101) · (1001) = (1111) since (x 3 + x 2 + 1) · (x 3 + 1) = x 6 + x 5 + x 2 + 1 and (x 6 + x 5 + x 2 + 1) mod (x 4 + x + 1) = x 3 + x 2 + x + 1. – (1101) −1 = (0100).

The element α = x = (0010) is a generator of F ∗ 2 4 since its order is 15 as the following calculations show: α 1 = (0010) α 2 = (0100) α 3 = (1000) 4 5 α = (0011) α = (0110) α 6 = (1100) 7 8 α = (1011) α = (0101) α 9 = (1010) 10 11 α = (0111) α = (1110) α 12 = (1111) 13 14 α = (1101) α = (1001) α 15 = (0001).

Selecting a reduction polynomial. A trinomial over F 2 is a polynomial of the form x m + x k + 1, where 1 ≤ k ≤ m − 1. A pentanomial over F 2 is a polynomial of the form x m + x k 3 + x k 2 + x k 1 + 1, where 1 ≤ k 1 &lt; k 2 &lt; k 3 ≤ m − 1. ANSI X9.62 speciﬁes the following rules for select- ing the reduction polynomial for representing the elem- ents of F 2 m .

1. If there exists an irreducible trinomial of degree m over F 2 , then the reduction polynomial f (x) must be an irreducible trinomial of degree m over F 2 . To maxi- mize the chances for interoperability, ANSI X9.62 rec- ommends that the trinomial used should be x m +x k +1 for the smallest possible k. 2. If there does not exist an irreducible trinomial of de- gree m over F 2 , then the reduction polynomial f (x) must be an irreducible pentanomial of degree m over F 2 . To maximize the chances for interoperability, ANSI X9.62 recommends that the pentanomial used should be x m + x k 3 + x k 2 + x k 1 + 1 chosen according to the following criteria: 1 (1) k 3 is as small as possible;

1 Actually, ANSI X9.62 recommends the following criteria for se- lecting the pentanomial: (1) k 1 is as small as possible; (2) for this particular value of k 1 , k 2 is as small as possible; and (3) for these particular values of k 1 and k 2 , k 3 is as small as possible. However, the ANSI X9F1 committee agreed in April 1999 to change this rec-

<!-- PDF_PAGE: 5 -->

## PDF page 5

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

40

(2) for this particular value of k 3 , k 2 is a small as pos- sible; and (3) for these particular values of k 3 and k 2 , k 1 is as small as possible.

### 3.2.2 Normal basis representations

A normal basis of F 2 m over F 2 is a basis of the form 2 m−1 {β, β 2 , β 2 , . . . , β 2 }, where β ∈ F 2 m . Such a basis always exists. Any element a ∈ F 2 m can be written as m−1 i a = i=0 a i β 2 , where a i ∈ {0, 1}. Normal basis repre- sentations have the computational advantage that squar- ing an element can be done very eﬃciently (see Field Operations below). Multiplying distinct elements, on the other hand, can be cumbersome in general. For this rea- son, ANSI X9.62 speciﬁes that Gaussian normal bases be used, for which multiplication is both simpler and more eﬃcient.

Gaussian normal bases (GNB). The type of a GNB is a positive integer measuring the complexity of the multi- plication operation with respect to that basis. Generally speaking the smaller the type, the more eﬃcient the mul- tiplication. For a given m and T , the ﬁeld F 2 m can have at most one GNB of type T . Thus it is proper to speak of the type T GNB of F 2 m . See Mullin et al. [69] and Ash et al. [5] for further information on GNBs.

Existence of Gaussian normal bases. A GNB exists when- ever m is not divisible by 8. Let m be a positive integer not divisible by 8, and let T be a positive integer. Then a type T GNB for F 2 m exists if and only if p = T m + 1 is prime and gcd(T m/k, m) = 1, where k is the multiplica- tive order of 2 modulo p.

2 m−1

Field elements. If {β, β 2 , β 2 , . . . , β 2 } is a normal ba- m−1 i sis of F 2 m over F 2 , then the ﬁeld element a = i=0 a i β 2 is represented by the binary string (a 0 a 1 . . . a m−1 ) of length m, so that

F 2 m = {(a 0 a 1 . . . a m−1 ) : a i ∈ {0, 1}}.

The multiplicative identity element (1) is represented by the bit string of all 1’s, while the additive identity element (0) is represented by the bit string of all 0’s.

Field operations. The following arithmetic operations are deﬁned on the elements of F 2 m when using a GNB of type T :

– Addition: If a = (a 0 a 1 . . . a m−1 ) and b = (b 0 b 1 . . . b m−1 ) are elements of F 2 m , then a + b = c = (c 0 c 1 . . . c m−1 ), where c i = (a i + b i ) mod 2. That is, ﬁeld addition is performed bitwise.

ommendation in a forthcoming revision of ANSI X9.62 to the one given above in order to be consistent with the IEEE 1363-2000 and FIPS 186-2 recommendations.

– Squaring: Let a = (a 0 a 1 . . . a m−1 ) ∈ F 2 m . Since squar- ing is a linear operation in F 2 m ,

m−1

2

m−1

2 i

i+1

2

a i β 2

a = a i β =

i=0 m−1

i=0

i

a i−1 β 2 = (a m−1 a 0 a 1 . . . a m−2 ),

=

i=0

with indices reduced modulo m. Hence squaring a ﬁeld element can be accomplished by a simple rotation of the vector representation. – Multiplication: Let p = T m + 1, and let u ∈ F p be an element of order T . Deﬁne the sequence F (1), F (2), . . . , F (p − 1) by

F (2 i u j mod p) = i for 0 ≤ i ≤ m − 1, 0 ≤ j ≤ T − 1.

If a = (a 0 a 1 . . . a m−1 ) and b = (b 0 b 1 . . . b m−1 ) are elem- ents of F 2 m , then a · b = c = (c 0 c 1 . . . c m−1 ), where

 p−2  k=1 a F (k+1)+l b F (p−k)+l    m/2 c l = k=1 (a k+l−1 b m/2+k+l−1   +a m/2+k+l−1 b k+l−1 )  p−2  + k=1 a F (k+1)+l b F (p−k)+l

if T is even,

if T is odd,

for each l, 0 ≤ l ≤ m − 1, where indices are reduced modulo m. – Inversion: If a is a non-zero element in F 2 m , the in- verse of a in F 2 m , denoted a −1 , is the unique element c ∈ F 2 m for which a · c = 1.

Example 3. (A Gaussian normal basis representation of the ﬁnite ﬁeld F 2 4 ) For the type T = 3 GNB for F 2 4 , let u = 9 ∈ F 13 be an element of order 3. The sequence of F (i)’s is:

F (1) = 0F (2) = 1F (3) = 0 F (4) = 2 F (5) = 1 F (6) = 1 F (7) = 3F (8) = 3F (9) = 0F (10) = 2F (11) = 3F (12) = 2.

The formulas for the product terms c l are:

c 0 = a 0 (b 1 + b 2 + b 3 ) + a 1 (b 0 + b 2 ) + a 2 (b 0 + b 1 ) + a 3 (b 0 + b 3 ) c 1 = a 1 (b 2 + b 3 + b 0 ) + a 2 (b 1 + b 3 ) + a 3 (b 1 + b 2 ) + a 0 (b 1 + b 0 ) c 2 = a 2 (b 3 + b 0 + b 1 ) + a 3 (b 2 + b 0 ) + a 0 (b 2 + b 3 ) + a 1 (b 2 + b 1 ) c 3 = a 3 (b 0 + b 1 + b 2 ) + a 0 (b 3 + b 1 ) + a 1 (b 3 + b 0 ) + a 2 (b 3 + b 2 ).

For example, if a = (1000) and b = (1101), then c = a · b = (0010).

Selecting a Gaussian normal basis. ANSI X9.62 speciﬁes the following rules for selecting a GNB for representing the elements of F 2 m (when m is not divisible by 8).

1. If there exists a type 2 GNB of F 2 m , then this basis must be used. 2. If there does not exist a type 2 GNB of F 2 m but there does exist a type 1 GNB, then the type 1 GNB must be used.

<!-- PDF_PAGE: 6 -->

## PDF page 6

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

3. If neither a type 1 nor a type 2 GNB of F 2 m exists, then the GNB of the smallest type must be used. The selection of type 2 GNBs over type 1 GNBs was some- what arbitrary – both types of GNBs admit eﬃcient im- plementation of ﬁeld arithmetic. This is not a practical concern since ﬁnite ﬁelds which have both type 1 and type 2 GNBs are relatively scarce – the only such ﬁelds F 2 m with m between 160 and 600 are F 2 210 and F 2 378 . Nei- ther of these two ﬁelds are among those recommended by NIST (see Sect. 10.2).

4 Elliptic curves over ﬁnite ﬁelds

We give a quick introduction to the theory of elliptic curves. Chapter 6 of Koblitz’s book [52] provides an intro- duction to elliptic curves and elliptic curve systems. For a more detailed account, consult Menezes [63] or Blake et al. [9]. Some advanced books on elliptic curves are Enge [24] and Silverman [94].

### 4.1 Elliptic curves over F p

Let p &gt; 3 be an odd prime. An elliptic curve E over F p is deﬁned by an equation of the form

y 2 = x 3 + ax + b,

(3)

where a, b ∈ F p , and 4a 3 + 27b 2 ≡ 0 (mod p). The set E(F p ) consists of all points (x, y), x ∈ F p , y ∈ F p that satisfy the deﬁning equation (3), together with a special point O called the point at inﬁnity.

Example 4. (Elliptic curve over F 23 ) Let p = 23 and con- sider the elliptic curve E : y 2 = x 3 + x + 4 deﬁned over F 23 . (In the notation of (3), we have a = 1 and b = 4.) Note that 4a 3 + 27b 2 = 4 + 432 = 436 ≡ 22 (mod 23), so E is indeed an elliptic curve. The points in E(F 23 ) are O and the following: (0, 2) (0, 21) (1, 11) (1, 12) (4, 7) (4, 16) (7, 3) (7, 20) (8, 8) (8, 15) (9, 11) (9, 12) (10, 5) (10, 18) (11, 9) (11, 14) (13, 11) (13, 12) (14, 5) (14, 18) (15, 6) (15, 17) (17, 9) (17, 14) (18, 9) (18, 14) (22, 5) (22, 19).

Addition formula. There is a rule, called the chord-and- tangent rule, for adding two points on an elliptic curve E(F p ) to give a third elliptic curve point. Together with this addition operation, the set of points E(F p ) forms a group with O serving as its identity. It is this group that is used in the construction of elliptic curve cryptosystems. The addition rule is best explained geometrically. Let P = (x 1 , y 1 ) and Q = (x 2 , y 2 ) be two distinct points on an elliptic curve E. Then the sum of P and Q, denoted R = (x 3 , y 3 ), is deﬁned as follows. First draw a line through P and Q; this line intersects the elliptic curve at

41

Fig. 1. Geometric description of the addition of two distinct ellip- tic curve points: P + Q = R

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 6]

a third point. Then R is the reﬂection of this point in the x axis. This is depicted in Fig. 1. The elliptic curve in the ﬁgure consists of two parts, the ellipse-like ﬁgure and the inﬁnite curve. If P = (x 1 , y 1 ), then the double of P , denoted R = (x 3 , y 3 ), is deﬁned as follows. First draw a tangent line to the elliptic curve at P . This line intersects the elliptic curve at a second point. Then R is the reﬂection of this point in the x axis. This is depicted in Fig. 2. The following algebraic formulas for the sum of two points and the double of a point can now be derived from the geometric description.

1. P + O = O + P = P for all P ∈ E(F p ). 2. If P = (x, y) ∈ E(F p ), then (x, y) + (x, −y) = O. (The point (x, −y) is denoted by −P , and is called the nega- tive of P ; observe that −P is indeed a point on the curve.) 3. (Point addition) Let P = (x 1 , y 1 ) ∈ E(F p ) and Q = (x 2 , y 2 ) ∈ E(F p ), where P = ±Q. Then P + Q = (x 3 , y 3 ), where

y 2 − y 1 x 2 − x 1

2

− x 1 − x 2 and

x 3 =

Fig. 2. Geometric description of the doubling of an elliptic curve point: P + P = R

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 6]

<!-- PDF_PAGE: 7 -->

## PDF page 7

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

42

y 2 − y 1 x 2 − x 1

(x 1 − x 3 ) − y 1 .

y 3 =

4. (Point doubling) Let P = (x 1 , y 1 ) ∈ E(F p ), where P = −P . Then 2P = (x 3 , y 3 ), where

2

3x 21 + a 2y 1 3x 21 + a 2y 1

− 2x 1 and

x 3 =

(x 1 − x 3 ) − y 1 .

y 3 =

Observe that the addition of two elliptic curve points in E(F p ) requires a few arithmetic operations (addition, subtraction, multiplication, and inversion) in the under- lying ﬁeld F p .

Example 5. (Elliptic curve addition) Consider the ellip- tic curve deﬁned in Example 4.

1. Let P = (4, 7) and Q = (13, 11). Then P + Q = (x 3 , y 3 ) is computed as follows:

2

11 − 7 − 4 − 13 = 3 2 − 4 − 13 13 − 4 = − 8 ≡ 15 (mod 23),

x 3 =

and

y 3 = 3(4 − 15) − 7 = −40 ≡ 6 (mod 23).

Hence P + Q = (15, 6). 2. Let P = (4, 7). Then 2P = P + P = (x 3 , y 3 ) is com- puted as follows:

2

3(4 2 ) + 1 − 8 = 15 2 − 8 14 = 217 ≡ 10 (mod 23),

x 3 =

and

y 3 = 15(4 − 10) − 7 = −97 ≡ 18 (mod 23).

Hence 2P = (10, 18).

### 4.2 Elliptic curves over F 2 m

An elliptic curve E over F 2 m is deﬁned by an equation of the form

y 2 + xy = x 3 + ax 2 + b,

(4)

where a, b ∈ F 2 m , and b = 0. The set E(F 2 m ) consists of all points (x, y), x ∈ F 2 m , y ∈ F 2 m that satisfy the deﬁning equation (4), together with a special point O called the point at inﬁnity.

Example 6. (Elliptic curve over F 2 4 ) Consider F 2 4 as represented by the irreducible trinomial f (x) = x 4 + x + 1

(see Example 2 of Sect. 3). Consider the elliptic curve E : y 2 + xy = x 3 + α 4 x 2 + 1 over F 2 4 . (In the notation of (4), we have a = α 4 and b = 1.) Note that b = 0, so E is indeed an elliptic curve. The points in E(F 2 4 ) are O and the following: (0, 1) (1, α 6 ) (1, α 13 ) (α 3 , α 8 ) (α 3 , α 13 ) 5 3 5 11 (α , α ) (α , α ) (α 6 , α 8 ) (α 6 , α 14 ) (α 9 , α 10 ) (α 9 , α 13 ) (α 10 , α) (α 10 , α 8 ) (α 12 , 0) (α 12 , α 12 ).

Addition formula. As with elliptic curves over F p , there is a chord-and-tangent rule for adding points on an el- liptic curve E(F 2 m ) to give a third elliptic curve point. Together with this addition operation, the set of points E(F 2 m ) forms a group with O serving as its identity. The algebraic formula for the sum of two points and the double of a point are the following. 1. P + O = O + P = P for all P ∈ E(F 2 m ). 2. If P = (x, y) ∈ E(F 2 m ), then (x, y) + (x, x + y) = O. (The point (x, x + y) is denoted by −P , and is called the negative of P ; observe that −P is indeed a point on the curve.) 3. (Point addition) Let P = (x 1 , y 1 ) ∈ E(F 2 m ) and Q = (x 2 , y 2 ) ∈ E(F 2 m ), where P = ±Q. Then P + Q = (x 3 , y 3 ), where

2

y 1 + y 2 x 1 + x 2 y 1 + y 2 x 1 + x 2

y 1 + y 2 + x 1 + x 2 + a and x 1 + x 2

x 3 =

+

y 3 =

(x 1 + x 3 ) + x 3 + y 1 .

4. (Point doubling) Let P = (x 1 , y 1 ) ∈ E(F 2 m ), where P = −P . Then 2P = (x 3 , y 3 ), where

b x 21

y 1 x 1

x 3 = x 21 + and y 3 = x 21 + x 1 + x 3 + x 3 .

Example 7. (Elliptic curve addition) Consider the elliptic curve deﬁned in Example 6.

1. Let P = (α 6 , α 8 ) and Q = (α 3 , α 13 ). Then P + Q = (x 3 , y 3 ) is computed as follows:

2

α 8 + α 13 α 6 + α 3

α 8 + α 13 + α 6 + α 3 + α 4 α 6 + α 3

x 3 =

+

2

α 3 α 2

α 3 + α 6 + α 3 + α 4 = 1 α 2

= +

and

α 8 + α 13 (α 6 + 1) + 1 + α 8 α 6 + α 3 α 3 (α 13 ) + α 2 = α 13 . α 2

y 3 =

=

Hence P + Q = (1, α 13 ). 2. Let P = (α 6 , α 8 ). Then 2P = P + P = (x 3 , y 3 ) is com- puted as follows:

1 = α 12 + α 3 = α 10 (α 6 ) 2

x 3 = (α 6 ) 2 +

<!-- PDF_PAGE: 8 -->

## PDF page 8

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

and

2 α y 3 = α 6 + α 6 + 6 α 10 + α 10 α = α 12 + α 13 + α 10 = α 8 .

8

Hence 2P = (α 10 , α 8 ).

### 4.3 Basic facts

Group order. Let E be an elliptic curve over a ﬁnite ﬁeld F q . Hasse’s theorem states that the number of points on an elliptic curve (including the point at inﬁnity) is √ #E(F q ) = q + 1 − t where |t| ≤ 2 q; #E(F q ) is called the order of E and t is called the trace of E. In other words, the order of an elliptic curve E(F q ) is roughly equal to the size q of the underlying ﬁeld.

Group structure. E(F q ) is an abelian group of rank 1 or 2. That is, E(F q ) is isomorphic to Z n 1 × Z n 2 , where n 2 di- vides n 1 , for unique positive integers n 1 and n 2 . Here, Z n denotes the cyclic group of order n. Moreover, n 2 divides q − 1. If n 2 = 1, then E(F q ) is said to be cyclic. In this case E(F q ) is isomorphic to Z n 1 , and there exists a point P ∈ E(F q ) such that E(F q ) = {kP : 0 ≤ k ≤ n 1 − 1}; such a point is called a generator of E(F q ).

Example 8. (Cyclic elliptic curve) Consider the elliptic curve E(F 23 ) deﬁned in Example 4. Since #E(F 23 ) = 29, which is prime, E(F 23 ) is cyclic and any point other than O is a generator of E(F 23 ). For ex- ample, P = (0, 2) is a generator, as the following shows: 1P = (0, 2) 2P = (13, 12) 3P = (11, 9) 4P = (1, 12) 5P = (7, 20) 6P = (9, 11) 7P = (15, 6) 8P = (14, 5) 9P = (4, 7) 10P = (22, 5) 11P = (10, 5) 12P = (17, 9) 13P = (8, 15) 14P = (18, 9) 15P = (18, 14) 16P = (8, 8) 17P = (17, 14) 18P = (10, 18) 19P = (22, 18) 20P = (4, 16) 21P = (14, 18) 22P = (15, 17) 23P = (9, 12) 24P = (7, 3) 25P = (1, 11) 26P = (11, 14) 27P = (13, 11) 28P = (0, 21) 29P = O.

5 ECDSA domain parameters

The domain parameters for ECDSA consist of a suitably chosen elliptic curve E deﬁned over a ﬁnite ﬁeld F q of characteristic p, and a base point G ∈ E(F q ). Domain pa- rameters may either be shared by a group of entities, or speciﬁc to a single user. Section 5.1 describes the requirements for what consti- tutes “suitable” domain parameters. In Sect. 5.2, a pro- cedure is speciﬁed for generating elliptic curves veriﬁably at random. Section 5.3 outlines a method for generating

43

domain parameters, while Sect. 5.4 presents a procedure for verifying that a given set of domain parameters meets all requirements.

### 5.1 Domain parameters

In order to facilitate interoperability, some restrictions are placed on the underlying ﬁeld size q and the repre- sentation used for the elements of F q . Moreover, to avoid some speciﬁc known attacks, restrictions are placed on the elliptic curve and the order of the base point.

Field requirements. The order of the underlying ﬁnite ﬁeld is either q = p, an odd prime, or q = 2 m , a power of 2. In the case q = p, the underlying ﬁnite ﬁeld is F p , the in- tegers modulo p. In the case q = 2 m , the underlying ﬁnite ﬁeld is F 2 m whose elements are represented with respect to a polynomial or a normal basis as described in Sect. 3.

Elliptic curve requirements. In order to avoid Pollard’s rho [83] and the Pohlig-Hellman [81] attacks on the el- liptic curve discrete logarithm problem (see Sect. 8.1), it is necessary that the number of F q -rational points on E be divisible by a suﬃciently large prime n. ANSI X9.62 mandates that n &gt; 2 160 . Having ﬁxed an underlying ﬁeld F q , n should be selected to be as large as possible, i.e., one should have n ≈ q, so #E(F q ) is almost prime. In the remainder of this paper, we shall assume that √ n &gt; 2 160 and that n &gt; 4 q. The co-factor is deﬁned to be h = #E(F q )/n. Some further precautions should be exercised when selecting the elliptic curve. To avoid the reduction algo- rithms of Menezes et al. [64] and Frey and Rück [29], the curve should be non-supersingular (i.e., p should not divide (q + 1 − #E(F q ))). More generally, one should verify that n does not divide q k − 1 for all 1 ≤ k ≤ C, where C is large enough so that it is computationally infeasible to ﬁnd discrete logarithms in F q C (C = 20 suf- ﬁces in practice [3]). Finally, to avoid the attack of Se- maev [93], Smart [98], and Satoh and Araki [88] on F q - anomalous curves, the curve should not be F q -anomalous (i.e., #E(F q ) = q). A prudent way to guard against these attacks, and similar attacks against special classes of curves that may be discovered in the future, is to select the elliptic curve E at random subject to the condition that #E(F q ) is divisible by a large prime – the probability that a ran- dom curve succumbs to these special-purpose attacks is negligible. A curve can be selected veriﬁably at random by choosing the coeﬃcients of the deﬁning elliptic curve equation as the outputs of a one-way function such as SHA-1 according to some pre-speciﬁed procedure. A pro- cedure for accomplishing this, similar in spirit to the method given in FIPS 186 [70] for selecting DSA primes veriﬁably at random, is described in Sect. 5.2.

Summary. To summarize, domain parameters are com- prised of:

<!-- PDF_PAGE: 9 -->

## PDF page 9

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

44

1. a ﬁeld size q, where either q = p, an odd prime, or q = 2 m ; 2. an indication FR (ﬁeld representation) of the repre- sentation used for the elements of F q ; 3. (optional) a bit string seedE of length at least 160 bits, if the elliptic curve was generated in accordance with the method described in Sect. 5.2; 4. two ﬁeld elements a and b in F q which deﬁne the equa- tion of the elliptic curve E over F q (i.e., y 2 = x 3 + ax + b in the case p &gt; 3, and y 2 + xy = x 3 + ax 2 + b in the case p = 2); 5. two ﬁeld elements x G and y G in F q which deﬁne a ﬁ- nite point G = (x G , y G ) of prime order in E(F q ); √ 6. the order n of the point G, with n &gt; 2 160 and n &gt; 4 q; and 7. the cofactor h = #E(F q )/n.

### 5.2 Generating an elliptic curve veriﬁably at random

This subsection describes the method that is used for generating an elliptic curve veriﬁably at random. The deﬁning parameters of the elliptic curve are deﬁned to be outputs of the one-way hash function SHA-1 (as speci- ﬁed in FIPS 180-1 [71]). The input seed to SHA-1 then serves as proof (under the assumption that SHA-1 cannot be inverted) that the elliptic curve was indeed generated at random. This provides some assurance to the user of the elliptic curve that the entity who generated the ellip- tic curve did not intentionally construct a “weak” curve which the entity could subsequently exploit to recover the user’s private keys. Use of this generation method can also help mitigate concerns regarding the possible future discovery of new and rare classes of weak elliptic curves, as such rare curves would essentially never be generated.

### 5.2.1 The case q = p

The following notation is used: t = log 2 p, s = (t − 1)/160, and v = t − 160 · s.

Algorithm 1: Generating a random elliptic curve over F p . Input: A ﬁeld size p, where p is an odd prime. Output: A bit string seedE of length at least 160 bits and ﬁeld elements a, b ∈ F p that deﬁne an elliptic curve E over F p .

1. Choose an arbitrary bit string seedE of length g ≥ 160 bits. 2. Compute H = SHA-1(seedE), and let c 0 denote the bit string of length v bits obtained by taking the v rightmost bits of H. 3. Let W 0 denote the bit string of length v bits obtained by setting the leftmost bit of c 0 to 0. (This ensures that r &lt; p.) 4. Let z be the integer whose binary expansion is given by the g-bit string seedE.

5. For i from 1 to s do: 4.1. Let s i be the g-bit string which is the binary ex- pansion of the integer (z + i) mod 2 g . 4.2. Compute W i = SHA-1(s i ). 6. Let W be the bit string obtained by concatenating W 0 , W 1 , . . . , W s as follows: W = W 0 W 1 · · · W s . 7. Let r be the integer whose binary expansion is given by W . 8. If r = 0 or if 4r + 27 ≡ 0 (mod p) then go to step 1. 9. Choose arbitrary integers a, b ∈ F p , not both 0, such that r · b 2 ≡ a 3 mod p. (For example, one may take a = r and b = r.) 10. The elliptic curve chosen over F p is E : y 2 = x 3 + ax + b. 11. Output(seedE, a, b).

Isomorphism classes of elliptic curves over F p . Two el- liptic curves E 1 : y 2 = x 3 + a 1 x + b 1 and E 2 : y 2 = x 3 + a 2 x + b 2 deﬁned over F p are isomorphic over F p if and only if there exists u ∈ F p , u = 0, such that a 1 = u 4 a 2 and b 1 = u 6 b 2 . (Isomorphic elliptic curves are essentially the same. In particular, if E 1 is isomorphic to E 2 , then the groups E 1 (F p ) and E 2 (F p ) are isomorphic as abelian groups.) Observe that if E 1 and E 2 are isomorphic a 3 a 3 and b 1 = 0 (so b 2 = 0), then b 2 1 = b 2 2 . The singular elliptic

1 2

curves, i.e., the curves E : y 2 = x 3 + ax + b for which 4a 3 + 27b 2 ≡ 0 (mod p) are precisely those which either have 3 27 a = 0 and b = 0, or a b 2 = − 27 4 . If r ∈ F p , r = 0, r = − 4 , then there are precisely two isomorphism classes of curves 3 E : y 2 = x 3 + ax + b with a b 2 ≡ r (mod p). Hence, there are essentially only two choices for (a, b) in step 9 of Al- gorithm 1. The conditions r = 0 and r = − 27 4 imposed in step 8 ensure the exclusion of singular elliptic curves. Fi- nally, we mention that this method of generating curves will never produce the elliptic curves with a = 0, b = 0, nor the elliptic curves with a = 0, b = 0. This is not a con- cern because such curves constitute a negligible fraction of all elliptic curves, and therefore are unlikely to ever be generated by any method which selects an elliptic curve uniformly at random.

The twist of an elliptic curve over F p . The non-isomorphic elliptic curves E 1 : y 2 = x 3 + ax + b and E 2 : y 2 = x 3 + ac 2 x 2 + bc 3 , where c ∈ F p is a quadratic non-residue mod- ulo p, are said to be twists of each other. Note that both these curves have the same r value. Their orders are re- lated by the equation #E 1 (F p ) + #E 2 (F p ) = 2p + 2. Thus, if one is able to compute #E 1 (F p ), then one can easily deduce #E 2 (F p ).

Algorithm 2: Verifying that an elliptic curve was randomly generated over F p . Input: A ﬁeld size p (a prime), a bit string seedE of length g ≥ 160 bits, and ﬁeld elements a, b ∈ F p that de- ﬁne an elliptic curve E : y 2 = x 3 + ax + b over F p . Output: Acceptance or rejection that E was randomly generated using Algorithm 1.

<!-- PDF_PAGE: 10 -->

## PDF page 10

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

1. Compute H = SHA-1(seedE), and let c 0 denote the bit string of length v bits obtained by taking the v right- most bits of H. 2. Let W 0 denote the bit string of length v bits obtained by setting the leftmost bit of c 0 to 0. 3. Let z be the integer whose binary expansion is given by the g-bit string seedE. 4. For i from 1 to s do: 4.1. Let s i be the g-bit string which is the binary expan- sion of the integer (z + i) mod 2 g . 4.2. Compute W i = SHA-1(s i ). 5. Let W be the bit string obtained by concatenating W 0 , W 1 , . . . , W s as follows: W = W 0 W 1 · · · W s . 6. Let r be the integer whose binary expansion is given by W . 7. If r · b 2 ≡ a 3 (mod p) then accept; otherwise reject.

### 5.2.2 The case q = 2 m

The following notation is used: s = (m − 1)/160 and v = m − 160 · s. Algorithm 3: Generating a random elliptic curve over F 2 m . Input: A ﬁeld size q = 2 m . Output: A bit string seedE with a length of at least 160 bits and ﬁeld elements a, b ∈ F 2 m , which deﬁne an elliptic curve E over F 2 m .

1. Choose an arbitrary bit string seedE of length g ≥ 160 bits. 2. Compute H = SHA-1(seedE), and let b 0 denote the bit string of length v bits obtained by taking the v right- most bits of H. 3. Let z be the integer whose binary expansion is given by the g-bit string seedE. 4. For i from 1 to s do: 4.1. Let s i be the g-bit string which is the binary expan- sion of the integer (z + i) mod 2 g . 4.2. Compute b i = SHA-1(s i ). 5. Let b be the ﬁeld element obtained by concatenating b 0 , b 1 , . . . , b s as follows: b = b 0 b 1 · · · b s . 6. If b = 0 then go to step 1. 7. Let a be an arbitrary element of F 2 m . 8. The elliptic curve chosen over F 2 m is E : y 2 + xy = x 3 + ax 2 + b. 9. Output(seedE, a, b).

Isomorphism classes of elliptic curves over F 2 m . Two el- liptic curves E 1 : y 2 + xy = x 3 + a 1 x 2 + b 1 and E 2 : y 2 + xy = x 3 + a 2 x 2 + b 2 deﬁned over F 2 m are isomorphic over F 2 m if and only if b 1 = b 2 and Tr(a 1 ) = Tr(a 2 ), where Tr is the trace function Tr : F 2 m −→ F 2 deﬁned by Tr(α) = α + 2 m−1 α 2 + α 2 + · · · + α 2 . (Isomorphic elliptic curves are es- sentially the same. In particular, if E 1 is isomorphic to E 2 , then the groups E 1 (F 2 m ) and E 2 (F 2 m ) are isomorphic as abelian groups.) It follows that a set of representatives of the isomorphism classes of elliptic curves over F 2 m is

45

{y 2 + xy = x 3 + ax 2 + b | b ∈ F 2 m , b = 0, a ∈ {0, γ}}, where γ ∈ F 2 m is a ﬁxed element with Tr(γ) = 1 (if m is odd, we can take γ = 1). Hence, having selected b, there are essen- tially only two choices for a in step 7 of Algorithm 3.

The twist of an elliptic curve over F 2 m . The non-iso- morphic elliptic curves E 1 : y 2 + xy = x 3 + a 1 x 2 + b and E 2 : y 2 + xy = x 3 + a 2 x 2 + b where Tr(a 1 ) = Tr(a 2 ) are said to be twists of each other. Their orders are related by the equation #E 1 (F 2 m ) + #E 2 (F 2 m ) = 2 m+1 + 2. Thus, if one is able to compute #E 1 (F 2 m ), then one can easily de- duce #E 2 (F 2 m ). The order of an elliptic curve over F 2 m is always even. Furthermore, #E 1 (F 2 m ) ≡ 0 (mod 4) if Tr(a 1 ) = 0, and #E 1 (F 2 m ) ≡ 2 (mod 4) if Tr(a 1 ) = 1.

Algorithm 4: Verifying that an elliptic curve was randomly generated over F 2 m . Input: A ﬁeld size q = 2 m , a bit string seedE of length g ≥ 160 bits, and ﬁeld elements a, b ∈ F 2 m , which deﬁne an elliptic curve E : y 2 + xy = x 3 + ax 2 + b over F 2 m . Output: Acceptance or rejection that E was randomly generated using Algorithm 3.

1. Compute H = SHA-1(seedE), and let b 0 denote the bit string of length v bits obtained by taking the v right- most bits of H. 2. Let z be the integer whose binary expansion is given by the g-bit string seedE. 3. For i from 1 to s do: 4.1. Let s i be the g-bit string which is the binary ex- pansion of the integer (z + i) mod 2 g . 4.2. Compute b i = SHA-1(s i ). 4. Let b be the ﬁeld element obtained by concatenating b 0 , b 1 , . . . , b s as follows: b = b 0 b 1 · · · b s . 5. If b = b then accept; otherwise reject.

### 5.3 Domain parameter generation

The following is one way to generate cryptographically se- cure domain parameters: 1. Select coeﬃcients a and b from F q veriﬁably at random using Algorithm 1 or Algorithm 3. Let E be the curve y 2 = x 3 + ax + b in the case q = p, and y 2 + xy = x 3 + ax 2 + b in the case q = 2 m . 2. Compute N = #E(F q ). 3. Verify that N is divisible by a large prime n (n &gt; 2 160 √ and n &gt; 4 q). If not, then go to step 1. 4. Verify that n does not divide q k − 1 for each k, 1 ≤ k ≤ 20. If not, then go to step 1. 5. Verify that n = q. If not, then go to step 1. 6. Select an arbitrary point G ∈ E(F q ) and set G = (N/n)G . Repeat until G = O.

Point counting. In 1985 Schoof [91] presented a polyno- mial-time algorithm for computing #E(F q ), the number of points on an elliptic curve over F q in the case when q is odd; the algorithm was later extended to the case

<!-- PDF_PAGE: 11 -->

## PDF page 11

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

46

of q = 2 m by Koblitz [50]. Schoof’s algorithm is rather ineﬃcient in practice for the values of q which are of prac- tical interest (i.e., q &gt; 2 160 ). In the last few years a lot of work has been done on improving and reﬁning Schoof’s algorithm, now called the Schoof–Elkies–Atkin (SEA) al- gorithm; for example, see Lercier and Morain [58] and Lercier [56]. With these improvements, cryptographically suitable elliptic curves over ﬁelds whose orders are as large as 2 200 can be randomly generated in a few hours on a workstation (see Lercier [57] and Izu et al. [44]). More recently, Satoh [87] (see also M. Fouquet et al. [26]) pre- sented a new algorithm for point counting over binary ﬁelds that is superior to the SEA algorithm. With Satoh’s algorithm, the number of points on an elliptic curve over F 2 m for m ≈ 200 can be determined in only a few seconds on a fast PC.

The complex multiplication (CM) method. Another method for generating cryptographically suitable ellip- tic curves is the CM method. Over F p the CM method is also called the Atkin–Morain method [68]; over F 2 m it is also called the Lay–Zimmer method [55]. A detailed description of the CM method can be found in IEEE 1363-2000 [39]. Let E be an elliptic curve over F q of order N . Let Z = 4q − (q + 1 − N ) 2 and write Z = DV 2 where D is a squarefree integer. Then E is said to have complex mul- tiplication by D. If one knows D for a given curve, then one can eﬃciently compute the order of the curve. The CM method ﬁrst ﬁnds a D for which there exists an elliptic curve E over F q with complex multiplication by D and having nearly prime order N = nh (where n is prime), and furthermore where n = q and n does not divide q k − 1 for each 1 ≤ k ≤ 20. It then constructs the coeﬃcients of E. The CM method is only eﬃcient for small D, in which case it is much faster than Schoof’s al- gorithm. Thus, a potential drawback of the CM method is that it can only be used to generate elliptic curves having complex multiplication by small D.

Koblitz curves. These curves, also known as anomalous binary curves, were ﬁrst proposed for cryptographic use by Koblitz [51]. They are elliptic curves over F 2 m whose deﬁning equations have coeﬃcients in F 2 . Thus, there are two Koblitz curves over F 2 m : y 2 + xy = x 3 + 1 and y 2 + xy = x 3 + x 2 + 1. Solinas [100, 102], building on the ear- lier work of Meier and Staﬀelbach [62], showed how one can compute kP very eﬃciently for arbitrary k where P is a point on a Koblitz curve. Since performing such scalar multiplications is the dominant computational step in ECDSA signature generation and veriﬁcation (see Sect. 7), Koblitz curves are very attractive for use in the ECDSA.

### 5.4 Domain parameter validation

Domain parameter validation ensures that the domain parameters have the requisite arithmetical properties.

Reasons for performing domain parameter validation in practice include: (1) prevention of malicious insertion of invalid domain parameters which may enable some at- tacks; and (2) detection of inadvertent coding or trans- mission errors. Use of an invalid set of domain parameters can void all expected security properties. An example of a concrete (albeit far-fetched) attack that can be launched if domain parameter validation for a signature scheme is not performed was demonstrated by Blake-Wilson and Menezes [11]. The attack is on a key agreement protocol which employs the ElGamal signa- ture scheme.

Methods for validating domain parameters. The assur- ance that a set D = (q, FR, a, b, G, n, h) of EC domain parameters is valid can be provided to an entity using one of the following methods:

1. A performs explicit domain parameter validation using Algorithm 5 (shown below). 2. A generates D itself using a trusted system. 3. A receives assurance from a trusted party T (e.g., a certiﬁcation authority) that T has performed ex- plicit domain parameter validation of D using Algo- rithm 5. 4. A receives assurance from a trusted party T that D was generated using a trusted system.

Algorithm 5: Explicit validation of a set of EC domain parameters. Input: A set of EC domain parameters D = (q, FR, a, b, G, n, h). Output: Acceptance or rejection of the validity of D.

1. Verify that q is an odd prime (q = p) or a power of 2 (q = 2 m ). 2. Verify that FR is a “valid” representation for F q . 3. Verify that G = O. 4. Verify that a, b, x G , and y G are properly represented elements of F q (i.e., integers in the interval [0, p − 1] in the case q = p, and bit strings of length m bits in the case q = 2 m ). 5. (Optional) If the elliptic curve was randomly gener- ated in accordance with Algorithm 1 or Algorithm 3 of Sect. 5.2, verify that seedE is a bit string with a length of at least 160 bits and use Algorithm 2 or Al- gorithm 4 to verify that a and b were suitably derived from seedE. 6. Verify that a and b deﬁne an elliptic curve over F q (i.e., 4a 3 + 27b 2 ≡ 0 (mod p) if q = p; b = 0 if q = 2 m ). 7. Verify that G lies on the elliptic curve deﬁned by a and 2 2 b (i.e., y G = x 3 G + ax G + b in the case q = p, and y G + 3 2 m x G y G = x G + ax G + b in the case q = 2 ). 8. Verify that n is prime. √ 9. Verify that n &gt; 2 160 and that n &gt; 4 q. 10. Verify that nG = O. √ 11. Compute h = ( q + 1) 2 /n and verify that h = h . 12. Verify that n does not divide q k − 1 for each k, 1 ≤ k ≤ 20.

<!-- PDF_PAGE: 12 -->

## PDF page 12

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

13. Verify that n = q. 14. If any veriﬁcation fails, then D is invalid; otherwise D is valid.

Verifying the order of an elliptic curve. Recall that by √ √ Hasse’s theorem, ( q − 1) 2 ≤ #E(F q ) ≤ ( q + 1) 2 . Hence √ 2 n &gt; 4 q implies that n does not divide #E(F q ), and thus E(F q ) has a unique subgroup of order n. Also, √ √ √ since ( q + 1) 2 − ( q − 1) 2 = 4 q, there is a unique inte- √ √ ger h such that q + 1 − 2 q ≤ nh ≤ q + 1 + 2 q, namely √ 2 h = ( q + 1) /n. Thus steps 9, 10, and 11 of Algo- rithm 5 verify that #E(F q ) is indeed equal to nh. As noted in Sect. 5.2, counting the number of points on a randomly generated elliptic curve is a complicated and cumbersome task. In practice, one may buy software from a vendor to perform the point counting. We note that since the alleged order of an elliptic curve can be ef- ﬁciently veriﬁed with 100% certainty, such software does not have to be trusted.

6 ECDSA key pairs

An ECDSA key pair is associated with a particular set of EC domain parameters. The public key is a random multiple of the base point, while the private key is the integer used to generate the multiple. Section 6.1 summa- rizes the procedure for key pair generation. Section 6.2 presents a procedure for verifying that a given public key meets all requirements. Section 6.3 discusses the impor- tance of proving possession of a private key corresponding to a public key to a certiﬁcation authority (CA) when the public key is being certiﬁed by the CA.

### 6.1 Key pair generation

An entity A’s key pair is associated with a particular set of EC domain parameters D = (q, FR, a, b, G, n, h). This association can be assured cryptographically (e.g., with certiﬁcates) or by context (e.g., all entities use the same domain parameters). The entity A must have the assur- ance that the domain parameters are valid (see Sect. 5.4) prior to key generation.

ECDSA key pair generation. Each entity A does the fol- lowing:

1. Select a random or pseudorandom integer d in the in- terval [1, n − 1]. 2. Compute Q = dG. 3. A’s public key is Q; A’s private key is d.

### 6.2 Public key validation

Public key validation, as ﬁrst enunciated by Johnson [46], ensures that a public key has the requisite arithmetical

47

properties. Successful execution of this routine demon- strates that an associated private key logically exists, although it does not demonstrate that someone has actu- ally computed the private key nor that the claimed owner actually possesses the private key. Reasons for performing public key validation in practice include: (1) prevention of malicious insertion of an invalid public key that may en- able some attacks; and (2) detection of inadvertent cod- ing or transmission errors. Use of an invalid public key can void all expected security properties. An example of a concrete attack that can be launched if public key validation is not performed was demon- strated by Lim and Lee [60]. The attack is on a Diﬃe– Hellman-based key agreement protocol.

Methods for validating public keys. The assurance that a public key Q is valid can be provided to an entity A using one of the following methods: 1. A performs explicit public key validation using Algo- rithm 6 (shown below). 2. A generates Q itself using a trusted system. 3. A receives assurance from a trusted party T (e.g., a certiﬁcation authority) that T has performed ex- plicit public key validation of A using Algorithm 6. 4. A receives assurance from a trusted party T that Q was generated using a trusted system. Algorithm 6: Explicit validation of an ECDSA public key. Input: A public key Q = (x Q , y Q ) associated with valid domain parameters (q, FR, a, b, G, n, h). Output: Acceptance or rejection of the validity of Q. 1. Check that Q = O. 2. Check that x Q and y Q are properly represented elem- ents of F q (i.e., integers in the interval [0, p − 1] in the case q = p, and bit strings of length m bits in the case q = 2 m ). 3. Check that Q lies on the elliptic curve deﬁned by a and b. 4. Check that nQ = O. 5. If any check fails, then Q is invalid; otherwise Q is valid.

### 6.3 Proof of possession of a private key

If an entity C is able to certify A’s public key Q as its own public key, then C can claim that A’s signed messages originated from C. To avoid this, the CA should require all entities A to prove possession of the private keys cor- responding to its public keys before the CA certiﬁes the public key as belonging to A. This proof of possession can be accomplished by a variety of means, for example by re- quiring A to sign a message of the CA’s choice, or by using zero-knowledge techniques (see Chaum et al. [19]). Note that proof of possession of a private key provides diﬀerent assurances than from public key validation. The former demonstrates possession of a private key even though it

<!-- PDF_PAGE: 13 -->

## PDF page 13

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

48

may correspond to an invalid public key, while the latter demonstrates validity of a public key but not ownership of the corresponding private key. Doing both provides a high level of assurance.

7 ECDSA signature generation and veriﬁcation

This section describes the procedures for generating and verifying signatures using the ECDSA.

ECDSA signature generation. To sign a message m, an entity A with domain parameters D = (q, FR, a, b, G, n, h) and associated key pair (d, Q) does the following: 1. Select a random or pseudorandom integer k, 1 ≤ k ≤ n − 1. 2. Compute kG = (x 1 , y 1 ) and convert x 1 to an integer x 1 . 3. Compute r = x 1 mod n. If r = 0 then go to step 1. 4. Compute k −1 mod n. 5. Compute SHA-1(m) and convert this bit string to an integer e. 6. Compute s = k −1 (e + dr) mod n. If s = 0 then go to step 1. 7. A’s signature for the message m is (r, s).

ECDSA signature veriﬁcation. To verify A’s signature (r, s) on m, B obtains an authentic copy of A’s domain parameters D = (q, FR, a, b, G, n, h) and associated pub- lic key Q. It is recommended that B also validates D and Q (see Sects. 5.4 and 6.2). B then does the following: 1. Verify that r and s are integers in the interval [1, n − 1]. 2. Compute SHA-1(m) and convert this bit string to an integer e. 3. Compute w = s −1 mod n. 4. Compute u 1 = ew mod n and u 2 = rw mod n. 5. Compute X = u 1 G + u 2 Q. 6. If X = O, then reject the signature. Otherwise, con- vert the x coordinate x 1 of X to an integer x 1 , and compute v = x 1 mod n. 7. Accept the signature if and only if v = r.

Proof that signature veriﬁcation works. If a signature (r, s) on a message m was indeed generated by A, then s = k −1 (e + dr) mod n. Rearranging gives

k ≡ s −1 (e + dr) ≡ s −1 e + s −1 rd ≡ we + wrd ≡ u 1 + u 2 d (mod n).

Thus u 1 G + u 2 Q = (u 1 + u 2 d)G = kG, and so v = r as re- quired.

Conversion between data types. ANSI X9.62 speciﬁes a method for converting ﬁeld elements to integers. This is used to convert the ﬁeld element x 1 to an integer in step 2 of signature generation and step 6 of signature veriﬁcation prior to computing x 1 mod n. ANSI X9.62

also speciﬁes a method for converting bit strings to in- tegers. This is used to convert the output e of SHA-1 to an integer prior to its use in the modular computation in step 5 of signature generation and step 2 of signature veriﬁcation.

Public-key certiﬁcates. Before verifying A’s signature on a message, B needs to obtain an authentic copy of A’s domain parameters D and associated public key Q. ANSI X9.62 does not specify a mechanism for achieving this. In practice, authentic public keys are most com- monly distributed via certiﬁcates. A’s public-key certiﬁ- cate should include a string of information that uniquely identiﬁes A (such as A’s name and address), her domain parameters D (if these are not already known from con- text), her public key Q, and a CA’s signature over this information. B can then use his authentic copy of the CA’s public key to verify A’s certiﬁcate, thereby obtain- ing an authentic copy of A’s static public key.

Rationale for checks on r and s in signature veriﬁca- tion. Step 1 of signature veriﬁcation checks that r and s are integers in the interval [1, n − 1]. These checks can be performed very eﬃciently and are prudent measures in light of known attacks on related ElGamal signature schemes that do not perform these checks (for examples of such attacks, see Bleichenbacher [12]). The following is a plausible attack on ECDSA if the check r = 0 (and, more generally, r ≡ 0 (mod n)) is not performed. Sup- pose that A is using the elliptic curve y 2 = x 3 + ax + b over F p , where b is a quadratic residue modulo p, and suppose √ that A uses a base point G = (0, b) of prime order n. (It is plausible that all entities select a base point with 0 x coordinate in order to minimize the size of domain pa- rameters.) An adversary can now forge A’s signature on any message m of its choice by computing e = SHA-1(m). It can easily be checked that (r = 0, s = e) is a valid signa- ture for m.

Comparing DSA and ECDSA. Conceptually, the ECDSA is simply obtained from the DSA by replacing the sub- group of order q of Z p ∗ generated by g with the subgroup of points on an elliptic curve that are generated by G. The only signiﬁcant diﬀerence between ECDSA and DSA is in the generation of r. The DSA does this by taking the random element X = g k mod p and reducing it mod- ulo q, thus obtaining an integer in the interval [1, q − 1]. The ECDSA generates r in the interval [1, n − 1] by taking the x coordinate of the random point kG and reducing it modulo n.

8 Security considerations

The security objective of ECDSA is to be existentially un- forgeable against a chosen-message attack. The goal of an adversary who launches such an attack against a legiti- mate entity A is to obtain a valid signature on a single

<!-- PDF_PAGE: 14 -->

## PDF page 14

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

message m, after having obtained A’s signature on a col- lection of messages (not including m) of the adversary’s choice. Some progress has been made in proving the security of ECDSA, albeit mostly in strong theoretical models. Slight variants of DSA and ECDSA (but not ECDSA itself) have been proven to be existentially unforge- able against chosen-message attack by Pointcheval and Stern [82] (see also [14]) under the assumptions that the discrete logarithm problem is hard and that the hash function employed is a random function. ECDSA itself has been proven secure by Brown [15] under the assump- tion that the underlying group is a generic group and that the hash function employed is collision resistant. The possible attacks on ECDSA can be classiﬁed as follows:

1. Attacks on the elliptic curve discrete logarithm prob- lem. 2. Attacks on the hash function employed. 3. Other attacks. This section summarizes the current knowledge of these attacks and how they can be avoided in practice.

### 8.1 The elliptic curve discrete logarithm problem

One way in which an adversary can succeed is to com- pute A’s private key d from A’s domain parameters (q, FR, a, b, G, n, h) and public key Q. The adversary can subsequently forge A’s signature on any message of its choice.

Problem deﬁnition. The elliptic curve discrete logarithm problem (ECDLP) is: given an elliptic curve E deﬁned over a ﬁnite ﬁeld F q , a point P ∈ E(F q ) of order n, and a point Q = lP where 0 ≤ l ≤ n − 1, determine l.

### 8.1.1 Known attacks

This subsection overviews the algorithms known for solv- ing the ECDLP and discusses how they can be avoided in practice.

1. Naive exhaustive search. In this method, one simply computes successive multiples of P : P , 2P , 3P , 4P, . . . until Q is obtained. This method can take up to n steps in the worst case. 2. Pohlig–Hellman algorithm. This algorithm, due to Pohlig and Hellman [81], exploits the factorization of n, the order of the point P . The algorithm reduces the problem of recovering l to the problem of recovering l modulo each of the prime factors of n; the desired number l can then be recovered by using the Chinese remainder theorem. The implications of this algorithm are the follow- ing. To construct the most diﬃcult instance of the ECDLP, one must select an elliptic curve whose order

49

is divisible by a large prime n. Preferably, this order should be a prime or almost a prime (i.e., a large prime n times a small integer h). For the remainder of this section, we shall assume that the order n of P is prime. 3. Baby-step giant-step algorithm. This algorithm is a time-memory trade-oﬀ of the method √ of exhaustive search. It requires storage for about n points, and its √ running time is roughly n steps in the worst case. 4. Pollard’s rho algorithm. This algorithm, due to Pol- lard [83], is a randomized version of the baby-step giant-step algorithm. It has roughly the same ex- pected running time ( πn/2 steps) as the baby-step giant-step algorithm, but is superior in that it requires a negligible amount of storage. Gallant et al. [31] and Wiener and Zuccherato [111] showed how Pollard’s rho algorithm can be sped up √ by a factor of 2. Thus the expected running √ time of Pollard’s rho method with this speedup is ( πn)/2 steps. 5. Parallelized Pollard’s rho algorithm. Van Oorschot and Wiener [80] showed how Pollard’s rho algorithm can be parallelized so that when the algorithm is run in parallel on r processors, the √ expected running time of the algorithm is roughly ( πn)/(2r) steps. That is, using r processors results in an r-fold speedup. 6. Pollard’s lambda method. This is another random- ized algorithm due to Pollard [83]. Like Pollard’s rho method, the lambda method can also be paral- lelized with a linear speedup. The parallelized lambda method is slightly slower than the parallelized rho method [80]. The lambda method is, however, faster in situations when the logarithm being sought is known to lie in a subinterval [0, b] of [0, n − 1], where b &lt; 0.39n [80]. 7. Multiple logarithms. R. Silverman and Stapleton [97] observed that if a single instance of the ECDLP (for a given elliptic curve E and base point P ) is solved using (parallelized) Pollard’s rho method, then the work done in solving this instance can be used to speed up the solution of other instances of the ECDLP (for the same curve E and base point P ). More precisely, if the ﬁrst instance takes an expected time t, √ then the second instance takes an expected time ( 2 − 1)t ≈ 0.41t. Having solved these two in- stances, √ √ the third instance takes an expected time ( 3 − 2)t ≈ 0.32t. Having solved these three in- stances, √ √ the fourth instance takes an expected time ( 4 − 3)t ≈ 0.27t, and so on. Thus subsequent in- stances of the ECDLP for a particular elliptic curve become progressively easier. Another way of looking at this is that solving k instances of the ECDLP (for √ the same curve E and base point P ) takes only k as much work as it does to solve one instance of the ECDLP. This analysis does not take into account stor- age requirements. Concerns that successive logarithms become easier can be addressed by ensuring that the elliptic param-

<!-- PDF_PAGE: 15 -->

## PDF page 15

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

50

eters are chosen so that the ﬁrst instance is infeasible to solve. 8. Supersingular elliptic curves. Menezes et al. [63, 64] and Frey and Rück [29] showed how, under mild as- sumptions, the ECDLP in an elliptic curve E deﬁned over a ﬁnite ﬁeld F q can be reduced to the ordinary DLP in the multiplicative group of some extension ﬁeld F q k for some k ≥ 1, where the number ﬁeld sieve algorithm applies. The reduction algorithm is only practical if k is small – this is not the case for most elliptic curves, as shown by Balasubramanian and Koblitz [6]. To ensure that the reduction algorithm does not apply to a particular curve, one only needs to check that n, the order of the point P , does not di- vide q k − 1 for all small k for which the DLP in F q k is tractable – in practice, when n &gt; 2 160 then 1 ≤ k ≤ 20 suﬃces [3]. An elliptic curve E over F q is said to be supersin- gular if the trace t of E is divisible by the charac- teristic p of F q . For this very special class of ellip- tic curves, it is known that k ≤ 6. It follows that the reduction algorithm yields a subexponential-time al- gorithm for the ECDLP in supersingular curves. For this reason, supersingular curves are explicitly ex- cluded from use in the ECDSA by the above divisibil- ity check. More generally, the divisibility check rules out all el- liptic curves for which the ECDLP can be eﬃciently reduced to the DLP in some small extension of F q . These include the supersingular elliptic curves and el- liptic curves of trace 2 (elliptic curves E over F q for which #E(F q ) = q − 1). 9. Prime-ﬁeld anomalous curves. An elliptic curve E over F p is said to be prime-ﬁeld-anomalous if #E(F p ) = p. Semaev [93], Smart [98], and Satoh and Araki [88] showed how to eﬃciently solve the ECDLP for these curves. The attack does not ex- tend to any other classes of elliptic curves. Con- sequently, by verifying that the number of points on an elliptic curve is not equal to the cardinal- ity of the underlying ﬁeld, one can easily ensure that the Semaev–Smart–Satoh–Araki attack does not apply. 10. Curves deﬁned over a small ﬁeld. Suppose that E is an elliptic curve deﬁned over the ﬁnite ﬁeld F 2 e . Gallant et al. [31], and Wiener and Zuccherato [111] showed how Pollard’s rho algorithm for computing elliptic curve logarithms √ in E(F 2 ed ) can be further sped up by a factor of d – thus the expected run- ning time of Pollard’s rho method for these curves is ( πn/d)/2 steps. For example, if E is a Koblitz curve (see Sect. 5.3), then Pollard’s rho algorithm for computing elliptic curve logarithms in E(F 2 m ) √ can be sped up by a factor of m. This speedup should be considered when doing a security analysis of elliptic curves whose coeﬃcients lie in a small subﬁeld.

11. Curves deﬁned over F 2 m , m composite. Galbraith and Smart [30], expanding on earlier work of Frey [27, 28], discuss how the Weil descent might be used to solve the ECDLP for elliptic curves deﬁned over F 2 m where m is composite (such ﬁelds are sometimes called composite ﬁelds). More recently, Gaudry et al. [32] reﬁned these ideas to provide some evidence that when m has a small divisor l, e.g., l = 4, the ECDLP for elliptic curves deﬁned over F 2 m can be solved faster than with Pollard’s rho algorithm. See also Menezes and Qu [66] for an analysis of the Weil descent attack. In light of these results, it seems prudent to not use elliptic curves over composite ﬁelds. It should be noted that some ECC standards, in- cluding the draft ANSI X9.63 [4], explicitly exclude the use of elliptic curves over composite ﬁelds. The ANSI X9F1 committee also agreed in January 1999 to exclude the use of such curves in a forthcoming revi- sion of ANSI X9.62. 12. Non-applicability of index-calculus methods. Whether or not there exists a general subexponential-time al- gorithm for the ECDLP is an important unsettled question, and one of great relevance to the security of ECDSA. It is extremely unlikely that anyone will ever be able to prove that no subexponential-time al- gorithm exists for the ECDLP. However, much work has been done on the DLP over the past 24 years, and more speciﬁcally on the ECDLP over the past 16 years, and no subexponential-time algorithm has been discovered for the ECDLP. Miller [67] and J. Silver- man and Suzuki [96] have given convincing arguments for why the most natural way in which the index- calculus algorithms can be applied to the ECDLP is most likely to fail. 13. Xedni-calculus attacks. A very interesting line of at- tack on the ECDLP, called the xedni-calculus attack was recently proposed by J. Silverman [95]. One in- triguing aspect of the xedni-calculus attack is that it can be adapted to solve both the ordinary dis- crete logarithm and the integer factorization prob- lems. However, it was subsequently shown by a team of researchers including J. Silverman (see Jacobson et al. [45]) that the attack is virtually certain to fail in practice. 14. Hyperelliptic curves. Hyperelliptic curves are a family of algebraic curves of arbitrary genus that includes el- liptic curves. Hence, an elliptic curve can be viewed as a hyperelliptic curve of genus 1. Adleman et al. [1] (see also Stein et al. [106]) presented a subexponential- time algorithm for the discrete logarithm problem in the jacobian of a large genus hyperelliptic curve over a ﬁnite ﬁeld. However, in the case of elliptic curves, the algorithm is worse than naive exhaustive search. 15. Equivalence to other discrete logarithm problems. Stein [105] and Zuccherato [113] showed that the dis-

<!-- PDF_PAGE: 16 -->

## PDF page 16

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

crete logarithm problem in real quadratic congruence function ﬁelds of genus 1 is equivalent to the ECDLP. Since no subexponential-time algorithm is known for the former problem, this may provide further evidence for the hardness of the ECDLP.

### 8.1.2 Experimental results

The best general-purpose algorithm known for the ECDLP is the parallelized version of Pollard’s √ rho algo- rithm, which has an expected running time of ( πn)/(2r) steps, where n is the (prime) order of the base point P and r is the number of processors utilized.

Certicom’s ECC challenge. Certicom initiated an ECC challenge [18] in November 1997 in order to encourage and stimulate research on the ECDLP. Their challenges consist of instances of the ECDLP on a selection of el- liptic curves. The challenge curves are divided into three categories listed below. In the following, ECCp-k de- notes a random curve over a ﬁeld F p , ECC2-k denotes a random curve over a ﬁeld F 2 m , and ECC2K-k de- notes a Koblitz curve (see Sect. 5.3) over F 2 m ; k is the bitlength of n. In all cases, the bitsize of the order of the underlying ﬁnite ﬁeld is equal or slightly greater than k (so curves have either prime order or almost prime order).

1. Randomly generated curves over F p , where p is prime: ECCp-79, ECCp-89, ECCp-97, ECCp-109, ECCp- 131, ECCp-163, ECCp-191, ECCp-239, and ECCp- 359. 2. Randomly generated curves over F 2 m , where m is prime: ECC2-79, ECC2-89, ECC2-97, ECC2-109, ECC2-131, ECC2-163, ECC2-191, ECC2-238, and ECC2-353. 3. Koblitz curves over F 2 m , where m is prime: ECC2K- 95, ECC2-108, ECC2-130, ECC2-163, ECC2-238, and ECC2-358.

Results of the challenge. Escott et al. [25] report on their 1998 implementation of the parallelized Pollard’s rho algorithm which incorporates some improvements of Teske [107]. The hardest instance of the ECDLP they solved was the Certicom ECCp-97 challenge. For this task they utilized over 1200 machines from at least 16 countries, and found the answer in 53 days. The total number of steps executed was about 2 × 10 14 elliptic curve √ additions, which is close to the expected time (( πn)/2 ≈ 3.5 × 10 14 , where n ≈ 2 97 ). Escott et al. [25] conclude that the running time of Pollard’s rho algorithm in practice ﬁts well with the theoretical predictions. They estimate that the ECCp-109 challenge could be solved by a network of 50 000 Pentium Pro 200 MHz machines in about 3 months.

51

### 8.1.3 Hardware attacks

Van Oorschot and Wiener [80] examined the feasibil- ity of implementing parallelized Pollard’s rho algorithm using special-purpose hardware. They estimated that if n ≈ 10 36 ≈ 2 120 , then a machine with r = 330 000 pro- cessors could be built for about U.S. $10 million that could compute a single elliptic curve discrete logarithm in about 32 days. Since ANSI X9.62 mandates that the pa- rameter n should satisfy n &gt; 2 160 , such hardware attacks appear to be infeasible with today’s technology.

### 8.2 Attacks on the hash function

Deﬁnition. A (cryptographic) hash function H is a func- tion that maps bit strings of arbitrary lengths to bit strings of a ﬁxed length t such that: 1. H can be computed eﬃciently; 2. (Preimage resistance) For essentially all y ∈ {0, 1} t it is computationally infeasible to ﬁnd a bit string x such that H(x) = y; and 3. (Collision resistance) It is computationally infeasi- ble to ﬁnd distinct bit strings x 1 and x 2 such that H(x 1 ) = H(x 2 ).

SHA-1 security requirements. The following explains how attacks on ECDSA can be successfully launched if SHA-1 is not preimage resistant or not collision resistant. 1. If SHA-1 is not preimage resistant, then an adversary E may be able to forge A’s signatures as follows. E se- lects an arbitrary integer l and computes r as the x coordinate of Q + lG reduced modulo n. E sets s = r and computes e = rl mod n. If E can ﬁnd a message m such that e = SHA-1(m), then (r, s) is a valid signa- ture for m. 2. If SHA-1 is not collision resistant, then an entity A may be able to repudiate signatures as follows. A ﬁrst generates two messages m and m such that SHA-1(m) = SHA-1(m ); such a pair of messages is called a collision for SHA-1. She then signs m and later claims to have signed m (note that every signa- ture for m is also a signature for m ).

Ideal security. A t-bit hash function is said to be have ideal security [65] if both: (1) given a hash output, pro- ducing a preimage requires approximately 2 t operations; and (2) producing a collision requires approximately 2 t/2 operations. SHA-1 is a 160-bit hash function and is be- lieved to have ideal security. The fastest method known for attacking ECDSA by exploiting properties of SHA-1 is to ﬁnd collisions for SHA-1. Since this is believed to take 2 80 steps, attacking ECDSA in this way is computation- ally infeasible. Note, however, that this attack imposes an upper bound of 2 80 on the security level of ECDSA, re- gardless of the size of the primary security parameter n. Of course, this is also the case with all present signature

<!-- PDF_PAGE: 17 -->

## PDF page 17

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

52

schemes with appendix since the only hash functions that are widely accepted as being both secure and practical are SHA-1 and RIPEMD-160 (see Dobbertin et al. [22]), both of which are 160-bit hash functions.

Variable output length hash functions. It is expected that SHA-1 will soon be replaced by a family of hash func- tions H l , where H l is an l-bit hash function having ideal security. If one uses ECDSA with parameter n, then one would use H l , where l = log 2 n, as the hash function. In this case, attacking ECDSA by solving the ECDLP and attacking ECDSA by ﬁnding collisions for H l both take approximately the same amount of time. The new family will have output lengths of 256, 384, and 512 bits [76].

### 8.3 Other attacks

Security requirements for per-message secrets. The per- message secrets k in ECDSA signature generation have the same security requirements as the private key d. This is because if an adversary E learns a single per- message secret k which was used by A to generate a signature (r, s) on some message m, then E can re- cover A’s private key since d = r −1 (ks − e) mod n where e = SHA-1(m) (see step 6 of ECDSA signature gener- ation). Hence per-message secrets must be securely gen- erated, securely stored, and securely destroyed after they have been used.

Repeated use of per-message secrets. The per-message secrets k used to sign two or more messages should be generated independently of each other. In particular, a diﬀerent per-message secret k should be generated for each diﬀerent message signed; otherwise, the private key d can be recovered. Note that if a secure random or pseu- dorandom number generator is used, then the chance of generating a repeated k value is negligible. To see how private keys can be recovered if per-message se- crets are repeated, suppose that the same per-message secret k was used to generate ECDSA signatures (r, s 1 ) and (r, s 2 ) on two diﬀerent messages m 1 and m 2 . Then s 1 ≡ k −1 (e 1 + dr) (mod n) and s 2 ≡ k −1 (e 2 + dr) (mod n), where e 1 = SHA-1(m 1 ) and e 2 = SHA-1(m 2 ). Then ks 1 ≡ e 1 + dr (mod n) and ks 2 ≡ e 2 + dr (mod n). Subtraction gives k(s 1 − s 2 ) ≡ e 1 − e 2 (mod n). If s 1 ≡ s 2 (mod n), which occurs with overwhelming probability, then k ≡ (s 1 − s 2 ) −1 (e 1 − e 2 ) (mod n). Thus, an adver- sary can determine k and then use this to recover d.

Vaudenay’s attacks. Vaudenay [109] demonstrated a the- oretical weakness in DSA based on his insight that the actual hash function used in the DSA is SHA-1 modulo q, not just SHA-1, where q is a 160-bit prime. (Since SHA-1 is a 160-bit hash function, some of its outputs, when converted to integers, are larger than q. Hence, in gen- eral, SHA-1(m) = (SHA-1(m) mod q).) This weakness al- lows the selective forgery of one message if the adversary

can select the domain parameters. This weakness is not present in ECDSA because of the requirement that n (the analogous quantity to q in the DSA) be greater than 2 160 .

Duplicate-signature key selection. A signature scheme S is said to have the duplicate-signature key selection (DSKS) property if given A’s public key P A and given A’s signature s A on a message M , an adversary E is able to select a valid key pair (P E , S E ) for S such that s A is also E’s signature on M . Note that this deﬁnition requires that S E is known to E. Blake-Wilson and Menezes [11] showed how this property can be exploited to attack a key agreement protocol which employs a signature scheme. They also demonstrated that if entities are permitted to select their own domain parameters, then ECDSA pos- sesses the DSKS property. To see this, suppose that A’s domain parameters are D A = (q, FR, a, b, G, n, h), A’s key pair is (Q A , d A ), and (r, s) is A’s signature on M . The adversary E selects an arbitrary integer c, 1 ≤ c ≤ n − 1, such that t := ((s −1 e + s −1 rc) mod n) = 0, computes X = s −1 eG + s −1 rQ (where e = SHA-1(M )) and G = (t −1 mod n)X. E then forms D E = (q, FR, a, b, G, n, h) and Q E = cG. Then it is easily veriﬁed that D E and Q E are valid and that (r, s) is also E’s signature on M . If one mandates that the generating point G be se- lected veriﬁably at random during domain parameter generation (using a method akin to those in Sect. 5.2 for generating elliptic curves veriﬁably at random), then it appears that ECDSA no longer possesses the DSKS prop- erty. It must be emphasized that possession of the DSKS property does not constitute a weakness of the signature scheme – the goal of a signature scheme is to be exis- tentially unforgeable against an adaptive chosen-message attack. Rather, it demonstrates the importance of audit- ing domain parameter and public key generation.

Implementation attacks. ANSI X9.62 does not address attacks that could be launched against implementations of ECDSA such as timing attacks (Kocher [53]), dif- ferential fault analysis (Boneh et al. [13]), diﬀerential power analysis (Kocher et al. [54]), and attacks which ex- ploit weak random or pseudorandom number generators (Kelsey et al. [48]).

9 Implementation considerations

Before implementing ECDSA, several basic choices have to be made including: 1. Type of underlying ﬁnite ﬁeld F q (F p or F 2 m ). 2. Field representation (e.g., polynomial or normal basis for F 2 m ). 3. Type of elliptic curve E over F q (e.g., random curve or Koblitz curve). 4. Elliptic curve point representation (e.g., aﬃne or pro- jective coordinates [39]). There are many factors that can inﬂuence the choices made. All of these must be considered simultaneously in

<!-- PDF_PAGE: 18 -->

## PDF page 18

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

order to arrive at the best solution for a particular appli- cation. The factors include: – Security considerations. – Suitability of methods available for optimizing ﬁnite ﬁeld arithmetic (addition, multiplication, squaring, and inversion). – Suitability of methods available for optimizing elliptic curve arithmetic (point addition, point doubling, and scalar multiplication). – Application platform (software, hardware, or ﬁrm- ware). – Constraints of a particular computing environment (e.g., processor speed, storage, code size, gate count, power consumption). – Constraints of a particular communications environ- ment (e.g., bandwidth, response time).

Selected references to the literature. The most detailed and comprehensive reference available on techniques for eﬃcient ﬁnite ﬁeld and elliptic curve arithmetic is IEEE 1363-2000 [39]. See Gordon [36] for a detailed survey of various methods for scalar multiplication. For an im- plementation report of elliptic curve operations over F p and F 2 m , see Schroeppel et al. [92], De Win et al. [112], Hasegawa et al. [38], Brown et al. [16, 17], and Hankerson et al. [37].

10 Interoperability considerations

The goals of cryptographic standards are twofold: 1. To facilitate the widespread use of cryptographically sound and well-speciﬁed techniques. 2. To promote interoperability between diﬀerent imple- mentations.

Factors aﬀecting interoperability. Interoperability is en- couraged by completely specifying the steps of the cryp- tographic schemes and the formats for shared data such as domain parameters, keys, and exchanged messages, and by limiting the number of options available to the implementor. For elliptic curve cryptography and, in par- ticular, the ECDSA, the factors that can impact interop- erability include: 1. The number, and types, of allowable ﬁnite ﬁelds. 2. The number of allowable representations for the elem- ents of an allowable ﬁnite ﬁeld. 3. The number of allowable elliptic curves over an allow- able ﬁnite ﬁeld. 4. The formats for specifying ﬁeld elements, elliptic curve points, domain parameters, public keys, and sig- natures.

### 10.1 ECDSA standards

Among the standards and draft standards which spec- ify ECDSA, the ones which have been oﬃcially ap-

53

proved by their respective accredited organizations are ANSI X9.62 [3], FIPS 186-2 [74], IEEE 1363-2000 [39], and ISO 14888-3 [42]. ECDSA has also been standard- ized by the Standards for Eﬃcient Cryptography Group (SECG) [103], which is a consortium of companies formed to address potential interoperability problems with cryp- tographic standards. The salient features of these standards are described ﬁrst, and then the standards are compared with regards to their compatibility with each other. This is followed by a brief overview of some other standards that specify or use ECDSA.

Core ECDSA standards. 1. ANSI X9.62 : This project began in 1995 and was adopted as an oﬃcial ANSI standard in January 1999. The primary objectives of ANSI X9.62 were to achieve a high level of security and interoperability. The un- derlying ﬁeld is restricted to being a prime ﬁnite ﬁeld F p or a binary ﬁnite ﬁeld F 2 m . The elements of F 2 m may be represented using a polynomial or a nor- mal basis over F 2 . If a polynomial basis is desired, ANSI X9.62 mandates that the reduction polynomial be an irreducible trinomial, provided one exists, and an irreducible pentanomial otherwise. To facilitate in- teroperability, a speciﬁc reduction polynomial is rec- ommended for each ﬁeld F 2 m . If a normal basis is desired, ANSI X9.62 mandates that a speciﬁc Gaus- sian normal basis be used. The primary security re- quirement imposed on elliptic curves in ANSI X9.62 is that n, the order of the base point G, be greater than 2 160 . Elliptic curves may either be selected arbitrar- ily (subject to the security constraints mentioned in Sect. 5.1) or veriﬁably at random (using the procedure described in Sect. 5.3). ANSI X9.62 deﬁnes a manda- tory octet string representation for elliptic points in either compressed, uncompressed, or hybrid form. Op- tional ASN.1 (abstract syntax notation one) syntax is provided for unambiguously describing domain pa- rameters, public keys, and signatures. 2. FIPS 186-2 : In May 1997, NIST announced plans to revise FIPS 186 by including RSA and elliptic curve signature algorithms. In December 1998, FIPS 186 was revised to include both the DSA and RSA sig- nature schemes (as speciﬁed in ANSI X9.31 [2]); the revised standard was called FIPS 186-1 [73]. Shortly after that, in June 1999, NIST presented a list of 15 elliptic curves that were recommended for U.S. Federal Government use. These curves are compliant with the ANSI X9.62 formats (and therefore also with IEEE 1363-2000 formats) and are discussed further in Sect. 10.2. In February 2000, FIPS 186-1 was revised to include ECDSA as speciﬁed in ANSI X9.62 with the aforementioned recommended elliptic curves; the re- vised standard is called FIPS 186-2. 3. IEEE 1363-2000 : This project was formally approved as an IEEE standard in August 2000. IEEE 1363’s

<!-- PDF_PAGE: 19 -->

## PDF page 19

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

54

scope is very broad and includes public-key crypto- graphic techniques for encryption, key agreement, and signatures based on the intractability of integer fac- torization, discrete logarithms in ﬁnite ﬁelds, and el- liptic curve discrete logarithms. It diﬀers fundamen- tally from ANSI X9.62 and FIPS 186-2 in that it does not mandate minimum security requirements (e.g., lower bounds on the order n of the base point G) and has an abundance of options. Consequently, 1363-2000 should neither be viewed as a security standard nor as an interoperability standard, but rather as a reference for speciﬁcations of a variety of techniques from which applications may select. With regards to the elliptic curve schemes and, in particular, ECDSA, the under- lying ﬁeld is restricted to being a prime ﬁnite ﬁeld F p or a binary ﬁnite ﬁeld F 2 m . The elements of F 2 m may be represented with respect to any polynomial or nor- mal basis over F 2 . The representation of F p elements as integers and F 2 m elements as bit strings are consis- tent with ANSI X9.62 and FIPS 186-2 conventions. 4. ISO/IEC 14888-3 [42]: This standard contains high- level descriptions of some signature algorithms includ- ing ECDSA, whose description is consistent with that of ANSI X9.62. 5. SEC 1 [103] and SEC 2 [104]: SEC 1 describes the ECDSA, and also elliptic curve public-key encryp- tion and key agreement protocols. A speciﬁc list of recommended elliptic curve domain parameters are provided in SEC 2. SEC 1 ECDSA is compliant with ANSI X9.62, except that the former permits some ﬁelds of bitlength less than 160.

Compatibility. Any ECDSA implementation that is con- formant with FIPS 186-2 is also conformant with SEC 1; however, the converse is not necessarily true. Any ECDSA implementation that is conformant with SEC 1 (with n &gt; 2 160 ) is conformant with ANSI X9.62; however, the converse is not necessarily true. Furthermore, any ECDSA implementation that is conformant with ANSI X9.62 is also conformant with IEEE 1363-2000; however, the converse is not necessarily true. Finally, any ECDSA implementation that is conformant with IEEE 1363-2000 is also conformant with ISO 14888-3, but the converese is not necessarily true. This conformance relationship between the ﬁve ECDSA standards is de- picted in Fig. 3.

Other ECDSA standards. ECDSA is being considered for inclusion in numerous core cryptography and applica- tions standards. These include: 1. ISO/IEC 15946 [43]: This draft standard speciﬁes var- ious cryptographic techniques based on elliptic curves including signature schemes, public-key encryption schemes, and key establishment protocols. ISO/IEC 15946 allows any ﬁnite ﬁeld, unlike ANSI X9.62, IEEE 1363-2000, and FIPS 186-2 where the under- lying ﬁeld is required to be either a prime ﬁeld or

ISO 14888-3 IEEE 1363-2000 ANSI X9.62 SEC 1 FIPS 186-2

Fig. 3. Compatibility of FIPS 186-2, SEC 1, ANSI X9.62, IEEE 1363-2000, and ISO 14888-3 speciﬁcations of ECDSA

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 19]

a binary ﬁeld. It is expected that the ECDSA descrip- tion will be consistent with that of ANSI X9.62. 2. IETF PKIX (Internet Engineering Task Force Pub- lic Key Infrastructure X.509-Based): An internet draft [7] proﬁles the format of ECDSA domain pa- rameters and public keys for use in X.509 certiﬁcates. The formats are consistent with those present in ANSI X9.62. 3. IETF TLS (Internet Engineering Task Force Trans- port Layer Security): This is the IETF’s adoption of SSL (secure sockets layer) which provides conﬁ- dentiality, integrity, and authentication for network connections. ANSI X9.62 ECDSA is currently being considered for inclusion as one of the signature algo- rithms [20]. 4. WAP WTLS [110] (Wireless Application Protocol Wireless Transport Layer Security): Provides trans- port layer security for an architecture that enables secure web browsing for mobile devices such as cel- lular phones, personal device assistants, and pagers. ANSI X9.62 ECDSA is used for authentication.

### 10.2 NIST recommended curves

This section presents the 15 elliptic curves that were rec- ommended (but not mandated) by NIST for U.S. Federal Government use [74].

Recommended ﬁnite ﬁelds. There are 10 recommended ﬁ- nite ﬁelds:

1. The prime ﬁelds F p for p = 2 192 − 2 64 − 1, p = 2 224 − 2 96 + 1, p = 2 256 − 2 224 + 2 192 + 2 96 − 1, p = 2 384 − 2 128 − 2 96 + 2 32 − 1, and p = 2 521 − 1. 2. The binary ﬁelds F 2 163 , F 2 233 , F 2 283 , F 2 409 , and F 2 571 .

The factors which inﬂuenced the choices of ﬁelds were:

(i)

The ﬁelds were selected so that the bitlengths of their orders are twice the key lengths of common symmetric-key block ciphers – this is because ex- haustive key search of a k-bit block cipher is ex- pected to take roughly the same time as the solution of an instance of the elliptic curve discrete logarithm problem using Pollard’s rho algorithm for an ap- propriately selected elliptic curve over a ﬁnite ﬁeld

<!-- PDF_PAGE: 20 -->

## PDF page 20

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

whose order has bitlength 2k. The correspondence between symmetric cipher key lengths and ﬁeld sizes is given in Table 1. (ii) For prime ﬁelds F p , the prime moduli p are of a special type (called generalized Mersenne num- bers) for which modular multiplication can be car- ried out more eﬃciently than in general; see [74] and [101]. (iii) For binary ﬁelds F 2 m , m was chosen so that there ex- ists a Koblitz curve of almost prime order over F 2 m . Since #E(F 2 l ) divides #E(F 2 m ) whenever l divides m, this requirement imposes the condition that m be prime.

Recommended elliptic curves. There are three types of el- liptic curves:

1. Random elliptic curves over F p . 2. Koblitz elliptic curves over F 2 m . 3. Random elliptic curves over F 2 m .

The parameters of these curves are presented below. In these subsections, parameters are either given in decimal

55

form or in hexadecimal form preceded by ‘0x’. For the bi- nary ﬁelds, the additive and multiplicative identities are simply denoted by 0 and 1. A method for converting be- tween polynomial and normal basis representations for F 2 m is given at the end of this section.

### 10.2.1 Random elliptic curves over F p

The following parameters are given for each elliptic curve:

The order of the prime ﬁeld F p . The seed used to randomly generate the coeﬃ- cients of the elliptic curve using Algorithm 1. The output of SHA-1 in Algorithm 1. The coeﬃcients of the elliptic curve y 2 = x 3 + ax + b satisfying rb 2 ≡ a 3 mod p. The selection a = −3 was made for reasons of eﬃciency; see IEEE 1363-2000 [39]. The x and y coordinates of the base point G. The (prime) order of G. The co-factor.

p seedE

r a, b

x G , y G n h

Table 1. Recommended ﬁeld sizes for U.S. Federal Government use.

Symmetric cipher key length

Example algorithm

80 112 128 192 256

SKIPJACK [77] Triple-DES AES small [75] AES medium [75] AES large [75]

Bitlength of p in prime ﬁeld F p

Dimension m of binary ﬁeld F 2 m

192 224 256 384 521

163 233 283 409 571

<!-- PDF_PAGE: 21 -->

## PDF page 21

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

56

### 10.2.2 Koblitz elliptic curves over F 2 m

The parameters of the (same) Koblitz curve and base point are given in both normal basis representation (in- dicated by FR) and in polynomial basis representation (indicated by FR2). A method for converting between the two representations is given at the end of this sec- tion. The following parameters are given for each Koblitz curve:

The extension degree of the binary ﬁeld F 2 m . An indication of the representation used for the elements of F 2 m in accordance with ANSI X9.62. The coeﬃcients of the elliptic curve y 2 + xy = x 3 + ax 2 + b. The x and y coordinates of the base point G. The (prime) order of G. The co-factor.

m FR

a, b

x G , y G n h

<!-- PDF_PAGE: 22 -->

## PDF page 22

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

FR2

An indication of the second representation used for the elements of F 2 m in accordance with ANSI X9.62. a2, b2 The coeﬃcients of the (same) elliptic curve using representation FR2. x G 2, y G 2 The x and y coordinates of the (same) base point G using representation FR2.

57

### 10.2.3 Random elliptic curves over F 2 m

Each random elliptic curve over F 2 m was generated using Algorithm 3. The output of SHA-1 was interpreted as an element of a binary ﬁeld represented with a Gaussian nor- mal basis. The parameters of the (same) elliptic curve and base point are given in both normal basis representation

<!-- PDF_PAGE: 23 -->

## PDF page 23

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

58

(indicated by FR) and in polynomial basis representation (indicated by FR2). A method for converting between the two representations is given at the end of this section. The following parameters are given for each elliptic curve:

The extension degree of the binary ﬁeld F 2 m . An indication of the representation used for the elements of F 2 m in accordance with ANSI X9.62. The seed used to randomly generate the co- eﬃcients of the elliptic curve using Algo- rithm 3. The coeﬃcients of the elliptic curve y 2 + xy = x 3 + ax 2 + b. The x and y coordinates of the base point G. The (prime) order of G. The co-factor.

m FR

seedE

a, b

x G , y G n h

An indication of the second representation used for the elements of F 2 m in accordance with ANSI X9.62. a2, b2 The coeﬃcients of the (same) elliptic curve using representation FR2. x G 2, y G 2 The x and y coordinates of the (same) base point G using representation FR2.

FR2

### 10.2.4 Converting between polynomial and normal basis representations

This section describes one method, utilizing multipli- cation by a change-of-basis matrix, for converting the elements of F 2 m represented with respect to a particu- lar polynomial basis to the elements of F 2 m represented with respect to a particular normal basis, and vice versa.

<!-- PDF_PAGE: 24 -->

## PDF page 24

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

The change-of-basis matrices for converting between the polynomial basis and normal basis representations of the ﬁelds F 2 163 , F 2 233 , F 2 283 , F 2 409 , and F 2 571 are presented. There are other methods available for performing the con- versions; e.g., see Kaliski and Yin [47].

Normal basis to polynomial basis conversion. Suppose that α is an element of the ﬁeld F 2 m . Let a be its bit string representation with respect to a given nor- mal basis, and let a be its bit string representation

59

with respect to a given polynomial basis. Then a can be derived from a via the matrix computation a = aA, where A is an m × m binary matrix. The matrix A, which depends only on the bases, can be computed eas- ily given its top row R as follows. Let β be the elem- ent of F 2 m whose representation with respect to the polynomial basis is R. Then the rows of A, from top to bottom, are the bit strings representing the elem- 2 m−1 ents β, β 2 , β 2 , . . . , β 2 with respect to the polynomial basis.

<!-- PDF_PAGE: 25 -->

## PDF page 25

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

60

The following gives the top row R for each conversion from the normal bases indicated by FR to the polynomial bases indicated by FR2.

Polynomial basis to normal basis conversion. Suppose that α is an element of the ﬁeld F 2 m . Let a be its bit string representation with respect to a given nor- mal basis, and let a be its bit string representation with respect to a given polynomial basis. Then a can be derived from a via the matrix computation a = aB, where B is an m × m binary matrix. The matrix B, which depends only on the bases, can be computed eas- ily given its second-to-last row S as follows. Let β be the element of F 2 m whose representation with respect to the normal basis is S. Then the rows of B, from top

to bottom, are the bit strings representing the elem- ents β m−1 , β m−2 , . . . , β 2 , β, 1 with respect to the normal basis. The following gives the second-to-last row S for each conversion from the polynomial bases indicated by FR2 to the normal bases indicated by FR.

11 Conclusions

ECDSA is now an ANSI, IEEE, NIST, and ISO stan- dard and is being standardized by several other standards organizations. This paper described the ANSI X9.62 ECDSA, presented rationale for some design decisions, and discussed related security, implementation, and in-

<!-- PDF_PAGE: 26 -->

## PDF page 26

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

teroperability issues. We hope that this paper con- tributes to an increased understanding of the properties of ECDSA, and facilitates its use in practice.

Acknowledgements. The authors would like to thank the members of the ANSI X9F1 and IEEE P1363 working groups, and, in par- ticular, Jerry Solinas, for their many comments and contributions during the development of the ECDSA standards.

### References

1. Adleman L, DeMarrais J, Huang M (1994) A subexponential algorithm for discrete logarithms over the rational subgroup of the jacobians of large genus hyperelliptic curves over ﬁnite ﬁelds. In: Algorithmic Number Theory, Lecture Notes in Com- puter Science, vol 877. Springer, Berlin Heidelberg New York, pp 28–40 2. ANSI X9.31 (1998) Digital signatures using reversible public key cryptography for the ﬁnancial services industry (rDSA) 3. ANSI X9.62 (1999) Public key cryptography for the ﬁnancial services industry: the elliptic curve digital signature algorithm (ECDSA) 4. ANSI X9.63 (2000) Public key cryptography for the ﬁnancial services industry: elliptic curve key agreement and key trans- port protocols. Working draft 5. Ash D, Blake I, Vanstone S (1989) Low complexity normal bases. Discrete Appl Math25:191–210 6. Balasubramanian R, Koblitz N (1998) The improbability that an elliptic curve has subexponential discrete log problem under the Menezes–Okamoto–Vanstone algorithm. J Cryptol- ogy 11:141–145 7. Bassham L, Johnson D, Polk T (1999) Representation of El- liptic Curve Digital Signature Algorithm (ECDSA) Keys and Signatures in Internet X.509 Public Key Infrastructure Cer- tiﬁcates. Internet Draft, Available at http://www.ietf.org 8. Bellare M, Canetti R, Krawczyk H (1998) A modular ap- proach to the design and analysis of authentication and key exchange protocols. In: Proceedings of the 30th Annual ACM Symposium on the Theory of Computing, Dallas. ACM Press, pp 419–428 9. Blake I, Seroussi G, Smart N (1999) Elliptic curves in cryptog- raphy. Cambridge University Press, Cambridge 10. Blake-Wilson S, Menezes A (1997) Entity authentication and authenticated key transport protocols employing asymmetric

61

techniques. In: Proceedings of the 5th International Workshop on Security Protocols, Lecture Notes in Computer Science, vol 1361. Springer, Berlin Heidelberg New York, pp 137–158 11. Blake-Wilson S, Menezes A (1999) Unknown key-share at- tacks on the station-to-station (STS) protocol. In: Public Key Cryptography – Proceedings of PKC ’99, Lecture Notes in Computer Science, vol 1560. Springer, Berlin Heidelberg New York, pp 154–170 12. Bleichenbacher D (1996) Generating ElGamal signatures without knowing the secret key. In: Advances in Cryptology – Eurocrypt ’96, Lecture Notes in Computer Science, vol 1070. Springer, Berlin Heidelberg New York, pp 10–18 13. Boneh D, DeMillo R, Lipton R (1997) On the importance of checking cryptographic protocols for faults. In: Advances in Cryptology – Eurocrypt ’97, Lecture Notes in Computer Science, vol 1233. Springer, Berlin Heidelberg New York, pp 37–51 14. Brickell E, Pointcheval D, Vaudenay S, Yung M (2000) Design validations for discrete logarithm based signature schemes. In: Public Key Cryptography – Proceedings of PKC 2000, Lec- ture Notes in Computer Science, vol 1751. Springer, Berlin Heidelberg New York, pp 276–292 15. Brown D (2000) The exact security of ECDSA. Technical re- port CORR 2000-54, Department of C&amp;O, University of Wa- terloo. Available from http://www.cacr.math.uwaterloo.ca 16. Brown M, Cheung D, Hankerson D, Hernandez J, Kirkup M, Menezes A (2000) PGP in constrained wireless devices. In: Proceedings of the Ninth USENIX Security Symposium, Denver. USENIX Association, pp 247-261 17. Brown M, Hankerson D, Hernandez J, Menezes A (2001) Soft- ware implementation of the NIST elliptic curves over prime ﬁelds. In: Topics in Cryptology – CT-RSA 2001, Lecture Notes in Computer Science, vol 2020, Springer, Berlin Heidelberg New York, pp 250–265 18. Certicom ECC Challenge (1997) http://www.certicom.com 19. Chaum D, Evertse J-H, van de Graaf J (1988) An improved protocol for demonstrating possession of discrete logarithms and some generalizations. In: Advances in Cryptology – Eu- rocrypt ’87, Lecture Notes in Computer Science, vol 304. Springer, Berlin Heidelberg New York, pp 127–141 20. Dierks T, Anderson B (1998) ECC cipher suites for TLS. Internet Draft, Available at http://www.ietf.org 21. Diﬃe W, van Oorschot P, Wiener M (1992) Authentication and authenticated key exchanges. Des Codes Cryptography 2:107–125 22. Dobbertin H, Bosselaers A, Preneel B (1996) RIPEMD-160: a strengthened version of RIPEMD. In: Fast Software Encryp-

<!-- PDF_PAGE: 27 -->

## PDF page 27

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

62

tion – FSE ’96, Lecture Notes in Computer Science, vol 1039. Springer, Berlin Heidelberg New York, pp 71–82 23. ElGamal T (1985) A public key cryptosystem and a signature scheme based on discrete logarithms. IEEE Trans Inf Theory 31:469–472 24. Enge A (1999) Elliptic curves and their applications to cryp- tography – an introduction. Kluwer, Boston 25. Escott A, Sager J, Selkirk A, Tsapakidis D (1999) Attack- ing elliptic curve cryptosystems using the parallel Pollard rho method. CryptoBytes – The Technical Newsletter of RSA Laboratories 4(2):15–19; Also available at http://www.rsasecurity.com 26. Fouquet M, Gaudry P, Harley R (2000) On Satoh’s algorithm and its implementation, J Ramanujan Math Soc 15:281–318 27. Frey G (1998) How to disguise an elliptic curve (Weil descent). Talk at ECC ’98. Workshop on Elliptic Curve Cryptography. Slides available at http://www.cacr.math.uwaterloo.ca 28. Frey G (2001) Applications of arithmetical geometry to cryp- tographic constructions. Proceedings of the Fifth Interna- tional Conference on Finite Fields and Applications. Springer, Berlin Heidelberg New York, pp 128–161 29. Frey G, Rück H (1994) A remark concerning m-divisibility and the discrete logarithm in the divisor class group of curves. Mathematics Comput 62:865–874 30. Galbraith S, Smart N (1999) A cryptographic application of Weil descent. In: Codes and Cryptography, Lecture Notes in Computer Science, vol 1746. Springer, Berlin Heidelberg New York, pp 191-200 31. Gallant R, Lambert R, Vanstone S (2000) Improving the par- allelized Pollard lambda search on anomalous binary curves. Mathematics Computation 69:1699–1705 32. Gaudry P, Hess F, Smart N (2000) Constructive and de- structive facets of Weil descent on elliptic curves, preprint. Available from http://www.hpl.hp.com/techreports/2000/ HPL-2000-10.html 33. Goldwasser S, Micali S, Rivest R (1988) A digital signature scheme secure against adaptive chosen message attacks, SIAM J Comput 17:281–308 34. Gordon D (1993) Designing and detecting trapdoors for dis- crete log cryptosystems. In: Advances in Cryptology – Crypto ’92, Lecture Notes in Computer Science, vol 740. Springer, Berlin Heidelberg New York, pp 66-75 35. Gordon D (1993) Discrete logarithms in GF (p) using the num- ber ﬁeld sieve. SIAM J Discrete Math 6:124–138 36. Gordon D (1998) A survey of fast exponentiation methods. J Algorithms 27:129–146 37. Hankerson D, Hernandez J, Menezes A (2001) Software im- plementation of elliptic curve cryptography over binary ﬁelds. In: Proceedings of CHES 2000. Lecture Notes in Computer Science, vol 1965. Springer, Berlin Heidelberg New York, pp 1–24 38. Hasegawa T, Nakajima J, Matsui M (1998) A practical im- plementation of elliptic curve cryptosystems over GF (p) on a 16-bit microcomputer. In: Public Key Cryptography – Pro- ceedings of PKC ’98, Lecture Notes in Computer Science, vol 1431. Springer, Berlin Heidelberg New York, pp 182–194 39. IEEE 1363 (2000) Standard Speciﬁcations for Public- Key Cryptography. http://grouper.ieee.org/groups/1363/ index.html 40. ISO/IEC 9798-3 (1993) Information technology – security techniques – entity authentication mechanisms. Part 3: En- tity authentication using a public-key algorithm, 1st edn. ISO, International Organization for Standardization, Geneva 41. ISO/IEC 11770-3 (1999) Information technology – security techniques – key management. Part 3: Mechanisms using asymmetric techniques. ISO, International Organization for Standardization, Geneva 42. ISO/IEC 14888-3 (1998) Information technology – security techniques – digital signatures with appendix. Part 3: Certiﬁ- cate based-mechanisms. ISO, International Organization for Standardization, Geneva 43. ISO/IEC 15946 (1999) Information technology – security tech- niques – cryptographic techniques based on elliptic curves, committee draft. ISO, International Organization for Stan- dardization, Geneva

44. Izu T, Kogure J, Noro M, Yokoyama K (1999) Eﬃcient imple- mentation of Schoof’s algorithm. In: Advances in Cryptology – Asiacrypt ’98, Lecture Notes in Computer Science, vol 1514. Springer, Berlin Heidelberg New York, pp 66–79 45. Jacobson M, Koblitz N, Silverman J, Stein A, Teske E (2000) Analysis of the xedni calculus attack. Des Codes Cryptogra- phy 20:41–64. 46. Johnson D (1997) Key validation. Contribution to ANSI X9F1 working group 47. Kaliski B, Yin Y (1999) Storage-eﬃcient ﬁnite ﬁeld basis con- version. In: Selected Areas in Cryptography, Lecture Notes in Computer Science, vol 1556. Springer, Berlin Heidelberg New York, pp 81–93 48. Kelsey J, Schneier B, Wagner D, Hall C (1998) Cryptanalytic attacks on pseudorandom number generators. In: Fast Software Encryption – FSE ’98, Lecture Notes in Computer Science, vol 1372. Springer, Berlin Heidelberg New York, pp 168–188 49. Koblitz N (1987) Elliptic curve cryptosystems. Math Comput 48:203–209 50. Koblitz N (1991) Constructing elliptic curve cryptosystems in characteristic 2. In: Advances in Cryptology – Crypto ’90, Lecture Notes in Computer Science, vol 537. Springer, Berlin Heidelberg New York, pp 156–167 51. Koblitz N (1992) CM-curves with good cryptographic proper- ties. In: Advances in Cryptology – Crypto ’91, Lecture Notes in Computer Science, vol 576. Springer, Berlin Heidelberg New York, pp 279–287 52. Koblitz N (1994) A course in number theory and cryptogra- phy, 2nd edn. Springer, Berlin Heidelberg New York 53. Kocher P (1996) Timing attacks on implementations of Diﬃe- Hellman, RSA, DSS, and other systems. In: Advances in Cryptology – Crypto ’96, Lecture Notes in Computer Science, vol 1109. Springer, Berlin Heidelberg New York, pp 104–113 54. Kocher P, Jaﬀe J, Jun B (1999) Diﬀerential power analysis. In: Advances in Cryptology – Crypto ’99, Lecture Notes in Com- puter Science, vol 1666. Springer, Berlin Heidelberg New York, pp 388–397 55. Lay G, Zimmer H (1994) Constructing elliptic curves with given group order over large ﬁnite ﬁelds. In: Algorithmic Num- ber Theory, Lecture Notes in Computer Science, vol 877. Springer, Berlin Heidelberg New York, pp 250–263 56. Lercier R (1996) Computing isogenies in F 2 n . In: Algorithmic Number Theory, Lecture Notes in Computer Science, vol 1122. Springer, Berlin Heidelberg New York, pp 197–212 57. Lercier R (1997) Finding good random elliptic curves for cryptosystems deﬁned F 2 n . In: Advances in Cryptology – Eu- rocrypt ’97, Lecture Notes in Computer Science, vol 1233. Springer, Berlin Heidelberg New York, pp 379–392 58. Lercier R, Morain F (1995) Counting the number of points on elliptic curves over ﬁnite ﬁelds: strategies and performances. In: Advances in Cryptology – Eurocrypt ’95, Lecture Notes in Computer Science, vol 921. Springer, Berlin Heidelberg New York, pp 79–94 59. Lidl R, Niederreitter H (1984) Introduction to ﬁnite ﬁelds and their applications, Cambridge University Press, Cambridge 60. Lim C, Lee P (1997) A key recovery attack on discrete log- based schemes using a prime order subgroup. In: Advances in Cryptology – Crypto ’97, Lecture Notes in Computer Science, vol 1294. Springer, Berlin Heidelberg New York, pp 249–263 61. McEliece R (1987) Finite ﬁelds for computer scientists and engineers. Kluwer, Boston 62. Meier W, Staﬀelbach O (1993) Eﬃcient multiplication on certain nonsupersingular elliptic curves. In: Advances in Cryptology – Crypto ’92, Lecture Notes in Computer Sci- ence, vol 740. Springer, Berlin Heidelberg New York, pp 333– 344 63. Menezes A (1993) Elliptic curve public key cryptosystems. Kluwer, Boston 64. Menezes A, Okamoto T, Vanstone S Reducing elliptic curve logarithms to logarithms in a ﬁnite ﬁeld. IEEE Trans Inf The- ory 39:1639–1646 65. Menezes A, van Oorschot P, Vanstone S Handbook of applied cryptography. CRC Press, Boca Raton, FL 66. Menezes A, Qu M (2001) Analysis of the Weil descent at- tack of Gaudry, Hess and Smart. In: Topics in Cryptology –

<!-- PDF_PAGE: 28 -->

## PDF page 28

### D. Johnson, A. Menezes, S. Vanstone: The Elliptic Curve Digital Signature Algorithm (ECDSA)

CT-RSA 2001, Lecture Notes in Computer Science, vol 2020, Springer, Berlin Heidelberg New York, pp 308–318 67. Miller V (1986) Uses of elliptic curves in cryptography. In: Advances in Cryptology – Crypto ’85, Lecture Notes in Com- puter Science, vol 218. Springer, Berlin Heidelberg New York, pp 417–426 68. Morain F (1991) Building cyclic elliptic curves modulo large primes. In: Advances in Cryptology – Eurocrypt ’91, Lecture Notes in Computer Science, vol 547. Springer, Berlin Heidel- berg New York, pp 328–336 69. Mullin R, Onyszchuk I, Vanstone S, Wilson R (1988/89) Opti- mal normal bases in GF (p n ). Discrete Appl Math 22:149–161 70. National Institute of Standards and Technology (1994) Digi- tal signature standard. FIPS Publication 186, available from http://csrc.nist.gov/encryption/ 71. National Institute of Standards and Technology (1995) Secure hash standard (SHS). FIPS Publication 180-1, available from http://csrc.nist.gov/encryption/ 72. National Institute of Standards and Technology (1997) Entity authentication using public key cryptography. FIPS Publica- tion 196, available from http://csrc.nist.gov/encryption/ 73. National Institute of Standards and Technology (1998) Digi- tal signature standard. FIPS Publication 186-1, available from http://csrc.nist.gov/encryption/ 74. National Institute of Standards and Technology (2000) Digi- tal signature standard. FIPS Publication 186-2, available from http://csrc.nist.gov/encryption/ 75. National Institute of Standards and Technology, Advanced Encryption Standard, work in progress, available from http://csrc.nist.gov/encryption/ 76. National Institute of Standards and Technology (2000) De- scriptions of SHA-256, SHA-384, and SHA-512, preprint 77. National Security Agency (1998) SKIPJACK and KEA algo- rithm speciﬁcation, Version 2.0, 29 May 1998 78. Nyberg K, Rueppel R (1993) A new signature scheme based on the DSA giving message recovery. In: 1st ACM Confer- ence on Computer and Communications Security, Fairfax, VA. ACM Press, pp 58–61 79. Nyberg K, Rueppel R (1996) Message recovery for signature schemes based on the discrete logarithm problem. Des Codes Cryptography 7:61–81 80. van Oorschot P, Wiener M (1999) Parallel collision search with cryptanalytic applications. J Cryptology 12:1–28 81. Pohlig S, Hellman M (1978) An improved algorithm for computing logarithms over GF (p) and its cryptographic sig- niﬁcance. IEEE Trans Inf Theory 24:106–110 82. Pointcheval D, Stern J (1993) Security proofs for signature schemes. In: Advances in Cryptology – Eurocrypt ’96, Lec- ture Notes in Computer Science, vol 1070. Springer, Berlin Heidelberg New York, pp 387–398 83. Pollard J (1978) Monte Carlo methods for index computation mod p. Math Comput 32:918–924 84. Rabin M (1979) Digitalized signatures and public-key func- tions as intractable as factorization, MIT/LCS/TR-212. MIT Laboratory for Computer Science, Cambridge, MA 85. Rivest R, Shamir A, Adleman L (1978) A method for obtain- ing digital signatures and public-key cryptosystems. Commun ACM 21:120–126 86. Rueppel R, Lenstra A, Smid M, McCurley K, Desmedt Y, Odlyzko A, Landrock P (1993) The Eurocrypt ’92 controver- sial issue – trapdoor primes and moduli. In: Advances in Cryp- tology – Eurocrypt ’92, Lecture Notes in Computer Science, vol 658. Springer, Berlin Heidelberg New York, pp 194–199 87. Satoh T (2000) The canonical lift of an ordinary elliptic curve over a prime ﬁeld and its point counting. J Ramanujan Math Soc 15:247–270 88. Satoh T, Araki K (1998) Fermat quotients and the polynomial time discrete log algorithm for anomalous elliptic curves. Comment Math Univ Sancti Pauli 47:81–92 89. Schirokauer O (1993) Discrete logarithms and local units. Phi- los Trans R Soc London A 345:409–423 90. Schnorr C (1991) Eﬃcient signature generation by smart cards. J Cryptology 4:161–174

63

91. Schoof R (1985) Elliptic curves over ﬁnite ﬁelds and the com- putation of square roots mod p. Math Comput 44:483–494 92. Schroeppel R, Orman H, O’Malley S, Spatscheck O (1995) Fast key exchange with elliptic curve systems. In: Advances in Cryptology – Crypto ’95, Lecture Notes in Computer Science, vol 963. Springer, Berlin Heidelberg New York, pp 43–56 93. Semaev I (1998) Evaluation of discrete logarithms in a group of p-torsion points of an elliptic curve in characteristic p. Math Comput 67:353–356 94. Silverman J (1986) The arithmetic of elliptic curves. Springer, New York 95. Silverman J (2000) The xedni calculus and the elliptic curve discrete logarithm problem. Des Codes Cryptography20:5–40 96. Silverman J, Suzuki J (1999) Elliptic curve discrete logarithms and the index calculus. Advances in Cryptology – Asiacrypt ’98, Lecture Notes in Computer Science, vol 1514. Springer, Berlin Heidelberg New York, pp 110–125 97. Silverman R, Stapleton J (1997) Contribution to ANSI X9F1 working group (unpublished) 98. Smart N (1999) The discrete logarithm problem on elliptic curves of trace one. J Cryptology 12:193–196 99. Smid M, Branstad D (1993) Response to comments on the NIST proposed digital signature standard. Advances in Cryp- tology – Crypto ’92, Lecture Notes in Computer Science, vol 740. Springer, Berlin Heidelberg New York, pp 76–88 100. Solinas J (1997) An improved algorithm for arithmetic on a family of elliptic curves. In: Advances in Cryptology – Crypto ’97, Lecture Notes in Computer Science, vol 1294. Springer, Berlin Heidelberg New York, pp 357–371 101. Solinas J (1999) Generalized Mersenne numbers. Technical report CORR 99-39, Department of C&amp;O, University of Wa- terloo. Available from http://www.cacr.math.uwaterloo.ca 102. Solinas J (2000) Eﬃcient arithmetic on Koblitz curves. Des Codes Cryptography 19:195–249 103. Standards for Eﬃcient Cryptography Group (2000) SEC 1: elliptic curve cryptography, version 1.0. Available at http://www.secg.org 104. Standards for Eﬃcient Cryptography Group (2000) SEC 2: recommended elliptic curve domain parameters, version 1.0. Available at http://www.secg.org 105. Stein A (1997) Equivalences between elliptic curves and real quadratic congruence function ﬁelds. J Théor Nombres Bor- deaux 9:75–95 106. Stein A, Müller V, Thiel C (1999) Computing discrete log- arithms in real quadratic congruence function ﬁelds of large genus. Math Comput 68:807–822 107. Teske E (1998) Speeding up Pollard’s rho method for com- puting discrete logarithms. In: Algorithmic Number Theory, Lecture Notes in Computer Science, vol 1423. Springer, Berlin Heidelberg New York, pp 541–554 108. Vanstone S (1992) Responses to NIST’s proposal. Commun ACM 35:50–52 109. Vaudenay S (1996) Hidden collisions on DSS. In: Advances in Cryptology – Crypto ’96, Lecture Notes in Computer Science, vol 1109. Springer, Berlin Heidelberg New York, pp 83–88 110. WAP WTLS (1999) Wireless application protocol wire- less transport layer security speciﬁcation. Wireless Ap- plication Protocol Forum. Drafts available at http://www.wapforum.org 111. Wiener M, Zuccherato R (1999) Faster attacks on elliptic curve cryptosystems. In: Selected Areas in Cryptography, Lec- ture Notes in Computer Science, vol 1556. Springer, Berlin Heidelberg New York, pp 190–200 112. De Win E, Mister S, Preneel B, Wiener M (1998) On the performance of signature schemes based on elliptic curves. In: Algorithmic Number Theory, Lecture Notes in Computer Science, vol 1423. Springer, Berlin Heidelberg New York, pp 252–266 113. Zuccherato R (1998) The equivalence between elliptic curve and quadratic function ﬁeld discrete logarithms in charac- teristic 2. In: Algorithmic Number Theory, Lecture Notes in Computer Science, vol 1423. Springer, Berlin Heidelberg New York, pp 621–638
