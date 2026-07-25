# [9] Lattice-Based Signature Schemes and Their Sensitivity to Fault Attacks

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 15
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-09"
derived_asset_id: "PCM-DFA-REF-09-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[9] Lattice-Based Signature Schemes and Their Sensitivity to Fault Attacks.pdf"
source_sha256: "8f8c2199ff29c23e2d04c8c85a4e21be0f4fa079c65d451b25f7c73ac8a354f0"
pages: 15
bbox_words: 15029
consumed_bbox_words: 15029
numeric_tokens: 1498
consumed_numeric_tokens: 1498
source_blocks: 303
consumed_source_blocks: 303
emitted_blocks: 287
embedded_raster_images: 42
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 15
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

2016 Workshop on Fault Diagnosis and Tolerance in Cryptography

Lattice-Based Signature Schemes and their Sensitivity to Fault Attacks

Nina Bindel and Johannes Buchmann and Juliane Krämer

Technische Universität Darmstadt, Germany Email: {nbindel, buchmann, jkraemer}@cdc.informatik.tu-darmstadt.de

Abstract Due to their high efﬁciency and their strong security properties, lattice-based cryptographic schemes seem to be a very promising post-quantum replacement for currently used public key cryptogra- phy. The security of lattice-based schemes has been deeply analyzed mathematically, whereas little effort has been spent on the analysis against implementa- tion attacks. In this paper, we start with the fault analysis of one of the most important cryptographic primitives: signature schemes. We investigate the vulnerabil- ity and resistance of the currently most efﬁcient lattice-based signature schemes BLISS (CRYPTO 2013), ring-TESLA (AfricaCrypt 2016), and the GLP scheme (CHES 2012) and their implementations. We consider different kinds of (ﬁrst-order) randomizing, zeroing, and skipping faults. For each of the signature schemes, we found at least six effective attacks. To increase the security of lattice-based signature schemes, we propose countermeasures for each of the respective attacks. Keywords. lattice-based cryptography, signature scheme, fault attack, side channel analysis

I. I NTRODUCTION Since the invention of Shor’s algorithm, which solves the discrete logarithm and the integer factorization prob- lem in polynomial time using quantum computation, most of our daily used public key cryptography is on threat as soon as large enough quantum computers can be built. Due to the expectable development of large quantum computers in the near future, research on cryptographic construc- tions which are secure even in the presence of large quantum computers - called post-quantum cryptography - has seen a boost in recent years. This is also reﬂected in two current announcements by the National Security Agency (NSA) and the National Institute of Standards and Technology (NIST): in 2015, NSA advertised lattice-based cryptography over elliptic curve cryptography [24] and in 2016, NIST announced to start a standardization process for post-quantum cryptography [25]. These developments show that post-quantum cryptography is standing on the edge of being used in practical applications.

978-1-5090-1108-7/16 $31.00 © 2016 IEEE DOI 10.1109/FDTC.2016.11

Lattice-based constructions promise to be a valuable post-quantum replacement for current public-key cryp- tography because of their broad applicability, their high efﬁciency, and their strong security properties. However, when novel cryptographic schemes are brought into prac- tice, their mathematical security is not sufﬁcient. Physical attacks which target cryptographic schemes while they are being executed also have to be considered to provide the desired level of security. For lattice-based cryptographic schemes, until now, little effort has been spent in analyzing their vulnerability against such attacks. While lately the research on side channel attacks has advanced [8], [27], there are no results on fault attacks against schemes over general lattices yet 1 . Hence, the natural question arises whether lattice-based primitives and their implementations are vulnerable against fault attacks. 1) Contribution: In this paper, we start to investigate the vulnerability of lattice-based cryptography towards fault attacks. We analyze signature schemes and their implementations and scrutinize whether certain schemes or instantiations thereof are more vulnerable than others. We consider the signature schemes BLISS [11], ring- TESLA [1], and the GLP scheme [16], since these are the most promising ones with respect to efﬁciency, i.e., run- time, signature sizes, and key sizes. Concerning the faults that we consider, we focus on ﬁrst-order fault attacks, regarding randomizing 2 , skipping, and zeroing faults. We explore the reasons for the vulnerability and resistance, respectively, of the key generation, sign, and veriﬁcation algorithms. Furthermore, we propose countermeasures for each of the developed attacks. To reduce the number of necessary faults, we propose a hybrid approach of fault attacks and lattice analysis. In the three analyzed signature schemes, the secret is a polynomial s ∈ Z q [x]/(x n + 1) with small coefﬁcients. The hybrid approach allows an attacker to determine not

1 A few results for fault attacks on NTRU-lattices and -schemes exist, e.g., [18]. These cannot be transfered to signature schemes over non- NTRU lattices which are used nowadays. 2 We do not analyze bit ﬂips separately since they are either covered by randomization faults or in practice considered as unrealistic [15].

63 64

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 2 -->

## PDF page 2

all, but only a necessary amount of the coefﬁcients of the secret with the help of faults such that the remaining lattice problem can be solved mathematically. We gen- erally analyze how many coefﬁcients of the secret must be recovered by fault attacks in order to use the hybrid approach for BLISS, ring-TESLA, and the GLP scheme. We apply this approach on our randomization fault attack. Our research shows that all examined signature schemes and their implementations are vulnerable to all three kinds of considered fault attacks, since we ﬁnd effective attacks against each of them. A summary of the analyzed attacks and the respective vulnerabilities of the three signature schemes is given in Table I. Note that certain effects can be achieved with different kinds of fault attacks, e.g., some variables can be zeroed out both with a zeroing fault and a skipping fault. Such fault attacks are only listed once in Table I, but mentioned and explained in all relevant sections in the remainder of this paper.

TABLE I C OMPARISON OF THE GLP SCHEME , BLISS, AND RING -TESLA

WITH RESPECT TO THEIR VULNERABILITY TO THE ATTACKS DESCRIBED IN THIS PAPER . T HE TABLE SHOWS THE ALGORITHMS WHICH THE FAULT ATTACKS TARGET , I . E ., KEY GENERATION (KG), SIGNATURE GENERATION (S), AND VERIFY (V), AND IF THE SCHEME IS VULNERABLE TO THE RESPECTIVE ATTACK , I . E ., VULNERABLE G, VULNERABLE WITH A HUGE NUMBER OF NEEDED FAULTS (G), NOT VULNERABLE H, NOT APPLICABLE -.

Fault Attack Algorithm GLP BLISS

ring- TESLA H H H H H G (G) H H G H H G H G

Section

G H H H H G (G) G H G G G G H G

G H H H - G (G) H - G G - G H G

Rand. of secret Rand. of error Rand. of modulus Rand. of randomness Skip of mod-reduction Skip of addition Skip of rejection Skip of addition Skip of mod-reduction Skip of correct-check Skip of size-check Zero. of secret Zero. of randomness Zero. of hash value Zero. of hash polynomial

S S S S KG KG S S S V V KG S S V

III-A III-B III-C III-D IV-A1 IV-A2 IV-B1 IV-B2 IV-B3 IV-C1 IV-C2 V-A V-B V-C V-D

We show that two commonly used tweaks in the con- struction of lattice-based signature schemes, which are deployed for efﬁciency reasons, should only be carefully applied. First, our analysis shows a difference between the vulnerability of ideal-lattice-based schemes and standard- lattice-based schemes with respect to fault attacks. In standard-lattice-based schemes the underlying lattice is , deﬁned by a uniformly sampled matrix A ∈ Z m×n q whereas ideal lattices can be deﬁned via a polynomial of degree n . The resulting additional structure of ideal lattices leads to much smaller key sizes and better run- times. Up to know, mathematical cryptanalysis could not

exploit the additional cyclic structure of ideal lattices. However, based on our results, we show that ideal-lattice- based schemes are indeed more vulnerable to zeroing attacks than schemes over standard lattice. Secondly, we show that instantiating a scheme with common (ideal-) lattice problems, i.e., choosing the secret polynomial to be Gaussian distributed, is less vulnerable than more efﬁcient instantiations. For example, the GLP scheme and BLISS 3 are more vulnerable to randomizing faults since the coefﬁcients of the secret polynomial are chosen to be in {−1, 0, 1} or {−2, ..., 3} , respectively, instead of Gaussian distributed as it is done for ring-TESLA. This has already been feared from a theoretical perspective [26] and is now shown in this work from the practical point of view. We expect that our fault analysis and the proposed countermeasures are not limited to signature schemes, but that they can easily be transfered to most of the existing lattice-based constructions. 2) Organization: In Sec. II, we introduce the analyzed signature schemes, i.e., GLP, BLISS, and ring-TESLA, and explain the hybrid approach for combined fault attacks and lattice analyses. In Sec. III, we present randomizing attacks on all three schemes. Skipping attacks for the same schemes are explained in Sec. IV and in Sec. V, their vulnerability towards zeroing faults is investigated. We present countermeasures against the attacks and guidelines for fault-attack-resistant implementations in Sec. VI and conclude in Sec. VII.

### II. P RELIMINARIES

A. Notation

Let k ∈ N and n = 2 k ∈ N throughout this paper. We deﬁne q ∈ N to be a prime with q = 1 (mod 2n) . We denote by Z q the ﬁnite ﬁeld Z /q Z with representatives in −q/2, q/2 ∩ Z. We write (mod q) to denote the unique representative in Z q . Furthermore, we deﬁne the rings R = Z [x]/(x n + 1) and R q = i Z q [x]/(x n + 1) and the sets R q,[B] = { n−1 i=0 a i x | a [−B, B] ∩ Z } for B ∈ [0, q/2] ∩ Z and B n,ω = i ∈ 2 i a = n−1 i=0 a i x | a i ∈ {0, 1},a = ω for ω ∈ [0, n]∩ Z. We indicate the Euclidean norm of a vector v ∈ R n by v . Similarly, we deﬁne a = a 20 + ... + a 2 n−1 for n−1 i a = i=0 a i x . We denote polynomials by lower case letters (e.g., p ) and (column) vectors by bold lower case letters (e.g., v ). We write matrices by bold upper case letters (e.g., M ) and the transpose of a matrix M by M T .

