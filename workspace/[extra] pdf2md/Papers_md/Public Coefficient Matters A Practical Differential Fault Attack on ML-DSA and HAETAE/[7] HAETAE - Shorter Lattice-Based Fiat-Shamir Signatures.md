# [7] HAETAE - Shorter Lattice-Based Fiat-Shamir Signatures

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 51
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-07"
derived_asset_id: "PCM-DFA-REF-07-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[7] HAETAE - Shorter Lattice-Based Fiat-Shamir Signatures.pdf"
source_sha256: "a3bbcfa0b23d7a2f97660389080ea2151482a1c3b173dfbbdc6a89457d3b3454"
pages: 51
bbox_words: 26384
consumed_bbox_words: 26384
numeric_tokens: 3229
consumed_numeric_tokens: 3229
source_blocks: 936
consumed_source_blocks: 936
emitted_blocks: 872
embedded_raster_images: 0
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 51
glyph_chars_removed: 29
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

IACR Transactions on Cryptographic Hardware and Embedded Systems ISSN 2569-2925, Vol. 2024, No. 3, pp. 25–75. DOI:10.46586/tches.v2024.i3.25-75

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

Jung Hee Cheon 1,2 , Hyeongmin Choe 1 , Julien Devevey 3 , Tim Güneysu 4,5 , Dongyeon Hong 6 , Markus Krausz 4 , Georg Land 4 , Marc Möller 4 , Damien Stehlé 7 and MinJune Yi 1

1 Seoul National University, Seoul, Republic of Korea jhcheon@snu.ac.kr,sixtail528@snu.ac.kr,yiminjune@snu.ac.kr 2 CryptoLab Inc., Seoul, Republic of Korea 3 ANSSI, Paris, France julien.devevey@ens-lyon.fr 4 Ruhr University Bochum, Bochum, Germany firstname.lastname@rub.de,mail@georg.land 5 DFKI, Bremen, Germany 6 The Affiliated Institute of ETRI, Daejeon, Republic of Korea jjoker041@gmail.com 7 CryptoLab Inc., Lyon, France damien.stehle@cryptolab.co.kr

Abstract. We present HAETAE (Hyperball bimodAl modulE rejecTion signAture schemE), a new lattice-based signature scheme. Like the NIST-selected Dilithium signature scheme, HAETAE is based on the Fiat-Shamir with Aborts paradigm, but our design choices target an improved complexity/compactness compromise that is highly relevant for many space-limited application scenarios. We primarily focus on reducing signature and verification key sizes so that signatures fit into one TCP or UDP datagram while preserving a high level of security against a variety of attacks. As a result, our scheme has signature and verification key sizes up to 39% and 25% smaller, respectively, compared than Dilithium. We provide a portable, constant- time reference implementation together with an optimized implementation using AVX2 instructions and an implementation with reduced stack size for the Cortex-M4. Moreover, we describe how to efficiently protect HAETAE against implementation attacks such as side-channel analysis, making it an attractive candidate for use in IoT and other embedded systems.

Keywords: Signature, Fiat-Shamir, Lattice-based Cryptography, Bimodal Distribu- tion

1 Introduction

The rise of quantum computing has brought up – among others – the necessity of new, post-quantum digital signature schemes. In the standardization process of post-quantum cryptography by the American National Institute of Standards and Technology (NIST), the lattice-based schemes Falcon [FHK + 18] and Dilithium [DKL + 18] have already been announced as future standards, and another 40 new candidates are on-ramp for an additional process. The critical challenge in developing lattice-based digital signatures lies in finding a balance between security and practicality: while developing secure schemes against a wide range of attacks is essential, it is also vital to ensure they are practical for real-world applications. This challenge becomes even more critical with the increasing

This work is submitted to ‘Korean Post-Quantum Cryptography Competition’ (www.kpqc.or.kr) and ‘NIST Post-Quantum Cryptography Standardization of Additional Digital Signature Schemes.’

Licensed under Creative Commons License CC-BY 4.0. Received: 2024-01-15 Accepted: 2024-03-15

Published: 2024-07-18

<!-- PDF_PAGE: 2 -->

## PDF page 2

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

26

Table 1: NIST security level, signature size, verification key size, and implementation security, with respect to constant-time and masking of selected signature schemes Scheme Lvl. Sig. vk Const.-time. Maskable Falcon-512 1 666B 897B 3 [Por19] 7 [Pre23] Dilithium-2 2 2,420B 1,312B 3 [DKL + 18] 3 [MGTF19] HAETAE-120 2 1,474B 992B 3 3

prevalence of embedded devices and the Internet of Things (IoT). Both technologies have become ubiquitous, from home appliances to medical devices connected to the internet.

In particular, this leads to two practical requirements:

1. The verification key and signature sizes must be as small as possible since both are frequently transmitted. Specifically, it is helpful if the signature is small enough to be sent in only one UDP or TCP datagram, as this minimizes the need for packet fragmentation. The importance of the signature and verification key sizes for communication protocols has been highlighted already in multiple evaluations [Wes21, PST20, GS23]. Paquin et al. [PST20] observe for TLS, that fragmentation over many packets has a significant performance impact for network links with non-ideal packet loss rates. Benchmarking DNSSEC [GS23] revealed, that the smaller signatures of Falcon lead to faster resolution times in comparison to Dilithium in most scenarios, although the signature computation and verification is much faster with Dilithium compared to Falcon.

2. The secret-dependent operations such as key generation and message signing must be easy to protect against implementation attacks. This is essential in embedded use cases like the IoT, where attackers have physical access and can measure power consumption or electromagnetic emanation [KA21], additionally to the timing behaviour [Sch00], which is also exploitable from remote.

In this context, Falcon fulfills the first requirement very well, but efforts for making it to satisfy the second requirement, namely Mitaka [EFG + 22], were recently broken [Pre23]. Dilithium, on the other hand, focuses on being easy to implement and protecting against side- channel attacks. However, this comes at the sacrifice of larger signatures and verification keys, which, for example, do not allow a signature to fit in one UDP datagram. We summarize this discussion in Table 1 and compare the two with HAETAE.

Contribution. We present HAETAE 1 , a lattice-based digital signature scheme that improves over Dilithium by up to 39 % smaller signature and key sizes. Moreover, this improvement is not expected to come at a significant increase in the cost to protect the scheme against physical attacks. Namely, the most significant difference (w.r.t. masking in comparison to Dilithium) is the usage of fix-point arithmetic which is similar to masking integers. Its quantum security is based on the hardness of the module versions of the lattice problems LWE and SIS [BGV12, LS15], in the Quantum Random Oracle Model (QROM). The scheme design follows the “Fiat-Shamir with Aborts” paradigm [Lyu09, Lyu12], which relies on rejection sampling: rejection sampling is used to transform a signature trial whose distribution depends on sensitive information, into a signature whose distribution can be publicly simulated. HAETAE is in part inspired from Dilithium, a post-quantum “Fiat-Shamir with Aborts” signature scheme, notably concerning the use of the module LWE and SIS assumptions. HAETAE differs from Dilithium in two major aspects: (i) we use a bimodal distribution for the rejection sampling, like in the BLISS signature scheme [DDLL13], instead of a

1 The haetae is a mythical Korean lion-like creature with the innate ability to distinguish right from wrong.

<!-- PDF_PAGE: 3 -->

## PDF page 3

Team HAETAE

27

“unimodal” distribution like Dilithium, (ii) we sample from and reject to hyperball uniform distributions, instead of discrete hypercube uniform distributions. The design departs from BLISS, as HAETAE relies on module lattice problems while BLISS relies either on assumptions on unstructured lattices or the NTRU assumption [HPS98]: this leads us to introduce a new key generation algorithm. A further difference is that BLISS, which can be seen as Dilithium with bimodal rejection from Gaussians, involves discrete Gaussian distributions whereas HAETAE considers hyperball uniform distributions as suggested in [DFPS22]. We recall from [DFPS22] that, with a rejection rate constraint, the choice of bimodal rejection sampling from the hyperballs results in the optimal signature sizes among the possible variants of Dilithium. This choice also allows for simple rejection sampling without transcendental function computation on the secret key and approximations for tail-cutting, while retaining the signature compactness. HAETAE benefits from several novel improvements in the key generation algorithm. We introduce a new rejection procedure in the key generation algorithm to minimize the magnitude of the secret key when multiplied by the challenge. This facilitates rejection sampling in the signing algorithm and leads to smaller signatures. The key generation rejection is also designed to be efficient and simple to implement. It significantly improves over a procedure with a similar objective in the key generation of BLISS. Furthermore, we introduce to the bimodal setting a verification key truncation with the same objective as Dilithium’s. A direct adaptation would lead to large bounds for the verification algorithm and degraded security. Instead, we compensate for the verification key truncation by correcting the signing key accordingly. It increases the magnitude of the signing key, but by a much smaller amount than the naive approach. For the signing algorithm, we adapt Dilithium’s signature compression so that it is compatible with our module lattices key generation algorithm, by taking into account the residues modulo 2. The main novelty in the signing algorithm is a detailed description of a fixed-point arithmetic algorithm for sampling uniformly in a discrete hyperball, which was left open in [DFPS22]. The discretization leads to numerical errors on the uniform distribution: we bound them and bound their effect on the scheme security. High precision is required during signing; however, by applying the entropy encoding technique from [ETWY22] to hyperball uniform distributions, the output signature of the signing algorithm becomes as compact as its entropy, which is much smaller than Dilithium. We present in Table 2 a brief comparison between the main divergence points of Dilithium, HAETAE and BLISS. Most importantly, the choice of bimodal hyperballs in HAETAE does not need to compute a secret-dependent transcendental function during signature rejection, just like Dilithium, contrary to BLISS.

Table 2: Comparison between Dilithium, HAETAE and an hypothetical update of BLISS, obtained by interpolating our approach and BLISS’s approach of rejection sampling via bimodal Gaussians. Completely updating BLISS is out of the scope of this paper and left as future work. “Maybe” means that masking is doable using generic techniques, but optimized gadgets are not yet available. Dilithium HAETAE Updated BLISS Rejection Step Deterministic Deterministic Probabilistic Arithmetic Integers Fix-point Fix-point Maskable Yes Maybe Maybe Sizes Long Short Similar to HAETAE Additional primitives ◦ Gaussian sampler ◦ Hyperball sampler to implement N/A ◦ CRT for mod2q ◦ CRT for mod2q w.r.t. Dilithium ◦ Secure rejection step

Implementation and Performance. We propose three parameter sets with NIST

<!-- PDF_PAGE: 4 -->

## PDF page 4

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

28

Table 3: Relative comparison between HAETAE, Dilithium, and Falcon. The security levels are given in the parameter sets instead of their name. The percentages are the ratio of their sizes and the execution times. The execution time is measured as the median cycle counts among 1000 executions, obtained on one core of an Intel Core i7-10700k, with TurboBoost and hyperthreading disabled. Parameter set Sig. size vk size KeyGen Sign Verify HAETAE-2 / Dilithium-2 61% 76% 409% 507% 100% HAETAE-3 / Dilithium-3 71% 75% 376% 444% 113% HAETAE-5 / Dilithium-5 64% 80% 328% 454% 91% HAETAE-2 / Falcon-1 221% 111% 3% 35% 365% HAETAE-5 / Falcon-5 230% 116% 2% 30% 399%

security levels 2, 3 and 5. Each parameter set of HAETAE has 20-25% smaller verification key size and 29-39% shorter signatures than its counterpart in Dilithium. Based on our portable and constant-time reference implementation of HAETAE, the verification process is as fast as Dilithium’s, while the resulting key generation and signing algorithm are up to five times slower than Dilithium’s. Up to 80% of the signing time is consumed by the hyperball sampling. Thus, any improvement to this sampling would contribute greatly to the efficiency of HAETAE, an independent speedup to further optimizations. Nonetheless, our benchmarks indicated signing with HAETAE is still around three times faster than with Falcon (portable Falcon with emulated floating-point operations). We summarize the comparison results in Table 3. We provide a detailed, implementation-oriented specification using Chinese Remainder Theorem (CRT) and Number-Theoretic Transform (NTT), which enables efficient implementation of HAETAE (Section 5). We additionally developed an optimized version using AVX2 instructions (Section 6), and an implementation for the Cortex-M4 (Section 7), where we explore stack reduction techniques. Moreover, we observe that masking HAETAE against physical attacks is only slightly more complex than masking Dilithium, based on the similarity of the scheme design and the use of fixed-point arithmetic. One of the conceptual differences between HAETAE and Falcon (and their variants) regarding physical attacks is that HAETAE only needs Gaussian samples for secret-independent centers and standard deviations. Finally, we note that like other Fiat-Shamir signatures, such as Schnorr signa- tures [Sch90], the randomized signing of HAETAE can take advantage of pre-computations. By sampling from the hyperball and pre-computing the message-independent components offline, the online signing phase of HAETAE is cut by factor five. Our code is publicly available.

Related Work. An alternative approach to avoid leakage during the rejection step in Fiat-Shamir signatures based on lattices is to remove it altogether. A first approach is to flood what depends on the signature key in signatures by a much larger quantity. As shown in [ASY22], relying on the Rényi divergence for the security analysis allows to limit the amount of flooding. A concrete instantiation was recently proposed in [dPEK + ]. This however results in signature sizes that are much higher than ours. A second approach was recently given in [DPS23], which uses Gaussian convolutions to obtain signatures that can be simulated, without flooding nor rejection sampling. However, signing is more complex as it relies on sampling from large-dimensional integer Gaussian distribution with non-diagonal covariance matrices. Also, the signature sizes provided in [DPS23] are worse than ours for the smallest parameter set, and only marginally smaller for larger parameter sets. An extensive comparison of the recent lattice signatures can be found in Appendix A.

<!-- PDF_PAGE: 5 -->

## PDF page 5

Team HAETAE

2 Preliminaries

29

Before introducing specific results adapted to the setting in HAETAE in Section 3 and the HAETAE scheme itself in Section 4, we start by defining notations used throughout this paper and recapitulate relevant fundamental works.

### 2.1 Notations

Matrices are denoted in bold font and upper case letters (e.g., A), while vectors are denoted in bold font and lowercase letters (e.g., y or z 1 ). The i-th component of a vector is denoted with subscript i (e.g., y i for the i-th component of y). Every vector is a column vector. We denote concatenation between vectors by putting the rows below as (u, v) and the columns on the right as (u|v). We naturally extend the latter notation to concatenations between matrices and vectors (e.g., (A|b) or (A|B)). We let bye be a rounding of y ∈ R to the nearest integer. We naturally extend the rounding notation to vectors and polynomials by applying it component-wise. We let R = Z[x]/(x n + 1) be a polynomial ring where n is a power of 2 integer and for any positive integer q the quotient ring R q = Z[x]/(q, x n + 1) = Z q [x]/(x n + 1). We abuse notations and identify R 2 with the set of elements in R with binary coefficients. We also let R R = R[x]/(x n + 1) be a polynomial ring over real numbers. For an integer η, we let S η denote of degree less than n with coefficients in [−η, η] ∩ Z. P the set of polynomials P Given y = ( 0≤i&lt;n y i x i , · · · , 0≤i&lt;n y nk−n+i x i ) &gt; ∈ R k (or R k R ), we define its ` 2 -norm as the ` 2 -norm of the corresponding “flattened” vector kyk 2 = k(y 0 , · · · , y nk−1 ) &gt; k 2 . Let B R,m (r, c) = {x ∈ R m R |kx − ck 2 ≤ r} denote the continuous hyperball with center c ∈ R m and radius r &gt; 0 in dimension m &gt; 0. When c = 0, we omit it. Let B (1/N )R,m (r, c) = (1/N )R m ∩ B R,m (r, c) denote the discretized hyperball with radius r &gt; 0 and center c ∈ R m in dimension m &gt; 0 with respect to a positive integer N . When c = 0, we omit it. Given a measurable set X ⊆ R m of finite volume, we let U (X) denote the continuous uniform distribution over X. It admits x 7→ χ X (x)/Vol(X) as a probability density, where χ X is the indicator function of X and Vol(X) is the volume of the set X. For the normal distribution over R centered at µ with standard deviation σ, we use the notation N (µ, σ). For a positive integer α, we define r mod ± α as the unique integer r 0 in the range [−α/2, α/2) satisfying the relation r = r 0 mod α. We also define r mod + α as the unique integer r 0 in the range [0, α) that satisfies r = r 0 mod α. We denote the least significant bit of an integer r with LSB(r). We naturally extend this to integer polynomials and vectors of integer polynomials, by applying it component-wise.

i-th

For a sequence of real numbers a 0 , . . . , a n , we denote the i-th maximum as max a j .

### 2.2 Signatures

We briefly recall the formalism of digital signatures.

j

Definition 1 (Digital Signature). A signature scheme is a tuple of PPT algorithms (KeyGen, Sign, Verify) with the following specifications:

• KeyGen : 1 λ → (vk, sk) outputs a verification key vk and a signing key sk;

• Sign : (sk, µ) → σ takes as inputs a signing key sk and a message µ and outputs a signature σ;

• Verify : (vk, µ, σ) → b ∈ {0, 1} is a deterministic algorithm that takes as inputs a verification key vk, a message µ, and a signature σ and outputs a bit b ∈ {0, 1}.

<!-- PDF_PAGE: 6 -->

## PDF page 6

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

30

Let γ &gt; 0. We say that it is γ-correct if for any pair (vk, sk) in the range of KeyGen and µ,

Pr[Verify(vk, µ, Sign(sk, µ)) = 1] ≥ γ,

where the probability is taken over the random coins of the signing algorithm. We say that it is correct in the (Q)ROM if the above holds when the probability is also taken over the randomness of the random oracle modeling the hash function used in the scheme.

We also give two security notions, namely the existential unforgeability under chosen message attacks, and under no-message attacks.

Definition 2 (Security). Let T, δ ≥ 0. A signature scheme sig = (KeyGen, Sign, Verify) is said to be (T, δ)-UF-CMA secure in the QROM if for any quantum adversary A with runtime ≤ T given (classical) access to the signing oracle and (quantum) access to a random oracle H, it holds that

Pr [Verify(vk, µ ∗ , σ ∗ ) = 1|(µ ∗ , σ ∗ ) ← A H,Sign (vk)] ≤ δ,

(vk,sk)

where the randomness is taken over the random coins of A and (vk, sk) ← KeyGen(1 λ ). The adversary should also not have issued a sign query for µ ∗ . The above probability of - CMA (A). If A does forging a signature is called the advantage of A and denoted by Adv UF sig not output anything, then it automatically fails. Existential unforgeability against no-message attack, denoted by UF-NMA is defined similarly except that the adversary is not allowed to query any signature per message. Strong existential unforgeability, denoted by sUF-CMA, allows an adversary to query signatures for its target message, as long as it does not output a queried signature.

### 2.3 Lattice Assumptions

We first recall the well-known lattice assumptions MLWE and MSIS on algebraic lattices.