3 We are aware of the fact that the publicly available implementation of BLISS is not to be used for security applications. However, it is one of the most efﬁcient signature scheme implementations. By analyzing this software, the research community still can gain insights about how to implement schemes resistant against fault attacks.

64 65

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 3 -->

## PDF page 3

Via the coefﬁcient embedding, we identify a polynomial a = a 0 + a 1 x + ... + a n−1 x n−1 ∈ R q with its coefﬁcient vector a = (a 0 , . . . , a n−1 ) T . Without further mentioning, we denote the coefﬁcient vector of a polynomial a ∈ R q by a . We deﬁne rot(a) = (−a n−1 , a 0 , . . . , a n−2 ) T and Rot(a) = (a, rot(a), rot 2 (a), . . . , rot n−1 (a)) ∈ Z n×n . q Polynomial multiplication of a, b ∈ R q is equivalent to the matrix-vector multiplication Rot(a)b in Z q . For values a, b ∈ R, we write a &lt;&lt; b if a is much smaller than b . All logarithms are in base 2. Let d ∈ N, c ∈ Z. We denote by [c] 2 d the unique repre- sentative of c modulo 2 d in (−2 d−1 , 2 d−1 ]∩ Z. Let · d be the rounding operator · d : Z → Z , c → (c − [c] 2 d )/2 d . We naturally extend these deﬁnitions to vectors and poly- nomials by applying · d and [·] 2 d to each component of the vector and to each coefﬁcient of the polynomial, respectively. We abbreviate v (mod q) d by v d,q . Let σ ∈ R &gt;0 . Let D σ be the discrete Gaussian dis- tribution on Z with standard deviation σ . We denote by d ← D σ the operation of sampling an element d with distribution D σ . When writing v ← D σ n we mean sampling each coefﬁcient of a polynomial v Gaussian distributed. For a ﬁnite set S , we write s ← $ S to indicate that an element s is sampled uniformly at random from S . Let n ≥ k &gt; 0 . A k -dimensional lattice Λ is a discrete additive subgroup of R n containing all integer linear combinations of k linearly independent vectors {b 1 , . . . , b k } = B , i.e., Λ = Λ(B) = {Bx | x ∈ Z k } . The determinant of a lattice is deﬁned by det(Λ(B)) = det (B B) . The basis is not unique for a lattice and moreover, the determinant of a lattice is independent of the basis. Throughout this paper we are mostly concerned with q -ary lattices. Λ ∈ Z n is called a q-ary lattice if q Z ⊂ Λ for some q ∈ Z. Let A ← $ Z m×n . We deﬁne the q-ary q n | Ax = 0 (mod q)} and (A) = {x ∈ Z lattices Λ ⊥ q Λ q (A) = {x ∈ Z n | ∃s ∈ Z m s.t. x = A s (mod q)}.

B. Description of the Lattice-Based Signature Schemes

In this subsection, we recall the signature schemes that we analyze in this work. We describe the GLP scheme by Güneysu et al. [16], ring-TESLA by Akleylek et al. [1], and BLISS by Ducas et al. [11]. We depict the three schemes in Appendix A in Fig. 3, 4, and 5, respectively. We follow the notation of the respective ﬁgures. The security of the signature schemes is based on the ring learning with errors (R-LWE), the ring short integer solution (R-SIS), or the decisional compact knapsack (DCK) problem. We give a formal deﬁnition of R-LWE in Appendix B. For a formal deﬁnition of DCK and R-SIS we refer to the original works. 1) GLP: The secret key consist of two polynomi- als s, e ← $ R q,[1] with ternary coefﬁcients, i.e., with coefﬁcients in {−1, 0, 1} ; the public key is a tuple of

a ← $ R q and b = as + e (mod q) . On input μ , the sign algorithm ﬁrst samples y 1 , y 2 ← $ R q,[k] . Afterwards, it hashes the most signiﬁcant bits of ay 1 + y 2 together with μ . The signature polynomials z 1 and z 2 are computed. To hide the secret, rejection sampling is applied, i.e., z 2 is compressed to z 2 and the signature is returned only with some probability (see [20] for further information on the rejection sampling). The veriﬁcation algorithm checks the size of z 1 and z 2 and the equality of c and H az 1 + z 2 − bc d,q , μ . Güneysu et al. [16] state the parameter set GLP-Set-I with n = 512 and q = 8383489 . This instantiation of the DCK gives a hardness of at least 80 bit [11]. 2) ring-TESLA: The secret key sk is a tuple of three polynomials s, e 1 , and e 2 with small coefﬁcients; the pub- lic key vk consists of the polynomials a 1 , a 2 ← $ R q , b 1 = a 1 s + e 1 (mod q) , and b 2 = a 2 s + e 2 (mod q) . During signing a message μ , a random polynomial y ← $ R q,[B] is sampled. Afterwards, the hash value c of the most signif- icant bits of the products a 1 y and a 2 y and μ is computed and encoded as the polynomial c ∈ B n,ω . The signature σ of μ consists of c and the polynomial z = y + sc . Before returning the signature, rejection sampling is applied. For veriﬁcation of the signature (c , z) , the size of z and the equality of c and H(a 1 z − b 1 c d,q , a 2 z − b 2 c d,q , μ) is checked, where c is again the encoded polynomial of c . Akleylek et al. [1] proposed the parameter set ring- TESLA-II to achieve 128-bit hardness from the underlying R-LWE problem: n = 512 , σ = 52 , q = 39960577 . 3) BLISS: The key pair is chosen NTRU-like, i.e., the public key is vk = (a 1 , a 2 ) = 2 2g+1 (mod q), q − 2 , f n−1 = { i=0 h i x i |h i ∈ where f, g ← $ F d 1 ,d 2 {−2, −1, 0, 1, 2}, |{h i = ±1}| = d 1 , |{h i = ±2}| = d 2 } and f is invertible modulo q . The secret key sk consists of sk = (s 1 , s 2 ) T = (f, 2g + 1) T . Furthermore, the vectors (a 1 , a 2 ) , (s 1 , s 2 ) T , and ξ ∈ Z are chosen such that (a 1 , a 2 )(s 1 , s 2 ) T = q = −q ( mod 2q) , ξ(q − 2) = 1 ( mod 2q) , and hence ξ(a 1 , a 2 ) = (ξa 1 , 1) ( mod 2q) . To sign a message μ , random vectors y 1 and y 2 are sampled with Gaussian distribution. A hash value c is computed from the randomness, the public key, ξ , and the message μ . Afterwards, the value b ← $ {0, 1} is chosen, the polynomials z 1 = y 1 + (−1) b s 1 c and z 2 = y 2 +(−1) b s 2 c are computed, rejection sampling is applied, and z 2 is compressed to z 2 . During veriﬁcation of the signature (z 1 , z 2 , c) , the sizes of z 1 and z 2 and the equality of c and H ξa 1 z 1 + ξqc( mod 2q) d,2q + z 2 ( mod p), μ are checked. Ducas et al. [11] give two parameter sets to achieve 128-bit hardness of the underlying problem: BLISS-I with n = 512 , σ = 215 , q = 12289 and BLISS- II with n = 512 , σ = 107 , q = 12289 . Furthermore, we like to emphasize that in the instantiations BLISS-I and

65 66

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 4 -->

## PDF page 4

BLISS-II, d 2 = 0 . Hence, it holds true that ⎧ ⎪ ⎪ ⎨ {−1, 0, 1} if j = 1, s j,i ∈ {−1, 1, 3} if j = 2, i = 0, ⎪ ⎪ ⎩ {−2, 0, 2} if j = 2, i ∈ {1, ..., n − 1}, where s 1 = ni=0 s 1,i x i and s 2 = ni=0 s 2,i x i .

### C. Description of the Hybrid Approach of Lattice Analysis and Fault Attacks

In this section, we describe how to combine fault attacks and algorithms that solve lattice problems such as LWE or SIS. Via this combination, which we call hybrid approach, we can reduce the number of faults necessary to receive the secret drastically. Revealing all coefﬁcients of the secret of a lattice problem with high dimension might require a huge amount of fault attacks. Instead, we analyze that it is sufﬁcient to reveal just enough coefﬁcients with the help of faults to solve the remaining instance with algorithms that solve lattice problems, e.g., the embedding approach. We describe our hybrid approach for the LWE problem next. We describe the analysis for SIS in the full version of this paper [6]. Let As + e = b (mod q) be an LWE instance, with A ∈ Z m×n , s ∈ Z nq , and e ∈ Z m q q . Assume that k coefﬁcients of the secret s are known. W.l.o.g., we can assume that the ﬁrst k coefﬁcients of s are known, since the samples of an LWE instance can be reordered. Then, this instance can be written as

T

(A 1 |A 2 ) s 1 , s 2 + e = A 1 s 1 + A 2 s 2 + e = b,

with A 1 ∈ Z m×k , A 2 ∈ Z q , and s 1 ∈ Z kq , s 2 ∈ q Z n−k . Let b = b − A 1 s 1 . Thus, A 2 s 2 + e = b (mod q q) deﬁnes an LWE instance with the same number m of samples but with a decreased dimension n−k of the secret vector. To compute the minimal value of k , we ﬁrst choose the time T (in seconds) how long the LWE solver should run, e.g., one day T = 86400 . Afterwards, we compute the corresponding Hermite delta by the estimation made by Linder and Peikert [19] 1.8 . log 2 (δ(T )) = (1) log 2 (T ) + 110

m×(n−k)

The Hermite delta is a measurement for the quality of a basis reduction, for more information we refer to [19]. Given n , m , and δ and following the embedding approach proposed in [14], we can compute the value k . We emphasize that we are aware that the embedding approach is not always the best attack to solve LWE. Nevertheless, it yields an upper bound on the number of fault attacks needed.

In the embedding approach the LWE instance is reduced to an instance of the unique shortest vector problem (uSVP) [3], [4]. To this end, an embedding lattice Λ is deﬁned in which the error vector e is embedded. Following the explanation by Dagdelen et al. [31], we know that a short vector can be found if

1

dim(Λ) 1 Γ(1 + dim(Λ) 2 √ ) det(Λ) dim(Λ) , ≤ ||e||τ π

dim(Λ)

δ

(2)

where τ ≈ 0.4 is constant and Γ(n) is the gamma function. Two different ways to deﬁne Λ were proposed, which are described next. During the standard embedding ap- proach we apply a uSVP solver on the lattice Λ = A 2 b (m+1)×(n−k+1) Λ q (A st ) with A st = ∈ Z q . 0 1 Hence, dim(Λ q (A st )) = m + 1 and det(Λ q (A st )) = q m−n+k . Thus, Equation (2) gives the following inequal- ity:

1

) (m+1) k−n−1 Γ(1 + m+1 √ 2 · q ≤ . π||e|| · τ

m+1

δ

(3)

During the dual embedding approach we apply a uSVP solver on the lattice Λ = Λ ⊥ q (A D ) with

A 2 |I m |b

m×(n−k+m+1)

A D

∈ Z q

=

. Hence,

⊥ m dim(Λ ⊥ q (A D )) = n−k +m+1 and det(Λ q (A D )) = q . Thus, Equation (2) gives

1

) (n−k+m+1) k−n−1 Γ(1 + n−k+m+1 2 √ · q ≤ . τ · πe

n−k+m+1

δ

(4)

Assume that the computations should not run longer than a day (resp., a week). By Equation (1) this corresponds to the Hermite delta δ 1 = 1.0099 (resp., δ 2 = 1.0097 ). Finally, given n , m , and δ , we can compute the minimal value for k such that Equation (3) or Equation (4) is fulﬁlled. Applying the hybrid approach to BLISS, ring-TESLA, and the GLP scheme with δ 1 shows that it is sufﬁcient to reveal k = 344 , k = 405 , and k = 118 , respectively, instead of all secret coefﬁcients by fault attacks. Given δ 2 the minimal values are k = 337 , k = 389 , and k = 105 , respectively. Note that the bit-security of the GLP scheme is 80-bit, whereas the proposed instantiations BLISS-I, BLISS-II, and ring-TESLA-II give 128 bit of security. We explain the derivation of k for each of the three schemes in detail in the full version of this paper [6].

### III. R ANDOMIZATION F AULTS

A randomization fault randomly changes the value of a variable that is processed in the attacked alorithm, i.e., the attacker does not know the value of the variable after the attack, but beneﬁts from knowing that it has

66 67

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 5 -->

## PDF page 5

been changed within a certain range. Depending on the attacker’s abilities, the fault targets the whole variable or only some bytes or bits of it [29]. We analyze the effects of a randomization fault targeting the secret polynomial (Sec- tion III-A), the error polynomial (Section III-B), the mod- ulus (Section III-C), and the randomness (Section III-D) during the signature generation.

A. Randomization of the Secret Polynomial

In 1996, Bao et al. introduced a method to attack sig- nature schemes with binary secret keys [5]. In particular, they show how to attack RSA, the ElGamal scheme, and Schnorr signature schemes. In this section, we ﬁrst describe how to adjust the attack from [5] to lattice-based Schnorr-like signature schemes instantiated with binary secret over standard lattices. Afterwards, we describe a more evolved attack on the GLP scheme. Take b = As + e (mod q) with s ∈ {0, 1} n and e ← χ , where χ is some error distribution over Z n . The public key is (A, b) and the secret key consists of (s, e) . The signature of a message μ is computed as follows: choose randomness y , compute the hash value c = H(Ay d,q , μ) , compute z = sc + y , and return σ = (z, c) . Assume one coefﬁcient of s is changed via a fault attack, i.e., the secret s = (s 1 , ..., s i−1 , s i , s i+1 , ..., s n ) T is used to generate a signature. Hence, σ = (z , c) = (s c + y, c) is returned as faulty signature of μ . Now, an attacker checks whether H Az − bc − Av i,α c d,q , μ = c , where v i,α is the zero vector except that the i -th entry is equal to α ∈ {−1, 0, 1} . Depending on the value of α and the index i , the attacker can determine the value of s i : ⎧ ⎪ ⎪ ⎨ 0 then s i = s i , run attack again, If α = 1 then s i = 1, ⎪ ⎪ ⎩ −1 then s i = 0.

Hence, in case of a successful fault attack, i.e., s i = s i , an attacker ﬁnds out one coefﬁcient of the secret for each injected fault. To our knowledge, there is no lattice-based signature scheme instantiated over binary LWE. However, recent results on the hardness of binary LWE [2], [10], [21] show an interest in this instantiation and also a lattice- based encryption scheme with binary secret was recently proposed [9]. With our description above we stand in line with those being cautious about instantiations of schemes with binary LWE. 1) Applying the Attack to the GLP Scheme: In this section we describe a generalization of the attack by Bao et al. [5] to ternary secret keys, i.e., to secret keys with coefﬁcients in {−1, 0, 1} . We explain the attack by applying it to the GLP scheme, since its secret key is

chosen to be ternary. Furthermore, we assume that the attack changes up to r consecutive coefﬁcients instead of only a single coefﬁcient of the secret. This is generally considered to be a more realistic scenario [15]. Assume that an attacker changes r consecutive co- efﬁcients of the secret s , i.e., s = s + ε with ε = j+r i , 0 ≤ j &lt; n where all ε , s ∈ {−1, 0, 1} . ε x i i i=j i The attack consists of three steps: inducing a random- ization fault, querying a signature on some message, i.e., σ = (z 1 , z 2 , c) = (s c + y, z 2 , c) with s being the faulty secret, and analyzing the output by running a software implementation of the algorithm GeneralBao (·) that is depicted in Fig. 1. The attacker repeats those three steps until sufﬁciently many coefﬁcients of the secret are determined such that the hybrid approach described in Sec. II-C can be applied. The algorithm GeneralBao (·) gets as input the public key, a signature of a message μ , and two lists: the list secret where the determined coefﬁcients of the secret are saved and the list determined where the information whether or not a coefﬁcient is already determined is saved. The algorithm GeneralBao (·) returns updated lists secret and determined . Let α be the difference between n−1 the i secret s and the faulty secret s , i.e., α = i=0 α i x is a polynomial with α i ∈ {−2, −1, 0, 1, 2} . The attacker checks whether H(az 1 + z 2 − bc − aαc d,q , μ) = c with α i , ..., α i+r ∈ {−2, −1, 0, 1, 2} for i ∈ {0, ..., n − 1 − r} . Thereby, the attacker gains information about the value and index of s i . The possible values for s i , s i , and α i are shown in Table II.

TABLE II P OSSIBLE C OMBINATIONS FOR THE C OEFFICIENTS OF s, s , AND α.

s i s i α i = s i − s i

0 0 0

0 1 -1

0 -1 1

1 0 1

1 1 0

1 -1 2

-1 0 -1

-1 1 -2

-1 -1 0

As indicated by Fig. 1, the procedure GeneralBao (·) distinguishes between ﬁve different cases for each coef- ﬁcient of α once the correct values of α 0 , ..., α n−1 are found. ⎧ ⎪ ⎪ 2 then s i = −1, ⎪ ⎪ ⎪ ⎪ ⎪ ⎨ −2 then s i = 1, If α i = 1 then s i = 1 or s i = 0, ⎪ ⎪ ⎪ then s i = −1 or s i = 0, −1 ⎪ ⎪ ⎪ ⎪ ⎩ 0 then s i = s i .

In the latter cases, the attacker can not determine s i uniquely. Let s j be a coefﬁcient which was changed during a fault attack such that α j,1 = α j = ±1 . Assume that s j is

67 68

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 6 -->

## PDF page 6

changed again by another fault attack with difference α j,2 . Then the attacker can determine s j uniquely if α j,1 = α j,2 and α j,2 = 0 . The list determined is used for exactly this purpose: to remember which coefﬁcients were changed but could not be determined uniquely.

GeneralBao(·): Input: σ = (z 1 , z 2 , c), μ, vk = (a, b), list determined, list secret; signature σ is computed with a faulty secret Output: determined, secret n−1 1 poly α = 0 #α = i=0 α i x i 2 For i ∈ {0, ..., n − 1}: 3 For α i ∈ {0, −2, −1, 1, 2}: 4 For α i+1 ∈ {0, −2, −1, 1, 2}: 5 ... 6 For α i+r ∈ {0, −2, −1, 1, 2}: 7 If H(az 1 + z 2 − bc − aαc d,q , μ) = c : 8 For j ∈ {i, ..., i + r}: 9 If α j = 2 : 10 secret[j] = −1, determined[j] = 2 11 If α j = −2 : 12 secret[j] = 1, determined[j] = 2 13 If α j = −1 : 14 If determined[j] = 1 : 15 secret[j] = 0, determined[j] = 2 16 Else: 17 = −1 determined[j] 18 If α j = 1 : 19 If determined[j] = −1 : 20 secret[j] = 0, determined[j] = 2 21 Else: 22 determined[j] = 1 23 Return determined, secret

Fig. 1. Algorithm to compute coefﬁcients of the secret given a signature computed with a faulty secret where maximal r of the coefﬁcients are changed by a randomization fault

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 6]

As described in Sec. II-C, at most k = 118 coefﬁcients of s have to be determined via fault attacks to compute the whole secret via the hybrid approach. Hence, next we analyze the expected number of faults that we have to induce to determine k = 118 coefﬁcients of s . We assume that the index of the ﬁrst of the r changed coefﬁcients is chosen uniformly random in {0, ..., n − 1} . Since r &lt;&lt; n , we assume that the changed (and hence the determined) coefﬁcients are uniformly distributed over all coefﬁcients s 0 , ..., s n−1 . Assume the j -th fault attack is induced after i j coefﬁcients have already been determined uniquely. Then the number of newly determined coefﬁcients after j−1 , since n is the the j -th fault attack is given by 29 r 512−i n number of coefﬁcients of s and following Table II, the probability that a coefﬁcient is changed such that it can be determined uniquely is 2/9 . Assume the fault attack targets one byte. Since each coefﬁcient can be saved in