Definition 3 (Decision-MLWE n,q,k,`,η ). For positive integers q, k, `, η and the dimension n of R, we say that the advantage of an adversary A 1 solving the decision-MLWE n,q,k,`,η problem is Pr b = 1 | A ← R k×` ; b ← R kq ; b ← A 1 (A, b) q A ← R k×` ; (s 1 , s 2 ) ← S η ` × S η k ; . Adv MLWE q n,q,k,`,η (A 1 ) = − Pr b = 1 b ← A 1 (A, As 1 + s 2 )

Definition 4 (Search-MSIS n,q,k,`,β ). For positive integers q, k, `, a positive real number β and the dimension n of R, we say that the advantage of an adversary A 2 solving the search-MSIS n,q,k,`,β problem is

0 &lt; kyk 2 &lt; β ∧ (A| Id k ) · y = 0 mod q

Adv MSIS n,q,k,`,β (A 2 ) = Pr

k+` A ← R k×` ; y ∈ R ← A (A) . 2 q q

Moreover, we finally introduce a variant of the SelfTargetMSIS problem introduced in Dilithium [DKL + 18], which corresponds to our setting.

Definition 5 (BimodalSelfTargetMSIS H,n,q,k,`,β ). Let H : {0, 1} ∗ × M → R 2 be a crypto- graphic hash function, where M ⊆ {0, 1} ∗ is a message space. Let q, k, ` &gt; 0, β ≥ 0 and the dimension n of R. An adversary A 3 solving the search-BimodalSelfTargetMSIS H,n,q,k,`,β

<!-- PDF_PAGE: 7 -->

## PDF page 7

Team HAETAE

31

problem with respect to j ∈ R k 2 \ {0} has an advantage of

   Adv BimodalSelfTargetMSIS (A ) = Pr 3 H,n,q,k,`,β  

0 &lt; kyk 2 &lt; β ∧ H(Ay − qcj mod 2q, µ) = c (A 0 |b) ← R k×` ; q A = (2b + qj| 2A 0 | 2Id k ) mod 2q; |H(·)i (y, c, µ) ∈ R k+` × R 2 × M ← A 3 (A) q

   .  

In the ROM (resp. QROM), the adversary is given classical (resp. quantum) access to H.

The following classical reduction from MSIS to BimodalSelfTargetMSIS is very similar to the reduction from MSIS to SelfTargetMSIS introduced in [DKL + 18] and is similarly non-tight. As this latter reduction, it cannot be straightforwardly extended to a reduction in the QROM, since it relies on the forking lemma.

Theorem 1 (Classical Reduction from MSIS to BimodalSelfTargetMSIS). Let q &gt; 0 be an odd modulus, H : {0, 1} ∗ × M → R 2 be a cryptographic hash function modeled as a random oracle and that every polynomial-time classical algorithm has a negligible advantage against MSIS n,q,k,`,β . Then every polynomial-time classical algorithm has negligible advantage against BimodalSelfTargetMSIS n,q,k,`,β/2 .

Proof sketch. Consider a BimodalSelfTargetMSIS n,q,k,`,β/2 classical algorithm A that is polynomial-time and has classical access to H. If A H(·) (A) makes Q hash queries H(w i , µ i ) for i = 1, · · · , Q and outputs a solution (y, c, µ j ) for some j ∈ [Q], then we can construct an adversary A 0 for MSIS n,q,k,`,β as follows. The adversary A 0 can first rewind A to the point at which the j-th query was made and reprogram the hash as H(w j , µ j ) = c 0 (6 = c). Then, with probability approximately 1/Q, algorithm A will produce another solution (y 0 , c 0 , µ j ). We then have ( Ay − qcj = z j = Ay 0 − qc 0 j mod 2q, kyk 2 , ky 0 k 2 &lt; β/2.

As q is odd, we have A(y − y 0 ) = (c − c 0 )j mod 2. The fact that c 0 6 = c implies that the latter is non-zero modulo 2, and hence so is y − y 0 over the integers. As it also satisfies (b| A 0 | Id k ) · (y − y 0 ) = 0 mod q and ky − y 0 k &lt; β, it provides a MSIS n,q,k,`,β solution for the matrix (b| A 0 | Id k ), where the submatrix (−b| A 0 ) ∈ R k×` is uniform. q

Sampling from the Continuous Hyperball-uniform

2.4

In order to sample in practice from hyperball uniform, we rely on the following result.

y ← U (B R,k (r)):

1: y i ← N (0, 1) for i = 0, · · · , nk + 1 2: L ← k(y 0 , · · · , y nk+1 ) &gt; k 2

3: y ← r/L · (

P n−1

i i=0 y i x , · · · ,

4: return y

P nk−1

i &gt; i=nk−n y i x )

. y ∈ R k R

Figure 1: Hyperball uniform sampling

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 7]

Lemma 1 ( [VGS17]). The distribution of the output of the algorithm in Figure 1 is U (B R,k (r)).

<!-- PDF_PAGE: 8 -->

## PDF page 8

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

32

Sampling from continuous hyperball-uniform can be done using the algorithm in Figure 1 due to Lemma 1. However, to allow side-channel secure implementations of HAETAE, we sample from discrete hyperball-uniform. We delay to Section 3.2 the analysis of a discretized version which turns discrete Gaussian samples to discrete hyperball-uniform distribution.

Signature Encoding via Range Asymmetric Numeral System

2.5

A HAETAE signature is essentially a vector z, that is compressed into z 2 with smaller dimension and a hint h, that are then encoded. While Huffman coding would be applied on each coordinate at a time, an arithmetic coding encodes the entire vector coordinates in a single number. In contrast to Huffman coding, arithmetic coding gets close to entropy also for alphabets, where the probabilities of the symbols are not powers of two. We recall a recent type of entropy coding, named range Asymmetric Numeral systems (rANS) [Dud14], that encodes the state in a natural number and thus allows faster implementations. The rANS encoding technique was recently used in [ETWY22] and we adapt it to hyperball uniform distributions. As a stream variant, rANS can be implemented with finite precision integer arithmetic by using renormalization.

Coding). Let t &gt; 0 and Definition 6 (Range Asymmetric Numeral System (rANS) P S ⊆ [0, 2 t − 1]. Let g : [0, 2 t − 1] → Z ∩ (0, 2 t ] such that x∈S g(x) ≤ 2 t and g(x) = 0 for all x ∈ / S. We define the following: P s−1 • CDF : S → Z, defined as CDF(s) = y=0 g(y).

• symbol : Z → S, where symbol(y) is defined as s ∈ S satisfying CDF(s) ≤ y &lt; CDF(s + 1).

• C : Z × S → Z, defined as

x C(x, s) = · 2 t + (x mod + g(s)) + CDF(s). g(s)

Then, we define the rANS encoding/decoding for the set S and frequency g/2 t as in Figure 2.

Encode((s 1 , · · · , s m ) ∈ S m ): 1: x 0 = 0 2: for i = 0, · · · , m − 1 do 3: x i+1 = C(x i , s i+1 ) 4: return x m

Decode(x ∈ Z): 1: y 0 = x 2: i = 0 3: while y i &gt; 0 do 4: s 0 i+1 = symbol(y i mod + 2 t ) 5: y i+1 = by i /2 t c · g(s 0 i+1 ) + (y i mod + 2 t ) − CDF(s 0 i+1 ) 6: i++ 7: m = i − 1 8: return (s 0 m , · · · , s 0 1 ) ∈ S m

Figure 2: rANS encoding and decoding procedures

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 8]

<!-- PDF_PAGE: 9 -->

## PDF page 9

Team HAETAE

33

Lemma 2 (Adapted from [Dud14]). The rANS coding is correct, and the size of the rANS code is asymptotically equal to Shannon entropy of the symbols. That is, for any choice of s = (s 1 , · · · , s m ) ∈ S m , Decode(Encode(s)) = s. Moreover, for any positive x and any probability distribution p over S, it holds that X X 2 t g(s) p(s) log 2 (C(x, s)) ≤ log 2 (x) + p(s) log 2 + . t 2 x

s∈S

s∈S

Finally, the cost in bitlength of encoding the first symbol is ≤ t, i.e., for any s ∈ S, we have log 2 (C(0, s)) ≤ t.

We determine the frequency of the symbols experimentally, by executing the signature computation and collecting several million samples. Finally, we P apply some rounding strategy in order to heuristically minimize the empirical entropy s∈S p(s) log(g(s)/2 n ).

3 HAETAE-specific Results

While our scheme is reminiscent of Dilithium, the bimodal setting hinders the use of some of its base components. In this section, we describe parts that are specifically adapted to HAETAE. First, the key generation algorithm departs from known key generation algorithms for BLISS, as we work in the module setting. Second, we study the precision needed when discretizing the hyperball sampler from Section 2.4 to enable fixed-point arithmetic. Then, we explain how challenges are computed in HAETAE. Next, we describe the rejection sampling procedure and estimate its expected number of iterations depending on the fixed-point arithmetic precision. Finally, we explain how to split the coordinates of a signature vector into high and low bits, allowing for signature compression via low bits drop. This order is consistent with the order in which those results are used during signing.

### 3.1 Key Generation

When using bimodal rejection sampling, the verification step relies on a specific key k×(k+`) b pair (A, s) ∈ R p × R k+` such that the bimodal centers (−1) As mod p (b = 0, 1) p are the same, regardless of the bit b. To generate such a pair, following [DDLL13], we choose p = 2q and aim at As = qj mod 2q for j = (1, 0, . . . , 0) &gt; .

### 3.1.1 Key Generation and Encoding

To build such a key pair (A, s), we do as follows. We first generate an MLWE sample b = k×(`−1) A gen s gen + e gen mod q, where A gen ←- U (R q ) and (s gen , e gen ) ←- U (S η `−1 × S η k ). We &gt; then define A = (−2b + qj| 2A gen | 2Id k ) mod 2q as well as s &gt; = (1|s &gt; gen |e gen ). This is a valid verification key pair for HAETAE, but the choice of even modulus 2q makes it hard to truncate the least significant bits of b as in Dilithium. To enable the verification key truncation, we modify the key generation algorithm, as follows. We use an extra randomness a gen ←- U (R kq ) and let b−a gen = A gen s gen +e gen mod q. For any decomposition b = b 1 + b 0 , we then define A = (2(a gen − b 1 ) + qj|2A gen |2I k ) &gt; as well as s &gt; = (1|s &gt; gen |(e gen − b 0 ) ). One sees that As = qj mod 2q. In practice, the verification key is then comprised of b 1 and the seed that allows generating A gen and a gen . The secret key is the seed used to generate s and (A gen , a gen ). It remains to choose the decomposition of b, that we see as an nk-dimensional vector with coordinates in [0, q − 1]. We set the coordinates of b 1 as follows. If some coordinate of b is even, then we take the same value for the corresponding coordinate of b 1 . Else, we

<!-- PDF_PAGE: 10 -->

## PDF page 10

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

34

take the rounding of this coordinate to the nearest multiple of 4 as value for b 1 . Next we set b 0 = b − b 1 and we note that coordinates of b 0 lie in [−1, 1], i.e., b 0 ∈ S 1 k . We can then write b = b 0 + 2b 0 1 , where b 0 1 is encoded using dlog 2 (q) − 1e bits per coordinate, i.e. one less bit than b. This is computed coordinate-wise with b 0 = (−1) bb/2c mod 2 b mod 2. In all of the following, we let (LowBits vk (b), HighBits vk (b)) denote (b 0 , b 1 ). When b is uniform, we notice that the coordinates of b 0 roughly follow a (centered) binomial law with parameters (2, 1/2), which experimentally leads to smaller choices for γ, which we discuss and introduce below. Note that the truncation reduces each coeffficient of b by 1 bit. So the verification key becomes shorter, but not significantly. Thus, we use the truncation for lower security levels and keep the no-truncation version for the highest level. In the following, we refer to the truncated version as d = 1 and the non-truncated version as d = 0, where d is the vk truncation bit.

### 3.1.2 Rejection Sampling on the Key

A critical step of our scheme is bounding kcsk 2 , where s is generated as before and c ∈ R is a polynomial with coefficients in {0, 1} and has less than or equal to τ nonzero coefficients. The lower this bound is, the smaller the signature is, which in turn leads to the harder forging. In the key generation algorithm, we √ apply the following rejection condition for some heuristic value γ, bounding kcsk 2 ≤ γ τ :

m X

i-th

N (s) := τ ·

(m+1)-th

max ks(ω j )k 22 + r · max ks(ω j )k 22 ≤ γ 2 n,

0≤j&lt;2n

i=1

0≤j&lt;2n

where m = bn/τ c, r = n mod τ , ω j ’s are the primitive 2n-th roots of unity (0 ≤ j ≤ 2n − 1). Note that s(ω j ) is defined as (s 1 (ω j ), · · · , s k+` (ω j )) ∈ C k+` given the secret key s = (s 1 , · · · , s k+` ) ∈ R k+` . Below, we prove that the √ left hand side is a bound on nτ · kcsk 22 and that this condition leads to asserting kcsk 2 ≤ γ τ .

Lemma 3. For any challenge c ∈ {0, 1} n with Hamming weight τ and a secret s ∈ S η k+` , the value kcsk 22 is upper bounded by ! m X (m+1)-th τ i-th τ · max ks(ω j )k 22 + r · max ks(ω j )k 22 , 0≤j&lt;2n 0≤j&lt;2n n i=1

where m = bn/τ c, r = n mod τ , and ω j ’s are the primitive 2n-th roots of unity.

Proof. We first rewrite kcsk 22 as:

P

kcsk 22 =

2 2 i |c(ω j )| · ks(ω j )k 2

,

n