two bits, this corresponds to four changed coefﬁcients, i.e., r = 4 . Hence, solving the following equation for m gives us the number of m = 151 (expected) needed faults to determine k = 118 coefﬁcients of the secret s : m 2r 512 − i j−1 · ≥ k, 9 512

j=1

with i 0 = 0 . In case r = 1 , the expected number of needed fault attacks to uniquely determine k = 118 coefﬁcients of s is m = 604 . Hence, the generalization to targeting more coefﬁcients is not only more realistic, but also needs a much smaller number of fault attacks. On the other hand the runtime of the software to ﬁnd the polynomial α is longer, since it takes 512 · 5 r times the runtime of the hash query for every fault attack. 2) Application to BLISS: As described in Sec. II-B3, the secret keys of the instantiations BLISS-I and BLISS-II 4 are two polynomials s 1 , s 2 with ternary-like instantiation. Therefore, the attack on the 128-bit instanti- ations of BLISS can be described in a similar manner as it was done for the GLP scheme. As before, assume r coefﬁcients are changed during a fault attack. We assume that the coefﬁcients of the faulty secret polynomial(s) are in the set {−3, ..., 3} , since it can be assumed that each coefﬁcient is saved n−1 i in three bits. Let α = i=0 α i x . Given a faulty sig- nature σ = (z 1 , z 2 , c) of the message μ , the attacker runs an algorithm similar to GeneralBao (·) , Fig. 1. The only difference is that the values of α lie in different intervals: in case the fault was induced on s 1 , the at- tacker checks H ξa 1 z 1 + ξqc − ξαc d,2q + z 2 , μ = c for α i 1 , ..., α i r ∈ {−4, ..., 4} for i 1 , ..., i r ∈ {0, ..., n − 1} . In case the fault was induced on s 2 , the attacker checks H ξa 1 z 1 + ξqc − αc d,2q + z 2 , μ = c for α i 1 , ..., α i r ∈ {−5, ..., 5} for i 1 , ..., i r ∈ {0, ..., n−1} 5 . As in the attack against the GLP scheme, sometimes the secret coefﬁcients can be determined uniquely. The probability that a coefﬁcient of s 1 (resp., s 2 ) is determined uniquely is 2/21 (resp., 4/21 ). We assume again that the indices of the changed coefﬁcients are distributed uniformly random over the original coefﬁcients. Hence, we roughly estimate the expected number of needed fault attacks by

m r 1024 − i j−1 · ≥ k, 7 1024

j=1

with i 0 = 0 and notations as in Sec. III-A1. Hence, with

4 For the higher-security instantiations BLISS-III and BLISS-IV, d 2 ∈ {0.03, 0.06}, i.e., there are a very few coefﬁcients outside {−1, 0, 1}. Hence, extending our attack to those instantiations will increase the run time, but the attack still weakens the security. 5 To be exact, in case the fault was induced on s 2 , the attacker checks the hash values for α 0 ∈ {−4, ..., 6} and α 1 , ..., α n−1 ∈ {−5, ..., 5}.

68 69

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 7 -->

## PDF page 7

r = 1 an expected number of m = 2934 faults is needed to determine k = 344 (see Sec. II-C) coefﬁcients of the secret (with r = 4 an expected number of m = 733 is needed). We conclude that the attack is less efﬁcient on BLISS than on the GLP scheme, but it is still applicable. 3) Application The coefﬁcients of the n−1 to ring-TESLA: i of ring-TESLA are chosen with s x secret s = i=0 i Gaussian distributed. Hence, the possible values of α would be in a very large range. Even if we assume that the coefﬁcients are with high probability bounded by |s i | ≤ σ (with σ = 52 for instantiation ring-TESLA-I), the number of needed fault attacks would be huge. Hence, this attack does not seem to be a threat for ring-TESLA in particular and for instantiations with Gaussian distribution in general.

B. Randomization of the Error Polynomial

A similar attack as described in Sec. III-A could be used to compute the (secret) error polynomial e . Leaking e is as bad as leaking s , since s can be computed easily once e is known. Moreover, the success probability of most of the mathematical lattice analyses would increase since those algorithms also beneﬁt from reducing the key space from {−1, 0, 1} to {−1, 0} or {0, 1} . However, the GLP scheme is not vulnerable to this variant because of its compression and rounding functions, since then the equation H( az 1 + z 2 − bc − aαx i c d,q , μ) = c holds for several values of α . Hence, α can not be determined. Nevertheless, we mention this attack to raise awareness during the construction and instantiation of schemes. For example, instantiating ring-TESLA (which does not come with such a compression function) over ternary LWE should be considered very carefully.

### C. Randomization of the Modulus

The randomization of the modulus does not seem to reveal any information that helps to forge signatures, because the value of the faulty modulus would remain unknown. Furthermore, key and signature generation of lattice-based signature schemes are randomized at several points by construction. Hence, tools like the Chinese remainder theorem do not give access to the secret.

### D. Randomization of the Randomness

As expected, also the randomization of the random values, e.g., the product ay (or similar) or the hash output c , does not reveal information that the attacker can use to forge signatures, because such values look like (or are) random values by default.

### IV. S KIPPING F AULTS

Skipping faults consist in skipping, i.e., ignoring, se- lected lines of the program code. This can, for example, be achieved via CPU clock glitching [7]. By showing

that even higher-order skipping faults against a real-word cryptographic implementation are practical, the relevance of this kind of fault attacks has recently been strength- ened [7]. We analyze different ways to exploit skipping faults during the key generation (Section IV-A), the signature generation (Section IV-B), and the veriﬁcation algorithm (Section IV-C). In the majority of cases, we explain the fault attacks using the implementations of the signature schemes. Therefore, we use the publicly available soft- ware, i.e., we use the C++-implementation of BLISS [12], the C-implementation of the GLP scheme [17], and the C- implementation of ring-TESLA [1]. Since the implementa- tion of ring-TESLA and the GLP scheme use the beneﬁts of the AVX instructions, we sometimes also consider the X86 assembly code of respective code lines.

A. During Key Generation

In this section we describe two possible skipping attacks during the key generation. , 1) Skipping the Modulus Reduction: Let A ← $ Z n×m q and s, e are chosen with some distribution over Z n and Z m , respectively. Afterwards compute b = As+e without reducing modulo q . Solving SVP or CVP in the lattice Λ = {v ∈ Z n | Aw = v for some w ∈ Z m } is most often much easier than solving the same problem in Λ q (A) , since det(Λ) ≥ det(Λ q (A)) , especially in case A is invertible. Hence, skipping the modulo operation during the key generation algorithm seems to be a security ﬂaw. However, this fault attack is already prevented in the three considered signature schemes. We use the implementation of the GLP scheme to explain the prevention. As indicated by Listing 1, the value t (corresponding to b in our notation) is computed without the reduction step. The modulo operation is performed in the subroutine poly_pack. Skipping Line 78 of Listing 1 thwarts the modulo reduction. Afterwards, only the least 32 bits of (the faulty) t are saved in r. Hence, skipping Line 78 leads to a randomization fault on b which does not reveal secret information.

48 49 51

poly_mul_a(t, s1); poly_add_nored(t, t, s2); poly_pack(pk, t); [...] void poly_pack(unsigned char r[3*POLY_DEG], const poly f) { int i; signed long long t; for(i=0;i&lt;POLY_DEG;i++) { t = (unsigned long long)f[i]; t = ((t % PARAM_P) + PARAM_P) % PARAM_P; r[3*i+0] = t &amp; 0xff; r[3*i+1] = (t &gt;&gt; 8) &amp; 0xff; r[3*i+2] = (t &gt;&gt; 16) &amp; 0xff; } }

71

72 73 74 75 76 77 78 79 80 81 82 83

69 70

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 8 -->

## PDF page 8

Listing 1. C code of the GLP scheme for the computation of the public value b = as + e in the subroutine crypto_sign_keypair and of the modulus operation and compression in the subroutine poly_pack; the value t corresponds to the value b, the value s1 corresponds to s, and s2 corresponds to e in our notation.

2) Skipping the Addition: We explain the following attack using examples from the C-implementation of the GLP scheme. However, the attack can also be successfully applied to ring-TESLA and BLISS. Details about the attacks against ring-TESLA or BLISS can be found in the full version of this paper [6]. In the GLP implementation, the public key is computed as follows, see Listing 1: ﬁrst a and s are multiplied and saved in the value b (Line 48). Afterwards, the error e is added to b (Line 49). Hence, skipping the second operation yields b = as and an attacker can easily recover s by Gaussian reduction. Note that skipping Line 48 in Listing 1 results in an unallocated variable b, triggering a segmentation fault. Hence, no (predictable) information is returned which could be used by an attacker. Considering the assembly code 6 of the addition, see Listing 2, one can see that in Line 962 the command poly_add_nored@PLT is called. Hence, skipping this line results in b = as as described above.

958 959 960 961 962 962

.loc 1 49 0 movq %r12, %rdx movq %r14, %rsi movq %r14, %rdi call poly_add_nored@PLT

1254 4C89E2 1257 4C89F6 125a 4C89F7 25d E8000000 00

Listing 2. Assembly code corresponding to Line 49 in Listing 1 of the GLP implementation.

Skipping Line 962 (or Line 49 in Listing 1) yields b = as instead of b = as + e . Hence, although the attacker can compute s , the error vector e will remain unknown. In the GLP scheme, however, e is used to compute z 2 . Next we describe how an attacker can forge signatures anyway: the attacker chooses randomness y 1 , y 2 , computes the hash value c for a message μ , z 1 = y 1 + sc , and z 2 = y 2 (instead of z 2 = y 2 + ec ). The attacker applies rejection sampling and compresses z 2 to z 2 as usual and returns the signature σ = (z 1 , z 2 , c) . The verify algorithm accepts this signature σ as we show in the following. Due to the rejection sampling, z 1 , z 2 ∈ R q,[k−32] . Furthermore, it holds that az 1 + z 2 − tc d,q = az 1 + z 2 − tc d,q = asc + ay 1 + y 2 − asc d,q = ay 1 + y 2 d,q . Thus, by skipping a single line an attacker can reveal s and also forge a signature for any message μ .