P n where s(ω j ) = (s 1 (ω j ), · · · , s k+` (ω j )). We have that j=1 |c(ω j )| 2 = nτ and |c(ω j )| 2 = P n |ω j,1 + · · · + ω j,τ | 2 ≤ τ 2 . We can bound j=1 |c(ω j )| 2 · ks(ω j )k 22 by rearranging the order. Let m = bn/τ c and r = n mod τ . Then m is the maximum number of |c(ω j )| 2 ’s that can be τ 2 . By sorting ks(ω j )k 2 in a decreasing order,

ks(ω σ(1) )k 2 ≥ ks(ω σ(2) )k 2 ≥ · · · ≥ ks(ω σ(n) )k 2 ,

where σ is a permutation for the indices, we have

n X

m X

|c(ω j )| 2 · ks(ω j )k 22 ≤ |c(ω σ(j) )| 2 · ks(ω σ(j) )k 22 +

j=1

j=1

n X

|c(ω σ(j) )| 2 · ks(ω σ(m+1) )k 22 .

j=m+1

<!-- PDF_PAGE: 11 -->

## PDF page 11

Team HAETAE

35

Then it reaches the maximum when the m largest ks(ω j )k 22 ’s are multiplied with τ 2 ’s, i.e.,

n X

m X

|c(ω j )| 2 · ks(ω j )k 22 ≤ τ 2 · ks(ω σ(j) )k 22 +

j=1

j=1

m X

= τ 2 ·

j=1

This concludes the proof.

### 3.2 Sampling in a Discrete Hyperball

n X

|c(ω j )| 2 − mτ 2 · ks(ω σ(m+1) )k 22

j=1

ks(ω σ(j) )k 22 + r · τ · ks(ω σ(m+1) )k 22 .

In order to generate a hyperball uniform sample y, we apply a rounding-and-reject strategy to the discretization of the continuous hyperball uniform sampling from Figure 1, which allows to generate rightly distributed samples. Our approach in sampling is to avoid the use of floating point arithmetic for two reasons: First, many microarchitectures do not provide floating-point units and even if so, the execution time of floating-point instructions may be data-dependent and thus unsuitable [AKM + 15] for a constant-time implementation. Floating-point computation would also prohibit a masked implementation, that is protected against power side-channel attacks, because known masking techniques are only applicable to integers. And second, the required precision is higher than achievable even in IEEE double. In order to do so, we replace the continuous Gaussian sampler from Lemma 1 and instead use discrete Gaussian distributions, as we know that they approximate well continuous Gaussian distribution for large standard deviation.

Discretizing the Output. Once we obtain an “hyperball” sample, we choose to round it. Then, if the resulting sample lies too close to the border of the hyperball, we reject it. This ensures that for any possible sample, they have the same amount of pre-rounding predecessors. This also decreases the precision but the output is now discrete in a hyperball with a somewhat-smaller radius. We simply increase the starting radius to compensate.

y ← U (B (1/N )R,m (B)):

√

1: y ← U (B R,m (N B + mn/2)) 2: if kbyek 2 ≤ N B then

3: return bye/N 4: else, restart

. continuous sampling in Figure 1

. y ∈ B (1/N )R,m (B) ⊂ (1/N )R m

Figure 3: Discrete hyperball uniform sampling

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 11]

We study in the following lemma the rejection probability of this step.

Lemma 4. Let n be the degree of R, M 0 ≥ 1, B, m, N &gt; 0. At each iteration, the algorithm from Figure 3 succeeds with probability ≥ 1/M 0 and the distribution of the output is U (B (1/N )R,m (B)) if we set √ 1/(mn) mn M 0 +1 N ≥ · 1/(mn) . 2B M 0 − 1

The proof of this lemma can be found in Appendix C.

### 3.3 Challenge Sampling

Challenges in HAETAE are polynomials c ∈ R with binary coefficients and exactly τ of them are nonzero. As simply hashing the message and the commitment only yields a

<!-- PDF_PAGE: 12 -->

## PDF page 12

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

36

SampleBinaryChallenge τ (ρ) // for HAETAE-120 or HAETAE-180 1: Initialize c = c 0 c 1 . . . c 255 = 00 . . . 0 2: for i = 256 − τ to 255 do 3: j ←- {0, . . . , i} 4: c i = c j 5: c j = 1 6: Return c // for HAETAE-260 1: Initialize c = c 0 c 1 . . . c 255 = H(ρ) 2: if wt(c) &gt; 128 then 3: c = c ⊗ 11 · · · 1 4: else if wt(c) = 128 then 5: c = c ⊗ c 0 c 0 · · · c 0 6: Return c

Figure 4: Challenge sampling algorithm

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 12]

binary string ρ, we now explain how to format it to get such a challenge. Since n = 256 across all three parameter sets, the challenge space has size nτ exceeding the required entropy 2 192 and 2 225 for HAETAE-120 and HAETAE-180, respectively. To sample such challenges we rely on the (binary version of) SampleInBall algorithm from Dilithium, which we specify in the first half of Figure 4. For HAETAE-260, however, we require 255 bits of entropy for the challenge space, which cannot be reached with the fixed Hamming weights for n = 256. To achieve it, we replace the challenge space by a set containing exactly half of the bitstrings of length 256. Specifically, we choose a set containing all elements of Hamming weight strictly less than 128 and half of the elements of Hamming weight 128, using the following algorithm. Given a 256-bits hash with Hamming weight w, do the following. If w &lt; 128, we do nothing, and if w &gt; 128, we flip all the bits. If w = 128, we decide whether to flip or not, depending on the first bit. Exactly half of all binary polynomials are reachable this way, which means that the challenge set has size 2 255 as desired. The algorithm is specified in the second half of Figure 4. As a side note, this means that the hash function with which we instantiate the Fiat- Shamir transform is the composition of these two steps, hashing and formatting. Looking ahead, this corresponds to steps 6 and 7 of Figure 8. Contrary to Dilithium, we do not stray away from the Fiat-Shamir transform and include the challenge c in the signature as it is no bigger than ρ when encoded.

Bimodal Hyperball Rejection Sampling

3.4

Recently, Devevey et al. [DFPS22] conducted a study of rejection sampling in the context of lattice-based Fiat-Shamir with Aborts signatures. They observe that (continuous) uniform distributions over hyperballs can be used to obtain compact signatures, with a relatively simple rejection procedure. To make masking easier, HAETAE uses (discretized) uniform distributions over hyperballs, in the bimodal context. The proof of the following lemma is available in Appendix C.

Lemma 5 (Bimodal Hyperball Rejection Sampling). Let n be the degree of R, c &gt; 1,

<!-- PDF_PAGE: 13 -->

## PDF page 13

Team HAETAE

√

r, t, m &gt; 0, and B ≥

37

B 02 + t 2 . Define M = 2(B/B 0 ) mn and set √ 1 1 mn c 1/(mn) N ≥ 1/(mn) + . B 0 B c − 1 2

Let v ∈ R m ∩ B (1/N )R,m (t). Let p : R m → {0, 1/2, 1} be defined as follows  if kzk ≥ B 0 ,   0 p(z) = 1/2 else if kz − vk &lt; B ∧ kz + vk &lt; B,   1 otherwise.

Then there exists M 0 ≤ cM such that the output distributions of the two algorithms from Figure 6 are identical.

−v

v

Figure 5: The HAETAE eyes

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 13]

Figure 5 illustrates (the continuous version) of the rejection sampling that we consider. The black empty circles have radii equal to B and the green circle has radius B 0 . We sample a vector z uniformly inside one of the black circles (with probability 1/2 for each) and keep z with p(z) = 1/2 if z lies in the blue zone, with probability p(z) = 1 if it lies in the green zone, and with probability p(z) = 0 everywhere else. We now have all necessary ingredients in Figures 1, 3, 5, and 6 to make sure the resulting distribution of z is indeed uniform over the discretized hyperball. Thanks to Lemma 4 and Lemma 5, we already know the level of precision required for y to maintain the provable security of HAETAE.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 13]

### 3.5 High and Low Bits

Recall that a HAETAE signature is principally a vector z, whose lower part is replaced with a (smaller) hint. HAETAE makes use of two different high and low bits decompositions: one helps encoding a signature while the other is used when computing a hint. Following [ETWY22], the first is helpful in the sense that if we correctly choose the number of low bits, they will be distributed almost uniformly and can then be excluded from the encoding step. The high bits on the other hand, will then follow a distribution with a very small variance and we apply the rANS encoding on them only, making it much more efficient as the size of the alphabet greatly shrunk.

A(v) : B : 1: y ← U (B (1/N )R,m (B)) 1: z ← U (B (1/N )R,m (B 0 )) 2: b ← U ({0, 1}) 2: return z with probability 1/M 0 , else ⊥ b 3: z ← y + (−1) v 4: return z with probability p(z), else ⊥

Figure 6: Bimodal hyperball rejection sampling

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 13]

<!-- PDF_PAGE: 14 -->

## PDF page 14

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

38

The second decomposition allows to reduce the alphabet size of the resulting hint, and thus to reduce the size of its encoding. We use the following base method of decomposing an element in high and low bits. We first recall the Euclidean division with a centered remainder.

Lemma 6. Let a ≥ 0 and b &gt; 0. It holds that a + b/2 a = · b + (a mod ± b), b

and this writing as a = bq + r with r ∈ [−b/2, b/2) is unique.

We define our decomposition for compressing the upper part of the signature.

Definition 7 (High and low bits). Let r ∈ Z and α be a power of two integer. Define r 1 = b(r + α/2)/αc and r 0 = r mod ± α. Finally, define the tuple:

(LowBits(r, α), HighBits(r, α)) = (r 0 , r 1 ).

We extend these definitions to vectors by applying them component-wise. We state that this decomposition lets us recover the original element and bound the components of the decomposition in Lemma 7. The proof is available in Appendix C.

Lemma 7. Let α be a power of two. Let q &gt; 2 be a prime with α|2(q − 1) and r ∈ Z. Then it holds that

r = α · HighBits(r, α) + LowBits(r, α),

LowBits(r, α) ∈ [−α/2, α/2),

r ∈ [0, 2q − 1] =⇒ HighBits(r, α) ∈ [0, (2q − 1)/α] .

We define HighBits z1 (r) = HighBits(r, 256) and LowBits z1 (r) = LowBits(r, 256).

### 3.5.1 High and Low Bits for h

In order to produce the hint that we send instead of the lower part of z, we could use the previous bit decomposition. However, as noted in [DKL + 18, Appendix B] in a preliminary version, a slight modification allows to further reduce the entropy of the hint. The idea is to pack the high bits in the range [0, 2(q − 1)/α h ). This is possible if we use the range [−α h /2 − 2, 0) to represent the integers that are close to 2q − 1.

Definition 8 (High and low bits for h). Let r ∈ Z. Let q be a prime and α h |2(q − 1) be a power of two. Let m = 2(q − 1)/α h , r 1 = HighBits(r mod + 2q, α h ), and r 0 = LowBits(r mod + 2q, α h ). If r 1 = m, let (r 0 0 , r 1 0 ) = (r 0 − 2, 0). Else, (r 0 0 , r 1 0 ) = (r 0 , r 1 ). We define:

(LowBits h (r), HighBits h (r)) = (r 0 0 , r 1 0 ).

As before, we extend these definitions to vectors by applying them component-wise. We state that this decomposition lets us recover the original element and bound the decomposition components.

Lemma 8. Let r ∈ Z. Let q be a prime, α h |2(q − 1) be a power of two and define m = 2(q − 1)/α h . It holds that

r = α h · HighBits h (r) + LowBits h (r)

LowBits (r) ∈ [−α/2 − 2, α/2),

h

HighBits h (r) ∈ [0, m − 1] .

The proof of Lemma 8 is available in Appendix C.

mod 2q,

<!-- PDF_PAGE: 15 -->

## PDF page 15

Team HAETAE

4 The HAETAE Signature Scheme

39

In this section, we describe three different versions of HAETAE. As a warm-up, we give an uncompressed, un-truncated version of HAETAE, implementing the Fiat-Shamir with aborts paradigm in the bimodal hyperball-uniform setting. We then give the full description of optimized and deterministic HAETAE as we implemented it. Finally, we discuss the parts of the signing algorithm which can be pre-computed.

### 4.1 Uncompressed Description

As a first approach, we give a high-level, uncompressed, description of our signature scheme in Figure 7. In all of the following sections, we let j = (1, 0, . . . , 0) ∈ R k , as well as k, ` be two dimensions, N &gt; 0 the fix-point precision and τ &gt; 0 the challenge min-entropy parameter. The parameters B, B 0 , and B 00 refer to the radii of hyperballs. Let q be an odd prime and α h |2(q − 1) is a power of two. We recall the key rejection function based on Lemma 3: m X (m+1)-th i-th N : s 7→ τ · max ks(ω j )k 22 + r · max ks(ω j )k 22 .

j

i=1

j

√ With the parameter γ, we bound N (s) ≤ γ 2 n, which ensures that kcsk 2 ≤ γ τ for all c ∈ R 2 satisfying wt(c) ≤ τ . The key generation algorithm is a simplified version from Section 3.1, which removes the verification key truncation, for conceptual simplicity.

KeyGen(1 λ ):

1: (A gen ) ← R q

k×(`−1)

and (s gen , e gen ) ← S η `−1 × S η k 2: b = A gen · s gen + e gen ∈ R k q 3: A = (−2b + qj| 2A gen | 2Id k ) mod 2q 4: s = (1, s gen , e gen ) 5: if N (s) &gt; γ 2 n then restart 6: return sk = (A, s), vk = A

Sign(sk, M ): 1: y ← U (B (1/N )R,(k+`) (B)) 2: w ← Abye 3: c = H(w, M ) ∈ R 2 4: z = (z 1 , z 2 ) = y + (−1) b cs for b ← U ({0, 1}) 5: if kzk 2 ≥ B 0 then restart 6: else if k2z − yk 2 &lt; B then restart with probability 1/2 7: return σ = (bze, c)

Verify(vk, M, σ = (z, c)): 1: w̃ = Az − qcj mod 2q

2: return (c = H( w̃, M )) ∧

√

n(k+`) 2

kzk &lt; B +

Figure 7: Uncompressed description of HAETAE .

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 15]

### 4.2 Specification of HAETAE

We now give the full description of the signature scheme HAETAE in Figure 8 with the following building blocks:

<!-- PDF_PAGE: 16 -->

## PDF page 16

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

40

• Hash function H gen for generating the seeds and hashing the messages,

• Hash function H for signing, returning a seed ρ for sampling a challenge,

• Extendable output function expandA for deriving a gen and A gen from seed A ,

• Extendable output function expandS for deriving (s gen , e gen ) ∈ S η `−1 × S η k from seed sk and counter sk ,

• Extendable output function expandYbb for deriving y, b and b 0 from seed ybb and counter,

The above building blocks can be implemented with symmetric primitives. Note that at Step 6 of the Verify algorithm, the division by 2 is well-defined as the operand is even.

### 4.3 Theoretical Analysis

In this section, we prove the theoretical correctness and security of HAETAE.

### 4.3.1 Correctness and Runtime

Correctness. Before showing the correctness of the HAETAE scheme, we prove the following intermediary result.

Lemma 9. We borrow the notations from Figure 8. If we run Verify(vk, M, σ) on the signature σ returned by Sign(sk, M ) for an arbitrary message M and an arbitrary key-pair (sk, vk) returned by KeyGen(1 λ ), then the following relations hold:

1) w 1 = HighBits h (w),

2) w 0 j = LSB(by 0 e) · j = LSB(w) = LSB(w − 2bz 2 e),

3) 2bz 2 e − 2z̃ 2 = LowBits h (w) − LSB(w) assuming B 0 + α h /4 + 1 ≤ B 00 &lt; q/2.

Proof. Let m = 2(q − 1)/α h . Let us prove the first statement. By definition of h, it holds that w 1 = HighBits h (w) mod m. However, the latter part of the equality already lies in [0, m − 1] by Lemma 8. The first part lies in the same range as we reduce mod + m. Hence, the equality stands over Z too. We move on to the second statement. By considering only the first component of z = y + (−1) b cs, we obtain, modulo 2:

z̃ 0 = bz 0 e = by 0 e + (−1) b c = by 0 e + c.

Moreover, considering everywhere a 2 appears in the definition of A, we obtain that

w = A 1 bz 1 e − qcj = (bz 0 e − c)j mod 2.

For the last statement, let us use the two preceding results. In particular, we note

w 1 · α h + w 0 j = w − LowBits h (w) + LSB(w).

We note that the last two elements have same parity, as the former one has the same parity as LowBits(w, α h ). By Lemma 8 their sum has infinite norm ≤ α h /2 + 2. Hence from its definition, it holds that

2z̃ 2 = 2bz 2 e − LowBits h (w) + LSB(w) mod ± 2q.

Finally, this holds over the integers as the right-hand side has infinite norm at most 2B 0 + α h /2 + 2 &lt; q.

<!-- PDF_PAGE: 17 -->

## PDF page 17

Team HAETAE

KeyGen(1 λ ):

41

. KeyGen for d = 1

1: seed ← {0, 1} ρ 0 2: (seed A , seed sk , K) = H gen (seed) 3: (a gen | A gen ) := expandA(seed A ) ∈ R k×` q 4: counter sk = 0 5: (s gen , e gen ) := expandS(seed sk , counter sk ) 6: b = a gen + A gen · s gen + e gen ∈ R kq 7: (b 0 , b 1 ) = (LowBits vk (b), HighBits vk (b)) 8: A = (2(a gen − 2b 1 ) + qj| 2A gen | 2Id k ) mod 2q 9: s = (1, s gen , e gen − b 0 ) 10: if N (s) &gt; γ 2 n then counter sk ++ and Go to 5

11: return sk = (s, K), vk = (seed A , b 1 )

Sign(sk, M ): 1: µ = H gen (seed A , b 1 , M ) 2: seed ybb = H gen (K, µ) 3: counter = 0 4: (y, b, b 0 ) := expandYbb(seed ybb , counter) 5: w ← Abye h 6: ρ = H(HighBits (w), LSB(by 0 e), µ) 7: c = SampleBinaryChallenge τ (ρ) 8: z = (z 1 , z 2 ) = y + (−1) b cs h h + 2(q−1) 9: h = HighBits (w) − HighBits (w − 2bz 2 e) mod α h 10: if kzk 2 ≥ B 0 then 11: counter++ and Go to 4 12: else if k2z − yk 2 &lt; B ∧ b 0 = 0 then 13: counter++ and Go to 4 14: else 15: x = Encode(HighBits z1 (bz 1 e)) 16: v = LowBits z1 (bz 1 e) 17: return σ = (x, v, Encode(h), c)

Verify(vk, M, σ = (x, v, h, c)):

1: z̃ 1 = Decode(x) · 256 + v and h̃ = Decode(h) 2: (a gen | A gen ) = expandA(seed A )

3: A 1 = (2(a gen − 2b 1 ) + qj| 2A gen ) mod 2q

4: w 1 = h̃ + HighBits (A 1 z̃ 1 − qcj) mod

h

+ 2(q−1) α h

5: w 0 = LSB(z̃ 0 − c) ± 6: z̃ 2 = (w 1 · α h + w 0 j − (A 1 z̃ 1 − qcj)) /2 mod q 7: z̃ = (z̃ 1 , z̃ 2 )

8: µ̃ = H gen (seed A , b 1 , M ) 9: ρ̃ = H(w 1 , w 0 , µ̃) 10: return (c = SampleBinaryChallenge τ (ρ̃)) ∧ (kz̃k &lt; B 00 )

Figure 8: Full description of deterministic HAETAE. The KeyGen algorithm is slightly different for d = 0 (HAETAE-260), which do not truncate b. See Section 3.1.1 for details.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 17]

p √ Theorem 2 (Completeness). Assume that B 00 = B 0 + n(k + `)/2+ nk·(α h /4+1) &lt; q/2. Then the signature schemes of Figure 8 is complete, i.e., for every message M and every key-pair (sk, vk) returned by KeyGen(1 λ ), we have:

Verify(vk, M, Sign(sk, M )) = 1.

<!-- PDF_PAGE: 18 -->

## PDF page 18

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

42

Proof. We use the notations of the algorithms. The first and second equations from Lemma 9 state that ρ = ρ̃ and thus

c = SampleBinaryChallenge τ (ρ̃).

On the other hand, we use the last equation from the same lemma to bound the size of z̃. We have:

kz̃k ≤ kzk + kz − bzek + kbze − z̃k p ≤ B 0 + n(k + `) · kz − bzek ∞ + kbz 2 e − z̃ 2 k p n(k + `) √ 0 ≤ B + + nk · kLowBits h (w)k ∞ 2 p α n(k + `) √ h 0 ≤ B + + nk · +1 . 2 4

The definition of B 00 implies that the scheme is correct.

Runtime. A non-trivial task is analyzing the runtime of Fiat-Shamir with aborts schemes. As shown in [DFPS23, Section 6.1], degenerate cases exist where the signing algorithm does not terminate. In particular, it is impossible, even in the ROM, to show that the generic signing algorithm has polynomial expected runtime. However, in √ the case of HAETAE, all starting points y lying in the Euclidean ball of radius B 0 − γ τ have probability at least 1/2 of being accepted in the end, whatever shift ±sc is added, whatever instance of the hash function H is chosen. This gives rise to the following two points.

• With M 0 defined as in Lemma 5, the probability of doing more than i iterations is bounded from above by (1 − 1/M 0 ) i + 2 −α M 03 , where α is the commitment min-entropy.

• The signing algorithm has a finite expected runtime.

These are insufficient to conclude that the number of iterations is M 0 on average, but this is nonetheless what happens for our choice of parameters.

### 4.3.2 Theoretical Security

Compress(z, c): Decompress(A, (x, v, h), c): 1: if z =⊥ then 1: if (x, v, h) = (⊥, ⊥, ⊥) then 2: return (⊥, ⊥, ⊥) 2: return ⊥ 3: z = (z 1 , z 2 ) = y + (−1) b cs 3: z̃ 1 = Decode(x) · 256 + v h 4: h = HighBits (w) 4: h̃ = Decode(h) h + 2(q−1) 5: A = (A | 2I) mod 2q 1 −HighBits (w − 2bz 2 e) mod α h h z1 6: w 1 = HighBits (A 1 z̃ 1 − qcj) 5: x = Encode(HighBits (bz 1 e)) 2(q−1) + z1 + h̃ mod 6: v = LowBits (bz 1 e) α h 7: w 0 = LSB(z̃ 0 − c) 7: return (x, v, Encode(h)) 8: w̃ = A 1 z̃ 1 − qcj ± 9: z̃ 2 = (w 1 · α h + w 0 j − w̃) /2 mod q 10: return z̃ = (z̃ 1 , z̃ 2 )

Figure 9: Compression and decompression algorithms.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 18]

<!-- PDF_PAGE: 19 -->

## PDF page 19

Team HAETAE

43

We analyze the security of HAETAE by following standard arguments and proof techniques. We start by detailing the underlying canonical identification scheme that makes up HAETAE and give their properties in Lemma 10. We then show that HAETAE is UF-NMA secure in Lemma 11. Finally, we put everything together and give the security bound in Theorem 3 based on the reduction from [BBD + 23]. Reminders on canonical identification schemes and the Fiat-Shamir with aborts transform can be found in Appendix F. In Figure 10, we first describe in Figure 10a an “uncompressed” version of the identification scheme, as well as the HAETAE canonical identfication scheme in Figure 10b. The latter uses the Compress and Decompress functions, as described in Figure 9. We omit the instance generator for both CID, as it is exactly the key generation algorithm from HAETAE, except that do not do truncation for simplicity. Adding it can be done by noting that a gen gives uniform low bits that would otherwise be missing.

P (A, s) y ← U (B (1/N )R,(k+`) (B)) w = Abye mod 2q

w

−−−−−→ c ←−−−−

b ← U ({0, 1}) z = y + (−1) b cs If p(z), restart

bze

Else

−−−−−→

V (A)

c ← U (C)

Acc. if kbzek ≤ B 00 and Az − qcj = w mod 2q

(a) Uncompressed HAETAE

P (A, s) y ← U (B (1/N )R,(k+`) (B)) w = Abye mod 2q w 1 = HighBits h (w) w 0 = LSB(by 0 e)

w 0 ,w 1

−−−−−→ c ←−−−−

b ← U ({0, 1}) z = y + (−1) b cs If p(z), restart Else σ = Compress(bze, c)

σ

−−−−→

V (A)

c ← U (C)

z̃ = Decompress(A, σ, c) Acc. if kz̃k ≤ B 00 and Az̃ − qcj = w 1 α h + w 0 j mod 2q

(b) Compressed HAETAE

Figure 10: Underlying canonical identification schemes.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 19]

We sum up the properties of the CID from Figure 10b.

Lemma 10. The HAETAE canonical identification scheme from Figure 10b satisfies the following properties.

Commitment Min-entropy. The commitment (w 0 , w 1 ) has min-entropy ≥ n.