We create a description of the code written in C in assembly code via the command /usr/bin/gcc -Wall -g -O3 -c -Wa,-a,-ad -shared -fPIC file.c -o libfile.so &gt; assemblyoutputoffile.lst

6

B. During Signature Generation

The signature generation of the schemes that we con- sider in this paper is rather simple since it is a short se- quence of (polynomial) additions and multiplications. Fur- thermore, the signature generation is randomized. Hence, there are not many skipping operations which lead to in- formation about the secret key. We describe two skipping attacks during the sign algorithm in this section. 1) Skipping the Rejection Condition: Lyubashevsky ﬁrst applied rejection sampling (introduced by von Neu- mann [30]) to lattice-based signature schemes to assure that signatures are statistically independent of the secret used to generate them. Thus, learning-the-parallelepiped- attacks introduced by Nguyen and Regev [23] and im- proved by Ducas and Nguyen [13] are prevented. Ducas and Nguyen need roughly 8000 signatures to reveal the secret. In case of BLISS, ring-TESLA, and the GLP scheme, the rejection sampling is implemented as an if- condition, which would have to be skipped in order to circumvent the rejection sampling. Skipping this rejection- sampling-condition in many runs of the sign algorithm might introduce the same security ﬂaw as used by the attacks described in [23] and [13]. Since these attacks exploit the special structure of NTRU-lattices, BLISS might be especially vulnerable because its keys are chosen in an NTRU-like manner. However, to ﬁnd out the exact number of needed faults, the mentioned attacks have to be adapted to BLISS, ring-TESLA, and the GLP scheme, and to be simulated, which we leave for future work. 2) Skipping the Addition of the Randomness: In the C-implementation of the GLP scheme, z 1 and z 2 of the signature are computed in two steps: ﬁrst s (resp., e ) and c are multiplied. Afterwards, sc and y 1 (resp., ec and y 2 ) are added, as can be seen in Listing 3. Hence, skipping Line 108 (resp., Line 120) in Listing 3 yields z 1 = sc (resp., z 2 = ec ).

95 96

poly_setrandom_maxk(y1); poly_setrandom_maxk(y2); [...] poly_mul(z1,c,s1); poly_add_nored(z1,z1,y1); poly_coeffreduce(z1); [...] poly_mul(z2,c,s2); poly_add_nored(z2,z2,y2); poly_coeffreduce(z2);

107 108 109

119 120 121

Listing 3. C code of the GLP implementation for the computation of the signature values z 1 and z 2 .

As before, the assembly code of the respective code lines corresponds to jumping to another operation. Hence, this attack gives the same result as zeroing the whole randomness as described in Sec. V-B, i.e., by skipping one line an attacker knows the secret key. A similar attack is not possible in case of the BLISS or the ring-TESLA implementation. We explain the reason

70 71

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 9 -->

## PDF page 9

on the example of ring-TESLA. Explanations for BLISS can be found in the full version of this paper [6]. In the implementation of ring-TESLA the value sc is added to the value y as can be seen in Listing 4. Hence, skipping Line 323 in Listing 4 yields z = y (the value vec _ y is the output value in the implementation). Since the randomness changes for every run of the sign algorithm, the attacker does not learn anything about the secret.

323 poly_add(vec_y, vec_y, Sc);

Listing 4. C Code of ring-TESLA for the addition of sc and y.

3) Skipping the Modulus Reduction: Skipping the re- duction modulo q during the signature generation does not reveal information about the secret since during the computation of z = y + sc (the only value that is returned and depending on the secret) no modulo reduction is computed in all of the signature schemes. Moreover, the modulo operation is computed very often during the sign algorithm, i.e., it is rather difﬁcult to skip all the modulo operations during the computation via fault attacks.

### C. During Veriﬁcation

To prevent the installation of malicious malware it is not enough to use cryptographic signatures for software updates. It is also necessary to ensure that the veriﬁcation of these signatures is computed correctly [28]. Hence, we analyze fault attacks during the veriﬁcation algorithm in this section. We identify two ways to force the acceptance of an invalid signature for any message μ via skipping attacks. In all three signature schemes that are considered in this paper, the verify algorithm consists essentially of computing a hash value c , checking whether this is the same as the input value c (called the correctness check), and checking whether z (resp., z 1 and z 2 ) are small enough (called the size check). Note that we do not consider skipping the computation of the encoding function of the hash value c , since this would lead to an unallocated value. However, we consider zeroing c in Sec. V-D. 1) Skipping the Correctness Check: An adversary chooses c uniformly at random and chooses z (reps., z 1 and z 2 ) small enough and of the expected form (e.g., correct number of zero-coefﬁcients), such that the size check goes through. Afterwards, the attacker computes the hash value c . Hence, skipping the correctness check yields an acceptance of the (invalid) signature of any message. In the software of ring-TESLA, the correctness check is implemented as the following single if-condition:

378 if(memcmp(c,c_sig,32)) return -1;

where c_sig corresponds to c in our notation and returning -1 corresponds to not accepting a signature. In case of BLISS and the GLP scheme, the correctness

checks are implemented as if-conditions for each entry of c , see as an example the respective lines of the GLP implementation in Listing 5.

184 185 186

for(i=0;i&lt;20;i++) if(sm[i] != h[i]) goto fail;

Listing 5. C Code of the correctness check in the GLP scheme; sm[0],...,sm[19] corresponds to c and h corresponds to c in our notation; goto fail corresponds to not accepting a signature.

Therefore, the skip has to be realized as a jump out of the for-loop after the ﬁrst iteration. Hence, the invalid signature is accepted as long as c , z 1 , and z 2 are chosen such that c[0] = c [0] . 2) Skipping the Size Check: We explain this attack by the example of the GLP scheme. It can similarly be ap- plied to BLISS, while ring-TESLA is resistant to this kind of fault attack. The attack works as follows: the attacker chooses y 1 , y 2 ← $ R q,[k] and computes the hash value c for some self-chosen message. Afterwards, the attacker computes z 1 = a −1 (ay 1 + bc) (recall that the polynomial a is invertible) and z 2 = y 2 . Easy computation shows that as long as the size check is skipped, the signature σ = (z 1 , z 2 , c) is accepted. In case of GLP the size check is again implemented as a simple if-condition. This is also the case for BLISS, but by construction of the verify algorithm, two if-conditions have to be checked for z 1 as indicated by Fig. 5. However, the attack does not work for ring-TESLA for the following reason: to accept the signa- ture (z, c) the equation c = H w 1 d,q , w 2 d,q , μ has to hold. Therefore w i d,q = a i z − b i c d,q = a i y d,q has be fulﬁlled for i = 1, 2 , i.e., the signature value z has to fulﬁll two equations during the veriﬁcation. During the attack the value z would be uniquely computed via a 1 or a 2 . Hence, the probability that z would fulﬁll both equations is very small.

### V. Z EROING F AULTS

Zeroing fault attacks assume that the attacker can set a whole variable or a part thereof to zero. We present zeroing attacks during the key generation, the sign, and the verify algorithm. Although it has often been questioned if this is a realistic attack scenario, zeroing faults have been realized in practice [22]. In certain cases, zeroing attacks can be realized with skipping attacks, which is why we refer to Section IV in the respective cases.

A. Zeroing the Secret or Error During Key Generation

Zeroing the error polynomial can be implemented as skipping addition operations during the key generation. Hence, we refer to Sec. IV-A for more information. Similarly, one can zero the secret polynomial. Assume that during the key generation a zeroing fault is induced such that s = 0 , hence the value b = e (mod q) is

71 72

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 10 -->

## PDF page 10

returned and the attacker knows the error polynomial e . In case of the GLP scheme this is enough to forge signatures: in case of the GLP scheme, the attacker, know- ing e , can compute a (valid) signature for any message μ by choosing y 1 , y 2 ← $ R q,[k] and computing c ← H(ay 1 + y 2 d,q , μ) , z 2 = y 2 +ec , and its compression z 2 as usual. Then z 1 = y 1 with y 1 ← $ R q,[k−32] (instead of z 1 = y 1 + sc ). As in Sec. IV-A, easy computation shows that (z 1 , z 2 , c) will be accepted by the verify algorithm. In case of ring-TESLA, signatures cannot be forged in a similar manner, because a signature (c, z) has to fulﬁll two equations in order to be veriﬁed correctly: a 1 z − b 1 c d,q and a 2 z − b 2 c d,q . This only occurs if and only if e 1 c = e 2 c , which is very unlikely. The attack is not applicable to BLISS since the public value a q = 0 if one of the secret polynomials f, g is set to zero. Hence, the attacker gains not additional information. In the publicly available software implementation of GLP and ring-TESLA, the key generation and the sign algorithm do not test whether the keys are of the correct form. Thus, the respective attacks would not be detected in the currently available implementations.

B. Zeroing the Randomness During the Signature Gener- ation

In the following, we describe a zeroing attack on the randomness of the signature generation. First, we describe the attack on ring-TESLA. Afterwards, we describe sim- ilar attacks on BLISS and the GLP scheme. 1) Description of the Attack Against ring-TESLA: Throughout this section we use the following n−1 notation: j let the secret polynomial be s = j=0 s j x . Let (1) (1) (m) (m) (z , c ), ..., (z , c ) be signatures for any mes- n−1 (i) j n−1 (i) j (i) = sages with z (i) = j=0 z j x and c j=0 c j x

(i)

where c j ∈ {0, 1} for i = 1, ..., m . Furthermore, let y (1) , ..., y (m) be the faulty randomnesses with y (i) = n−1 (i) j j=0 y j x . Finally, let r ∈ {1, ..., n} be the number of coefﬁcients that are changed to zero during the fault attack. We assume that the coefﬁcients are changed block- (i) (i) wise, i.e., the coefﬁcients y j , ..., y j+r are changed for i ∈ {1, ..., m} and j ∈ {0, ..., n − 1} , and the attacker cannot control which block of r coefﬁcients is set to zero. The idea of the attack is as follows: ﬁrst the at- tacker induces a zeroing fault on the randomness and checks which of the coefﬁcients were changed to zero (we explain later in this section how this is done). (i) The attacker collects equations with y j = 0 , i.e.,