paHVZK. Assuming B 2 ≥ B 02 + γ 2 τ , the HAETAE CID satisfies the paHVZK property with the simulator described in Figure 11.

Computational Unique Response. Let A be an adversary against the CUR property of the scheme. There exist two adversaries B and B 0 with roughly the same runtime

<!-- PDF_PAGE: 20 -->

## PDF page 20

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

44

Sim 6⊥ (vk, c) :

1: z ← U (B (1/N )R,k+` (B 0 )) 2: w ← Abze − qcj 3: return (w, c, z)

Figure 11: Uncompressed HAETAE simulator.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 20]

such that:

MLWE MSIS 0 Adv CUR HAETAE (A) ≤ Adv n,q,k,`−1,η (B) + Adv n,q,k,`,2B 00 (B ).

Proof. Let us prove each point. Commitment Min-entropy. Recall that w 0 = LSB(by 0 e) is a binary polynomial of degree ≤ n. As the coefficients of y 0 are large and distributed following the distribution of a subset of a uniform-hyperball, we expect the coefficients of w 0 to be roughly uniform, hence the lower bound on the commitment min-entropy. paHVZK. We first prove that the CID from Figure 10a satisfies paHVZK. Consider the simulator described in Figure 11. The distribution of real non-aborting transcripts and the output distribution of Sim 6⊥ (vk, c) are identical under the condition on the radii. Indeed, by conditioning the distribution of the output of algorithms A and B from Lemma 5 on not being ⊥, the conditional (on A and c) distributions of z in the two cases are identical, and we note that (w, c, z) is a deterministic function of (A, c, z). Finally, given an uncompressed transcript (w, c, z) for the Figure 10a CID, we note that ((HighBits h (w), LSB(w 0 )), c, Compress(z, c)) is a valid transcript for the HAETAE CID. Indeed, note that w 0 = by 0 e mod 2 by definition of A. Moreover, applying this deterministic transform turns the distribution of real transcripts for the uncompressed CID to the distribution of real transcripts for the compressed CID. By an immediate reduction, the HAETAE CID also satisfies paHVZK. CUR. Given ((w 1 , w 0 ), c, σ, σ 0 ) such that Az − qcj = w 1 α h + w 0 j = Az 0 − qcj mod 2q, we get A(z − z 0 ) = 0 mod 2q, which we can reduce modq:

(−b|A gen |Id k )(z − z 0 ) = 0 mod q.

We prove that z 6 = z 0 mod q. Let z = (z 1 , z 1 ) and z 0 = (z 0 1 , z 0 2 ). Let σ = (x, v, h) and σ 0 = (x 0 , v 0 , h). If z 1 = z 0 1 then x = x 0 and v = v 0 due to the encoding being unique. This means that h 6 = h 0 , which in turn will give two different values for z 2 and z 0 2 as the other values composing z 2 and z 0 2 are identical. However, (A gen , b) is a MLWE n,q,k,`−1,η instance instead of being uniform. Both adversaries B and B 0 can run A by simulating a random oracle in the case of B and by forwarding the queries to its own oraclein the case of B 0 . Then, if A was successful, adversary B outputs “MLWE” while B 0 computes the MSIS solution as described above, and if A is unsuccessful, adversary B outputs “unif” while B 0 aborts. By the triangular inequality, we get the desired inequality.

We reduce the UF-NMA security of the signature scheme to the BimodalSelfTargetMSIS problem.

Lemma 11 (UF-NMA security). Let A be an adversary against the UF-NMA security of HAETAE. There exist two adversaries B and B 0 with essentially the same runtime as A such that:

BimodalSelfTargetMSIS - NMA MLWE Adv UF (B 0 ). HAETAE (A) ≤ Adv n,q,k,`−1,η (B) + Adv H,n,q,k,`,B 00

<!-- PDF_PAGE: 21 -->

## PDF page 21

Team HAETAE

45

Proof. Let us first describe B 0 . On input the public matrix A, it calls A on it. The adversary B 0 defines the random oracle H 0 : (w 1 , w 0 , µ) 7→ H(w 1 α h + w 0 j mod 2q, µ), to take care of the compression that does not appear in the BimodalSelfTargetMSIS problem. This can be simulated by B by applying the right function on the queries of A and forwarding it to its own random oracle H. When A outputs a valid forgery σ ∗ = ((x, v, h), c) for some message µ ∗ , ad- versary B 0 runs Decompress(A, (x, v, h), c) to get a vector z such that kzk ≤ B 00 and H 0 (HighBits h (w ∗ ), LSB(w 0 ∗ ), µ) = c, where we let w ∗ = Az − qcj mod 2q. By construction w ∗ = HighBits h (w ∗ )α h + LSB(w 0 ∗ )j mod 2q, meaning that c = H(w ∗ , µ). Then (z, c, µ ∗ ) is exactly a solution to the BimodalSelfTargetMSIS H,n,q,k,`,B 00 problem. Note that A is called on a “lossy” instance of HAETAE, where the verification key b does not have a signing key associated and is actually uniform. This difference in setting exactly corresponds to the MLWE n,q,k,`−1,η problem. As such the design of B is as follows: on input (A gen , b), it puts together the verification key A and calls A on it. It can simulate a random oracle for it, and outputs “MLWE” if A is successful at forging, “unif” otherwise.

We combine the previous results with Theorem 4 to get the following security bound for HAETAE.

Theorem 3. Let A be an adversary against the UF-CMA security of HAETAE making Q s signature queries and Q h hash queries. Let α be the commitment min-entropy of HAETAE. Let B 2 ≥ B 02 + γ 2 τ . There exist two adversaries B and B 0 such that

BimodalSelfTargetMSIS - CMA MLWE Adv UF (B 0 ) HAETAE (A) ≤ Adv n,q,k,`−1,η (B) + Adv H,n,q,k,`,B 00 s s (4.1) Q s 2 −α/2+1 Q s Q s −α/2+1 + Q h + 1 + +2 (Q h + 1) . 1 − β 1 − β 1 − β

If A is an adversary against the sUF-CMA security of HAETAE, then there exist two more adversaries B 00 and B 000 such that the previous bound holds by adding the extra MSIS 00 000 term Adv MLWE n,q,k,`−1,η (B ) + Adv n,q,k,`,2B 00 (B ).

### 4.4 HAETAE with Pre-computation

We observe that in the randomized signing process of HAETAE, many operations do not depend on the message M , and some do not even depend on the signing key. This enables efficient “offline” procedures, i.e., precomputations that speed up the “online” phase. Specifically, there are two levels of offline signing that can be applied to randomized HAETAE:

1. Generic. If neither the message M nor the signing key is chosen in advance, it is still possible to perform hyperball sampling. This removes the most time-consuming operation from the online phase.

2. Designated signing key. Here, only the message M is unknown during offline signing, while the signing key is fixed. This allows us to perform even more pre- computations by using only the verification key, as shown in Figure 12. Most notably, there is no longer a matrix-vector multiplication in the online phase.

We showcase the offline and online parts of the (randomized) version of HAETAE in Figure 12.

<!-- PDF_PAGE: 22 -->

## PDF page 22

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

46

Sign offline (vk): 1: (a gen | A gen ) = expandA(seed A ) 2: A 1 = (2(a gen − 2b 1 ) + qj| 2A gen ) mod 2q 3: List = () 4: for iter in [L] do 5: y ← U (B (1/N )R,(k+`) (B)) 6: w = Abye 7: w 1 = HighBits h (w) 8: List.append(y, w, w 1 , LSB(by 0 e)) 9: return List

Sign online (sk, List, M ): 1: µ = H gen (seed A , b 1 , M ) 2: tuple = (y, w, tuple 3 , tuple 4 ) ← List 3: List.delete(tuple) 4: c = SampleBinaryChallenge τ (H(tuple 3 , tuple 4 , µ)) 5: (b, b 0 ) ← {0, 1} 2 6: z = (z 1 , z 2 ) = y + (−1) b cs h + 2(q−1) 7: h = tuple 3 − HighBits (w − 2bz 2 e) mod α h 0 8: if kzk 2 ≥ B then Go to 2 9: else if k2z − yk 2 &lt; B ∧ b 0 = 0 then Go to 2 10: else 11: x = Encode(HighBits z1 (bz 1 e)) 12: v = LowBits z1 (bz 1 e) 13: return σ = (x, v, Encode(h), c)

Figure 12: Randomized, on/off-line signing.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 22]

### 4.5 Parameter Sets

To choose parameters reaching the desired NIST security levels, we estimated the costs of practical attacks, as in Dilithium, Falcon, and many other NIST-submitted schemes. In particular, our methodology is directly inspired from the one used in Dilithium, and we sum it up in the following. Looking at Equation 4.1, we note that we have highly underestimated the commitment min-entropy of the scheme in Lemma 10 as we ignored its biggest part w 1 , and we choose to ignore terms on the second line as we are confident that they are small enough. We first evaluate the cost of attacks on MLWE, i.e. key-recovery attacks. Second, to evalute the cost of forgery attacks, i.e. attacks on BimodalSelfTargetMSIS, we use the fact that the only known way to solve BimodalSelfTargetMSIS is to solve MSIS. Heuristically, the hash function is not aware of the algebraic structure of its input, and the random oracle assumption that c is uniform and independent from the input is sound. Thus, an adversary has no choice but to choose some w, hash its high and low bits along with some message, and try to compute a short preimage of w − qcj mod 2q. If the adversary succeeds, the preimage is in particular an MSIS n,q,k,`+1, √ B 002 +1 solution for the matrix [w|A]. Finally, we evaluate the cost of MSIS with a bound twice as loose to evaluate the strong unforgeability of the HAETAE scheme. Our cryptanalysis of these problems follows the approach taken in Dilithium. We provide a modification of their security estimation script 1 , where we also updated the cost of quantum attacks following recent works [CL21]. These estimations follow the CoreSVP

1 Available in the submission package.

<!-- PDF_PAGE: 23 -->

## PDF page 23

Team HAETAE

47

Table 4: HAETAE parameters sets. Hardness is measured with the Core-SVP methodology and a refined analysis is given for LWE. The numbers in parenthesis for SIS are for the strong unforgeability property. Security 120 180 260 n Degree of R (2.1) 256 256 256 (k, `) Dimensions of z 2 , z 1 (4.2) (2,4) (3,6) (4,7) q Modulus for MLWE &amp; MSIS (2.3) 64513 64513 64513 η Range of sk coefficients (2.1) 1 1 1 τ Weight of c (3.3) 58 80 128 γ sk rejection parameter (3.1) 48.858 57.707 55.13 Resulting key acceptance rate (3.1) 0.1 0.1 0.1 d Truncated bits of vk (3.1) 1 1 0 M Expected # of repetitions (3.4) 6.0 5.0 6.0 B y radius (3.4) 9846.02 18314.98 22343.66 B 0 Rejection radius (3.4) 9838.99 18307.70 22334.95 B 00 Verify radius (4.2) 12777.52 21906.65 24441.49 α z 1 compression factor (3.5) 256 256 256 α h h compression factor (3.5) 512 512 256 Forgery: SIS Hardness (Core-SVP) BKZ block-size b (GSA) 409 (333) 617 (512) 878 (735) Classical Core-SVP 119 (97) 180 (149) 256 (214) Quantum Core-SVP 105 (85) 158 (131) 225 (188) Key-recovery: LWE Hardness (Core-SVP and refined) BKZ block-size b (GSA) 428 810 988 Classical Core-SVP 125 236 288 Quantum Core-SVP 109 208 253 BKZ block-size b (simulation) 439 834 1019 log 2 Classical Gates 159 270 322 log 2 Classical Memory 99 177 214

approach. In the case of MLWE, we also give refined estimates, computed in a branch 1 of the leaky LWE estimator from [DDGR20]. We propose three different parameter sets with varying security levels, where we prioritize low signature and verification key sizes over faster execution time. The parameter choices are versatile, adaptable and allow size vs. speed trade-offs at consistent security levels. For example at cost of larger signatures, a smaller repetition rate M is possible and thus a faster signing process. This versatility is a notable advantage over Falcon and Mitaka. Like in Dilithium, our modulus q is constant over the parameter sets and allows an optimized NTT implementation shared for all sets. With only 16-bit in size, our modulus also allows storing coefficients memory-efficiently without compression.

5 Implementation Details

In this section, we detail how to efficiently implement HAETAE. However, we leave an extensive specification of implementation aspects to a separate document. The most notable remark from an implementation point of view is that b can be transmitted in NTT domain if no rounding is applied, and most arithmetic is carried out modulo q, and recovering the values modulo 2q is only required for computing the low and high bits. In

1 https://github.com/jdevevey/refined-haetae

<!-- PDF_PAGE: 24 -->

## PDF page 24

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

48

the following, we detail about the hyperball sampler, packing, and the performance of our reference implementation.

### 5.1 Hyperball Sampler

Essentially, the hyperball sampling procedure consists of four steps:

1. Sample n(k + `) + 2 discrete Gaussians with σ = 2 76 , sum up their squares, and drop two samples eventually.

2. Compute √ the inverse of the square root of the sum of squares, multiply the result by B 0 + nm/(2N ).

3. Multiply every sample from Step 1 by the result of Step 2.

4. Check the ` 2 norm of the resulting vector, start from Step 1 if this is bigger than B 0 N .

In the following, we explain how the Gaussian sampling and the approximation of the inverse of the square root can be implemented efficiently. Besides, we choose to generate each of the k + ` polynomials independently, which helps parallelizing the randomness generation for implementations that use vectorization and hardware implementations. Then, for the first two polynomials, we generate one more Gaussian sample each, which is never stored but included in the sum of squared samples.

### 5.1.1 Discrete Gaussian Sampling

As we will lose precision when computing the inverse square root of a Gaussian sample, we require a Gaussian sampler with high fix-point precision. This is achieved by sampling over Z with a large standard deviation and then scaling the resulting sample to our convenience. We use [Ros20, Algorithm 12] to sample from a discrete Gaussian distribution with σ = 2 76 , k = 2 72 . In essence, we start by sampling a discrete Gaussian x with σ = 16 using a Cumulative Distribution Table (CDT) and a uniform y ∈ {0, . . . , 2 72 − 1} and set the Gaussian sample candidate as r = x2 72 + y. Subsequently, this candidate is accepted with probability exp(−y(y + x2 73 )/2 153 ). Fortunately, we achieve a very low rejection rate of less than 5 %. Specifically, the CDT we use has 64 entries and uses a precision of 16 bit. Then, to compute the sample candidate’s square and the input to the exponential, we first compute r 2 and round the result to 76-bit precision, which is accumulated later if the sample is accepted. Subsequently, r 2 − 2 76 x 2 yields the input to the exponential.

Approximating the Exponential. For this, we need to approximate the exponential function e −x by a polynomial f (x) on the closed interval [c − w 2 , c + w 2 ], with center c and width w. We first determine an upper bound for the polynomial order required to approximate e −x , given an upper bound for the absolute error. We obtain f (x) by truncating the expansion of e −x into a series of Chebyshev polynomials of the first kind T n (x) with linearly transformed input, as this is known to yield small absolute approximation errors for a given polynomial order. We find:

∞ X

e −x = −e −c + 2e −c (−1) n I n

w 2

n=0

x−c w/2

x ∈ [c − w 2 , c + w 2 ]

T n

where I n (z) are modified Bessel functions of the first kind, which rapidly converge to zero for growing n. We recall kT n (x)k ≤ 1 for kxk ≤ 1. For intervals [0, w] with not too large

<!-- PDF_PAGE: 25 -->

## PDF page 25

Team HAETAE

49

widths we find 2e −c I m+1 ( w 2 ) to be a useful estimate of the maximum absolute error, when truncating the series at order m &gt; 1. This relation allows us to directly limit m according to the interval to cover and the maximum permissible error. We then determine the polynomial f (x) of at most order m by using the Chebyshev approximation formula, which has been shown to result in a nearly optimal approximation polynomial in the case of the exponential function [Li04]. The number of fraction bits is chosen to match the error. The numerical evaluation is performed in fixed-point arithmetic using the Horner’s scheme and multiplying with shifts to retain significant bits. When shifting right, we round half up, which retains about one additional bit of accuracy when compared to truncation. Barthe et al. [BBE + 19] introduced the GALACTICS toolbox to derive suitable polynomials approximating e −x . They numerically evaluate and modify trial polynomials, minimizing the relative error, until an acceptable level is reached. The polynomials are evaluated using a Horner’s scheme, similar to this work, but rely on truncation. When comparing to polynomials derived using the GALACTICS toolbox, our approximation has a slightly smaller absolute error for intervals of interest in this work, while maintaining the same polynomial order and constant time properties. This holds even when introducing rounding to the GALACTICS evaluation of polynomials. Moreover, our approach is somewhat less heuristic than the GALACTICS method. Practically, as can be seen in Listing 1, the approximation consists of six signed 48-bit multiplications with subsequent rounding (smulh48), several constant shifts with rounding and constant additions.

Listing 1: Fix-point approximation of the exponential function with 48 bit of precision.

1 2 3 4 5 6 7 8 9 10 11 12

static uint64_t approx_exp ( const int64_t result ; result = -0 x 0 0 0 0 B 6 C 6 3 4 0 9 2 5 A E L L ; result = (( smulh48 ( result , x ) + result = (( smulh48 ( result , x ) + result = (( smulh48 ( result , x ) + result = (( smulh48 ( result , x ) + result = (( smulh48 ( result , x ) + result = (( smulh48 ( result , x ) + result = (( smulh48 ( result , x ))) return result ; }

uint64_t x ) {

(1 LL &lt;&lt; 2)) &gt;&gt; 3) + 0 x 0 0 0 0 B 4 B D 4 D F 8 5 2 2 7 L L ; (1 LL &lt;&lt; 2)) &gt;&gt; 3) - 0 x 0 0 0 0 8 8 7 F 7 2 7 4 9 1 E 2 L L ; (1 LL &lt;&lt; 1)) &gt;&gt; 2) + 0 x 0 0 0 0 A A A A 6 4 3 C 7 E 8 D L L ; (1 LL &lt;&lt; 1)) &gt;&gt; 2) - 0 x 0 0 0 0 A A A A A 9 8 1 7 9 E 6 L L ; 1 LL ) &gt;&gt; 1) + 0 x 0 0 0 0 F F F F F F F B 2 E 7 A L L ; 1 LL ) &gt;&gt; 1) - 0 x 0 0 0 0 F F F F F F F F F 8 5 F L L ; + 0 x0000FFFFFFFFFFFCLL ;

Finalization. If the sample is accepted eventually, it is (implicitly) scaled by the factor 2 −76 to obtain a continuous sample from the standard normal distribution. Moreover, we only need to store the upper 64 bits of the sample and round off the rest. In summary, each Gaussian sample candidate requires 72 bit randomness for the lower part of the candidate (y), 16 bit randomness for the CDT sampling, and 48 bit randomness for rejecting the candidate conditionally according to the output of the exponential. This results in a vast randomness demand per hyperball sample, and explains the dominance of hashing in the cycle count performance.

Approximating the Inverse of the Square Root

5.1.2

To turn the vector of standard normal distributed variates into a hyperball sample candidate, we must compute its norm. For this, we accumulate all squared samples and approximate the inverse of the square root of √ the accumulated value. The approximation result is then multiplied by the constant r 0 + nm/(2N ), which yields the scaling factor that is multiplied to each Gaussian sample. For the inverse square root, we deploy Newton’s method, which is a well-known technique for that purpose. However, Newton’s method requires a starting approximation that is, with each iteration, turned into a better approximation. Fortunately,

<!-- PDF_PAGE: 26 -->

## PDF page 26

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

50

Table 5: Symbol mapping and encoding size parameters. Scheme cut h offset h |{S h (n)}| cut z 1 |{S z 1 (n)}| base h HAETAE-120 6 239 13 6 13 7 HAETAE-180 8 235 17 8 17 127 HAETAE-260 16 471 33 9 19 358

base z 1 132 376 501

we know that the sum of nm + 2 independent squared standard normal variables follows a χ 2 distribution with expected √ value nm + 2. Hence, the starting approximation can be fixed and precomputed as 1/ nm + 2. The number of iterations for a targeted precision can be determined experimentally. Therefore, we performed the approximation for the first input values that have negligible probabilities either for the cumulative distribution function of χ 2 (nm + 2) or its survival function, and checked how many iterations are required to still reach reasonable precision.

### 5.2 Signature Packing and Sizes

The last step of the signature generation is to compress and pack the elements of the signature. A packed HAETAE signature consists of the challenge c, the low bits of z 1 (LN coefficients), the high bits of z 1 and h (KN coefficients). Because the distributions of the values in the high bits of z 1 and the coefficients in h are both very dense, we can compress both polynomial vectors with encoding. Figure 13 displays the frequencies for the possible values for both vectors in HAETAE-120. Before compressing the values, we map them to a smaller symbol space and thereby reject the very unlikely values and the corresponding signatures. For h we cut out most of the values in the middle of the range, for HAETAE-120 this reduces the size of the symbol space from 252 to 13.   for 0 ≤ n ≤ cut h   n, ⊥, for cut h &lt; n ≤ cut h + offset h S h (n) =   n − offset h , for cut h + offset h &lt; n

For the high bits of z 1 we tail-cut the distribution left and right of the center at 0, and then shift the remaining values to the non-negative range beginning at 0. For HAETAE-120 this reduces the size of the symbol space from 37 to 13.   for n &lt; −cut z 1   ⊥, n + cut z 1 , for − cut z 1 ≤ n ≤ cut z 1 S z 1 (n) =   ⊥, for cut z 1 &lt; n

The parameters for these mappings are defined in Table 5. At the signature verification, the mapping must be reverted after decoding the compressed symbols. The reason for these mappings is mainly to get significantly smaller precomputation tables for the rANS encoding and decoding. Also, all symbols can now be represented with 8-bits, which simplifies the rANS implementation. Furthermore, for the high bits of z 1 , a mapping to non-negative values is necessary to be able to use rANS encoding. The effect on the resulting signature size is insignificant. The size of the compressed high bits of z 1 and h varies and must be included in the signature, to allow a correct unpacking and decoding. The size of one compressed polynomial vector is often more than 255 bytes, and can thus not be expressed by one byte. Its variance however, is limited, and thus we encode the size the compressed high bits of z 1 and h as positive offset to a fixed base value. This unsigned offset value fits into one byte in most of the cases, if not, the signature gets rejected. The base values can be found in Table 5.

<!-- PDF_PAGE: 27 -->

## PDF page 27

Team HAETAE

0.3

Frequency

0.2

0.1

20 40 60 80

(a) h

Frequency

−15 −10 −5

(b) HB(z 1 )

51

100 120 140 160 180 200 220 240

Coefficient values

0.4

0.3

0.2

0.1

5 10 15

Coefficient values

Figure 13: Distribution of the coefficients of h and HB(z 1 ) in HAETAE-120.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 27]

The final signature is then built as following: The first 32 bytes contain the seed for the challenge polynomial c. Following, we have LN bytes for the low bits of z 1 . The next first byte consists of the offset to the base size for the encoding of the high bits of z 1 and the second byte is the offset for h. Then we have the encoding of the high bits of z 1 and directly afterwards the encoding of h, both with varying sizes, which are indicated beforehand. Lastly, the signature is padded with zero bytes to reach the fixed signature size, if any bytes remain. Signatures that would exceed the fixed limit get rejected. To prevent signature forgeries, during signature unpacking and decoding multiple sanity checks have to be performed: the zero padding must be correct, the decoding must not fail and decode the expected number of coefficients while using exactly the amount of bytes indicated with the offset. Furthermore, rANS decoding must end with the fixed predefined start value to be unique. Our rANS encoding is based on an implementation by Fabian Giesen [Gie14]. To set the fixed signature size as reported in Table 6, we evaluated the distribution empirically and determined a threshold that requires a rejection in less than 0.1% of the cases. Figure 14 displays the raw signature size distribution of 20000 executions (without the size-based rejection sampling). In Table 6 we compare the signature and key sizes of HAETAE, Dilithium, and Falcon. The verification keys in HAETAE are 20% (HAETAE-260) to 25% (HAETAE-120 and HAETAE-180) smaller, than their counterparts in Dilithium. The advantage of the hyperball sampling manifests itself in the signature sizes, HAETAE has 29% to 39% smaller signatures than Dilithium. Less relevant are the secret key sizes, that are almost half the size in

<!-- PDF_PAGE: 28 -->

## PDF page 28

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

52

Frequency

3 2 1

1,462 1,464

(a) HAETAE-120

4 3 2 1

Frequency

2,338 2,340

(b) HAETAE-180

Frequency

4

2

2,940

(c) HAETAE-260

1,466 1,468 1,470 1,472 Signature size (bytes)

1,474 1,476

2,342 2,344 2,346 Signature size (bytes)

2,348 2,350 2,352

2,942 2,944 2,946 Signature size (bytes)

2,948 2,950

Figure 14: Raw signature size distribution over 20000 executions. We set the bound for the size-based rejection to result in a rejection rate of less than 0.1%.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 28]

HAETAE compared to Dilithium. A direct comparison to Falcon for the same claimed security level is only possible for the highest parameter set, Falcon-1024 has a signature of less than half the size compared to HAETAE-260, and its verification key is about 14% smaller.

Performance Reference Implementation

5.3

We developed an unoptimized, portable and constant-time implementation in C for HAETAE and report median and average cycle counts of one thousand executions for each parameter set in Table 7. Due to the key and signature rejection steps, the median and average values for key generation and signing respectively differ clearly, whereas the two values are much closer for the verification.

Table 6: NIST security level, signature and key sizes (bytes) of HAETAE, Dilithium, and Falcon. Scheme Lvl. vk Signature Sum Secret key HAETAE-120 2 992 1,474 2,466 1,376 HAETAE-180 3 1,472 2,349 3,821 2,080 HAETAE-260 5 2,080 2,948 5,028 2,720 Dilithium-2 2 1,312 2,420 3,732 2,528 Dilithium-3 3 1,952 3,293 5,245 4,000 Dilithium-5 5 2,592 4,595 7,187 4,864 Falcon-512 1 897 666 1,563 1,281 Falcon-1024 5 1,792 1,280 3,072 2,305

<!-- PDF_PAGE: 29 -->

## PDF page 29

Team HAETAE

53

Table 7: Reference implementation speeds. Median and average cycle counts of 1000 executions for HAETAE, Dilithium, and Falcon. Cycle counts were obtained on one core of an Intel Core i7-10700k, with TurboBoost and hyperthreading disabled. Scheme KeyGen Sign Verify med 1,403,402 6,039,674 376,486 HAETAE-120 ave 1,827,567 9,458,682 376,631 med 2,368,038 9,161,312 691,652 HAETAE-180 ave 3,448,185 11,611,868 692,014 med 3,101,280 11,444,678 895,098 HAETAE-260 ave 4,088,383 17,229,712 896,622 med 343,222 1,191,218 376,008 Dilithium-2 ave 343,639 1,527,406 376,543 med 630,170 2,061,816 612,538 Dilithium-3 ave 630,607 2,603,237 612,852 med 945,776 2,522,834 987,154 Dilithium-5 ave 949,662 3,080,734 988,250 med 53,778,476 17,332,716 103,056 Falcon-512 ave 60,301,272 17,335,484 103,184 med 154,298,384 38,014,050 224,378 Falcon-1024 ave 178,516,059 38,009,559 224,840

For a fair comparison, we also performed measurements on the same system with identical settings of the reference implementation of Dilithium 1 and the implementation with emulated floating-point operations, and thus also fully portable, of Falcon 2 , as given in Table 7. The performance of the signature verification for HAETAE is very close to Dilithium throughout the parameter sets. HAETAE-180 verification is 13% slower than its counter-part, HAETAE-260 on the other hand, is 9% faster than the respective Dilithium parameter set. For key generation and signature computation, our current implementation of HAETAE is clearly slower than Dilithium. We measure a slowdown of factors three to five. In comparison to Falcon, however, HAETAE has 38-50 times faster key generation and around three times faster signing speed. For the verification, Falcon outperforms both Dilithium and HAETAE by roughly a factor of four. A closer look at the key generation reveals that the complex Fast Fourier Transformation, that is required for the rejection step, is with 53% by far the most expensive operation and a sensible target for optimized implementations. Profiling the signature computation reveals that the slowdown compared to Dilithium is mainly caused by the sampling from a hyperball, where about 80% of the computation time is spent. The hyperball sampling itself is dominated by the generation of randomness, which we derive from the extendable output function SHAKE256 [Dwo15], which is also used in the Dilithium implementation. Almost 60% of the signature computation time is spent in SHAKE256. Based on the profiling and benchmarking of subcomponents, we estimate the performance of a randomized HAETAE implementation with pre-computation. The generic version, which is independent of the key, would already achieve a speedup of a factor five for its online signing, because the expensive hyperball sampling can be done offline. For the pre-computation variant with a designated signing key, additionally, a lot of matrix-vector multiplications and therefore most of the transformations from and to the NTT domain, can be precomputed. We estimate about 12% of the full deterministic signing running time, for the online signing in this case.

1 https://github.com/pq-crystals/dilithium/tree/master/ref

2 https://falcon-sign.info/falcon-round3.zip

<!-- PDF_PAGE: 30 -->

## PDF page 30

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

54

Optimized Implementation for AVX2

6

Advanced Vector Extensions 2 (AVX2) is an extension to the x86 instruction set architecture and available in processors since 2011. It provides Single Instruction Multiple Data (SIMD) operations on 256-bit registers, and thus allows to e.g. do an operation on eight 32-bit values in parallel. In this section we explain, how to exploit this parallelization. The three major components, that significantly determine the computation time of HAETAE are Keccak, the NTT and the hyperball sampling. For the first two components we can fall back to existing optimized code. For the NTT in particular, we can reuse the implementation in Dilithium with only slight adaptions with regard to constants. In the following we demonstrate how to implement the third component, the hyperball sampling efficiently using AVX2 instructions.

### 6.1 Vectorized Hyperball Sampling

After the parallel generation of the randomness, generally, we have two options to parallelize the hyperball sampling. First, we can sample four different polynomials in parallel, and second, we can generate the Gaussian samples within a polynomial in parallel, since they are generated independently. We opt for the first approach. As the sampling process is relatively complex, we cannot load input vectors, generate samples from them, and eventually store the samples. Instead, we pass several times over the internal memory state, dividing the procedure into seven separate steps:

1. parsing of the input randomness: separating the three parts for each sample candidate into separate memory locations such that later steps can process them quickly,

2. CDT sampling,

3. constructing the sample candidate, its square, and the input to the exponential approximation,

4. approximate the exponential,

5. generate masks which candidates to reject,

6. accumulate the squares of the non-rejected samples, and

7. storing only the accepted samples into the correct final memory positions.

In the following, we detail Steps 2, 3, and 4.

### 6.1.1 Parallel CDT Sampling

Although we perform 16-bit CDT sampling, we cannot use the 16-fold parallel vpcmpgtw comparison, since it is a signed comparison, and use vpcmpgtd instead, which operates on eight signed 32-bit integers. As we want to sample four samples in parallel, we store the CDT and the input randomness redundantly, such that we can perform the comparison with all 64 entries with 32 comparisons. However, since AVX2 only offers 16 vector registers, we have to perform this comparison in three chunks. vpcmpgtd c, a, b writes -1 to c if the respective vector element in a is in fact greater than its counterpart in b, and else 0. Thus, we can use vpaddd to accumulate these results, but they will be negative. For the final chunk, we use vpsrlq to line up the two intermediate results, then add them and negate them.

<!-- PDF_PAGE: 31 -->

## PDF page 31

Team HAETAE

### 6.1.2 Multi-precision Squaring

55

Since the sample candidate is 72 bits long and AVX2 only supports 32-bit multiplication, we perform vectorized multi-precision arithmetic. Therefore, we split the candidate into its low 32 bits, the middle 16 bits, and the upper 31 bits. For the schoolbook multiplication, we perform the six partial multiplications with vpmuludq consecutively, such that they can be executed pipelined and in parallel. The subsequent recombination and rounding can be performed with a sequence of 16 instructions of shifts (vpsrlq, vpsllq), additions (vpaddq), and ANDs (vpand).

### 6.1.3 Vectorized Approximation of the Exponential

The exponential approximation as explained in Section 5.1 consists of six signed 48-bit multiplications, which is not supported natively by AVX2. Consequently, we implement this operation with a vectorized multi-precision approach. More specifically, we know that the first operand of this multiplication is signed, and the second is not. Thus, splitting the second operand into a low and a high half is trivial, but for the signed operand, this requires a slightly more sophisticated approach: Here, the upper half is obtained by an arithmetic right-shift by 24. By shifting this result left again by 24 (shifting in zeros), and subtracting the result from the original value, we obtain the lower half. Since AVX2 does not offer a signed right shift over 64-bit entries, we generate a mask of sign bits and simulate a signed right shift by performing a bitwise OR. Unfortunately, we require this operation three times during a single signed multiplication operation. Notably, AVX512 offers a signed right shift, which will speed up this operation considerably. Eventually, we perform a vectorized signed 48-bit multiplication using 32 instructions, out of which 17 are used for the emulation of a signed right shift. Moreover, we use seven variable and three constant vector registers (out of which one is the second input, cf. Listing 1), which leaves six registers for other constants. Apart from the multiplication, we only make use of addition and shifts (vpaddq, vpsrlq).

### 6.2 Performance and Comparison AVX2

The impact of the parallelized Keccak can be observed by looking at the cycle costs for unpacking the matrix A, which is between five to seven times faster compared to the reference implementation. For e.g. HAETAE-120, the costs went down from around 132k cycles to 24k cycles. The picture is similar for the hyperball sampling, where we measure a speed-up of factor six to eight. The cycle counts for one function call in HAETAE-120 are around 1640k in the reference and 270k in the optimized implementation. The highly optimized NTT taken from Dilithium, is almost 19 times faster than the one in our portable reference code. Table 8 provides cycle numbers for the AVX2 optimized implementations of HAETAE, Dilithium 1 and Falcon 2 . Compared to our reference implementation, the signature generation is around five times faster in the optimized implementation. For the signature verification we observe an acceleration of around three to four. The comparison with Dilithium does not change distinctly with respect to the reference implementations, except for the key generation, where Dilithium experiences a much greater acceleration and is about ten times faster. Signature generation is about six times faster with Dilithium and the speed differences in the verification are up to 24% with the optimized implementations. Falcon on the other hand is considerably faster at the

1 https://github.com/pq-crystals/dilithium/tree/master/avx2

2 https://falcon-sign.info/falcon-round3.zip

<!-- PDF_PAGE: 32 -->

## PDF page 32

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

56

Table 8: AVX2 optimized implementation speeds. Median and average cycle counts of 1000 executions for HAETAE, Dilithium, and Falcon. Cycle counts were obtained on one core of an Intel Core i7-10700k, with TurboBoost and hyperthreading disabled. Scheme KeyGen Sign Verify med 882,350 1,323,118 115,638 HAETAE-120 ave 1,185,881 1,943,274 115,690 med 1,654,464 1,844,610 183,920 HAETAE-180 ave 2,242,520 2,299,298 184,003 med 2,199,678 2,069,734 223,852 HAETAE-260 ave 2,935,538 3,013,524 223,976 med 87,020 200,242 92,148 Dilithium-2 ave 86,937 252,905 92,190 med 146,560 334,898 148,810 Dilithium-3 ave 146,688 402,012 148,883 med 233,976 415,228 232,146 Dilithium-5 ave 233,895 484,119 232,241 med 24,663,306 863,076 100,540 Falcon-512 ave 26,637,878 863,420 100,709 med 71,013,520 1,740,188 228,086 Falcon-1024 ave 78,797,658 1,740,520 228,326

signature generation with its AVX2 implementation, compared to its portable reference code. The performance of the reference code in Table 7 showed around three times faster signature generation for HAETAE compared to Falcon. Optimized for AVX2 and also using the floating-point unit, Falcon becomes faster than HAETAE for signature generation. Key generation is still around thirty times faster and with HAETAE compared to Falcon, and the verification speed is very similar for both schemes. We note, however, that both Dilithium and Falcon went through a multi-year process of incrementally optimized implementations, whereas this process has just started for HAETAE. Moreover, when we apply the heuristic that sending one byte via internet costs at least 1000 cycles [BBC + 20, Sec. 5.4], remarkably, HAETAE is already nearly as performant as Dilithium in terms of signing plus sending the signature.

Embedded Implementation on Cortex-M4

7

To evaluate the suitability of HAETAE for embedded environments we developed an implementation for the STM32f4-Discovery board, featuring 128 KiB RAM and a Cortex- M4F processor which implements the ARMv7E-M ISA and operates on 32-bit words. We use the PQM4 framework [KRSS19] for development and evaluation, as it is the de facto standard for comparison of post-quantum cryptography schemes on Cortex-M4 processors. The Cortex-M4F, in contrast to the Cortex-M4, features a floating-point unit. Its floating point registers can be used to store and load intermediate values within a single cycle to reduce the pressure on the 13 general purpose registers. The profiling of the reference implementation already indicates that replacing the portable Keccak implementation with one optimized for the Cortex-M4 is an important and straightforward step towards fast execution time. The two other major components that are highly relevant are the polynomial arithmetic and the Gaussian sampler, both will be discussed in the following.

<!-- PDF_PAGE: 33 -->

## PDF page 33

Team HAETAE

### 7.1 Polynomial Arithmetic

57

In this section, we will address the issue of how to implement the required arithmetic operations on these rings and mappings between them on a Cortex-M4 platform.

Modular Reductions. In modular arithmetic, the Barret reduction [Bar87], the Montgomery modular multiplication [Mon85], and related techniques are indispensable for efficient computation, the first for reducing given numbers, the second for yielding the reduced result of a multiplication with a constant modq. The algorithms avoid computationally expensive divisions by q and replace them with a multiplication by a suitably chosen number and division by powers of two, which can be realized with shift operations. Both methods initially reduce the result to the interval [0, 2q] and perform the full reduction with a conditional subtraction, which can be done in constant time. In many cases one can forgo the final reduction for intermediate results, an approach dubbed lazy reduction. The prime chosen in the HAETAE scheme is q = 64513 = 0xFC01, the largest unsigned 16-bit prime with a 512 th root of unity. Fully reduced elements of Z q can be stored efficiently in 16-bit in the bottom or top half of a 32-bit register. Unfortunately, this does not carry over to arithmetic operations. A lazy reduction or an addition already requires 17 bits to store the result, a combination of a lazily reduced multiplication followed by an addition requires 18 bits. The recent advance of the Plantard multiplication [Pla21] is not useful within this work, as the prime in HAETAE is not √ u 0.618 R, i.e., q ≤ 40503 for compatible. Plantard multiplication requires q &lt; 1+ 2R 5 16 R = 2 . So the prime of HAETAE is too large for this use-case with Cortex-M4 16-bit DSP-instructions. The same goes for Seiler’s variant [Sei18] of signed Montgomery modular multiplication, which is only well-defined for q &lt; R 2 .

16-bit vs 32-bit. Quite a few post-quantum schemes use primes that are 13-bit values or smaller. In this case, one can both store and manipulate the coefficients graciously and efficiently as two signed 16-bit values packed into one 32-bit register, as the Cortex-M4 offers a wide range of instructions intended for Digital Signal Processor (DSP) applications, like mixed multiplication of upper and lower halves of two registers that can be used for this purpose. In the case of HAETAE, trade-offs need to be found between the compactness of 16-bit storage and doubled speed of access for consecutive coefficients on the one hand, and the required overhead to fully reduce the coefficients before writing them to memory. If coefficients are written once and afterwards are read repeatedly without alterations, the 16-bit representation can be worthwhile. When polynomials of the public key are expanded, the coefficients are sampled in fully reduced state, we therefore store them in halfwords. While it is feasible to use a modified Montgomery reduction with unsigned 16-bit integers as input and 17 bits output (or a 16-bit value with overflow flag), there are no corresponding instructions available to exploit this. In contrast, the Montgomery reduction in the Dilithium implementation for the Cortex-M4 uses R = 2 32 and takes only three instructions. We determined the overhead associated with full reductions required to store coefficients as 16-bit values to be too large to outperform the 32-bit variant for the NTT. The same applies to other polynomial arithmetic operations in HAETAE, besides the expanded polynomials of the public key, we therefore operate on 32-bit coefficients.

NTT. HAETAE, as other lattice-based schemes, extensively employs polynomial multipli- cation. The NTT is a generalization of the Fast Fourier Transform (FFT) and is the state- of-the-art technique to perform this operation, speeding up the computation considerably, as compared to, e.g., schoolbook multiplication. The addition and multiplication of

<!-- PDF_PAGE: 34 -->

## PDF page 34

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

58

polynomials transformed into the NTT domain are carried out coefficient-wise, greatly reducing the cost of the latter operation. The overhead to perform the transform and inverse transform, where required, is usually outweighed by the performance gain in the multiplication. HAETAE is specified such that large parts of the public key are expanded directly to the NTT domain. Fortunately, the closeness to Dilithium, which also uses polynomials of degree n = 256, allows us the reuse its highly optimized assembly code for the NTT developed for the Cortex-M4 by Abdulrahman et al. [AHKS22], which improves over previous work [GKOS18]. The code adjustments required for operation in HAETAE are limited to adjusting constants like the prime being used, the root of unity, which is chosen as 426 (the primitive 512 th root of unity of q = 64513) and the twiddle factors. Replacing the portable C code from the reference implementation with optimized assembly derived from the Dilithium implementation reduces the cycle count per invocation from 37506 cycles to 8047 cycles, a speed-up by a factor of 4.6. For the inverse NTT, the cycle count dropped from 43116 to 8369, a speed-up by a factor of 5.1.

### 7.2 Gaussian Sampler

The major numerical components of the Gaussian sampler are the CDT sampler for sampling the most significant bits and the fixed-point exponential function used in the rejection step. As both components are called repeatedly, both have been implemented in assembly code. The CDT sampler accumulates ones and zeros, depending on comparisons of a uniformly sampled 16-bit random value to tabled threshold values. We use the uadd16, usub16 and sel SIMD instructions from the Cortex-M4 instruction set to carry out two comparisons and accumulations in parallel. We furthermore optimize the memory access and unroll the loop. By doing so we reduce the instruction count from 800 cyles for the reference implementation to 206 cyles, a speed-up by a factor of 3.9. The exponential is approximated by a polynomial, which is evaluated using Horner’s scheme. The reference implementation of the exponential function uses fixed-point arithmetic with 48 fraction bits. Values are embedded in 64-bit integers and 64x64 to 128-bit multiplication is used. The latter operation has no native support on the Cortex-M4. To circumvent this limitation, the Cortex-M4 implementation splits the value into two signed components at the start of each multiplication, namely the most significant bits ah = a » 24 and the least significant bits as al = a - ah. For the accumulation of the results a 64-bit integer is used again, taking advantage of the smlal instruction. This repeated switch between representations allows for efficient computation of the individual Horner’s scheme iterations. Whereas the reference implementation of the exponential function takes 1658 cycles to execute, this is reduced to 563 instructions in the optimized Cortex-M4 code, a speed-up by a factor of 2.9.

### 7.3 Stack Optimization

Besides execution time, also the memory footprint is an important metric for constrained devices. The target device in this work has 128 KiB of RAM available as stack memory. In this context, data structures typically encountered in lattice based cryptography need to be considered as rather large. A single polynomial in HAETAE takes 512 B or 1 KiB of memory to store, depending on whether the data is represented as 16-bit or 32-bit values. So vectors or matrices of polynomials can occupy a considerable share of the available RAM, if stored in their entirety. In this section we explore how to minimize memory use; in some cases significant trade-offs between memory usage and execution speed can be made.

<!-- PDF_PAGE: 35 -->

## PDF page 35

Team HAETAE

59

The reference implementation of HAETAE is designed with an emphasis on readability and close similarity to the mathematical specification. This results in top level functions, which consist of long monolithic blocks with many large data structures, which do not necessarily have overlapping lifetimes, but nevertheless occupy stack space for the entire function lifecycle. Most stack memory is required for the signature generation. Due to the unnecessarily high stack usage of the reference implementation, HAETAE-180 and HAETAE-260 do not run on the STM32f4-Discovery board without optimizations. To reduce the memory footprint we executed two strategies. First, we carefully analyzed the liveness of each relevant variable and refactored the monolithic code into subroutines to reduce the scope of variables and thereby the total stack usage. This slightly impacts the readability of the code, but does not affect the speed. In a second variant we additionally opted for a more aggressive memory reduction, by recomputing polynomials on demand, this obviously comes with performance costs. We adapt the data structures to be primarily polynomial oriented instead of vector and matrix oriented representations. Recomputations are done during public key usage, where we generate each polynomial on demand, and during hyperball sampling, where we sample each polynomial twice, once for the evaluation of the normalization factor and a second time to sample the actual y values. Since the hyperball sampling is computationally very expensive, this leads to a severe overhead in runtime.

Performance and Comparison Cortex-M4

7.4

Table 9 shows the maximum stack size of our two Cortex-M4 implementations of HAETAE and values reported in the PQM4 framework about Dilithium and Falcon. With speed- opt, we refer to our implementation, that is optimized for the Cortex-M4 and includes multiple stack-size optimizations, but does not trade speed for better memory requirements. stack-opt refers to the version, where we additionally exploit speed vs memory trade-offs. First, we can observe that the memory requirements of HAETAE are small enough to run on the STM32f4-Discovery board for all parameter sets, even in the speed-opt version. Second, the stack sizes for HAETAE are in the same order of magnitude as Dilithium and Falcon. Compared to speed-opt HAETAE, Dilithium requires around two to three times more memory during key generation, and a similar overhead for signature verification. The difference is at most 20% for signature generation, for this operation Dilithium requires less memory than HAETAE for the first two parameter sets. Our stack-opt version reduces the stack-size up to 34% during signature generation and key generation, but does not differ for the verification. However, this comes with higher costs in terms of computation time. Falcon stands out for its stack-size below 10 KiB for both parameter sets during verification. Table 9 shows the cycles spend by our two Cortex-M4 implementations of HAETAE and values reported in the PQM4 framework 1 for Dilithium and Falcon. Our version using aggressive stack reduction techniques based on recomputations does not impact the signature verification time, but almost doubles the computation time for the signature generation. The time overhead for key generation is up to 30%. Similar to our AVX2 optimized implementation, the relative performance comparison of HAETAE to Dilithium and Falcon does not change drastically.

1 https://github.com/mupq/pqm4/blob/master/benchmarks.md

<!-- PDF_PAGE: 36 -->

## PDF page 36

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

60

Table 9: Maximum stack size in bytes and average kilo cycle counts of 1000 (100 for Falcon) executions for Cortex-M4 implementations of HAETAE, Dilithium, and Falcon. Stack size Cycle count Scheme KeyGen Sign Verify KeyGen Sign Verify speed-opt 19,796 54,564 22,532 8,905 27,312 1,054 HAETAE-120 stack-opt 17,364 40,732 22,532 10,819 51,017 1,054 speed-opt 29,612 69,631 31,020 17,666 34,466 2,026 HAETAE-180 stack-opt 22,444 57,116 31,020 22,860 65,855 2,026 speed-opt 34,108 102,964 36,428 22,851 50,175 2,733 HAETAE-260 stack-opt 22,356 68,380 36,428 23,213 99,472 2,733 Dilithium-2 38,408 49,380 36,212 1,598 4,112 1,572 Dilithium-3 60,836 68,836 57,724 2,830 6,588 2,691 Dilithium-5 97,692 115,932 92,788 4,826 8,779 4,706 Falcon-512 18,416 42,508 4,724 155,758 38,979 481 Falcon-1024 36,296 82,532 8,820 480,072 85,125 995

8 Conclusion

With HAETAE, we close an important gap between the two state-of-the-art digital signature schemes Dilithium and Falcon. Novel contributions in key generation and rejection sampling allow us to reach significantly smaller signature and verification key sizes, while still allowing physical side-channel protected implementations for IoT use-cases. Moreover, our first set of optimized implementations exhibits that our proposed algorithms run in feasible time both on embedded and high-end platforms and compete with existing schemes when considering sending latency. A possible direction to achieve a similar signature sizes with HAETAE could be following the BLISS approach, using the bimodal Gaussians in the module LWE setting with the compression techniques, which we did not go through to avoid computing a secret-dependent transcendental function during signature rejection to enhance the implementation security.

Acknowledgements

Part of this work was done while Damien Stehlé was in École Normale Supérieure de Lyon and Institut Universitaire de France, and Julien Devevey was in École Normale Supérieure de Lyon, and Dongyeon Hong and MinJune Yi were in CryptoLab Inc. Julien Devevey and Damien Stehlé were supported by the AMIRAL ANR grant (ANR-21-ASTR-0016), the PEPR quantique France 2030 programme (ANR-22-PETQ-0008) and the PEPR Cyber France 2030 programme (ANR-22-PECY-0003). Tim Güneysu, Markus Krausz, Georg Land and Marc Möller have been supported by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) under Germany’s Excellence Strategy - EXC 2092 CASA - 390781972, by the German Federal Ministry of Education and Research BMBF through the projects 6GEM (16KISK038) and FlexKI (01IS22086I), and by the European Commission under the grant agreement number 101070374 (CONVOLVE). Jung Hee Cheon and Hyeongmin Choe were supported by the National Research Foundation of Korea (NRF) grant funded by the Korea government (MSIT) (No. 2022R1A5A6000840).