(i) (i) (i)

(s j , ..., s 0 , −s n−1 , ..., −s j+1 )(c 0 , ..., c n−1 ) T = z j . The attacker repeats those steps until the set of n ≥ n collected equations is sufﬁcient, i.e., every coefﬁcient of s 0 , ..., s n−1 is at least once multiplied with a non-zero

(i )

c j k k . Hence, the attacker receives the following system of equations, which can be solved uniquely:

(i ) (i )

C · (s 0 , ..., s n−1 ) T = (z j 1 1 , ..., z j n n ) T , (5) ⎛ ⎞ (i 1 ) (i 1 ) (i 1 ) (i 1 ) c ... c −c ... −c 0 n−1 j 1 +1 ⎟ ⎜ j 1 ⎟ . ... ... with C = ⎜ ⎝ ⎠ (i n ) (i n ) (i n ) (i n ) ... c 0 −c n−1 ... −c j n +1 c j n Next we describe how an attacker can ﬁnd out which coefﬁcients of the randomness were changed to zero during the i -th fault attack. The equation z (i) = sc (i) +y (i) is equivalent to z (i) = Rot(s)c (i) + y (i) . To simplify the (i) (i) explanation we assume w.l.o.g. that c 0 = ... = c ω−1 = 1 (i) (i) and c ω = ... = c n−1 = 0 . Hence, we can write

(i)

(i)

z 0 =s 0 − s n−1 + ... − s n−ω + y 0

(i)

(i)

z 1 =s 1 + s 0 − s n−2 + ... − s n−ω+1 + y 1

...

(6)

(i) (i) z n−1 =s n−1 + s n−2 + ... + s n−ω−1 + y n−1 .

(i) (i) (i)

We deﬁne z j = ς j +y j for j = 0, ..., n−1 . Since s j ← D √ σ , the expectation value of |s j | is given by E [|s j |] = σ 2/π for j = 0, ..., n − 1 . Furthermore, since c = ω , √ (i) ς j is Gaussian distributed with standard deviation ωσ

(i)

and E [|ς j |] = holds that

2ω/πσ . Via the triangle inequality it

(i) (i)

B/2 − 2ω/πσ ≤ E [|ς j + y j |] ≤

2ω/πσ + B/2.

For the parameter set ring-TESLA-II, i.e., with B = 2 22 − (i) 1 , ω = 19 , and σ = 52 , E [|z j |] is given by ⎧ ⎨ 102, if y (i) = 0, (i) j E [|z j |] ≈ ⎩ 2 21 , if y j (i) = 0.

Since the difference between the expectation values is very large, we assume that the attacker can unambiguously (i) determine whether or not y j was changed to zero. The number of needed zeroing faults strongly depends on the value r . Let m be the number of necessary successful fault inductions to reveal the secret and let S be the set of equations which will be part of Equation (5). We assume that every successful fault induction adds r new equations to the set S , since the hash value c changes for every sign query. Hence, solving the following equation for m gives the number of necessary faults:

1 1 1 · r − n (k − 1) − r ≥ n. 3 2 2

m

(7)

k=1

3n Thus, m ≥ r−1/2r , where the factor 3 comes from the rejection probability of 0.34 stated in [1]. Assume the attacker can set 12 bytes to zero, i.e., r = 4 since each

72 73

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 11 -->

## PDF page 11

coefﬁcient of y can be saved in three bytes, then m = 384 . For r = 1 , we get m = 1536 . In case r = n , i.e., the complete randomness can be set to zero, only a single successful fault attack is necessary, since then the linear system of equations in Equation (6) can be solved uniquely with high probability. The reason is that the rows of a rotation matrix are Z- linearly independent and ±s 0 , ..., ±s n−1 are independent random variables with high probability. 2) Application to BLISS or the GLP Scheme: The attack can also be applied on BLISS and the GLP scheme. Assume that the zeroing fault was induced on y 1 of the GLP scheme. As explained above, we can recover s . Afterwards, we can compute e by e = t − as . Because of the compression function the attack is not effective if y 2 is faulty. Due to the compression algorithm, a maximum of six coefﬁcients are in the ﬁnal signature for the proposed instantiation. Similarly, we can assume that the zeroing fault was induced on y 1 during the sign algorithm of BLISS. As explained above, we can then recover s 1 and we can recover s 2 by s 2 = a 1 s 1 . For similar reasons as for the GLP scheme, the attack does not work effectively in case y 2 instead of y 1 is faulty. 3) Application to Signature Schemes over Standard- Lattices: The attack is far less efﬁcient and only appli- cable for r = n when applied to schemes deﬁned over standard lattices instead of ideal lattices. Let r = n , i.e., the randomness is equal to the zero vector. Let the notation and assumptions be as described above. Then the following system of equations gives n · m equations and n 2 unknowns and can be solved uniquely:

T

T

z (1) , ...., z (m) = Rot(s) c (1) , ..., c (m)

.

Still it is less efﬁcient than in the ring setting, since the attacker needs to induce at least 3n zeroing faults (again the factor 3 comes from the rejection probability). In the ring setting with the same assumption r = n , the attacker needs to induce (on average) three zeroing faults successfully. In case r &lt; n , the attack is in general not applicable to signature schemes over standard lattices, since the multiplication of matrices is not commutative, a condition that we need in Equation (5).

### C. Zeroing the Hash Value During the Signature Gener- ation

Zeroing the hash value c during the sign algorithm does not lead to more information about the secret key since only the product sc occurs in the ﬁnal signature. Hence, the attacker only gets access to the randomness, which changes for every run of the sign algorithm in BLISS, ring-TESLA, and the GLP scheme. Hence, knowledge of

one speciﬁc random value does not reveal information to successfully forge signatures.

### D. Zeroing Fault During the Veriﬁcation Algorithm

In this subsection, we describe a zeroing attack on the polynomial computed from the hash value c using the pseudo code of ring-TESLA. This attack works similarly on the GLP scheme and BLISS since they use the same mechanism as it is used in ring-TESLA, although this is not made explicit in their pseudo code. The goal of the attacker is to force the verify algorithm to accept a (unvalid) signature for a message μ . To this end, the attacker chooses z ← $ R q,[B−U ] , computes c ← H(a 1 z d,q , a 2 z d,q , μ) , and returns (c, z) as signature of μ . During the verify algorithm, ﬁrst the value c ← F (c ) is computed. Assume c was set to zero during a fault attacks. Hence, w 1 = a 1 z and w 2 = a 2 z , and c ← H(a 1 z d,q , a 2 z d,q , μ) . Thus, c = c and the signature is accepted.

### VI. C OUNTERMEASURES AND G UIDELINES

We describe countermeasures to prevent fault attacks for each kind of attack described in this paper. Additionally to our guidelines, we refer to the intensive literature about countermeasures in general [29]. Note that it is crucial that a countermeasure can not be easily circumvented by another fault attack. Hence, implementations of counter- measures should always consider preventions against all three kinds of attacks.

A. Countermeasures Against Randomization Faults

One way to prevent the randomization attack described in Sec. III is to check the correctness of the secret key. As long as the randomization fault is not implemented as a skipping attack, it can be prevented by simple correct- ness checks or comparisons. Our approach is somewhat different: let a −1 be the inverse polynomial of a in R q , s be the faulty secret, s be the original secret, and let b = as + e (mod q) . Instead of Line 8 of the GLP scheme (see Fig. 3), we compute z 1 = a −1 (b − b)c + s c + y 1 = sc + y 1 . Hence, we always return a signature generated with the correct secret key even if the fault attack described in Sec. III occurred. As long as implemented with respect to the guidelines mentioned in the next section, this countermeasure should not induce vulnerabilities against the described skipping or zeroing attacks. A disadvantage of this countermeasure is that the public key b has to be given as input, i.e., the key sizes are increased. Furthermore, the inverse of a has to be computed. Similarly to the protection of the secret polynomial, the error term could be protected if necessary. Our analysis in Sec. III indicates that aggressive instan- tiations such as DCK or NTRU are more vulnerable to

73 74

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 12 -->

## PDF page 12

randomization attacks. Hence, instantiating BLISS or the GLP scheme over ring-LWE or ring-SIS would strengthen the security of those schemes with respect to fault attacks. Most probably this would lead to a serious efﬁciency penalty.

B. Countermeasures Against Skipping Faults

We describe countermeasures to prevent the skipping attacks presented in Sec. IV. One way to prevent skipping faults addressing the addition in general is to deﬁne a new variable to save the resulting sum, e.g., Listing 6. Skipping Line 49 of the countermeasure in Listing 6 does not lead to a suc- cessful attack since the value b2 would not be allocated and a segmentation fault would be triggered. Hence, no information about the secret is revealed.

// original 48 poly_mul_a(b, s); 49 poly_add_nored(b,b,e);

// countermeasure poly_mul_a(b1, s); poly_add_nored(b2,b1,e);

Listing 6. Comparison of the original code of the GLP scheme and an example of a countermeasure against skipping the addition during key generation.

A different approach which prevents skipping attacks in certain cases is to add secret information to random information and not the other way around, e.g., use the code shown on the bottom of Listing 7 instead of the original GLP code. Hence, skipping Line 108b in Listing 7 results in z 1 = y 1 instead of z 1 = y 1 + as . Since y 1 changes for every sign query, the attacker does not gain information about the secret. This is already realized in the implementations of BLISS and ring-TESLA.

// original poly_setrandom_maxk(y1); [...] poly_mul(z1,c,s1); poly_add_nored(z1,z1,y1); poly_coeffreduce(z1);

95a

107a 108a 109a

//countermeasure poly_setrandom_maxk(z1); [...] poly_mul(v1,c,s1); poly_add_nored(z1,z1,v1); poly_coeffreduce(z1);

95b

107b 108b 109b

Listing 7. Comparison of the original code of the GLP scheme and an example of a countermeasure against skipping the addition of the randomness during signature generation.