### References

[ABC + 23] Melissa Azouaoui, Olivier Bronchain, Gaëtan Cassiers, Clément Hoffmann, Yulia Kuzovkova, Joost Renes, Tobias Schneider, Markus Schönauer, François-

<!-- PDF_PAGE: 37 -->

## PDF page 37

Team HAETAE

61

Xavier Standaert, and Christine van Vredendaal. Protecting dilithium against leakage revisited sensitivity analysis and improved implementations. IACR TCHES, 2023(4):58–79, 2023.

[AHKS22] Amin Abdulrahman, Vincent Hwang, Matthias J. Kannwischer, and Amber Sprenkels. Faster kyber and dilithium on the cortex-M4. In Giuseppe Ateniese and Daniele Venturi, editors, ACNS 22, volume 13269 of LNCS, pages 853–871. Springer, Heidelberg, June 2022.

[AKM + 15] Marc Andrysco, David Kohlbrenner, Keaton Mowery, Ranjit Jhala, Sorin Lerner, and Hovav Shacham. On subnormal floating point and abnormal timing. In 2015 IEEE Symposium on Security and Privacy, pages 623–639. IEEE, 2015.

[ASY22]

Shweta Agrawal, Damien Stehlé, and Anshu Yadav. Round-optimal lattice- based threshold signatures, revisited. In Mikolaj Bojanczyk, Emanuela Merelli, and David P. Woodruff, editors, ICALP 2022, volume 229 of LIPIcs, pages 8:1–8:20. Schloss Dagstuhl, July 2022.