Since our analysis focuses on (and our countermeasures protect against) ﬁrst order fault attacks we assume that an attack can not know the content of the cache and induce a skipping fault at the same time. Hence, the countermeasure described above should prevent ﬁrst order fault attacks. However, a stronger adversary might know the content of the cache, skip Line 95b, and hence can compute s 1 . We leave the analysis of this scenario for future work. Besides the countermeasures mentioned above, it should be ensured that only correctly formed or totally random keys are returned. In the following, we describe a method

to prevent the skipping attack presented in Sec. IV-A2. The goal of this attack is to skip operations during the key generation algorithm such that the public key is not of the correct form. A faulty b can either be b = as+e ( mod q) , b = as (mod q) , b = e (mod q) , or b = 0 . To prevent returning a faulty b , the additional computations shown in Fig. 2 should be implemented for the GLP scheme (and similarly for ring-TESLA and BLISS). In case b is not

b = as + e (mod q) u ← $ Z q ν = t−as+u e+u If s = νs ∧ e = νe: Return sk = (νs, νe) Else: Restart key generation

1 2 3 4 5 6 7

Fig. 2. Pseudo code of a countermeasure to check whether the key pair is generated correctly: the returned key pair is either of the correct form or the secret and the public key do not correspond to each other.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 12]

faulty, ν = 1 and the correct elements s, e are returned. In case b is faulty, no security ﬂaw occurs because even if Line 4 is skipped, the secret and the public key do not correspond to each other. Hence, at worst the signer uses the invalid keys to sign messages which can not be veriﬁed with the corresponding faulty b .

Due to (Gaussian) sampling of elements, it is rather difﬁcult to induce a skipping fault to skip the rejection sampling at the right time. Nevertheless, it is advisable to make sure that rejection sampling is applied correctly. In case of ring-TESLA and the GLP scheme the rejection sampling is implemented as an if-condition such that the signature is returned if the if-condition is true. In assembly code this means, that the signature is returned if the zero ﬂag is equal to 1. Hence, when the if- condition is skipped by fault, a signature is returned if and only if the zero ﬂag was set equal to 1 in an earlier computation. It is reasonable to assume that this happens with probability 0.5. Hence, formulating the if-condition as it is done for ring-TESLA and the GLP scheme does not prevent the skipping attack completely, but it doubles the (expected) number of necessary fault injections. In case of the BLISS implementation, the rejection sampling is implemented as if-condition(s) such that a signature is rejected if the if-condition holds true. Hence, skipping this if-condition means to skip the rejection sampling. Reformulating the if-condition as it is done for ring- TESLA and the GLP scheme would make this skipping attack much more complicated.

74 75

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 13 -->

## PDF page 13

### C. Countermeasures Against Zeroing Faults

Zeroing faults can often be categorized as randomiza- tion or skipping faults. Hence, zeroing faults can often be prevented by the countermeasures described in Sec. VI-A and VI-B. Assuming that the zeroing fault is not caused by skip- ping or randomizing faults, we can prevent a zeroing attack by simply checking whether the values of the secret or error polynomial (Sec. V-A), the randomness during signing (Sec. V-B), the hash value (Sec. V-C), or the encoding polynomial (Sec. V-D) are zero, since we only consider ﬁrst-order faults in this paper.

### VII. C ONCLUSION

In this paper, we analyzed the lattice-based signa- ture schemes BLISS, ring-TESLA, and the GLP scheme and their implementations with respect to fault attacks. Furthermore, we presented countermeasures against the described attacks. Hereby, we considered three types of faults: randomization, skipping, and zeroing faults. For nine of the 15 considered attacks at least one of the three schemes was vulnerable. We summarize our results in Table I. All three schemes are vulnerable against zeroing faults during the sign algorithm, against zeroing faults during the veriﬁcation, against skipping faults dur- ing the key generation, against two kinds of skipping faults during the veriﬁcation algorithm, and (to a variable extent) against skipping faults during the signature generation algorithm. Moreover, the GLP scheme is vulnerable to an additional skipping attack during the sign algorithm and an additional zeroing attack during the key generation. In Table III, we recall the (expected) minimal number of successful faults needed for the respective fault attacks.

TABLE III C OMPARISON OF THE GLP SCHEME , BLISS, AND RING -TESLA

WITH RESPECT TO THE EXPECTED NUMBER OF SUCCESSFUL FAULTS SUCH THAT THE FAULT ATTACK SUCCEEDS . T HE TABLE SHOWS THE ALGORITHMS WHICH THE FAULT ATTACKS TARGET , I . E ., KEY GENERATION (KG), SIGNATURE GENERATION (S), AND VERIFY (V). I F THE SCHEME IS VULNERABLE TO THE RESPECTIVE ATTACK , THE NUMBER OF NECESSARY SUCCESSFUL FAULTS IS GIVEN , OTHERWISE WE WRITE -.

Fault Attack

Algorithm GLP BLISS

ring- TESLA - 1 ? - 1 - - 1 1

Rand. of secret, r = 4 Skip of addition Skip of rejection Skip of addition Skip of correct-check Skip of size-check Zero. of secret Zero. of randomness, r = 1 Zero. of hash polynomial

S KG S S V V KG S V

151 1 ? 1 1 1 1 1 1

733 1 ? - 1 1 - 2 7 1

We state that the three signature schemes and their implementations behave rather similar under fault attacks. However, the different instantiations of the schemes lead to different vulnerabilities. BLISS and the GLP scheme are more vulnerable to a randomization attack during the key generation because of their aggressive instantiation with ternary secret and error. Moreover, our analysis shows that ideal-lattice-based schemes are in general more vulnerable to zeroing attacks during the sign algorithm than standard-lattice-based schemes. We propose effective countermeasures for each of the analyzed attacks. Most of them are very efﬁcient, since they do not require time- consuming computations. Future Work. This work is a starting point for fault analysis of lattice-based cryptography. It is not compre- hensive, e.g., we did not analyze underlying algebraic computations such as polynomial multiplications and we did not consider fault attacks targeting these underlying computations, e.g., we did not analyze the effects of zeroing attacks on the most (or least) signiﬁcant bits of polynomial coefﬁcients or the modulus. In addition to these ideas for deeper fault analysis, we leave for future work to compare the original implementa- tions with implementations that take our countermeasures into account and to verify the effectiveness of the proposed measures by a software simulation. Moreover, since this work focuses on theoretical fault analysis, the practical realization of the proposed attacks remains to be done.

R EFERENCES

[1] S. Akleylek, N. Bindel, J. Buchmann, J. Krämer, and G. A. Mar- son, “An efﬁcient lattice-based signature scheme with provably secure instantiation,” in International Conference on Cryptology – AFRICACRYPT 2016, D. Pointcheval, T. Rachidi, and A. Nitaj, Eds. Springer, 2016, pp. 44–60. 1, 3, 7, 10, 15 [2] M. R. Albrecht, C. Cid, J. Faugère, R. Fitzpatrick, and L. Perret, “Algebraic algorithms for LWE problems,” Cryptology ePrint Archive, Report 2014/1018, 2014. 5 [3] M. R. Albrecht, R. Fitzpatrick, and F. Göpfert, “On the efﬁcacy of solving LWE by reduction to unique-svp,” in Information Security and Cryptology - ICISC 2013, 2013, pp. 293–310. 4 [4] S. Bai and S. D. Galbraith, “An improved compression technique for signatures based on learning with errors,” in Topics in Cryptology - CT-RSA 2014, 2014, pp. 28–47. 4 [5] F. Bao, R. H. Deng, Y. Han, A. Jeng, A. D. Narasimhalu, and T. Ngair, “Breaking public key cryptosystems on tamper resistant devices in the presence of transient faults,” in Security Protocols: 5th International Workshop Paris, France, B. Christian- son, B. Crispo, M. Lomas, and M. Roe, Eds. Springer, 1998, pp. 115–124. 5 [6] N. Bindel, J. Buchmann, and J. Krämer, “Lattice-based signature schemes and their sensitivity to fault attacks,” Cryptology ePrint Archive, Report 2016/415, 2016. 4, 8, 9

7 Since the rejection sampling is applied independently from the randomness.

75 76

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 14 -->

## PDF page 14