[Bar87]

Paul Barrett. Implementing the Rivest Shamir and Adleman public key encryption algorithm on a standard digital signal processor. In Andrew M. Odlyzko, editor, CRYPTO’86, volume 263 of LNCS, pages 311–323. Springer, Heidelberg, August 1987.

[BBC + 20] Daniel J. Bernstein, Billy Bob Brumley, Ming-Shing Chen, Chitchanok Chuengsatiansup, Tanja Lange, Adrian Marotzke, Bo-Yuan Peng, Nicola Tuveri, Christine van Vredendaal, and Bo-Yin Yang. NTRU Prime: round 3. https://ntruprime.cr.yp.to/nist/ntruprime-20201007.pdf, 2020.

[BBD + 23] Manuel Barbosa, Gilles Barthe, Christian Doczkal, Jelle Don, Serge Fehr, Benjamin Grégoire, Yu-Hsuan Huang, Andreas Hülsing, Yi Lee, and Xiaodi Wu. Fixing and mechanizing the security proof of Fiat-Shamir with aborts and Dilithium. In Helena Handschuh and Anna Lysyanskaya, editors, CRYPTO 2023, Part V, volume 14085 of LNCS, pages 358–389. Springer, Heidelberg, August 2023.

[BBE + 19] Gilles Barthe, Sonia Belaïd, Thomas Espitau, Pierre-Alain Fouque, Mélissa Rossi, and Mehdi Tibouchi. GALACTICS: Gaussian sampling for lattice- based constant- time implementation of cryptographic signatures, revisited. In Lorenzo Cavallaro, Johannes Kinder, XiaoFeng Wang, and Jonathan Katz, editors, ACM CCS 2019, pages 2147–2164. ACM Press, November 2019.

[BGV12]

Zvika Brakerski, Craig Gentry, and Vinod Vaikuntanathan. (Leveled) fully homomorphic encryption without bootstrapping. In Shafi Goldwasser, editor, ITCS 2012, pages 309–325. ACM, January 2012.

[BP18]

Leon Groot Bruinderink and Peter Pessl. Differential fault attacks on deterministic lattice signatures. IACR TCHES, 2018(3):21–43, 2018. https: //tches.iacr.org/index.php/TCHES/article/view/7267.

[CL21]

André Chailloux and Johanna Loyer. Lattice sieving via quantum random walks. In Mehdi Tibouchi and Huaxiong Wang, editors, ASIACRYPT 2021, Part IV, volume 13093 of LNCS, pages 63–91. Springer, Heidelberg, December 2021.

<!-- PDF_PAGE: 38 -->

## PDF page 38

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

62

[DDGR20] Dana Dachman-Soled, Léo Ducas, Huijing Gong, and Mélissa Rossi. LWE with side information: Attacks and concrete security estimation. In Daniele Micciancio and Thomas Ristenpart, editors, CRYPTO 2020, Part II, volume 12171 of LNCS, pages 329–358. Springer, Heidelberg, August 2020.

[DDLL13] Léo Ducas, Alain Durmus, Tancrède Lepoint, and Vadim Lyubashevsky. Lattice signatures and bimodal Gaussians. In Ran Canetti and Juan A. Garay, editors, CRYPTO 2013, Part I, volume 8042 of LNCS, pages 40–56. Springer, Heidelberg, August 2013.

[DFPS22] Julien Devevey, Omar Fawzi, Alain Passelègue, and Damien Stehlé. On rejection sampling in lyubashevsky’s signature scheme. In Shweta Agrawal and Dongdai Lin, editors, ASIACRYPT 2022, Part IV, volume 13794 of LNCS, pages 34–64. Springer, Heidelberg, December 2022.

[DFPS23] Julien Devevey, Pouria Fallahpour, Alain Passelègue, and Damien Stehlé. A detailed analysis of Fiat-Shamir with aborts. In Helena Handschuh and Anna Lysyanskaya, editors, CRYPTO 2023, Part V, volume 14085 of LNCS, pages 327–357. Springer, Heidelberg, August 2023.

[DKL + 18] Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyubashevsky, Peter Schwabe, Gregor Seiler, and Damien Stehlé. CRYSTALS-Dilithium: A lattice-based digital signature scheme. IACR TCHES, 2018(1):238–268, 2018. https: //tches.iacr.org/index.php/TCHES/article/view/839.

[dPEK + ]

Rafaël del Pino, Thomas Espitau, Shuichi Katsumata, Mary Maller, Fabrice Mouhartem, Thomas Prest, Mélissa Rossi, and Markku-Juhani Saarinen. Raccoon: A side-channel secure signature scheme. Submission to the NIST Additional Post-Quantum Digital Signature Schemes standardization process. Available at https://raccoonfamily.org/wp-content/uploads/2023/07/ raccoon.pdf.

[DPS23]

Julien Devevey, Alain Passelègue, and Damien Stehlé. G+G: A fiat-shamir lattice signature based on convolved gaussians. In ASIACRYPT (7), volume 14444 of Lecture Notes in Computer Science, pages 37–64. Springer, 2023.

[Dud14]

Jarek Duda. Asymmetric numeral systems: entropy coding combining speed of Huffman coding with compression rate of arithmetic coding, 2014. ArXiv preprint, available at https://arxiv.org/abs/1311.2540.

[Dwo15]

Morris J Dworkin. SHA-3 standard: Permutation-based hash and extendable- output functions. FIPS 202, 2015.

[EFG + 22] Thomas Espitau, Pierre-Alain Fouque, François Gérard, Mélissa Rossi, Akira Takahashi, Mehdi Tibouchi, Alexandre Wallet, and Yang Yu. Mitaka: A simpler, parallelizable, maskable variant of falcon. In Orr Dunkelman and Stefan Dziembowski, editors, EUROCRYPT 2022, Part III, volume 13277 of LNCS, pages 222–253. Springer, Heidelberg, May / June 2022.

[ENST23] Thomas Espitau, Guilhem Niot, Chao Sun, and Mehdi Tibouchi. Square unstructured integer euclidean lattice signature. Submission to the NIST’s post-quantum cryptography standardization process, 2023.

[ETWY22] Thomas Espitau, Mehdi Tibouchi, Alexandre Wallet, and Yang Yu. Shorter hash-and-sign lattice-based signatures. In Yevgeniy Dodis and Thomas Shrimpton, editors, CRYPTO 2022, Part II, volume 13508 of LNCS, pages 245–275. Springer, Heidelberg, August 2022.