[7] J. Blömer, R. G. da Silva, P. Günther, J. Krämer, and J. Seifert, “A practical second-order fault attack against a real-world pairing implementation,” in 2014 Workshop on Fault Diagnosis and Tolerance in Cryptography, FDTC 2014, 2014, pp. 123–136. 7 [8] L. G. Bruinderink, A. Hülsing, T. Lange, and Y. Yarom, “Flush, gauss, and reload – a cache attack on the bliss lattice-based signature scheme,” Cryptology ePrint Archive, Report 2016/300, 2016. 1 [9] J. Buchmann, F. Göpfert, T. Güneysu, T. Oder, and T. Pöppel- mann, “High-performance and lightweight lattice-based public- key encryption,” in To appear in IoTPTS 2016. 5 [10] J. Buchmann, F. Göpfert, R. Player, and T. Wunderer, “On the hardness of lwe with binary error: Revisiting the hybrid lattice-reduction and meet-in-the-middle attack,” in International Conference on Cryptology AFRICACRYPT 2016. Springer, 2016, pp. 24–43. 5 [11] L. Ducas, A. Durmus, T. Lepoint, and V. Lyubashevsky, “Lattice signatures and bimodal gaussians,” in Advances in Cryptology - CRYPTO 2013, 2013, pp. 40–56. 1, 3, 15 [12] L. Ducas and T. Lepoint, “Bliss: Bimodal lattice signature schemes,” http://bliss.di.ens.fr/. 7 [13] L. Ducas and P. Q. Nguyen, “Learning a zonotope and more: Cryptanalysis of ntrusign countermeasures,” in Advances in Cryptology - ASIACRYPT 2012 - 18th International Conference on the Theory and Application of Cryptology and Information Security, Beijing, China, December 2-6, 2012. Proceedings, 2012, pp. 433–450. 8 [14] N. Gama and P. Q. Nguyen, “Predicting lattice reduction,” in Advances in Cryptology - EUROCRYPT 2008, 27th Annual International Conference on the Theory and Applications of Cryptographic Techniques, Istanbul, Turkey, April 13-17, 2008. Proceedings, 2008, pp. 31–51. 4 [15] C. Giraud and E. W. Knudsen, “Fault attacks on signature schemes,” in Information Security and Privacy: 9th Australasian Conference, ACISP, 2004, pp. 478–491. 1, 5 [16] T. Güneysu, V. Lyubashevsky, and T. Pöppelmann, “Practical lattice-based cryptography: A signature scheme for embedded systems,” in Cryptographic Hardware and Embedded Systems - CHES 2012, 2012, pp. 530–547. 1, 3, 14 [17] G. Güneysu, T. Oder, T. Pöppelmann, and P. Schwabe, “Software speed records for lattice-based signatures,” https://cryptojedi.org/ crypto/index.shtml#lattisigns. 7 [18] A. A. Kamal and A. M. Youssef, “Fault analysis of the ntruen- crypt cryptosystem,” IEICE Transactions, vol. 94-A, no. 4, pp. 1156–1158, 2011. 1 [19] R. Lindner and C. Peikert, “Better key sizes (and attacks) for lwe-based encryption,” in Topics in Cryptology - CT-RSA 2011, 2011, pp. 319–339. 4 [20] V. Lyubashevsky, “Lattice signatures without trapdoors,” in Advances in Cryptology - EUROCRYPT 2012, 2012, pp. 738– 755. 3 [21] D. Micciancio and C. Peikert, “Hardness of SIS and LWE with small parameters,” in Advances in Cryptology - CRYPTO 2013, 2013, pp. 21–39. 5 [22] D. Naccache, P. Q. Nguyen, M. Tunstall, and C. Whelan, “Ex- perimenting with faults, lattices and the DSA,” in Public Key Cryptography - PKC 2005, 2005, pp. 16–28. 9 [23] O. Nguyen, Phong Q.and Regev, “Learning a parallelepiped: Cryptanalysis of ggh and ntru signatures,” pp. 271–288, 2006. 8 [24] N. S. A. (NSA), “Cryptography today,” https://www.nsa.gov/ia/ programs/suiteb_cryptography/, Aug 19, 2015. 1 [25] N. I. of Standards and T. (NIST), “Post-quantum cryptography: Nist’s plan for the future,” https://pqcrypto2016.jp/data/pqc2016_ nist_announcement.pdf, Aug 19, 2015. 1 [26] C. Peikert, “How (not) to instantiate ring-lwe,” Cryptology ePrint Archive, Report 2016/351, 2016. 2

[27] M.-J. O. Saarinen, “Arithmetic coding and blinding countermea- sures for ring-lwe,” Cryptology ePrint Archive, Report 2016/276, 2016. 1 [28] J. Seifert, “On authenticated computing and rsa-based authentica- tion,” in Proceedings of the 12th ACM Conference on Computer and Communications Security, CCS 2005, 2005, pp. 122–127. 9 [29] I. Verbauwhede, D. Karaklajic, and J. Schmidt, “The fault attack jungle - A classiﬁcation model to guide you,” in 2011 Workshop on Fault Diagnosis and Tolerance in Cryptography, FDTC 2011, 2011, pp. 3–8. 5, 11 [30] J. von Neumann, “Various techniques used in connection with random digits,” in Monte Carlo Method, ser. National Bureau of Standards Applied Mathematics Series, A. S. Householder, G. E. Forsythe, and H. H. Germond, Eds., 1951, vol. 12, pp. 36–38. 8 [31] Özgür Dagdelen, R. E. Bansarkhani, F. Göpfert, T. Güneysu, T. Oder, T. Pöppelmann, A. H. Sánchez, and P. Schwabe, “High-speed signatures from standard lattices,” in Progress in Cryptology – LATINCRYPT 2014, D. F. Aranha and A. Menezes, Eds., vol. 8895. Springer, 2015, pp. 84–103. 4

A PPENDIX

A. Signature Schemes

In this section we depict the signature schemes GLP, ring-TESLA, and BLISS in Fig. 3, 4, and 5, respectively.

KeyGen(1 λ ) : 1 s, e ← $ R q,[1] 2 a ← $ R q 3 b ← as + e (mod q) 4 sk ← (s, e), vk ← (a, b) 5 Return (sk, vk)

Sign(μ; a, s, e) : 6 y 1 , y 2 ← $ R q,[k]

c ← H ay 1 + y 2 d,q , μ z 1 ← y 1 + sc z 2 ← y 2 + ec If z 1 , z 2 ∈ / R k−32 : Restart Else: z 2 ← compress(az 1 − tc, z 2 , p, k − 32) Return (z 1 , z 2 , c) Verify(μ; z 1 , z 2 , c; a, b)

7 8 9 10 11 12 13

c ← H az 1 + z 2 − bc d,q , μ If c = c ∧ z 1 , z 2 ∈ R k−32 : Return 1 Else: Return 0

14

15 16 17

Fig. 3. Speciﬁcation of the GLP scheme by Güneysu et al. [16]. The rounding operator · d,q corresponds to the function used in the original paper with d = log 2 (k), where k is the parameter used in [16]. For detailed information about the system parameters and the procedure compress, we refer to the original work.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 14]

B. The Ring Learning with Errors Problem (R-LWE)

In this section, we recall the ring learning with errors problem (R-LWE). We start by deﬁning the LWE distri- bution and then state the ring variants of the search and the decisional learning with errors problem.

76 77

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 15 -->

## PDF page 15

KeyGen(1 λ ) : 1 a 1 , a 2 ← $ R q 2 s, e 1 , e 2 ← D σ n 3 If checkE(e 1 ) = 0 ∨ checkE(e 2 ) = 0 4 Restart 5 b 1 ← a 1 s + e 1 (mod q) 6 b 2 ← a 2 s + e 2 (mod q) 7 sk ← (s, e 1 , e 2 ), vk ← (b 1 , b 2 ) 8 Return (sk, vk)

Sign(μ; a 1 , a 2 , s, e 1 , e 2 ) : 9 y ← $ R q,[B] 10 v 1 ← a 1 y (mod q) 11 v 2 ← a 2 y (mod q) 12 c ← H v 1 d,q , v 2 d,q , μ 13 c ← F (c ) 14 z ← y + sc 15 w 1 ← v 1 − e 1 c (mod q) 16 w 2 ← v 2 − e 2 c (mod q) 17 If |[w 1 ] 2 d |, |[w 2 ] 2 d | ∈ / R 2 d −L ∨z ∈ R B−U : 18 Restart 19 Return (z, c )

Verify(μ; z, c ; a 1 , a 2 , b 1 , b 2 ) 20 c ← F (c ) 21 w 1 ← a 1 z − b 1 c (mod q) 22 w 2 ← a 2 z − b 2 c (mod q) 23 c ← H w 1 d,q , w 2 d,q , μ 24 If c = c ∧ z ∈ R B−U : 25 Return 1 26 Else: Return 0

Fig. 4. Speciﬁcation of the scheme ring-TESLA by Akleylek et al. [1]. For detailed information about the system parameters and the procedure checkE, we refer to the original work.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 15]

Deﬁnition 1 (Learning with Errors Distribution): Let n, q &gt; 0 be integers, s ∈ R q , and χ be a distribution over R . We deﬁne by D s,χ the R-LWE distribution which outputs (a, a, s + e) ∈ R q × R q , where a ← $ R q and e ← χ . Deﬁnition 2 (Ring Learning with Errors Problem): Let n, q &gt; 0 be integers and n = 2 k for some k ∈ N &gt;0 and χ be a distribution over R . Given n, q , and m LWE-samples, the (search) ring learning with errors problem R − LW E n,m,q,χ is to ﬁnd the polynomial s . Given n, q , and samples (a 1 , b 1 ), ..., (a m , b m ) the (decisional) ring learning with errors problem is to decide whether the samples are LWE-samples or whether b 1 , ..., b m are chosen uniformly random over Z q [x]/(x n + 1) .

KeyGen(1 λ ) 1 f, g ← $ F d 1 ,d 2 2 If N λ (S) ≥ 5C 2 (δ 1 n + 44δ 2 n)κ 3 Restart 4 a q = (2g + 1)/f (mod q) 5 If f not invertible 6 Restart 7 (s 1 , s 2 ) T ← (f, 2g + 1) T 8 (a 1 , a 2 ) = (2a q , q − 2)(mod 2q) 9 sk ← (s 1 , s 2 ) T , vk ← (a 1 , a 2 ) 10 Return (sk, vk)

Sign(μ; A = (a 1 , q − 2); S = (s 1 , s 2 ) T ) : 11 y 1 , y 2 ← D σ 12 u = ξa 1 y 1 + y 2 (mod 2q) 13 c ← H u d,2q , μ 14 b ← $ {0, 1} 15 z 1 ← y 1 + (−1) b s 1 c 16 z 2 ← y 2 + (−1) b s 2 c 17 Continue with probability 1/ν 18 z 2 ← u d,2q − u − z 2 d,2q mod p 19 Return (z 1 , z 2 , c)

Verify(μ; A = (a 1 , q − 2); z 1 , z 2 , c) 20 c ← H ξa 1 z 1 + ξqc(mod 2q) d,2q + z 2 (mod p), μ 21 If c = c ∧ ||(z 1 |2 d z 2 )|| 2 ≤ B 2 ∧ ||(z 1 |2 d z 2 )|| ∞ ≤ B ∞ : 22 Return 1 23 Else: Return 0

Fig. 5. Speciﬁcation of the scheme BLISS by Ducas et al. [11]. For detailed information about the system parameters and the deﬁnition the original work. The set F d 1 ,d 2 is deﬁned of N λ (·), we refer to n−1 i as F d 1 ,d 2 = {h = i=0 h i x |h i ∈ {−2, −1, 0, 1, 2}, |{h i ∈ {−1, 1}}| = d 1 , |{h i ∈ {−2, 2}}| = d 2 } and ν = M exp −||Sc|| 2 /(2σ 2 )cosh(z, Sc/σ 2 ) .

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 15]

77 78

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:08 UTC from IEEE Xplore. Restrictions apply.