<!-- PDF_PAGE: 39 -->

## PDF page 39

Team HAETAE

63

[FHK + 18] Pierre-Alain Fouque, Jeffrey Hoffstein, Paul Kirchner, Vadim Lyubashevsky, Thomas Pornin, Thomas Prest, Thomas Ricosset, Gregor Seiler, William Whyte, Zhenfei Zhang, et al. Falcon: Fast-fourier lattice-based compact signatures over NTRU. Submission to the NIST’s post-quantum cryptography standardization process, 36(5), 2018.

[Gie14]

Fabian Giesen. Interleaved entropy coders. arXiv preprint arXiv:1402.3392, 2014.

[GKOS18] Tim Güneysu, Markus Krausz, Tobias Oder, and Julian Speith. Evaluation of lattice-based signature schemes in embedded systems. In 25th IEEE International Conference on Electronics, Circuits and Systems, ICECS 2018, Bordeaux, France, December 9-12, 2018, pages 385–388. IEEE, 2018.

[GS23]

Jason Goertzen and Douglas Stebila. Post-quantum signatures in DNSSEC via request-based fragmentation. In Thomas Johansson and Daniel Smith-Tone, editors, Post-Quantum Cryptography - 14th International Workshop, PQCrypto 2023, College Park, MD, USA, August 16-18, 2023, Proceedings, volume 14154 of Lecture Notes in Computer Science, pages 535–564. Springer, 2023.

[HDS23]

Abiodoun Clement Hounkpevi, Sidoine Djimnaibeye, and Michel Seck. EagleSign: A new post-quantum ElGamal-like signature over lattices. Submission to the NIST’s post-quantum cryptography standardization process, 2023.

[HPP + 23] Thomas Pornin Huang, Eamonn W Postlethwaite, Thomas Prest, Ludo N Pulles, and Wessel van Woerden. HAWK., 2023. Version 1.0.1 (July 19, 2023).

[HPS98]

Jeffrey Hoffstein, Jill Pipher, and Joseph H. Silverman. NTRU: A ring-based public key cryptosystem. In Joe Buhler, editor, ANTS-III, volume 1423 of LNCS, pages 267–288. Springer, 1998.

[KA21]

Emre Karabulut and Aydin Aysu. FALCON Down: Breaking FALCON post-quantum signature scheme through side-channel attacks. In 2021 58th ACM/IEEE Design Automation Conference (DAC), pages 691–696, 2021.

[KLS + 23] Markus Krausz, Georg Land, Florian Stolz, Dennis Naujoks, Jan Richter- Brockmann, Tim Güneysu, and Lucie Johanna Kogelheide. Generic accelerators for costly-to-mask PQC components. IACR Cryptol. ePrint Arch., page 1287, 2023.

[KRSS19] Matthias J. Kannwischer, Joost Rijneveld, Peter Schwabe, and Ko Stoffelen. pqm4: Testing and benchmarking NIST PQC on ARM cortex-M4. Cryptology ePrint Archive, Report 2019/844, 2019. https://eprint.iacr.org/2019/ 844.

[Li04]

Ren-Cang Li. Near optimality of chebyshev interpolation for elementary function computations. IEEE Trans. Computers, 53(6):678–687, 2004.

[LS15]

Adeline Langlois and Damien Stehlé. Worst-case to average-case reductions for module lattices. Des. Codes Cryptogr., 75(3):565–599, 2015.

[Lyu09]

Vadim Lyubashevsky. Fiat-Shamir with aborts: Applications to lattice and factoring-based signatures. In Mitsuru Matsui, editor, ASIACRYPT 2009, volume 5912 of LNCS, pages 598–616. Springer, Heidelberg, December 2009.

<!-- PDF_PAGE: 40 -->

## PDF page 40

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

64

[Lyu12]

Vadim Lyubashevsky. Lattice signatures without trapdoors. In David Pointcheval and Thomas Johansson, editors, EUROCRYPT 2012, volume 7237 of LNCS, pages 738–755. Springer, Heidelberg, April 2012.

[MGTF19] Vincent Migliore, Benoît Gérard, Mehdi Tibouchi, and Pierre-Alain Fouque. Masking Dilithium - efficient implementation and side-channel evaluation. In Robert H. Deng, Valérie Gauthier-Umaña, Martín Ochoa, and Moti Yung, editors, ACNS 19, volume 11464 of LNCS, pages 344–362. Springer, Heidelberg, June 2019.

[Mon85]

Peter L Montgomery. Modular multiplication without trial division. Mathematics of computation, 44(170):519–521, 1985.

[MUTS22] Soundes Marzougui, Vincent Ulitzsch, Mehdi Tibouchi, and Jean-Pierre Seifert. Profiling side-channel attacks on Dilithium: A small bit-fiddling leak breaks it all. Cryptology ePrint Archive, Report 2022/106, 2022. https://eprint. iacr.org/2022/106.

[Pla21]

Thomas Plantard. Efficient word size modular arithmetic. IEEE Transactions on Emerging Topics in Computing, 9(3):1506–1518, 2021.

[Por19]

Thomas Pornin. New efficient, constant-time implementations of Falcon. Cryptology ePrint Archive, Paper 2019/893, 2019.

[Pre17]

Thomas Prest. Sharper bounds in lattice-based cryptography using the Rényi divergence. In Tsuyoshi Takagi and Thomas Peyrin, editors, ASIACRYPT 2017, Part I, volume 10624 of LNCS, pages 347–374. Springer, Heidelberg, December 2017.

[Pre23]

Thomas Prest. A key-recovery attack against mitaka in the t-probing model. In Alexandra Boldyreva and Vladimir Kolesnikov, editors, PKC 2023, Part I, volume 13940 of LNCS, pages 205–220. Springer, Heidelberg, May 2023.

[PST20]

Christian Paquin, Douglas Stebila, and Goutam Tamvada. Benchmarking post-quantum cryptography in TLS. In Post-Quantum Cryptography: 11th International Conference, PQCrypto 2020, Paris, France, April 15–17, 2020, Proceedings 11, pages 72–91. Springer, 2020.

[Ros20]

Melissa Rossi. Extended Security of Lattice-Based Cryptography. PhD thesis, École Normale Supérieure de Paris, 2020.

[RS23]

Keegan Ryan and Adam Suhl. Round 1 (additional signatures) official comment: EHT, 2023.

[Sch90]

Claus-Peter Schnorr. Efficient identification and signatures for smart cards. In Gilles Brassard, editor, CRYPTO’89, volume 435 of LNCS, pages 239–252. Springer, Heidelberg, August 1990.

[Sch00]

Werner Schindler. A timing attack against RSA with the chinese remainder theorem. In Cryptographic Hardware and Embedded Systems—CHES 2000: Second International Workshop Worcester, MA, USA, August 17–18, 2000 Proceedings 2, pages 109–124. Springer, 2000.

[Sei18]

Gregor Seiler. Faster AVX2 optimized NTT multiplication for ring-LWE lattice cryptography. Cryptology ePrint Archive, Report 2018/039, 2018. https://eprint.iacr.org/2018/039.

<!-- PDF_PAGE: 41 -->

## PDF page 41

Team HAETAE

[SF23]

65

Igor Semaev, , and Martin Feussner. Digital signature algorithms EHTV3 and EHTV4 submission to NIST PQC. Submission to the NIST’s post-quantum cryptography standardization process, 2023.

[Tib23]

Mehdi Tibouchi. Round 1 (additional signatures) official comment: EagleSign, 2023.

[VGS17]

Aaron R Voelker, Jan Gosmann, and Terrence C Stewart. Efficiently sampling vectors and coordinates from the n-sphere and n-ball. Centre for Theoretical Neuroscience-Technical Report, 01 2017.

Sizing up post-quantum signatures.

[Wes21]

Bas Westerbaan. Cloudflare, 2021.

[YJL + 23]

Technical report,

Yang Yu, Huiwen Jia, Leibo Li, Delong Ran, Zhiyuan Qiu, Shiduo Zhang, Xiuhan Lin, and Xiaoyun Wang. HuFu: Hash-and-sign signatures from powerful gadgets. Algorithm specifications and supporting documentation., 2023. Version 1.1 (September 2, 2023).

A Recent lattice-based signatures

In this section, we give a size comparison of the recent lattice-based signature schemes. In Table 10, we compare the verification key and signature sizes (in bytes) of some selected lattice signature schemes, including the NIST’s on-ramp candidates. Note that we additionally showcase some disadvantages, e.g., some recent analyses reported at pqc- forum (some are verified by the submitters, and others are not) or the use of new family of assumptions, which may degrade the claimed security.

Table 10: Size comparison of recent lattice-based signatures.

Levels 1 &amp; 2 vk sig. sum ↑

Level 3 vk sig.

Scheme

Level 5 vk sig.

Ref.

sum

sum

EHTv4 1 1,110 369 1,479 — — — 1,110 369 1,479 [SF23] Falcon 2 897 666 1,563 — — — 897 666 1,563 [FHK + 18] 3 HAWK 1,024 555 1,579 — — — 1,024 555 1,579 [HPP + 23] 4 Mitaka 896 713 1,609 — — — 896 713 1,609 [EFG + 22] HAETAE 992 1,474 2,466 1,472 2,349 3,821 2,080 2,948 5,028 ours Dilithium 1,312 2,420 3,732 1,952 3,293 5,245 2,592 4,595 7,187 [DKL + 18] EagleSign 5 1,824 2,144 3,968 2,842 2,336 5,160 3,616 3,488 7,104 [HDS23] Raccoon 2,256 11,524 13,780 3,160 14,544 17,704 4,064 20,330 24,394 [dPEK + ] SQUIRRELS 682K 1,019 683K 1,600K 1,554 1,602K — — — [ENST23] HUFU 6 1,059K 2,450 1,061K 2,177K 3,540 2,181K 3,573K 4,520 3,578K [YJL + 23]

2 infeasible to mask, uses floating-point arithmetic

1 reported attack [RS23]

3 new assumptions

4 hard to mask, proposed masked Gaussian sampler recently broken [Pre23]

smLIP, omSVP attack [Tib23]

6 uses floating-point arithmetic

5 reported

Security against Physical Attacks

B

Implementation security is a crucial aspect of making cryptosystems feasible in real-world applications. A significant advantage of HAETAE is that it can be protected against power side-channel attacks efficiently and with reasonable overhead. In this context, we emphasize the similarity of HAETAE to Dilithium. Hence, past works analyzing concrete

<!-- PDF_PAGE: 42 -->

## PDF page 42

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

66

attacks [BP18, MUTS22], but also countermeasures [MGTF19, ABC + 23], mainly apply to HAETAE as well. While there is no known method to efficiently mask Falcon, Mitaka [EFG + 22] was designed to be easy to protect against implementation attacks, while still having the advantage of similarly small signatures as Falcon. For Mitaka, the crux regarding side- channel security is sampling Gaussian-distributed values. Together with Mitaka, an efficient, masked algorithm for discrete Gaussian sampling was presented. However, Prest broke its security proof recently [Pre23]. In this respect, HAETAE has the strong advantage that Gaussian sampling only needs to be secured against the much stronger Simple Power Analysis (SPA) attacker model, which allows for simpler countermeasures, while Mitaka’s side-channel security will always depend on a masked sampler. While a fully protected implementation of HAETAE is out of scope for this paper, we briefly sketch its feasibility.

Protecting the Arithmetic. Most notably, HAETAE does not deploy floating-point arithmetic at any point, and only few secrets require fix-point arithmetic. Remarkably, addition of fix-point arithmetic can be masked relatively easy, and HAETAE never requires a multiplication of fix-point values. During signing, the most critical operation is multiplying the (public) challenge polynomial c with s and subsequently adding the result to y. Since this operation may leak information about the secret key statistically over many executions, implementers must protect it accordingly. As countermeasures against these so-called Differential Power Analysis (DPA) attacks, masking has been proven effective. This operation is straightforward to mask at arbitrary order by splitting the secret key polynomials into multiple additive shares in R q . A masked implementation then stores the NTT of each share of s and multiplies them to c, obtaining a shared cs. Following this, the inverse NTT is applied share-wise. Since y is a polynomial vector in (1/N )R, it is not trivially possible to add our shares of cs ∈ R k+` . On the other hand, y is not a q secret-key-dependent value. Therefore, it is not required to be protected against DPA but only against the much stronger attacker model of a SPA. In fact, coefficient-wise shuffling of the addition might be sufficient at this point. Independent of whether the addition is shuffled or masked, this involves a masking conversion from Z q to Z 2 32 . Subsequently, the computation of 2z − y and the bound checks can be shuffled without applying costly masking.

Protecting the Hyperball Sampler. The same idea applies to the whole hyperball sampling procedure. Since the order of the Gaussian samples is, in principle, irrelevant, they can be generated in random order. This is particularly an advantage for randomized HAETAE. For the deterministic version, a masked CDT sampler, and a masked approximation of the exponential function are required. The former was shown to be feasible recently by Krausz et al. [KLS + 23], while the latter is a sequence of multiplications, shifting by a constant amount, and addition by constants, which is expected to be costly but feasible. It is noteworthy that the random oracle hash (which outputs the challenge) is only required to be protected against SPA as well. Since the input order into the hash function cannot be randomized, the preceding values must still be protected by masking. Therefore, if no masked hyperball sampling has been performed, we propose to perform a shuffled point-wise multiplication of A and y, directly followed by freshly masking the resulting coefficients. Then, a share-wise inverse NTT and a masking conversion to the Boolean domain will be performed, which enables a secure HighBits operation. For the LSBs of y 0 , generating a fresh Boolean masking during the shuffled generation of the hyperball sample’s coefficients is sufficient.

<!-- PDF_PAGE: 43 -->

## PDF page 43

Team HAETAE

C Additional Proofs

C.1 Useful Lemma

We will rely on the following claim.

67

Lemma 12. Let n be the degree of R. Let m, N, r &gt; 0 and v ∈ R m . Then the following statements hold:

1. |(1/N )R m ∩ B R,m (r)| = |R m ∩ B R,m (N r)|,

2. |R m ∩ B R,m (r, v)| = |R m ∩ B R,m (r)|,

√

3. Vol(B R,m (r −

√

mn m 2 )) ≤ |R ∩ B R,m (r)| ≤ Vol(B R,m (r +

mn 2 )).

Proof. For the first statement, note that we only scaled (1/N )R m and B R,m (r) by a factor N . For the second statement, note that the translation x 7→ x − v maps R m to R m . We now prove the third statement. For x ∈ R m , we define T x as the hypercube of R m R centered in x with side-length 1. Observe that the T x ’s tile the whole space when x ranges over R m (the way boundaries are handled does not matter for the proof). Also, √ each of those tiles has volume 1. As any element in T x is at Euclidean distance at most mn/2 from x, the following inclusions hold:

√

mn ⊆ 2

[

B R,m r −

x∈R m ∩B R,m (r)

Taking the volumes gives the result.

C.2 Proof of Lemma 4

√

mn . 2

T x ⊆ B R,m r +

√ Proof. To ease the notation, let us use B = r 0 . Let y ∈ B R,m (N r 0 + mn/2) and set z = bye. Note that z is sampled (before the rejection step) with probability

√ Vol(T z ∩ B R,m (N r 0 + mn/2)) , Vol(B R,m (N r 0 ))

where T z is the hypercube of R m R centered in z with √ side-length 1. By the triangle inequality, this probability is equal to 1/Vol(B R,m (N r 0 + mn/2) when z ∈ B R,m (N r 0 ). Hence the distribution of the output is exactly U (R m ∩ B R,m (N r 0 )), as each element is sampled with equal probability and as the algorithm almost surely terminates (its runtime follows a geometric law of parameter the rejection probability). It remains to consider the acceptance probability.

P

√

mn/2))

0 y∈R m ∩B R,m (N r 0 ) Vol(T y ∩ B R,m (N r + √ Vol(B R,m (N r 0 + mn/2))

By the triangle inequality and Lemma 12, it is

|R m ∩ B R,m (N r 0 )| √ ≥ Vol(B R,m (N r 0 + mn/2))

Note that by our choice of N , this is ≥ 1/M 0 .

.

mn √ N r 0 − mn/2 √ . N r 0 + mn/2

<!-- PDF_PAGE: 44 -->

## PDF page 44

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

68

C.3 Proof of Lemma 5

Proof. Figure 6 is the bimodal rejection sampling algorithm applied to the source distribution U ((1/N )R m ∩ B R,m (r 0 )) and target distribution U ((1/N )R m ∩ B R,m (r)) (see, e.g., [DFPS22]). It then suffices that the support of the bimodal shift of the source distribution by v contains the support of the target distribution. It is implied √ by r 0 ≥ r 2 + t 2 . We now consider the number of expected iterations, i.e., the maximum ratio between the two distributions. To guide the intuition, note that if we were to use continuous distributions, the acceptance probability 1/M 0 would be bounded by 1/M . In our case, the acceptance probability can be bounded as follows (using Lemma 12):

|(1/N )R m ∩ B R,m (r)| 1 |R m ∩ B R,m (N r)| = = 0 m 0 M 2|(1/N )R ∩ B R,m (r )| 2|R m ∩ B R,m (N r 0 )| √ Vol(B R,m (N r − mn/2)) √ ≥ 2Vol(B R,m (N r 0 + mn/2)) mn √ 1 N r − mn/2 √ = . 2 N r 0 + mn/2

It now suffices to bound the latter term from below by 1/(cM ) = 1/(2c(r 0 /r) mn ). This inequality is equivalent to: mn 0 √ mn r r + mn/(2N ) 1 √ c ≥ · · , 2 r 0 r − mn/(2N )

and to:

√

1

N ≥

·

c 1/(mn) − 1 which allows to complete the proof.

C.4 Proof of Lemma 7

1/(mn) c 1 + 0 , r r

mn 2

Proof. By Lemma 6, there exists a unique representation

r = b(r + α/2)/αc α + (r mod ± α).

By identifying HighBits(r, α) and LowBits(r, α) in the above equation, we obtain the first result. By definition of mod ± α, we have the second range. Finally, since r 7→ b(r + α/2)/αc is a non-decreasing function, it is sufficient to show that b(2q − 1 + α/2)/αc ≤ b(2q − 1)/αc. We have (2q − 1 + α/2) ≤ b(2q − 1)/αcα + α − 1 by assumption on q. Dividing by α and taking the floor yields the result.

C.5 Proof of Lemma 8

Proof. Let r ∈ [0, 2q − 1]. Let r 0 , r 1 , r 0 0 , and r 1 0 defined as in Definition 8. If r 0 0 = r 0 and r 1 0 = r 1 , the equality r 0 0 + r 1 0 · α h = r 0 + r 1 · α h mod 2q holds vacuously. If not, then r 0 0 = r 0 − 2 and r 1 0 = r 1 − 2(q − 1)/α h and r 0 0 + r 1 0 α h = r 0 + r 1 α h − 2q. By Lemma 7, we get the first equality. The second property stems from the second property in Lemma 7. The modifications to r 0 make r 0 0 lie in the range [−α h /2 − 2, α h /2). The last property stems from the third property in Lemma 7 and the fact that if r 1 = m, then we have r 1 0 = 0.

<!-- PDF_PAGE: 45 -->

## PDF page 45

Team HAETAE

69

Additional Implementation Specification

D

Algorithm 1 describes how to implement the unpacking of b A, and in Algorithm 2 we demonstrate how to apply the CRT.

Algorithm 1 Unpacking routine for b A. unpackA d (seed A , ψ) 1: if d = 0 then b gen := expandA d (seed A ) 2: A b := ψ 3: b 4: else 5: (a gen , b A gen ) := expandA d (seed A ) b 6: b := 2 · NTT(a gen − ψ · 2 d ) mod q b | 2 · A b gen ) mod q := ( b 7: return b A ∈ R k×` q

Notes Regarding Hardware Implementations

E

Hashing and generation of randomness are the most time-consuming operations of HAETAE. Therefore, we assume that hardware implementations will bring significant speedup and can be competitive to Dilithium, particularly through efficient Keccak cores. Furthermore, hardware implementations will benefit significantly from applying the offline approach. Naturally, a module generating hyperball samples can be instantiated and run parallel to the online phase, thus, hiding its latency behind the online phase. Moreover, high-speed applications could adopt the offline approach with designated signing key, including the multiplication of A and y, to further reduce the latency of the online phase.

Algorithm 2 Mapping from (R kq , R q ) to R k 2q

fromCRT(w, x)

1: parse w as vector of integers w of size kn 2: parse x as vector of integers x of size n 3: for i := 0 to n − 1 do

if LSB(x i ) = LSB(w i ) then w 0 i := w i else w 0 i := w i + q 8: for j := 1 to k − 1 do 9: for i := 0 to n − 1 do 10: if LSB(w nj+i ) = 0 then 11: w 0 nj+i := w nj+i 12: else w 0 nj+i := w nj+i + q 13:

4: 5: 6: 7:

14: arrange w 0 to w 0 , an element in R k 2q 15: return w 0

. Implement in constant time.

. Implement in constant time.

<!-- PDF_PAGE: 46 -->

## PDF page 46

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

70

P (x, y)

w (commitment)

−−−−−−−−−−−−−−→

c (challenge)

←−−−−−−−−−−−−

z (response)

−−−−−−−−−−−→

V (x)

c ← f (w)

Reject if z =⊥ Accept or reject

Figure 15: Interaction between P and V . We let hP (x, y) ↔ V (x)i f (·) denote the transcript (w, c, z).

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 46]

F Cryptographic Reminders

In this section, we recall the definition of a canonical identification scheme, which is the main building brick of HAETAE and the Fiat-Shamir with aborts transform, which allows one to turn a canonical identification scheme into a signature scheme.

F.1 Canonical Identification Schemes

We start by defining a canonical identification scheme.

Definition 9 (Canonical Identification Scheme with Aborts (CID)). A canonical identification scheme ID for a relation R is a three rounds interactive protocol between a prover P and a verifier V , as defined in Figure 15. The challenge is generated from f (w) set as the distribution U (C) for some challenge set C. The prover holds a pair (x, y) ∈ R while the verifier only has x, where the pair (x, y) was generated by a PPT algorithm Gen, called an instance generator. The event “z =⊥” is called an abort, and its probability β is called the probability of aborting.

The canonical identification schemes considered in this work are such that given c and z, there is only one w such that V accepts, which can be efficiently computed from c and z. We need the following flavor of zero knowledge, denoted perfect accepting honest verifier zero-knowledge.

Definition 10 (Perfect Accepting Honest Verifier Zero-Knowledge). Let ID be a canonical identification scheme. It satisfies paHVZK if there exists a PPT simulator Sim such that the output distribution of (w, c, z) resulting from the interaction hP (x, y) ↔ V (x)i U (C) conditioned on z 6 = ⊥ and (w 0 , c 0 , z 0 ) generated by Sim(x) for any (x, y) generated by Gen(1 λ ) are identical.

In the case of the HAETAE CID, the challenge c can be sampled uniformly from the challenge space C and passed over as input to the simulator Sim. To avoid using the same commitment twice, we require the min-entropy of the commitment to be high.

Definition 11 (Commitment Min-Entropy). For α ≥ 0, we say that an identification scheme ID with instance generator Gen has commitment min-entropy α if H ∞ [w|(w, c, z) ← hP (x, y) ↔ V (x)i U (C) ] ≥ α, for all (x, y) ← Gen(1 λ ).

Finally we need the notion of computational unique response to enable the strong unforgeability property of the final signature scheme.

Definition 12 (Computational Unique Response). Let ID be a canonical identification scheme with instance generator Gen. The advantage Adv CUR ID (A) of an adversary A against

<!-- PDF_PAGE: 47 -->

## PDF page 47

Team HAETAE

KeyGen(1 λ ):

Sign(sk, µ): 1: While z = ⊥ 1: (x, y) ← Gen(1 ) (w, c, z) ← 2: (vk, sk) = (x, (x, y)) 2: V (x)i H(·,µ) 3: return (vk, sk) 3: return σ = (c, z)

λ

71

Verify(vk, µ, σ): 1: Parse σ = (c, z) ↔ 2: Recover w from σ 3: return c = H(w, µ)

hP (x, y)

Figure 16: Fiat-Shamir with Aborts tranform FS[ID, H].

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 47]

the CUR property of ID is its probability of computing (w, c, z, z 0 ) such that V (x) accepts both (w, c, z) and (w, c, z 0 ) and z 6 = z 0 on input x generated from (x, y) ← Gen(1 λ ).

F.2 The Fiat-Shamir Transform

We now briefly recall how to turn a canonical identification scheme into a full-fledge signature scheme. To do so, the signing scheme runs the interactive protocol and outputs the transcript minus the commitment. The challenge is however generated by hashing the message along with the commitment to prevent an adversary from tampering with it. We recall the assumptions necessary to show the unforgeability of the resulting signature in the following theorem. The following theorem works in the case of quantum adversaries working in the QROM, but tighter statements can be obtained when restricting to classical adversaries in the ROM.

Theorem 4 (Adapted from [BBD + 23, Theorem 2]). Let ID be a canonical identification scheme with α commitment min-entropy and that satisfies paHVZK with probability of aborting β. For any quantum adversary A against the UF-CMA security of FS[ID, H] in the QROM making Q s signature queries and Q h hash queries, there exists an adversary B against the UF-NMA security of FS[ID, H] in the QROM such that: s s Q s Q s 2 −α/2+1 Q s UF - CMA UF - NMA −α/2+1 +2 (Q h +1) . Adv FS[ID,H] (A) ≤ Adv FS[ID,H] (B)+ Q h + 1 + 1 − β 1 − β 1 − β

Furthermore, if A is an adversary against the sUF-CMA security, there exists an adversary B 0 against the CUR property of ID such that the previous bound holds by 0 adding Adv CUR ID (B ) on the right-hand side.

The strong unforgeability statement comes from the fact that in the last game of their proof, the reduction fails if and only if the forgery uses the same commitment (and thus reprogrammed challenge) than the signature query. As this requires a different answer, this corresponds to an attack against the computational unique response property of the canonical identification scheme.

G Fixed-point Sampling Analysis

In this appendix, we quantify the precision needed to sample from the uniform-hyperball distribution by sampling from the discrete Gaussian distribution. We first describe the representation of numbers and operations. A fixed-point number in precision p will consist in a p-bit signed integer k ∈ Z ∩ [−2 p−1 , 2 p−1 ) along with an implicit scaling exponent e: the represented number is x = k · 2 e−p ∈ [−2 e−1 , 2 e−1 ). The data can for example be stored in a p-bit integer in two’s complement representation. The scaling exponent e is not stored, it only exists on paper. For convenience, a precision p fixed-point number x with implicit exponent e will be referred to as a (p, e)-number.

<!-- PDF_PAGE: 48 -->

## PDF page 48

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

72

When performing arithmetic operations on fixed-point numbers, particular care must be taken with overflows: in the analysis, we make sure that during the algorithm execution, any (p, e)-number x will satisfy |x| &lt; 2 e−1 . The following assumes no overflow occurs. We can add, subtract and negate (p, e)-numbers exactly (note that we only consider the situation where the operands of those operations share the same exponent). We assume that we can multiply (p, e 0 )-number x 0 with a (p, e 1 )-number x 1 into a (p, e × )-number x × as if the multiplication was exact and then rounded to a nearest representable number. Finally, we assume that we can compute an inverse square-root of a (p, e)-number x into a (p, e 0 )-number y with possibly slightly more error than that. This is summarized as follows:

x 0 ⊕ x 1 = x 0 + x 1 ; x 0

|(x 0 ⊗ e e × x 1 ) − (x 0 · x 1 )| ≤ 2 e × −p−1 ; 0 ,e 1

x 1 = x 0 − x 1 ; x = −x; √ e t √ |(1/ ·) e − 1/ x| ≤ 2 e t −p .

Discrete Gaussian samples as rounded Gaussian samples

G.1

The hyperball-uniform sampler relies on an algorithm that samples from the continuous Gaussian distribution. In our fixed-point sampling algorithm, we make do with fixed- point approximations to sample from the discrete Gaussian distribution, as described in Section 5.1.1. We analyze how this changes the final distribution in the following lemma, which could be rephrased using the smooth Rényi divergence introduced in [DFPS22].

Lemma 13. Let σ &gt; 0. Let D Z,σ (resp. D σ ) be the distribution D over Z (resp. R) such that D(k) ∼ exp(−k 2 /(2σ 2 )) for all k ∈ Z (resp. k ∈ R). Then we have:

Pr [|k| ≥ 14 · σ] ≤ 2 −140

and

k←D Z,σ

D Z,σ (k)

1 . 1 − 8/σ

max

≤

|k|≤14·σ bD σ e(k)

Proof. Using the discrete Gaussian tail bound from [Lyu12, Lemma 4.4], the weight of D Z,σ out of the interval [−14 · σ, 14 · σ] is ≤ 2 −140 . Using the Poisson Summation Formula, we have that:

∀k ∈ Z, D Z,σ (k) ≤

exp(−k 2 /(2σ 2 )) √ . σ 2π

Further, for k ∈ Z ∩ [−14 · σ, 14 · σ], the following inequalities hold: Z k+1/2 1 √ bD σ e(k) = exp(−x 2 /(2σ 2 ))dx σ 2π k−1/2

≥

≥

exp(−k 2 /(2σ 2 )) √ · exp(−(|k| + 1/4)/(2σ 2 )) σ 2π |k| + 1/4 exp(−k 2 /(2σ 2 )) √ · 1 − 2σ 2 σ 2π 2 2 8 exp(−k /(2σ )) √ · 1 − . σ σ 2π

≥

This completes the proof.

Lemma 13 implies that a signature forger for the imperfect Gaussian sampler succeeds with essentially the same probability with the ideal Gaussian sampler.

G.2 Normalization of Gaussian samples

In the following, we assume that we have access to arbitrarily many statistically independent (p, e)-numbers y i that approximate (perfect) samples y i from D 1 = N (0, 1). We first

<!-- PDF_PAGE: 49 -->

## PDF page 49

Team HAETAE

73

consider the algorithm of Figure 1 with radius 1, using fixed-point arithmetic. We show that the vector y output by the approximate algorithm is close to the vector y output by the exact algorithm. As y is uniformly distributed in a hyperball, the computed vector y is an approximation to such a sample. We first bound the quantities involved during the computations. These bounds are for the exact quantities. To avoid overflows, we actually need them for the corresponding computed quantities. We will see later that as the numerical errors are low, the bounds still essentially hold. The bounds are probabilistic, and hold with probability extremely close to 1.

Lemma 14. Let d min = 6 · 256 + 2 and d max = 11 · 256 + 2. The following bounds hold for all d ∈ [d min , d max ]: Pr [|y| ≥ 2 4 ] &lt; 2 −188 ,

y←D 1

Pr [kyk 2 ≥ 2 12 ] &lt; 2 −144 ,

y i ←D 1 ∀i∈[d]

Pr

z←U (B d−2 (1))

Pr [kyk 2 ≤ 2 9 ] &lt; 2 −144 .

y i ←D 1 ∀i∈[d]

[|z 1 | ≥ 2 −2 ] &lt; 2 −150 .

√ Proof. The first probability is 1 − erf(2 4 / 2). The two others are bounded with the Laurent-Massart bounds for the chi-squared distribution, i.e., for all d, t: √ √ Pr [kyk 2 ≥ d + 2 dt + 2t] ≤ exp(−t) and Pr y i ←D 1 [kyk 2 ≤ d − 2 dt] ≤ exp(−t).

y i ←D 1 ∀i∈[d]

∀i∈[d]

For the last bound, we use [DFPS22, Lemma A.13]. The probability is ex- actly I 1−1/η 2 ((d + 1)/2, 1/2) where I refers to the regularized incomplete Beta function and 1/η is probabilistic magnitude upper bound. We then use numerical computations.

Throughout the execution of the approximate version of the algorithm of Figure 1, we fix the precision to p ≥ 64. The implicit exponents vary depending on the algorithm step: the y i ’s are represented by (p, 5)-numbers, their squares by (p, 13)-numbers, the squared-norm kyk 2 by a (p, 13)-number, the inverse-norm 1/kyk by a (p, −3)-number and the output coordinates on (p, −1)-numbers. Assume that we have |y i − y i | ≤ 0 for all i, for some 0 ≥ 2 −p+5 /2 = 2 −p+4 . To avoid overflows of y i ’s, it suffices that |y i | ≤ 2 4 − 2 −p+5 − 0 . The first bound from Lemma 14 still holds for any 0 ≤ 2 −5 . We now consider the computations of the approximations y i 2 ’s to the y i 2 ’s. We have:

2 |(y i ⊗ 13 5,5 y i ) − y i | + |y i − y i | · |y i + y i |

y i 2 − y i 2

≤

≤ 2 −p+12 + |y i − y i | · [|y i − y i | + 2|y i |]

≤ 2 −p+12 + 2 6 · 0 .

As addition is exact, we obtain:

kyk 2 − kyk 2 ≤ d max · (2 −p+12 + 2 6 · 0 ) =: 1 .

To avoid overflow of kyk 2 and hence of the y i 2 ’s, it suffices that kyk 2 ≤ 2 12 − 2 −p−13 − 1 . The second bound from Lemma 14 still holds for any 0 ≤ 2 −5 .

<!-- PDF_PAGE: 50 -->

## PDF page 50

HAETAE: Shorter Lattice-Based Fiat-Shamir Signatures

74

We continue with the inverse square root computation. The following holds:

1 kyk

1/kyk − ≤

≤ 2 −p−3 +

√ 1 1 1 2 (1/ ·) −3 + − 13 (kyk ) − kyk kyk kyk

|kyk 2 − kyk 2 |

2[kyk 2 − |kyk 2 − kyk 2 |] 3/2 1 ≤ 2 −p−3 + 9 2[2 − 1 ] 3/2

≤ 2 −p−3 + 2 −15 (1 + 2 −1 ) 1 =: 2 ,

where the last inequality holds for any 0 ≤ 2 −15 . To avoid overflow of 1/kyk, it suffices that 1/kyk ≤ 2 −4 − 2 −p−3 − 2 . The third bound from Lemma 14 holds for any 0 ≤ 2 −15 . We finally evaluate the accuracy of the output vector z with respect to z := (y 1 , . . . , y d ) &gt; /kyk 2 . We have, for all i:

≤

y i ⊗ −1 5,−3 1/kyk − y i · 1/kyk + y i · 1/kyk − y i /kyk

z i − z i

≤ 2 −p−2 + 1/kyk − 1/kyk · |y i | + |y i − y i |/kyk

≤ 2 −p−2 + 2 5 · 2 + 2 −4 · 0 =: 3 .

To avoid overflow of z i , it suffices that |z i | ≤ 2 −2 − 2 −p−3 − 3 . The fourth bound from Lemma 14 still holds for any 0 ≤ 2 −20 . Note that 3 is of the order of 2 14 2 −p . This is a crude upper bound, as it assumes that errors are always in the same direction.

Rounding Continuous Hyperball-uniform

G.3

Let us now consider the algorithm from Figure 3. We consider a uniform y 0 ← U (B R,m (1)), its representation y ¯ 0 such that ky 0 − y ¯ 0 k ∞ ≤ 4 , the scaled sample y = r 00 √ · y 0 and its representation ȳ = r 00 · y ¯ 0 , computed exactly, where we let r 00 = N B + mn/2. In particular ky − ȳk ∞ ≤ r 00 4 . Now given any t with ktk ≤ r 0 = N B, the probability that the random variable y gets rounded to it is exactly the inverse of the volume of the hyperball V mn (r 00 ). However, when considering ȳ, this probability lies in [(1 − 2r 00 4 ) mn /V mn (r 00 ), (1 + 2r 00 4 ) mn /V mn (r 00 )]. The ratio of the probability densities thus always lies in [(1 − 2r 00 4 ) mn , (1 + 2r 00 4 ) mn ].

Rejection Sampling with Approximate Source Distribution

G.4

Here, we study the evolution of the rejection sampling steps from Figure 3 and Figure 6 when used with real, approximate distributions.

Theorem 5. Let M &gt; 1. Let δ M ≥ 1 ≥ δ m &gt; 0. Let Q r , Q i and P i such that for any x ∈ Supp(P i ), Q r (x)/Q i (x) ∈ [δ m , δ M ] and R ∞ (P i kQ i ) ≤ M . Consider P r , the probability distribution whose mass function is proportional to x 7→ P i (x)/(M Q i (x))Q r (x). Then P r (x)/P i (x) ∈ [δ m /δ M , δ M /δ m ] for any x ∈ Supp(P i ) = Supp(P r ).

Note that P r is the resulting distribution when using rejection sampling to go from Q i to P i with source distribution Q r .

Proof. The normalization factor is X P i (z) Q r (z) δ m δ M · ∈ , . M Q i (z) M M

z∈Supp(P i )

<!-- PDF_PAGE: 51 -->

## PDF page 51

Team HAETAE

75

As we consider positive values, its inverse then lies in [M/δ M , M/δ m ]. We conclude by considering that Q r (x)/(M Q i (x)) lies in [δ m /M, δ M /M ] for any x ∈ Supp(P i ).

This lemma is applied twice in a row, first to get the final discrete hyperball sample y and second to get the final signature z. In the second case, note that instead of bounding from above and below the distribution of z (before rejection), we can use the bound we get for y, due to data processing arguments.

G.5 Putting Everything together

The final interval in which lies the ratio of real and ideal distributions of z is " 2mn 2mn # 1 − 2r 00 4 1 + 2r 00 4 , , 1 + 2r 00 4 1 − 2r 00 4

where 4 ≈ 2 14−p , r 00 ≤ 2 28 and mn ≤ 2 11 . As max(1−1/x, x−1) = x−1 for positive x ≤ 1, we apply [Pre17, Lemma 3] and follow their subequently described strategy to derive the necessary precision. In order to get about 2 −37 precision in the bounds after rejection sampling, it is necessary to choose p ≈ 14 + 28 + 37 + 1, as the radius r 00 ≤ 2 28 . Going back to the σ of our discrete Gaussian distribution, as elements sampled from it will have absolute value at most 14σ ≈ p, we choose σ = 2 76 , which is also sufficiently big to use discrete Gaussians instead of rounded ones.
