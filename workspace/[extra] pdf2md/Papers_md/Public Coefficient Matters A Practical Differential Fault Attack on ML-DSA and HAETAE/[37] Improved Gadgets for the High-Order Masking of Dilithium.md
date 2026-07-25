# [37] Improved Gadgets for the High-Order Masking of Dilithium

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 36
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-37"
derived_asset_id: "PCM-DFA-REF-37-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[37] Improved Gadgets for the High-Order Masking of Dilithium.pdf"
source_sha256: "88e585522ab92cfcded0d33c60855115154c7a84475a0aad384506aa02e2f5ed"
pages: 36
bbox_words: 23704
consumed_bbox_words: 23704
numeric_tokens: 3193
consumed_numeric_tokens: 3193
source_blocks: 587
consumed_source_blocks: 587
emitted_blocks: 551
embedded_raster_images: 0
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 36
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

IACR Transactions on Cryptographic Hardware and Embedded Systems ISSN 2569-2925, Vol. 2023, No. 4, pp. 110–145. DOI:10.46586/tches.v2023.i4.110-145

Improved Gadgets for the High-Order Masking of Dilithium

Jean-Sébastien Coron 1 , François Gérard 1 , Matthias Trannoy 1,2 and Rina Zeitoun 2

1

University of Luxembourg, Esch-sur-Alzette, Luxembourg jean-sebastien.coron@uni.lu,francois.gerard@uni.lu 2 IDEMIA, Cryptography &amp; Security Labs, Courbevoie, France matthias.trannoy@idemia.com,rina.zeitoun@idemia.com

Abstract. We present novel and improved high-order masking gadgets for Dilithium, a post-quantum signature scheme that has been standardized by the National Institute of Standards and Technologies (NIST). Our proposed gadgets include the ShiftMod gadget, which is used for efficient arithmetic shifts and serves as a component in other masking gadgets. Additionally, we propose a new algorithm for Boolean-to-arithmetic masking conversion of a µ-bit integer x modulo any integer q, with a complexity that is independent of both µ and q. This algorithm is used in Dilithium to mask the generation of the random variable y modulo q. Moreover, we describe improved techniques for masking the Decompose function in Dilithium. Our new gadgets are proven to be secure in the t-probing model. We demonstrate the effectiveness of our countermeasures by presenting a complete high-order masked implementation of Dilithium that utilizes the improved gadgets described above. We provide practical results obtained from a C implementation and compare the performance improvements provided by our new gadgets with those of previous work.

Keywords: Lattice-based signature, Dilithium, high-order masking

1 Introduction

Dilithium signatures. The impending development of scalable quantum computers threat- ens the security of prevailing asymmetric cryptography primitives. In 1994, Shor showed that both RSA and ECC can be broken by a quantum computer in polynomial time. As a re- sult, the National Institute of Standards and Technologies (NIST) launched a competition in 2016 to select new standards for digital signature and public-key encryption/key- establishment algorithms. The competition came to a conclusion in 2022, with the announcement of CRYSTALS-Kyber for public-key encryption and CRYSTALS-Dilithium, FALCON, and SPHINCS+ for digital signature algorithms. This paper will focus on Dilithium, the primary post-quantum signature scheme standardized by NIST. Dilithium is a signature scheme based on lattice cryptography [BDK + 21]. It utilizes the “Fiat-Shamir with Aborts" technique developed by Lyubashevsky [Lyu09], which is based on rejection sampling. The security of Dilithium relies on the computational hardness of finding short vectors in lattices. NIST selected Dilithium as the primary post-quantum signature scheme due to its excellent performance and small signature size. To make implementation easier, Dilithium employs uniform sampling, as in [GLP12], rather than discrete Gaussian sampling, which would be much harder to protect against side-channel attacks.

Licensed under Creative Commons License CC-BY 4.0. Received: 2023-04-15 Accepted: 2023-06-15

Published: 2023-08-31

<!-- PDF_PAGE: 2 -->

## PDF page 2

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

111

Side-channel vulnerabilities. Like most implementations of cryptographic primitives, the Dilithium signature scheme is vulnerable to side-channel attacks. These attacks focus on exploiting physical leakage that occurs during the execution of an algorithm when run on an embedded device. Recently, Liu et al. [LZS + 21] described a side-channel attack on Dilithium that uses only a single bit of the nonce y for multiple signatures. They reduced the problem of recovering the secret key to a variant of the Integer Learning with Errors (ILWE) problem [BDE + 18] and proved that it can be solved using least squares method in polynomial time. Similarly, the authors of [MUTS22] used a profiled attack based on machine learning, targeting the secret signing nonce y for multiple signatures, followed by least-square regression and integer programming to solve a noisy linear system and recover the secret key.

The masking countermeasure. Side-channel attacks can be prevented by ensuring that any computation, and consequently any leakage, is independent of any secret the algorithm wields. At the simplest level, this can be achieved by splitting each secret variable x into shares x = x 1 ⊕ x 2 , where x 1 is a uniform random mask and x 2 = x ⊕ x 1 . By processing each share independently without recombining them, an attacker who probes only one variable through side-channel attacks will learn nothing about the secret key, since both x 1 and x 2 are uniformly distributed. More generally, [ISW03] introduced the t-probing model, where an attacker can probe up to t variables. The authors showed how to protect implementations using masks with n = 2t + 1 shares, i.e., x = x 1 ⊕ · · · ⊕ x n . More precisely, they showed how any Boolean circuit C of size |C| can be transformed into an equivalent circuit C̃ that is t-probing secure with size O(n 2 |C|). The number of shares was later reduced to n = t + 1 in [BBD + 15]. The authors introduced the (Strong) Non-Interference (SNI and NI) security notions and composability theorems so that the overall probing security of a scheme can be broken down to the security of its elementary parts. Although the generic conversion algorithm from [ISW03] can be used to make Dilithium signature generation secure against side-channel attacks, the specific operations used in lattice-based cryptography make this approach inefficient in practice. This is because lattice- based cryptography uses both arithmetic and Boolean operations, and arithmetic masking (x = x 1 + · · · + x n mod q) is preferred for arithmetic computations, while Boolean masking (x = x 1 ⊕ · · · ⊕ x n ) is used for Boolean operations, requiring frequent conversions between the two masked representations. To address this issue, efficient high-order conversion algorithms have been developed to work with any modulus q. The first high-order conversion between arithmetic and Boolean masking was described in [CGV14] for a power-of-two modulus q, for masking block-ciphers and hash functions that combine Boolean and arithmetic operations, such as SHA-1. The conversion technique from [CGV14] was then extended to any modulus q in [BBE + 18]. Additionally, [SPOG19] presented an efficient 1-bit Boolean to arithmetic conversion modulo q with a complexity of O(n 2 ). A generic conversion algorithm between arithmetic and Boolean masking was proposed in [CGMZ22], based on the randomized table countermeasure from [Cor14]. Furthermore, dedicated gadgets have been developed to handle specific operations in lattice-based encryption schemes more efficiently. For instance, [BDH + 21] and [CGMZ23] proposed specialized gadgets for masking the Kyber lattice-based encryption scheme when performing ciphertext comparison. In general, the use of lattice-based cryptography has led to the development of new dedicated gadgets to perform high-order masked computation more efficiently.

Masking Dilithium signatures. The first high-order masking of a lattice-based signature scheme was presented in [BBE + 18], which focused on masking the GLP signature scheme [GLP12]. Dilithium is a more advanced version of GLP, using the compression technique from [BG14] and additional optimizations. In [MGTF19], the authors demonstrated how to perform high-order masking of Dilithium. Furthermore, the authors presented a simplified

<!-- PDF_PAGE: 3 -->

## PDF page 3

Improved Gadgets for the High-Order Masking of Dilithium

112

version of Dilithium that used a power-of-two modulus q instead of a prime modulus, resulting in significant performance improvements for their countermeasure. In a signature generation algorithm, not all variables necessarily need to be masked. For Dilithium, the authors of [ABC + 22] revisited the sensitivity analysis presented in [MGTF19] and identified some intermediate variables that were incorrectly left unmasked in [MGTF19], which could potentially lead to the recovery of the private key. Conversely, they also showed that some other variables in [MGTF19] were unnecessarily protected. More specifically, the authors of [ABC + 22] argue that the vector w = Ay must be masked, as opposed to what was done in [MGTF19]. If left unmasked, since A is either a square matrix or has more rows than columns, the variable y can be efficiently recovered from w, which in turn enables the recovery of the secret key. On the other hand, the variable r = w − cs 2 = Az − ct can be considered public after the rejection sampling. Therefore, the computation of the hint vector h can be performed in the clear and need not be masked, as was done in [MGTF19]. In this paper, we follow the same approach as [ABC + 22]. The authors of [ABC + 22] have also proposed improved gadgets for the high-order masking of Dilithium. Specifically, they have presented an efficient high-order algorithm for performing the rejection sampling of the variables z and r̃, as well as an efficient masking technique for the Decompose function. They have argued that the variable w 1 in (w 1 , w 0 ) ← Decompose q (w) need not be masked since it is also publicly computed during signature verification. Thus, the challenge c̃ = H(M kw 1 ) need not be masked, and the Keccak hash function H need not be masked. However, this may not hold for an aborted signature, where knowledge of w 1 might reveal information to an attacker. The heuristic assumption (also used in [BBE + 18] and [MGTF19]) is that revealing the commitment w 1 of the aborted transcript does not compromise the security of the scheme. Recently, this assumption has been analyzed in [DFPS23] and shown to hold unconditionally by providing an efficient simulator for all transcripts, including aborted ones. Therefore, in this work, we adopt the same approach. Finally, the authors considered the masking of both deterministic Dilithium and randomized Dilithium. In this paper, for simplicity we only consider the masking of randomized Dilithium, since as demonstrated in [ABC + 22] its masking is significantly more efficient.

Our contributions. We describe improved high-order gadgets for the masking of Dilithium, with a proof of security in the t-probing model. Additionally, we provide an implementation to demonstrate the effectiveness of our countermeasures. More specifically:

• We introduce a new gadget called ShiftMod in Section 3.1 that allows for efficient arithmetic shifts. Compared to previous works such as [CGMZ22], our ShiftMod algorithm is more versatile since it can handle any integer modulus 2q instead of just 2 k . Our new gadget is particularly useful in the context of Dilithium, where we utilize it to develop a fast Boolean-to-arithmetic modulo q conversion, as well as a faster masking of the Decompose function (discussed below). Additionally, we can replace the arithmetic shift gadgets (Shift1 and Shift2) from [CGMZ22] with our ShiftMod algorithm, which is more efficient, to expedite the conversion from arithmetic modulo 2 k to Boolean masking.

• We propose a new algorithm to convert a µ-bit integer x from Boolean to arithmetic masking modulo any integer q, which is used in Dilithium for generating an arithmetic sharing of the random variable y modulo q. Unlike existing state-of-the-art methods, our algorithm exhibits a complexity that is independent of both the bit-size µ and the modulus q, assuming an arithmetic operation modulo q has a unit cost. Our approach builds upon the work of [BCZ18], which was limited to power-of-two moduli, and extends it to handle arbitrary moduli q. As in [BCZ18], the complexity of our

<!-- PDF_PAGE: 4 -->

## PDF page 4

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

113

algorithm is O(2 n ), which is exponential in the number of shares n but independent of the modulus size. For small values of n and large enough µ, our method is also significantly faster than alternative techniques such as [BBE + 18] and [SPOG19].

Our technique first applies [BCZ18] for a well-chosen modulus 2 k , and then performs a modulus switching of the arithmetic shares from modulo 2 k to modulo q. However, such modulus switching can introduce a small error e. To address this, we utilize our previous ShiftMod algorithm to remove the error e and obtain an exact conversion.

• For masking the Decompose algorithm of Dilithium, we improve the two existing approaches introduced in [ABC + 22]. Firstly, we expand on the first approach based on the Compress function of Kyber, by providing an alternative description of the Decompose procedure used in Dilithium, and a more efficient masking based on our ShiftMod algorithm. We also extend the second approach to cover any α = (q − 1)/δ, whereas in [ABC + 22], a power-of-two δ was required. Furthermore, we compare the two approaches and show that the first approach is more efficient in practice.

Finally, we present a complete high-order masked implementation of Dilithium, uti- lizing the improved gadgets described above. We provide the practical results of a C implementation and compare the performance improvement provided by our new gadgets with those from [BBE + 18], [SPOG19], and [ABC + 22]. For a non-bitsliced implementation, our techniques achieve a significant speedup compared to previous work. In particular, our new Boolean-to-arithmetic masking algorithm leads to a substantial improvement over the techniques presented in [SPOG19] and [BBE + 18]. Our improved approaches for masking the Decompose algorithm of Dilithium also provides better efficiency than the ones presented in [ABC + 22]. The plain C code is publicly available at

https://github.com/fragerar/Masked_Dilithium

Comparison with [ABC + 22]. In the following, we provide a more detailed comparison of our contributions with those of [ABC + 22]. Note that [ABC + 22] also describes a leveled approach combining the shuffling countermeasure with masking, which offers significantly better performances, but without the guarantee of t-probing security. Here we only consider the fully masked implementation from [ABC + 22]. As previously mentioned, we use the same global masking strategy as in [ABC + 22], which involves masking the same variables and keeping the same variables unmasked. Regarding the generation of the signing nonce y, the authors of [ABC + 22] rely on the Boolean to arithmetic conversion from [BBE + 18], with the bitsliced implementation from [BC22], while we use our new Boolean to arithmetic conversion algorithm from Section 4. Although our algorithm has a complexity independent from the bit-size of y and q, it is not compatible with bitslicing. Similarly, for the masking of Decompose, we describe improved gadgets in Section 5, which can leverage our more lightweight ShiftMod arithmetic shift algorithm. Our ShiftMod gadget is more efficient compared to the heavier arithmetic to Boolean conversion from [BBE + 18] used in [ABC + 22], but it is not compatible with bitslicing. Moreover, the authors of [ABC + 22] provide a complete benchmark for an ARM Cortex-M4 microcontroller for the full signature generation, while we only provide a C implementation for laptop execution. However, we provide a public implementation, whereas the source code for [ABC + 22] is not available. In summary, the main difference with [ABC + 22] is that we provide more efficient gadgets for a non-bitsliced implementation, whereas [ABC + 22] use more standard gadgets for which they can leverage the state-of-the-art bitsliced implementation from [BC22]. We provide in Section 7.1 a high-level comparison with the bitsliced approach of [BC22] for the high-order Boolean to arithmetic conversion modulo q.

<!-- PDF_PAGE: 5 -->

## PDF page 5

Improved Gadgets for the High-Order Masking of Dilithium

114

Notations and security definitions

2

### 2.1 Notations

We adopt the same notations as the Dilithium specifications [BDK + 21]. Let Z q denote the ring of integers modulo q. We will use both the positive representation of elements in Z q (i.e., Z q ≃ {0, . . . , q − 1}) and the centered representation (i.e., Z q ≃ {−(q − 1)/2, . . . , 0, . . . , (q − 1)/2} for odd q and Z q ≃ {−(q/2) + 1, . . . , 0, . . . , q/2} for even q). For x ∈ Z, we denote by x mod + q (resp. x mod ± q) the positive (resp. centered) representative of x modulo q. 256 We define the polynomial quotient rings + 1) and R q = Z q [X]/(X 256 + P R (i) = Z[X]/(X i z X ∈ R q is denoted by kzk ∞ and defined as 1). The infinity norm of an element z = follows:

kzk ∞ = max |z (i) mod ± q|

0≤i&lt;256

We use bold lower-case letters to represent column vectors with coefficients in R or R q . For a vector of polynomials z = (z 1 , . . . , z k ) ∈ R q k , the infinity norm is defined as kzk ∞ = max 1≤i≤k kz i k ∞ . The centered ball of radius η is denoted by S η and consists of elements w ∈ R such that kwk ∞ ≤ η, or equivalently, polynomials of R with coefficients in the range [−η, η]. Finally, we denote by S̃ η the polynomials of R with coefficients in the range ] − η, η].

### 2.2 Security definitions

In the following, we review the Non-Interference (NI) and Strong Non-Interference (SNI) security notions proposed in [BBD + 16], along with the stronger free-SNI notion introduced in [CS21]. These security notions are particularly useful for demonstrating probing security against attackers who can only probe a limited number of variables. In fact, by using composition theorems established in [BBD + 16], we can prove that an algorithm achieves probing security by breaking it down into smaller gadgets for which we individually prove either NI or SNI security.

Definition 1 (t-NI security). Let G be a gadget taking as input n shares (a 1 , . . . , a n ) and outputting n shares (b 1 , . . . , b n ). The gadget G is said to be t-NI secure if for any set of t 1 ≤ t probed variables there exists a subset of input indices I ⊂ [1, n] such that the t 1 probed variables can be perfectly simulated from a |I , with |I| ≤ t 1 .

Definition 2 (t-SNI security). Let G be a gadget taking as input n shares (a 1 , . . . , a n ) and outputting n shares (b 1 , . . . , b n ). The gadget G is said to be t-SNI secure if for any set of t 1 intermediate variables and any subset O ⊂ [1, n] of output indices such that t 1 + |O| ≤ t, there exists a subset of input indices I ⊂ [1, n] such that the t 1 intermediate variables and the outputs b |O can be perfectly simulated from a |I , with |I| ≤ t 1 .

The NI and SNI notions differ in the number of input shares required for the simulation. In the SNI case, this number is upper-bounded by the number of internal probes in the gadget. In contrast, for the NI notion, it is only bounded by the total number of probes, including the probes on the output shares. Finally, we also review the free-SNI notion introduced in [CS21]. This notion is stronger than the SNI notion, as a subset of the output shares can be perfectly simulated from a subset of the input shares, and all other output shares, except one, can be simulated using fresh uniform randoms.

Definition 3 (Free-t-SNI security). Let G be a gadget taking as input n shares (a i ) 1≤i≤n and outputting n shares (b i ) 1≤i≤n . The gadget G is said to be free t-SNI secure if for any set of t 1 ≤ t probed intermediate variables, there exists a subset I of input indices

<!-- PDF_PAGE: 6 -->

## PDF page 6

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

115

with |I| ≤ t 1 , such that the t 1 intermediate variables and the output variables b |I can be perfectly simulated from a |I , while for any O ( [1, n] \ I the output variables in b |O are uniformly and independently distributed, conditioned on the probed variables and b |I .

We recall in Appendix A.2 the mask refreshing algorithm RefreshMasks. The algorithm was proven (n − 1)-SNI in [BBD + 16]. The lemma below shows that it also satisfies the stronger free-SNI property.

Lemma 1 ([CS21]). The RefreshMasks algorithm is free-(n − 1)-SNI.

For masking Dilithium, the shares must be eventually recombined to output the signature in the clear. For this we use the extended notion of NI security from [BBE + 18, Definition 7], in which the output b of the gadget is given to the simulator.

Definition 4 (t-NIo security [BBE + 18]). Let G be a gadget taking as input (x i ) 1≤i≤n and outputting b. The gadget G is said t-NIo secure if for any set of t 1 ≤ t intermediate variables, there exists a subset I of input indices with |I| ≤ t 1 , such that the t 1 intermediate variables can be perfectly simulated from x |I and b.

To satisfy this definition when the output shares of a gadget need to be recombined with a public output, as shown in [CGMZ23, Appendix B.2], one can apply the free-SNI Refreshmasks algorithm and eventually recombine the shares.

3

Arithmetic shift and conversion from arithmetic to Boo- lean masking

In this section, we introduce a novel gadget called ShiftMod that enables efficient arithmetic shifts modulo any integer. The purpose of this gadget is to generate an arithmetic sharing of bx/2c modulo q, given an arithmetic sharing of x modulo 2q. We provide a detailed description of the properties of ShiftMod in Section 3.1. Compared to the arithmetic shift gadgets introduced in [CGMZ22], our ShiftMod algorithm is more versatile as it can operate modulo any integer 2q, not just 2 k . This enables the development of other gadgets for the masking of Dilithium, such as a fast Boolean-to-arithmetic modulo q conversion algorithm, which is detailed in Section 4. This conversion algorithm is crucial in generating an arithmetic sharing of the random polynomial y modulo q in Dilithium. Moreover, we also utilize ShiftMod to improve the masking of the Decompose function in Dilithium, as described in Section 5. Additionally, we demonstrate that our ShiftMod algorithm can be applied to expedite the conversion from arithmetic modulo 2 k to Boolean masking, even though this conversion is not directly used in our masking of Dilithium. For this, we utilize the same technique presented in [CGMZ22]. We apply a sequence of arithmetic shifts starting from x modulo 2 k , and extract the least significant bit of bx/2 i c at each step. This ultimately yields a Boolean masking of x. By employing our new ShiftMod gadget, we achieve significant improvements in conversion efficiency compared to the two arithmetic shift gadgets (Shift1 and Shift2) proposed in [CGMZ22].

### 3.1 New arithmetic shift modulo 2q

We consider an arbitrary integer q. Given as input an arithmetic sharing of x = x 1 +· · ·+x n (mod 2q), our new ShiftMod gadget high-order computes the shift:

j x k

a = =

2

x − (x mod 2) 2

(mod q)

(1)

<!-- PDF_PAGE: 7 -->

## PDF page 7

Improved Gadgets for the High-Order Masking of Dilithium

116

and returns an arithmetic sharing of a = a 1 +· · ·+a n (mod q), without leaking information about x. Our ShiftMod algorithm relies on a 1-bit Boolean-to-arithmetic conversion gadget, with the most efficient one being the 1bitB2A gadget from [SPOG19], which is proven SNI. However, to use this gadget in our ShiftMod algorithm, we require a slightly stronger property than SNI, namely free-SNI (see Definition 3). One approach to achieving free-SNI is to compose the 1bitB2A gadget from [SPOG19] with the RefreshMasks algorithm, as it achieves this property (see Lemma 1). However, we demonstrate that a minor modification to the 1bitB2A gadget directly achieves the free-SNI property, eliminating the need for RefreshMasks. This modification results in a more efficient ShiftMod algorithm. To high-order compute (1), the first step is to obtain an arithmetic masking modulo 2q of y = (x mod 2). For this, we consider the least significant bits b i of x i for 1 ≤ i ≤ n, and we perform a Boolean to arithmetic modulo 2q conversion of the shares b i , using the 1bitB2A algorithm from [SPOG19], which we recall in Section 3.2 (see Alg. 2). This gives:

y 1 + · · · + y n = b 1 ⊕ · · · ⊕ b n = (x mod 2)

(mod 2q)

In the second step, we high-order compute z = x − (x mod 2) (mod 2q) by letting z i = x i − y i mod 2q for all 1 ≤ i ≤ n. To high-order compute a = z/2 mod q, our technique is to obtain a new arithmetic sharing of z such that z i = 0 (mod 2) for all 1 ≤ i ≤ n; then we can simply divide by 2 each share z i independently. For this, we do a loop for i = 1 to n − 1, and we let z n ← z n + (z i mod 2) mod 2q, and z i ← z i − (z i mod 2) mod 2q. At the end of the loop, the shares z i still encode the same integer z, and all the shares z i are even. This is true by construction of the updated z i ’s for 1 ≤ i ≤ n − 1, and this must also be true for z n because z = 0 (mod 2). Therefore, we can eventually let a i = z i /2 for all 1 ≤ i ≤ n, which gives an arithmetic sharing modulo q of a = bx/2c (mod q). We obtain the following ShiftMod algorithm depicted in Algorithm 1. Note that the ShiftMod algorithm we propose can handle any integer q, including those for which gcd(q, 2) 6 = 1. As a result, computing a = z/2 mod q using high-order methods is not as simple as multiplying the shares z i of z by 2 −1 mod q. In particular, to perform an arithmetic shift by k bits, we will use the ShiftMod gadget iteratively with moduli of the form q = 2 i · p for i decreasing from k to 1. Therefore, we cannot assume gcd(q, 2) = 1.

Algorithm 1 ShiftMod Input: A modulus q 0 = 2q and x 1 , . . . , x n ∈ Z 2q Output: a 1 , . . . , a n ∈ Z q such that a 1 + · · · + a n = b(x 1 + · · · + x n )/2c (mod q)

1: for i = 1 to n do b i ← x i &amp; 1

2: (y 1 , . . . , y n ) ← 1bitB2A(2q, (b 1 , . . . , b n )) 3: for i = 1 to n do z i ← x i − y i mod 2q 4: for i = 1 to n − 1 do 5: z n ← z n + (z i &amp; 1) mod 2q 6: z i ← z i − (z i &amp; 1) mod 2q 7: end for

8: for i = 1 to n do a i ← z i 1 9: return a 1 , . . . , a n

Complexity. We recall the 1bitB2A algorithm in Section 3.2, and show that its number of elementary operations is T 1bitB2A (n) = 2n 2 + 4n − 6. The number of operations of ShiftMod is then T ShiftMod (n) = n + T 1bitB2A (n) + n + 3(n − 1) + n = 2n 2 + 10n − 9, assuming that operations modulo q have unit cost. The complexity is therefore 2n 2 + O(n), which is significantly better than the previous Shift1 and Shift2 algorithms from [CGMZ22], which

<!-- PDF_PAGE: 8 -->

## PDF page 8

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

117

have complexity 2n 3 and 20n 2 respectively (neglecting low-order terms). Therefore, the resulting arithmetic to Boolean conversion algorithm will be significantly more efficient (see Section 3.3). Moreover, our ShiftMod gadget is more general, as it can work modulo any integer 2q, instead of modulo 2 k only for Shift1 and Shift2.

Security. To prove the t-NI property of the ShiftMod algorithm above, it is sufficient to prove that after Line 3, we can perfectly simulate all variables (z i &amp; 1) for 1 ≤ i ≤ n, since the other operations (except 1bitB2A) compute the shares independently for each i. For this, it is sufficient to show that after Line P 3, all output shares z i except one can n be perfectly simulated; then, using the relation i=1 z i = 0 (mod 2), we can perfectly simulate all variables (z i &amp; 1) for 1 ≤ i ≤ n as required. For this, we crucially use the free-SNI property of 1bitB2A, which implies that for any subset O ( [1, n] \ I, the variables y |O are uniformly and independently distributed. Then such variables y i can play the role of a one-time-pad at Line 3 with respect to the variables x i for i ∈ / I, and therefore all variables z i except one can be perfectly simulated, as required. As required, we prove the free-SNI property of the 1bitB2A gadget from [SPOG19] in Section 3.2. As explained previously, without the free-SNI property of 1bitB2A, a full mask refreshing of the shares z i would have been required after Line 3, to get the free-SNI property of the composition (see Lemma 1). This would have added a term 3n 2 /2 in the number of operations of ShiftMod, which would then be 7n 2 /2 instead of 2n 2 (neglecting low order terms).

Theorem 1. The ShiftMod algorithm achieves the NI property, if the 1bitB2A algorithm achieves the free-SNI property.

Proof. We provide a proof based on simulation, namely, given any set of t probes, one constructs iteratively a subset I of indices of the input shares x i that are sufficient to simulate the t probes. Then by ensuring |I| ≤ t, we will deduce that the simulation can be performed without knowing the original variable x when t &lt; n. We let t 1 be the variables probed everywhere in the algorithm apart from 1bitB2A and t 2 the probed variables in 1bitB2A, such that t = t 1 + t 2 . In the following, we assume that t &lt; n, otherwise we can trivially simulate all probes with I = [1, n], which amounts to knowing x. We describe hereafter the construction of the set I ⊂ [1, n] initially empty. More precisely, we let I = J ∪ U and we describe the construction of the sets J and U . For every probed variable x i , b i , y i , z i or a i , we add i to J. For every probed variable z n,i corresponding to the result variable z n at loop i, we add n to J. Furthermore, the set U is constructed from the free-SNI property of 1bitB2A (Theorem 2) which allows to simulate the t 2 probed intermediate variables in 1bitB2A and the output variables y |U from a set U of indices where |U | ≤ t 2 . By construction, since one has added at most one index per probed variable in J, we have |J| ≤ t 1 . This gives |I| = |J ∪ U | ≤ t 1 + t 2 = t as required. The simulation of the probed variables is done as follows: if x i or b i is probed, then it can perfectly be simulated from the knowledge of x i since i ∈ J ⊂ I by construction. Then, for i ∈ U , the output variables y i are simulated from the free-SNI property of 1bitB2A. In the case where i ∈ / U , because we have t &lt; n, we know that there is at least one index i ? which does not belong to I. Therefore, the free-SNI property of 1bitB2A allows us to construct a set of output indices O = [1, n] \ (U ∪ {i ? }) ( [1, n] \ U such that the variables y |O are uniformly and independently distributed. Therefore, the variables y i such that i ∈ J \ U can be simulated by generating random values. The remaining variables y i , namely with i ∈ / I, can play the role of a one-time-pad at line 3 of ShiftMod with respect to the variables x i for i ∈ / I, and therefore all variables z i except z i ? at Line 3 can be perfectly simulated. The simulation continues as follows: any probed variable z i or z i &amp; 1 with 1 ≤ i ≤ n − 1 in the For loop, can be perfectly simulated as shown right above, since one has at most n − 1 such probes.

<!-- PDF_PAGE: 9 -->

## PDF page 9

Improved Gadgets for the High-Order Masking of Dilithium

118

It remains to perfectly simulate any probed intermediate variable z n,i for any i when n ∈ I. To this aim, we use the fact that the only values which enter into the computation of z n,i are the first z n value (namely z n,0 ), and the least significant bit of all z i ’s (namely z i &amp; 1 for 1 ≤ i ≤ n). Since we can perfectly simulate n − 1 variables z i and because we know that the sum of all z i ’s is even, L we can deduce the least significant bit of the unknown value z i ? , namely z i ? &amp; 1 = i6 = i ? (z i &amp; 1). Thus, we have shown that we can perfectly simulate any probed intermediate variable z n,i , including the output result z n at the end of the For loop. Eventually, the probed variable a i can also be directly computed from z i above since i ∈ I by construction, which concludes the proof.

1-bit Boolean to arithmetic conversion from [SPOG19]

3.2

In this section, we recall the 1-bit Boolean to arithmetic conversion algorithm 1bitB2A from [SPOG19], which is used in our ShiftMod algorithm above. This algorithm is currently the most efficient of its kind and has the same asymptotic complexity O(n 2 ) for n shares as the table-based algorithm from [CGMZ22], but with a better concrete complexity. We will demonstrate that with some minor modifications, the [SPOG19] algorithm can achieve the free-SNI property required for our ShiftMod gadget. For any integer q, the algorithm takes as input n shares x i ∈ {0, 1} and outputs n arithmetic shares y i ∈ Z q such that y 1 + · · · + y n = x 1 ⊕ · · · ⊕ x n (mod q). It works as follows. Assume that we have a n-shared encoding (y 1 , . . . , y n ) modulo q of a bit b ∈ {0, 1}, that is b = y 1 + · · · + y n (mod q). Then, we can easily compute an encoding of b̄ = 1 − b, simply by letting y 1 ← 1 − y 1 mod q and y i ← −y i mod q for all 2 ≤ i ≤ n. Using this technique, starting from an encoding (y 1 , . . . , y n ) of 0, we can iteratively process the input bits x i , and eventually obtain an encoding (y 1 , . . . , y n ) such that y 1 +· · ·+y n = x 1 ⊕· · ·⊕x n (mod q) as required. For security, we must refresh the shares y j after the processing of each x i . One uses a mask refreshing LinearRefresh that accumulates the randomness on the last share; we recall its description in Appendix A.1. As an optimization, instead of starting with n shares y j , it is actually more efficient to progressively increase the number of shares, from a single share to n shares. We recall the corresponding algorithm from [SPOG19] in Alg. 2 below. To facilitate the writing of our security proof of the free-SNI property, we include a minor modification. Namely, we start the processing of the input Boolean shares with x 2 , instead of x 1 ; we then process the remaining shares x 3 , . . . , x n , and eventually x n+1 = x 1 . Moreover, the last LinearRefresh is performed with reversed inputs, so that the randomness is accumulated on v 1 instead of v n . This cyclic shift of the inputs is to ensure that after the processing of x i , the randomness in LinearRefresh is always accumulated on the i-th column.

Algorithm 2 1bitB2A [SPOG19] Input: x 1 , . . . , x n ∈ {0, 1} Output: v 1 , . . . , v n ∈ Z q such that v 1 + · · · + v n mod q = x 1 ⊕ · · · ⊕ x n

1: x n+1 ← x 1 , v 1 ← x 2 2: for i = 2 to n do 3: (v 1 , . . . , v i ) ← LinearRefresh Z q (v 1 , . . . , v i−1 , 0) 4: (v 1 , . . . , v i ) ← (1 − 2x i+1 ) · (v 1 , . . . , v i ) mod q

5: v 1 ← v 1 + x i+1 mod q 6: end for 7: (v n , . . . , v 1 ) ← LinearRefresh Z q (v n , . . . , v 1 )

8: return (v 1 , . . . , v n )

. v 1 = x 2 (mod q)

P i

j=1 v i = x 2 ⊕ · · · ⊕ x i+1 (mod q)

.

<!-- PDF_PAGE: 10 -->

## PDF page 10

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

119

Complexity. The number of operations of LinearRefresh is 3i − 3 for i shares. Therefore, P n the total number of operations is T 1bitB2A (n) = i=2 (3i − 3 + i + 2) + 3n − 3 = 2n 2 + 4n − 6. More generally, to convert k-bit of Boolean masking into arithmetic masking, the complexity is T B2A (k, n) = k · (4n + T 1bitB2A (n)) = k · (2n 2 + 8n − 6).

Security. Algorithm 2 is already proven SNI in [SPOG19]. With Theorem 2, we prove a slightly stronger property, namely the free-SNI property (see Def. 3); we provide the proof in Appendix B. As explained previously, this enables to obtain a better asymptotic complexity for our ShiftMod algorithm.

Theorem 2 (free-SNI of 1bitB2A). For any set of t probes, there exists a subset I with |I| ≤ t, such that those t probes and v |I can be perfectly simulated. Moreover the shares in v |O are uniformly and independently distributed for any O ( [1, n] \ I, even conditioned on the probes and v |I .

Improved arithmetic to Boolean conversion

3.3

Finally, we show how to use our ShiftMod gadget for faster conversion from arithmetic to Boolean masking. Namely, in [CGMZ22], the authors described the arithmetic to Boolean conversion algorithm below, based on a generic high-order 1-bit arithmetic Shift, working modulo 2 k . Therefore, in the algorithm below, we can replace the Shift1 or Shift2 algorithms from [CGMZ22] by our improved ShiftMod gadget form Section 3.1. In that case, the ShiftMod algorithm takes as input a modulus q 0 = 2 k−j = 2q.

Algorithm 3 ArithmeticToBoolean (ABoptiNI) [CGMZ22] Input: k ∈ N + and z 1 , . . . , z n ∈ Z 2 k Output: s 1 , . . . , s n ∈ {0, 1} k such that s 1 ⊕ · · · ⊕ s n = z 1 + · · · + z n mod 2 k

1: for i = 1 to n do s i ← 0 2: for j = 0 to k − 1 do 3: for i = 1 to n do s i ← s i + ((z i &amp; 1) j) 4: (z 1 , . . . , z n ) ← ShiftMod(2 k−j , (z 1 , . . . , z n ))

5: end for 6: return s 1 , . . . , s n

Complexity. The complexity is T AB (n, k) = k · (3n + T shift (n)). Therefore, with the ShiftMod algorithm, the complexity is T AB (n, k) = k · (2n 2 + 13n − 9). The complexity is therefore 2kn 2 + O(kn), instead of 2kn 3 and 20kn 2 with Shift1 and Shift2 respectively (neglecting low-order terms). We provide a comparison in Table 1 below. We see that our new algorithm outperforms [CGV14] for security order t ≥ 4.

Theorem 3 (t − NI security of ABoptiNI). For any set of t intermediate variables, there exists a subset of input indices I ⊂ [1, n] such that the t intermediate variables can be perfectly simulated from inputs z |I , with |I| ≤ t.

Proof. The proof is straightforward as Algorithm 3 is the composition of the t−NI ShiftMod algorithm with sharewise operations.

<!-- PDF_PAGE: 11 -->

## PDF page 11

Improved Gadgets for the High-Order Masking of Dilithium

120

Table 1: Operation count for arithmetic modulo 2 k to k-bit Boolean conversion algorithms, up to security order t = 12, with n = t + 1 shares and k = 32.

A mod 2 32 → B

1 165

2 3 4

Goubin [Gou01] [CGV14] 32 → 32 Alg. 3 with Shift1 Alg. 3 with Shift2 Alg. 3 with ShiftMod

1 132 2 496 3 872 1 536

4

Security order t 5 6

8 10 12

2 070 4 030 6 218 8 597 15 053 23 655 33 572 5 248 9 600 15 936 24 640 50 688 90 816 148 096 7 520 12 448 18 656 26 144 44 960 68 896 97 952 2 400 3 392 4 512 5 760 8 640 12 032 15 936

Boolean to arithmetic conversion modulo q with size- independent complexity

In this section, we introduce a new algorithm that converts a µ-bit integer x from Boolean to arithmetic masking modulo any integer q. This conversion is used in Dilithium to generate an arithmetic sharing of the variable y modulo q. Currently, the state of the art method involves applying the 1-bit Boolean to arithmetic conversion algorithm from [SPOG19] µ times, resulting in a complexity of O(n 2 · µ). Alternatively, one can use the Boolean to arithmetic conversion algorithm from [BBE + 18], which has a complexity of O(n 2 · log q), or even O(n 2 · log log q) using the Kogge-Stone adder as in [CGTV15]. Our contribution is to describe a Boolean to arithmetic conversion algorithms with complexity independent of both the bitsize µ and the modulus q. We assume that an arithmetic operation modulo q has a unit cost. We build on the work of [BCZ18], which described a µ-bit Boolean to arithmetic modulo 2 k conversion algorithm with complexity O(2 n ), exponential in the number of shares n, but independent of the bitsize µ and the register size k. For small values of n, this method is at least one order of magnitude faster than alternative techniques. We generalize this algorithm to any modulus q, and as in [BCZ18], we obtain a significant improvement for small n values, for large enough µ as in Dilithium. We start with an approximate algorithm that can induce a small error e in the conversion, based on modulus switching. For this, we first apply the conversion of [BCZ18] from a µ-bit Boolean masking into an arithmetic modulo 2 k masking, for a certain parameter k ≥ µ. In a second step, we convert from arithmetic masking modulo 2 k to modulo q, using modulus switching, with complexity O(n). To obtain an exact algorithm, we show how to remove the small error e from the approximate algorithm, using our ShiftMod gadget from Section 3.1, with additional complexity O(n 2 log n). The total complexity remains O(2 n ) and is independent of the modulus size as in [BCZ18]. In summary, our new algorithm works for any modulus q, whereas [BCZ18] only worked for a power-of-two modulus. In the context of Dilithium, we must generate an arithmetically masked polynomial y modulo q, with randomly distributed coefficients in ] − γ 1 , γ 1 ], with γ 1 = 2 17 for security level 2. Therefore, for each coefficient, we first generate a random µ-bit Boolean masked x, simply by generating n uniformly random µ-bit Boolean shares. By applying our exact conversion algorithm, we obtain an arithmetically masked x modulo q, with uniform distribution in [0, 2 µ [. Therefore, we set µ = 18, and we subtract γ 1 − 1 = 2 17 − 1 from the first share to obtain the required uniform distribution in ] − γ 1 , γ 1 ].

### 4.1 Tool: modulus switching

We begin by introducing our primary method: modulus switching over arithmetic shares. This technique was already used in [CGMZ23] to mask the Compress function of Kyber.

<!-- PDF_PAGE: 12 -->

## PDF page 12

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

121

In this section, we provide an analysis of the fundamental modulus switching approach. Specifically, we examine the error that arises when n arithmetic shares are switched from a modulus p 1 to a modulus p 2 . We demonstrate that the error e is confined within the range of 0 ≤ e ≤ n − 1.

Algorithm 4 Modulus switching (ModSwitch) Input: p 1 , p 2 ∈ N, an arithmetic masking x 1 , . . . , x n ∈ Z p 1 such that x = x 1 + · · · + x n (mod p 1 ). Output: y 1 , . . . , y n ∈ Z p 2 such that y 1 + · · · + y n = bx · p 2 /p 1 c + e mod p 2 , for 0 ≤ e &lt; n.

1: for i = 1 to n do y i ← bx i · p 2 /p 1 c mod p 2 2: y 1 ← y 1 + (n − 1) mod p 2 3: return (y 1 , . . . , y n )

Lemma 2. Let p 1 and p 2 be two positive integers. Let x i ∈ Z p 1 for 1 ≤ i ≤ n and let x = x 1 + · · · + x n (mod p 1 ). Let y 1 , . . . , y n be the output of ModSwitch. Then: x · p 2 + e (mod p 2 ) (2) y 1 + · · · + y n = p 1

for some 0 ≤ e ≤ n − 1.

Proof. We write x = x 1 + · · · + x n − λ · p 1 for some λ ∈ Z, so we can write:

n X x · p 2 x i · p 2 = − λ · p 2 p 1 p 1 i=1

For 1 ≤ i ≤ n, we can write by Euclidean division x i · p 2 = p 1 · bx i · p 2 /p 1 c + r i with 0 ≤ r i &lt; p 1 , and similarly x · p 2 = p 1 · bx · p 2 /p 1 c + r with 0 ≤ r &lt; p 1 . This gives: X X n n x · p 2 x i · p 2 r i r = + − − λ · p 2 p 1 p 1 p p 1 i=1 i=1 1

P n P n Moreover, p 1 ), we must have r = i=1 r i (mod p 1 ), and therefore P n since 0 x = i=1 x i (mod r = i=1 r i − e · p 1 for some e 0 ∈ Z, with 0 ≤ e 0 ≤ n − 1. This gives: n X x i · p 2 x · p 2 = + e 0 − λ · p 2 p 1 p 1 i=1

= y 1 + · · · + y n − (n − 1) + e 0 − λ · p 2

Finally, by letting e = (n − 1) − e 0 and after reduction modulo p 2 , we obtain (2).

Approximate conversion using modulus switching

4.2

In the following we describe an approximate conversion algorithm based on modulus switching that can induce a small error e in the conversion. More precisely, we are given as input a Boolean masking of x, such that 0 ≤ x &lt; 2 µ , with x = u 1 ⊕ · · · ⊕ u n . Our goal is to obtain an arithmetic masking of x + e modulo q, for a small error e ∈ Z with 0 ≤ e ≤ n − 1: y 1 + · · · + y n = x + e (mod q)

We assume that µ and the modulus q are fixed (for example, µ = 18 and q = 2 23 − 2 13 + 1 in Dilithium). Note that we can get a centered error by letting y 1 0 := y 1 − bn/2c, which gives |e 0 | ≤ bn/2c.

<!-- PDF_PAGE: 13 -->

## PDF page 13

Improved Gadgets for the High-Order Masking of Dilithium

122

We first apply the [BCZ18] Boolean to arithmetic conversion algorithm, which gives x = x 1 + · · · + x n (mod 2 k ), for a parameter k that will be determined later. We then apply Lemma 2 by performing a modulus switching from the modulus p 1 = 2 k to a new modulus p 2 = a · q, for some integer a that will also be determined later, and we reduce the shares y i directly modulo q. More precisely, given as input the shares x i modulo 2 k such that x = x 1 + · · · + x n (mod 2 k ), we compute for 1 ≤ i ≤ n:

j x · a · q k

y i =

i

2 k

mod q

and y 1 ← y 1 + (n − 1), as in Lemma 2. After reduction modulo q, from (2) we obtain for some 0 ≤ e ≤ n − 1: j x · a · q k y 1 + · · · + y n = + e (mod q) (3) 2 k

Equation (3) is not sufficient for our purposes as, due to the modulus switching, it only gives us an arithmetic sharing modulo q of bx · a · q/2 k c instead of x. To address this issue, we use a trick: we select an integer a such that a · q is very close to 2 k , which allows us to obtain the correct value of x. More precisely, our goal is now to ensure that for any 0 ≤ x &lt; 2 µ , we have

j x · a · q k

2 k

= x

(4)

which using (3) will give y 1 + · · · + y n = x + e (mod q). This is as required an arithmetic sharing of x modulo q, up to some small error e. The following lemma ensures that when the integer a · q is sufficiently close to 2 k , Equality (4) holds as the modulus switching does not change the value of x.

Lemma 3. Let k := dlog 2 qe + µ and a := d2 k /qe. Then for any 0 ≤ x &lt; 2 µ , we have bx · a · q/2 k c = x.

Proof. We must ensure that for any 0 ≤ x &lt; 2 µ , we have 0 ≤ x · a · q/2 k − x &lt; 1. It suffices to ensure that this holds for the upper-bound x = 2 µ , that is 0 ≤ 2 µ · a · q/2 k − 2 µ &lt; 1, which gives the sufficient condition 0 ≤ a · q − 2 k &lt; 2 k−µ . From a := d2 k /qe, we get 2 k = q · a − r for 0 ≤ r &lt; q, which gives 0 ≤ q · a − 2 k &lt; q. From k := dlog 2 qe + µ, we get 2 k ≥ q · 2 µ , which gives 0 ≤ q · a − 2 k &lt; q ≤ 2 k−µ as required.

This gives the following BtoA q Approx algorithm depicted in Algorithm 5. We denote by BtoAExp the Boolean to arithmetic algorithm from [BCZ18]. For Dilithium with Security Level 2, with q = 2 23 − 2 13 + 1 and µ = 18, we obtain k = 41 and a = 262 401.

Algorithm 5 Boolean to Arithmetic conversion (BtoA q Approx) Input: A modulus q, a µ-bit Boolean masking u 1 , . . . , u n such that u 1 ⊕ · · · ⊕ u n = x Output: An arithmetic sharing y 1 , . . . , y n such that y 1 + · · · + y n = x + e (mod q), for 0 ≤ e &lt; n.

1: k ← dlog 2 qe + µ 2: a ← d2 k /qe 3: x 1 , . . . , x n ← BtoAExp µ,2 k (u 1 , . . . , u n )

4: for i = 1 to n do y i ← bx i · a · q/2 k c mod q 5: y 1 ← y 1 + (n − 1) mod q

6: return (y 1 , . . . , y n )

<!-- PDF_PAGE: 14 -->

## PDF page 14

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

123

Complexity. The values k and a can be computed prior to the execution of the al- gorithm and are therefore not considered in the complexity. The number of opera- tions of BtoAExp µ,2 k using [BCZ18] is T BtoAExp = 10 · 2 n − 6n − 13. Furthermore, the For loop in Algorithm 5 costs 3n operations. Therefore the overall complexity is T BtoA q Approx = 10 · 2 n − 6n − 13 + 3n = 10 · 2 n − 3n − 13 and asymptotically the number of operation is O(2 n ). As in [BCZ18], this number of operations is exponential in n, but independent from the size of the modulus q.

Lemma 4. The BtoA q Approx algorithm is (n − 1)-SNI.

Proof. The BtoA q Approx algorithm is the composition of the BtoAExp algorithm which is (n − 1)-SNI, followed by independent operations on each shares. The resulted algorithm is therefore (n − 1)-SNI.

Exact conversion using modulus switching

4.3

The drawback of the previous approach is that we get an error e in the arithmetic masking of x modulo q. In this section, we show how to get rid of the error e, by using the ShiftMod algorithm from Section 3.1. As previously, we consider a µ-bit Boolean masking of x with x = u 1 ⊕ · · · ⊕ u n , and our goal is to obtain an arithmetic masking of x modulo q, but with no error:

z 1 + · · · + z n = x

(mod q)

As previously, we assume that the bit-size µ and the modulus q are fixed. We let α := dlog 2 ne. Starting from the Boolean shares u i of x, we consider the shifted shares u 0 i := u i α of x 0 = 2 α · x, of bit-size µ 0 = µ + α. We also consider the modulus q 0 := 2 α · q. We apply the previous BtoA q Approx algorithm (Alg. 5) with parameters µ 0 and q 0 , with the shares u 0 i as input. This provides an arithmetic masking of x 0 = 2 α · x modulo q 0 , with an error 0 ≤ e ≤ n − 1:

y 1 + · · · + y n = 2 α · x + e (mod q 0 )

Since we are working modulo q 0 = 2 α · q, we can then iterate the ShiftMod algorithm (Alg. 1) α times, and since by definition 0 ≤ e ≤ n − 1 &lt; 2 α , we get rid of the error e and obtain an arithmetic masking of x modulo q as required: y 1 + · · · + y n z 1 + · · · + z n = = x (mod q) 2 α

This gives the following BtoA q Exact algorithm depicted in Algorithm 6.

Algorithm 6 Boolean to Arithmetic conversion (BtoA q Exact) Input: A modulus q, a µ-bit Boolean masking x 1 , . . . , x n such that u 1 ⊕ · · · ⊕ u n = x Output: An arithmetic sharing y 1 , . . . , y n such that y 1 + · · · + y n = x mod q

1: α ← dlog 2 ne, k ← dlog 2 qe + µ + α, q 0 ← 2 α · q, a ← d2 k /qe. 2: x 1 , . . . , x n ← BtoAExp µ,2 k (u 1 , . . . , u n )

3: for i = 1 to n do y i ← (x i · a · q)/2 k−α mod q 0 4: y 1 ← y 1 + n − 1 5: for i = 0 to α − 1 do (y 1 , . . . , y n ) ← ShiftMod(2 α−i · q, (y 1 , . . . , y n ))

6: return (y 1 , . . . , y n )

Note that for simplicity, in the algorithm above, we actually run the initial BtoAExp algorithm from [BCZ18] directly with the input Boolean shares u i instead of u 0 i , to get

<!-- PDF_PAGE: 15 -->

## PDF page 15

Improved Gadgets for the High-Order Masking of Dilithium

124

an arithmetic sharing of x = x 1 + · · · + x n (mod 2 k ), and then use x 0 i = 2 α · x i for all i, which gives an arithmetic sharing of x 0 = 2 α · x modulo 2 k+α . Therefore we must have k 0 = k + α, where k 0 = dlog 2 q 0 e + µ 0 is the parameter used in Alg. 5, which gives 0 k = k 0 − α = dlog 2 qe + µ + α. We then work with a = d2 k /q 0 e = d2 k /qe. The modulus 0 0 k 0 switching is then performed with y i = b(x i · a · q )/2 c = b(x i · a · q)/2 k−α c mod q 0 .

Complexity. The values α, k, q 0 and a can be computed prior to the execution of the algorithm and are therefore not considered in the complexity. The number of operations of BtoAExp µ,2 k using [BCZ18] is T BtoAExp = 10 · 2 n − 6n − 13. Furthermore, the For loop at Line 3 costs 3n operations. Eventually, the cost of Line 5 is α(2n 2 + 10n − 9) operations, with α = dlog 2 ne. Therefore the overall complexity is T BtoA q Exact = 10 · 2 n − 6n − 13 + 3n + α(2n 2 + 13n − 9) = 10 · 2 n − 3n − 13 + α(2n 2 + 13n − 9) and asymptotically the number of operation is O(2 n + α · n 2 ) = O(2 n + n 2 log n) which is still O(2 n ) in total.

Lemma 5. The BtoA q Exact algorithm is (n − 1)-NI.

Proof. The BtoA q Exact algorithm is the composition of the BtoAExp algorithm which is (n − 1)-SNI, followed by independent operations on each shares and by the ShiftMod algorithm which is also (n − 1)-NI. The resulting algorithm is therefore (n − 1)-NI.

### 4.4 Comparison

We provide a comparison between the various Boolean to arithmetic conversion algorithms in Table 2. We see that for µ = 18 as in Dilithium with Security Level 2, the new algorithms BtoAqApprox and BtoAqExact outperform the state of the art algorithms for security order t ≤ 8. The approximate conversion BtoAqApprox performs better than BtoAqExact, but with the drawback of a small error in the conversion. However, we show in Appendix C that it can still be safely used in the masking of Dilithium by employing slightly restrictive rejection sampling. While this modification results in perfectly valid Dilithium signatures, the signature algorithm would not fully conform to the standardized algorithm. Therefore, for the high-order masking of Dilithium in sections 6 and 7, we only consider the exact conversion algorithm BtoAqExact. We also show in Appendix D that BtoAqApprox and BtoAqExact consume much less randomness than [SPOG19].

Table 2: Operation count for 18-bit Boolean to arithmetic modulo q conversion algorithms, up to security order t = 12, with n = t + 1 shares, for prime q = 2 23 − 2 13 + 1.

B → A mod q

Security order t 2 3 4 5 6 8 [BBE + 18] 18 → mod q 2 841 5 215 8 782 12 897 17 825 30 235 [SPOG19] 18 → mod q 804 1 414 2 186 3 120 4 216 6 894 [CGMZ22] 18 → mod q 993 1 885 3 065 4 533 6 289 10 665 BtoAqApprox 58 135 292 609 1 246 5 080 BtoAqExact 154 285 610 1 032 1 786 6 160

5 Masking the Decompose function

10 46 012 10 220 16 193 20 434 21 938

12 64 776 14 194 22 873 81 868 83 860

In Dilithium, the Decompose function is used at signature generation to extract the high and low order bits of w = Ay mod q, with (w 0 , w 1 ) := Decompose q (w, 2γ 2 ). We recall the function below, for a single element r ∈ Z q .

<!-- PDF_PAGE: 16 -->

## PDF page 16

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

Algorithm 7 Decompose q (r, α)

1: r := r mod + q 2: r 0 := r mod ± α 3: if r − r 0 = q − 1 then r 1 := 0, r 0 := r 0 − 1 4: else r 1 = (r − r 0 )/α

5: return (r 1 , r 0 )

125

Existing work. In [ABC + 22], the authors describe two distinct approaches for masking the Decompose q (r, α) function, depending on the value of α. In both cases, the input r is arithmetically masked modulo q, the value r 1 is returned in the clear, while r 0 remains arithmetically masked modulo q. For NIST security level 2, where α = (q − 1)/44, the authors show that r 1 can be computed using the Compress function from Kyber, which can be masked using a technique described in [CGMZ23]. Although their approach is heuristic, the correctness of their method can be exhaustively verified for all possible values of r modulo q, since q is relatively small. For NIST security levels 3 and 5, with α = (q − 1)/16, the authors describe a second approach using an arithmetic modulo q to Boolean conversion, taking advantage that 16 is a power-of-two, so that it suffices to keep the 4 least significant bits of the output.

Our contribution. In this section, we present an extension of the two approaches from [ABC + 22], so that each approach can cover all NIST security levels. Firstly, we expand on the first approach based on the Compress function, by providing an alternative description of the Decompose procedure used in Dilithium. This alternative method is proven to be equivalent to the original Decompose and can work for any α = (q − 1)/δ, not just for α = (q − 1)/44. We then describe the masking of the resulting algorithm based on our new ShiftMod algorithm, which is more efficient than the full arithmetic to Boolean conversion used in [ABC + 22] and [CGMZ23]. The masking complexity of this approach is O(n 2 log qn). Secondly, we extend the second approach of [ABC + 22] to cover any α = (q − 1)/δ, by providing an alternative description of the Decompose procedure used in Dilithium. This alternative method is straightforward to mask with an arithmetic to Boolean conversion, including NIST security level 2 with α = (q − 1)/44, whereas the initial approach in [ABC + 22] only worked for a power-of-two δ. The masking complexity of this approach is O(n 2 log q). Finally, we provide a comparison of the two approaches. Although the second approach is asymptotically faster, with a complexity of O(n 2 log q) instead of O(n 2 log qn), the first approach tends to be faster in practice. This is because the second approach requires a full arithmetic modulo q to Boolean conversion, which is more costly than the first approach that can employ our more lightweight ShiftMod algorithm from Section 3.1.

### 5.1 First alternative Decompose algorithm

Algorithm 7 would be difficult to mask directly, because of the test at Line 3. Therefore, we consider the following alternative algorithm for Decompose, and prove that the two algorithms actually compute the same function. This corresponds to the first approach in [ABC + 22], which the authors used for security level 2 with α = (q − 1)/δ where δ = 44. The authors computed the output r 1 using the Compress function from Kyber, which in turn can be masked using a technique described in [CGMZ23]. Although their approach was heuristic, the correctness of their method can be exhaustively verified for all possible values of r modulo q, since q is relatively small in Dilithium.

<!-- PDF_PAGE: 17 -->

## PDF page 17

Improved Gadgets for the High-Order Masking of Dilithium

126

Using the DecomposeComp algorithm below, we extend this approach to any δ, and prove that the original Decompose and our DecomposeComp algorithms compute the same function. We then provide a more efficient masking technique than in [CGMZ23], based on our ShiftMod algorithm from Section 3.1.

Algorithm 8 DecomposeComp q (r, α)

1: δ := (q − 1)/α

2: r 1 := bδ · r/qe mod + δ 3: r 0 := r − r 1 · α mod ± q 4: return (r 1 , r 0 )

Lemma 6. Let δ ∈ Z and α = (q − 1)/δ, and assume α = 0 (mod 2). The algorithms Decompose and DecomposeComp compute the same function.

Proof. We can assume wlog that 0 ≤ r &lt; q. We first consider the original Decompose algorithm, with (r 1 , r 0 ) ← Decompose q (r, α). We write:

r = r 1 0 · α + r 0 0

(5)

with −α/2 &lt; r 0 0 ≤ α/2, so that r 0 0 = r mod ± α. Therefore r 0 0 corresponds to the variable r 0 at Step 2 of Decompose. Note that since 0 ≤ r ≤ q −1, we must have 0 ≤ r 1 0 ≤ (q −1)/α = δ. For 0 ≤ r &lt; (q − 1) − α/2, we have 0 ≤ r 1 0 &lt; δ, so that r − r 0 0 = r 1 0 · α &lt; q − 1, and therefore by definition of Decompose, we have r 0 = r 0 0 and r 1 = r 1 0 . On the other hand, for q − 1 − α/2 ≤ r &lt; q, we have r 1 0 = δ, which gives r − r 0 0 = q − 1, and therefore r 1 = 0 and r 0 = r 0 0 − 1. Therefore, we always have r 1 = r 1 0 mod + δ. We now consider (r 1 00 , r 0 00 ) ← DecomposeComp(r, α). We have using (5):

r 1 00 =

δ · (r 1 0 · α + r 0 0 ) δ · r = (mod δ) q q δ · r 0 0 + (q − 1) · r 1 0 δ · r 0 0 − r 1 0 = = r 1 0 + q q

(mod δ)

(6)

Using −α/2 &lt; r 0 0 ≤ α/2 and 0 ≤ r 1 0 ≤ δ, we have δ · r 0 0 − r 1 0 ≤ δ · α/2 ≤ (q − 1)/2, and similarly δ · r 0 0 − r 1 0 ≥ δ · (−α/2 + 1) − δ ≥ −(q − 1)/2. Therefore |δ · r 0 0 − r 1 0 | ≤ (q − 1)/2, which from (6) implies r 1 00 = r 1 0 mod + δ and therefore r 1 00 = r 1 . Finally, since for both Decompose and DecomposeComp we have r = r 0 + r 1 · α (mod q) and r = r 0 00 + r 1 00 · α (mod q), and moreover r 1 = r 1 00 , we obtain r 0 = r 0 00 (mod q), and from −(q − 1)/2 ≤ r 0 ≤ (q − 1)/2 and −(q − 1)/2 ≤ r 0 00 ≤ (q − 1)/2, we must have r 0 00 = r 0 .

Masking DecomposeComp. Starting from an arithmetic masking of r modulo q, the main challenge is to mask the computation of r 1 = br · δ/qe mod + δ at Step 2. Our approach is captured by Equation (7) in the lemma below. It shows that the high-order computation of bx · p/qe can be written as the composition of two high-order computations. Firstly we apply a modulus switching from modulo q to modulo p · 2 ρ for a large enough ρ, using the ModSwitch algorithm from Section 4.1. Such algorithm can induce an error 0 ≤ e &lt; n (see Lemma 2), but since Equation (7) is valid for any such e, we are guaranteed to get the correct result after Euclidean division by 2 ρ . Secondly, from the arithmetic masking modulo p · 2 ρ , we perform a sequence of ρ ShiftMod to compute the arithmetic division by 2 ρ , and eventually we get the desired result modulo p. We obtain Algorithm 9 below.

<!-- PDF_PAGE: 18 -->

## PDF page 18

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

127

Lemma 7. For any odd positive integer q, any positive integer p, any n ≥ 2, any integer x ∈ Z q , any integer 0 ≤ e &lt; n and any integer ρ such that 2 ρ ≥ 2q · n, the following holds: x · p x · p · 2 ρ = + 2 ρ−1 + e /2 ρ (mod p) (7) q q

Proof. We can assume 0 ≤ x &lt; q. We write x · p = y · q + r with −(q − 1)/2 ≤ r ≤ (q − 1)/2, and y = bx · p/qe. This gives: x · p · 2 ρ r · 2 ρ ρ−1 ρ +2 + e = y · 2 + + 2 ρ−1 + e q q

Therefore, to get (7), it suffices to ensure that 0 ≤ br · 2 ρ /qc + 2 ρ−1 + e &lt; 2 ρ . From 2 ρ ≥ 2q · n, we have 2 ρ−1 /q ≥ n, and therefore d2 ρ−1 /qe ≥ n, which implies using −(q − 1)/2 ≤ r ≤ (q − 1)/2 and 0 ≤ e &lt; n: −(q − 1) · 2 ρ−1 r · 2 ρ (q − 1) · 2 ρ−1 ρ−1 ρ−1 +2 +2 + 2 ρ−1 + n ≤ + e&lt; q q q ρ−1 2 r · 2 ρ ρ−1 ρ + e&lt; 2 − +2 + n ≤ 2 ρ 0 ≤ q q

Algorithm 9 SecDecomposeComp Input: x 1 , . . . , x n ∈ Z q , with r = x 1 + · · · + x n mod q Output: r 1 and y 1 , . . . , y n ∈ Z q , such that (r 1 , r 0 ) = Decompose q (r, α), with r 0 = y 1 + · · · + y n (mod q)

1: Let ρ ← dlog 2 (q · n)e + 1 2: for i = 1 to n do z i := bx i · δ · 2 ρ /qc mod (δ2 ρ ) 3: z 1 ← z 1 + (n − 1) + 2 ρ−1 mod (δ2 ρ )

4: for i = 0 to ρ − 1 do z 1 , . . . , z n ← ShiftMod(2 ρ−i · δ, (z 1 , . . . , z n )) 5: (z 1 , . . . , z n ) ← RefreshMasks δ (z 1 , . . . , z n ) P + 6: r 1 := i z i mod δ 7: (y 1 , . . . , y n ) := (x 1 , . . . , x n ) 8: y 1 := y 1 − α · r 1 mod q

9: return r 1 , (y 1 , . . . , y n )

Complexity. To do the masking with DecomposeComp, we first perform the modulus switching with δ · 2 ρ for ρ = dlog 2 qne + 1. This requires 2n operations. Then we perform a sequence of ρ ShiftMod. Then we do a refresh, and compute the sum to recover r 1 . The complexity is T (q, n) = 2n + ρ · T shiftMod (n) + T Refresh (n) + n − 1 + 2 = O(n 2 log qn).

Security. We claim our algorithm achieves the t − NI security when the output r 1 is public.

Theorem 4 (t − NIo of SecDecomposeComp). For any set of t intermediate variables, there exists a subset I with |I| ≤ t such that the t intermediate variables can be perfectly simulated from inputs x |I when r 1 is given to the simulator.

Proof. Assuming r 1 is public, Algorithm 9 until Line 4 is the composition of the NI gadget ShiftMod with sharewise computations and therefore is NI. Moreover, the shares z i of r 1 are securely recombined due to the free-SNI of RefreshMasks.

<!-- PDF_PAGE: 19 -->

## PDF page 19

Improved Gadgets for the High-Order Masking of Dilithium

128

Second alternative Decompose algorithm

5.2

We consider the following second alternative algorithm for Decompose, and prove that the two algorithms actually compute the same function. This corresponds to the second approach in [ABC + 22], which initially worked for α = (q − 1)/δ for a power-of-two δ, as in NIST security levels 3 and 5 with δ = 16. Using the DecomposeMod algorithm below, we extend this approach to any δ, including δ = 44 as for NIST security level 2.

Algorithm 10 DecomposeMod q (r, α)

1: δ := (q − 1)/α 2: s := (−δ · r + (q − 1)/2) mod + q 3: r 1 := s mod + δ 4: r 0 := r − r 1 · α mod ± q

5: return (r 1 , r 0 )

Lemma 8. Let δ ∈ Z and α = (q − 1)/δ, and assume α = 0 (mod 2). The algorithms Decompose and DecomposeMod compute the same function.

Proof. As in the proof of Lemma 6, we write r = r 1 0 · α + r 0 0 with −α/2 &lt; r 0 0 ≤ α/2. We consider (r 1 00 , r 0 00 ) ← DecomposeMod(r, α). Using δ · α = q − 1, we obtain:

(mod q)

s = −δ · r + (q − 1)/2 = −δ · r 0 0 + r 1 0 + (q − 1)/2

From −α/2 &lt; r 0 0 ≤ α/2 and 0 ≤ r 1 0 ≤ δ, we must have 0 ≤ −δ·r 0 0 +r 1 0 +(q−1)/2 ≤ q−1, and therefore s = −δ · r 0 0 + r 1 0 + (q − 1)/2 over Z. From r 1 00 = s mod + δ, we get r 1 00 = r 1 0 mod + δ, which implies r 1 00 = r 1 .

The above DecomposeMod algorithm is relatively easy to mask. Starting from an arithmetic masking of r modulo q, we easily obtain an arithmetic masking of s modulo q at Step 2. Then, to high-order compute s mod + δ at Step 3, we first convert the masking of s from arithmetic modulo q to Boolean. One must be careful to use a Boolean masking of a representative of s ∈ Z q such that 0 ≤ s &lt; q, which is the case in the arithmetic to Boolean conversion from [BBE + 18]. Then one can convert back from Boolean masking to arithmetic masking modulo δ of s mod + δ. Using the BtoA δ algorithm from [SPOG19] which achieves the free-SNI property, one can directly recombine the shares to get r 1 in the clear. Eventually, we obtain an arithmetic sharing modulo q of r 0 simply by subtracting α · r 1 to the first share x 1 of the input r. We obtain the SecDecomposeMod algorithm below.

Algorithm 11 SecDecomposeMod Input: x 1 , . . . , x n ∈ Z q , with r = x 1 + · · · + x n mod q Output: r 1 and y 1 , . . . , y n ∈ Z q , such that (r 1 , r 0 ) = Decompose q (r, α), with r 0 = y 1 + · · · + y n (mod q)

1: for i = 1 to n do s i := −δ · x i mod q

2: s 1 := s 1 + (q − 1)/2 mod q 3: s 0 1 , . . . , s 0 n := AtoB q (s 1 , . . . , s n ) 4: s 00 , s 00 n := BtoA δ (s 0 1 , . . . , s 0 n ) 1 , . . . P 00 + 5: r 1 := i s i mod δ 6: (y 1 , . . . , y n ) := (x 1 , . . . , x n )

7: y 1 := y 1 − α · r 1 mod q 8: return r 1 , (y 1 , . . . , y n )

P . s = i s i (mod q) . s 0 1 ⊕ · · · ⊕ s 0 n = s P . i s 00 i = s (mod δ)

<!-- PDF_PAGE: 20 -->

## PDF page 20

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

129

Remark 1. When δ is a power-of-two, as in NIST security levels 3 and 5, there is no need to perform a Boolean to arithmetic conversion at Step 4, as one can simply recombine the last 4 bits of the Boolean shares s 0 i of s after a full mask refreshing, as in [ABC + 22].

Complexity. We use the arithmetic modulo q to Boolean conversion AtoB q from [BBE + 18] and the Boolean to arithmetic BtoA δ conversion from [SPOG19]. The number of operation is therefore:

T SecDecomposeMod (n, q) = n + 1 + T AtoB (n, q) + T BtoA (n, dlog 2 qe) + (n − 1) + 2

= O(log(q)n 2 )

Security. We claim our algorithm achieves the t − NI security when the output r 1 is public. The proof is similar to the proof of Theorem 4 and is therefore omitted.

Theorem 5 (t − NIo of SecDecomposeMod). For any set of t intermediate variables, there exists a subset I with |I| ≤ t such that the t intermediate variables can be perfectly simulated from inputs x |I when r 1 is given to the simulator.

### 5.3 Comparison

In Table 3, we compare different techniques used for masking the Decompose function in the Dilithium signature scheme. Our SecDecomposeComp algorithm is shown to be faster than SecDecomposeMod and [ABC + 22] for all security levels. Specifically, for security level 2, our SecDecomposeComp algorithm is faster than [ABC + 22] because the latter uses a full arithmetic to Boolean conversion to mask the Compress function, moreover with a non power-of-two modulus, whereas we use our more lightweight ShiftMod algorithm. Likewise, for security levels 3 and 5, our SecDecomposeComp algorithm outperforms [ABC + 22], which is equivalent to SecDecomposeMod, as both require a full arithmetic modulo q to Boolean conversion, which is more computationally expensive than our ShiftMod algorithm.

Table 3: Operation count for masking Decompose with n = t + 1 shares, for prime q = 2 23 − 2 13 + 1.

Security order t 3 4 5 6 8 10 5 365 9 719 14 399 20 040 35 410 54 365 1 669 2 503 3 385 4 378 6 940 9 803 5 952 10 065 14 751 20 359 34 492 52 464 4 082 7 177 10 632 14 796 25 402 38 995 1 669 2 503 3 385 4 378 6 940 9 803

2 + [ABC 22] 2 886 Sec. Level 2 SecDecomposeComp 1 033 SecDecomposeMod 3 261 + [ABC 22], SecDecomposeMod 2 196 Sec. Level 3 &amp; 5 SecDecomposeComp 1 033

6 Application to masking Dilithium

Dilithium [BDK + 21] is a lattice-based signature scheme based on the MLWE (Module Learning With Errors) and the SelfTargetMSIS (Module Short Integer Solution) problems [LS15]. It was selected by NIST as the primary standard for quantum safe digital signatures. In this section, we describe the complete high-order masking of Dilithium, utilizing the improved gadgets described in the previous sections. We provide the practical results of a C implementation and compare the performance of our new gadgets with those from [BBE + 18], [SPOG19], and [ABC + 22]. For simplicity, we focus on the randomized version of Dilithium, since as shown in [ABC + 22] it leads to a significantly faster masked

<!-- PDF_PAGE: 21 -->

## PDF page 21

Improved Gadgets for the High-Order Masking of Dilithium

130

implementation than the deterministic version. We recall in Table 4 the parameters of Dilithium for NIST security levels 2, 3 and 5.

Table 4: Dilithium parameters for different NIST security levels

Level

q γ 1 γ 2

2 3 5

8380417 8380417 8380417

2 17 2 19 2 19

(q − 1)/88 (q − 1)/32 (q − 1)/32

### 6.1 Pseudo-code of Dilithium

(k, l)

Repetitions

η β ω

(4, 4) (6, 5) (8, 7)

2 4 2

78 196 120

80 55 75

### 4.25 5.1 3.85

We first recall the pseudo-code of Dilithium in Fig. 1, using the version from the reference implementation, and formally described in [ABC + 22]. Namely, one can distinguish two equivalent versions of Dilithium signatures, the r-version and the r̃-version [ABC + 22]. The Dilithium specification [BDK + 21, Fig. 4] provides the pseudo-code description of the r-version. In this version, one computes w 1 := HighBits q (w, 2γ 2 ) and r 0 := LowBits q (w − cs 2 , 2γ), and performs the rejection sampling on r 0 . On the other hand, the r̃-version comes from the reference implementation, as discussed in [BDK + 21, Section 5.1], and formally described in [ABC + 22, Appendix A]. We recall its pseudo-code description in Fig. 1. In this r̃-version, one first computes (w 0 , w 1 ) ← Decompose q (w, 2γ 2 ) at Line 5, and then computes r̃ := w 0 − cs 2 at Line 9. Finally, one performs the rejection sampling on r̃ at Line 10. In the rest of this paper, as in [ABC + 22], we consider this r̃-version because it is easier to mask. We refer to [BDK + 21] for the definition of the UseHint and MakeHint algorithms. Given (w 0 , w 1 ) ← Decompose q (w, 2γ 2 ), as in [BDK + 21] we write HighBits q (w, 2γ 2 ) := w 1 and LowBits q (w, 2γ 2 ) := w 0 . We now show that signature verification works. Using

Az − ct = A(y + cs 1 ) − c(As 1 + s 2 ) = Ay − cs 2

and from w = Ay = w 1 · α + w 0 (mod q), we have:

h = MakeHint q (−ct 0 , w 0 − cs 2 + α · w 1 + ct 0 , 2γ 2 )

= MakeHint q (−ct 0 , w − cs 2 + ct 0 , 2γ 2 )

= MakeHint q (−ct 0 , Az − ct + ct 0 , 2γ 2 )

(8)

Using Az − ct 1 · 2 d = Az − ct + ct 0 , we have w 1 0 = UseHint q (h, Az − ct + ct 0 , 2γ 2 ). From (8) and using kct 0 k ∞ &lt; γ 2 , this enables to recover the high bits of Az − ct from the hint h, using [BDK + 21, Lemma 1]:

w 1 0 = UseHint q (h, Az − ct + ct 0 , 2γ 2 )

= HighBits q (Az − ct, 2γ 2 ) = HighBits q (w − cs 2 , 2γ 2 )

Moreover, using [BDK + 21, Lemma 3], from kw 0 − cs 2 k ∞ &lt; γ 2 − β, we have HighBits q (w − cs 2 , 2γ 2 ) = HighBits q (w, 2γ 2 ) and therefore w 1 0 = w 1 , which gives c̃ = H(M k w 1 0 ) as required.

<!-- PDF_PAGE: 22 -->

## PDF page 22

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

KeyGen

1: A ← R q k×`

2: (s 1 , s 2 ) ← S η ` × S η k 3: t := As 1 + s 2 4: (t 1 , t 0 ) := Power2Round q (t, d) 5: return (pk = (A, t 1 ), sk = (A, t 1 , s 1 , s 2 , t 0 ))

131

Sign(sk, M ) 1: (z, h) := ⊥ 2: while (z, h) = ⊥ do 3: y ← S̃ γ ` 1 4: w := Ay 5: (w 0 , w 1 ) := Decompose q (w, 2γ 2 ) 6: c̃ := H(M k w 1 ) 7: c := SampleInBall(c̃) 8: z := y + cs 1 9: r̃ := w 0 − cs 2 10: if kzk ∞ ≥ γ 1 − β or kr̃k ∞ ≥ γ 2 − β, then (z, h) := ⊥ 11: else 12: h := MakeHint q (−ct 0 , r̃ + α · w 1 + ct 0 , 2γ 2 ) 13: if kct 0 k ∞ ≥ γ 2 or the # of 1’s in h is greater than ω, then (z, h) := ⊥ 14: end while 15: return σ = (c̃, z, h)

Verify(pk, M, σ = (c̃, z, h)) 1: c := SampleInBall(c̃) 2: w 1 0 := UseHint q (h, Az − ct 1 · 2 d , 2γ 2 ) 3: return Jkzk ∞ &lt; γ 1 − βK and Jc̃ = H(M k w 1 0 )K and J# of 1’s in h is ≤ ωK

Figure 1: Template of Dilithium with r̃-version (reference implementation).

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 22]

### 6.2 Masking Dilithium key generation

In the key generation of Dilithium, the private-key elements s 1 and s 2 must be returned as arithmetically masked modulo q. As shown in Figure 1, the variables s 1 and s 2 are sampled uniformly from S η ` and S η k respectively, i.e, vectors of polynomials with each coefficient uniformly and independently distributed in [−η, η]. To obtain a masked generation, since η is a small value (e.g., η = 2, 4, and 2 for NIST security levels 2, 3, and 5, respectively), we proceed by first generating n arithmetic shares s 1,i and s 2,i uniformly in the range [0, 2η + 1[. This corresponds to an arithmetic sharing modulo 2η + 1 of s 1 and s 2 .

Next, we convert this arithmetic sharing modulo 2η + 1 into an arithmetic masking modulo q using the table-based countermeasure from [CGMZ22], which has a complexity of O(n 2 ). Specifically, the table has 2η + 1 rows for −η ≤ i ≤ η, and initially, the row of index i is an encoding of i modulo q. The rows of the table are randomly rotated and refreshed n times, resulting in an n-encoding modulo q of a uniform random in [−η, η]. The same operation is repeated for each coefficient of s 1 and s 2 .

With the arithmetic sharing modulo q of s 1 and s 2 , we can then high-order compute t = As 1 + s 2 using the linearity over Z q . Since the security proof of Dilithium considers t to be public [BDK + 21], we can securely recombine the shares by applying a full refresh. The overall complexity of the masked key-generation algorithm is O(n 2 ), as summarized in Figure 2.

<!-- PDF_PAGE: 23 -->

## PDF page 23

Improved Gadgets for the High-Order Masking of Dilithium

132

KeyGen

1: A ← R q k×` 2: for i = 1 to n do 3: s 1,i ← [0, 2η + 1[ 256` , s 2,i ← [0, 2η + 1[ 256k 4: end for 5: s 1,1 , . . . , s 1,n ← A 2η+1 toA q Table(s 1,1 , . . . , s 1,n ) 6: s 2,1 , . . . , s 2,n ← A 2η+1 toA q Table(s 2,1 , . . . , s 2,n )

. s j = i s j,i mod

±

2η + 1

P

7: for i = 1 to n do t i := As 1,i + s 2,i mod q 8: t 1 , . . . , t n = Refresh(t 1 , . . . , t n ) P 9: t := i t i mod q 10: (t 1 , t 0 ) := Power2Round q (t, d) 11: return (pk = (A, t 1 ), sk = (A, t 1 , (s 1,1 , . . . , s 1,n ), (s 2,1 , . . . , s 2,n ), t 0 ))

Figure 2: Masked Dilithium key generation

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 23]

Masking Dilithium signature generation

6.3

Our masking strategy for Dilithium signature generation is similar to that of [ABC + 22]. Specifically, we mask the same variables and leave unmasked the same variables. The first step is to mask the random vector of polynomials y, since its knowledge would directly lead to the computation of s 1 = (z − y)/c, given that z and c are public. Similarly, we need to mask w = Ay, as A is full rank with high probability and could allow one to retrieve y from w. As explained in introduction, following [ABC + 22], the variable w 1 in (w 1 , w 0 ) ← Decompose q (w) need not be masked since it is also publicly computed during signature verification. Thus, the challenge c̃ = H(M kw 1 ) need not be masked, and the Keccak hash function H need not be masked. However, w 0 must remain masked, as using w 1 would allow one to recover w = w 1 · α + w 0 mod q and eventually y and s 1 . We stress that the variables z and r̃ must remain masked until the rejection sampling has been performed. If the value z is rejected due to an out-of-bounds coefficient |z i | ≥ γ 1 − β, then the knowledge of z i would leak information about the secret s 1 . The same holds for r̃. Therefore, the variables z and r̃ must remain masked until the rejection sampling has been completely performed, and the rejection sampling must be done in a masked way so that whenever a polynomial coefficient is rejected, the adversary does not learn more about the rejected coefficient. Lastly, after the rejection sampling of z and r̃, one can then securely recombine the shares of z. Namely, without the public-key compression, z would have been returned as a valid Dilithium signature. Note that we cannot recombine the shares of z before the rejection sampling of r̃, as knowing z would enable to compute:

r̃ = w 0 − cs 2 = w − αw 1 − cs 2 = Az − ct − αw 1

and assuming heuristically that the coefficients of w 0 are uniformly distributed in ] − γ 2 , γ 2 ], an out-of-bound coefficient of r̃ would leak information about s 2 . Eventually, after the rejection sampling of z and r̃, once the shares of z have been recombined, as in [ABC + 22] the hint h can be computed in the clear, by computing h = MakeHint(−ct 0 , Az − ct + ct 0 , 2γ 2 ). In the following, we describe in more details the high-order masking of Dilithium signature generation, following each step of Fig. 1. The globally masked algorithm is formally described in Figure 3 below.

Generation of y ∈ S̃ γ ` 1 . In order to generate y ∈ S̃ γ ` 1 at Step 3 in Fig. 1, we first generate an n-shared Boolean masking of each coefficient of y, which is then converted into an arithmetic masking using the technique described in Section 4.3.

<!-- PDF_PAGE: 24 -->

## PDF page 24

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

133

More precisely, in the signature generation of Dilithium, each coefficient of y must be uniformly distributed in ] − γ 1 , γ 1 ]. For this, we can first generate each share uniformly in [0, 2γ 1 [ and then subtract γ 1 − 1. Since γ 1 is a power-of-two (γ 1 = 2 17 , 2 19 , 2 19 for levels 2, 3, 5 respectively), the uniform generation in [0, 2γ 1 [ corresponds to the uniform generation of a (log 2 γ 1 + 1)-bit integer, so we generate the n Boolean shares as random (log 2 γ 1 + 1)-bit integers. We then convert the Boolean masking into an arithmetic masking modulo q, using the exact conversion method described in Section 4.3. This gives an arithmetic sharing modulo q of y ∈ [0, 2γ 1 [ 256` that can eventually be translated into ] − γ 1 , γ 1 ] 256` by subtracting γ 1 − 1 to each coefficient of the first share. We obtain an arithmetic masking y 1 , . . . , y n modulo q of the signing nonce y.

Computation of w = Ay. From the linearity of matrix multiplication in Z q , the vector w can be computed share by share. In Fig. 3, we denote by W i = A · y i mod q the arithmetic shares of w modulo q. As explained above, we cannot unmask the shares W i into w, as this would lead to y since A is public and full rank with high probability.

Computation of (w 0 , w 1 ) = Decompose q (w, 2γ 2 ). As explained previously, we can compute w 1 in the clear, but the Decompose function must be high-order computed, and w 0 must remain arithmetically masked, as in [ABC + 22]. Such masking of Decompose is described in Section 5.2, with two possible approaches. In Fig. 3, we denote by w 0,i the n arithmetic shares modulo q of w 0 .

Computation of z and r̃. The vector z is computed share by share from the shares y i and s 1,i of y and s 1 respectively. The same holds for r̃ = w 0 − cs 2 .

Sign(sk, M ) 1: (z, h) := ⊥ 2: while (z, h) = ⊥ do 256` 3: for i = 1 to n do y i ← [0, 2γ 1 [ 4: y 1 , . . . , y n := BtoA q Exact(y 1 , . . . , y n ) P ± 5: y 1 := y 1 − (γ 1 − 1) . y = P i y i mod q 6: for i = 1 to n do W i := Ay i . w = P i W i (mod q) 7: w 1 , (w 0,1 , . . . , w 0,n ) := SecDecompose((W 1 , . . . , W n ), 2γ 2 ) . w 0 = i w 0,i (mod q) 8: c̃ := H(M k w 1 ) 9: c := SampleInBall(c̃) P 10: for i = 1 to n do z i := y i + cs 1,i . z = i z i (mod q) 11: if SecRejectionSampling((z 1 , . . . , z n ), γ 1 , β) then (z, h) = ⊥ 12: else P 13: for i = 1 to n do r̃ i := w 0,i − cs 2,i mod q . r̃ = i r̃ i (mod q) 14: if SecRejectionSampling((r̃ 1 , . . . , r̃ n ), γ 2 , β), then (z, h) := ⊥ 15: else 16: z 1 , . P . . , z n := RefreshMasks(z 1 , . . . , z n ) 17: z = i z i mod q 18: r := Az − ct mod q 19: h := MakeHint q (−ct 0 , r + ct 0 , 2γ 2 ) 20: if kct 0 k ∞ ≥ γ 2 or the # of 1’s in h is greater than ω, then (z, h) := ⊥ 21: end while 22: return σ = (c̃, z, h)

Figure 3: Template of Masked Dilithium signature generation.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 24]

Rejection sampling of z and r̃. We implement the rejection sampling of z and r̃ using the method described in [ABC + 22]. The test is conducted on the arithmetic shares z i of z

<!-- PDF_PAGE: 25 -->

## PDF page 25

Improved Gadgets for the High-Order Masking of Dilithium

134

and the arithmetic shares r̃ i of r̃. We perform the rejection sampling iteratively on the masked coefficients of z and r̃, and the result of the test is computed in the clear for each coefficient. If any coefficient fails the test, the vectors z and r̃ are rejected immediately. To perform the masked rejection sampling of each coefficient, we utilize the method from [ABC + 22] based on the SecA2BModp and SecLeq gadgets. This method is more efficient than the technique presented in [BBE + 18].

Recombining the shares of z and computing the hint. As explained above, after the rejection sampling of z and r̃, one can securely recombine the shares of z, after a full mask refreshing, and then compute h = MakeHint(−ct 0 , Az − ct + ct 0 , 2γ 2 ) in the clear. We summarize the fully masked Dilithium signature generation in Fig. 3 above.

Complexity. Based on the individual complexities of the gadgets, we can conclude that the overall complexity of signature generation is O(2 n +n 2 log q) when using the BtoA q Exact algorithm from Section 4 for generating y, and the SecDecomposeComp algorithm from Section 5.1. As shown in Section 4.4, our BtoA q Exact algorithm has exponential complexity O(2 n ), but is much faster than other algorithms for small values of n. To guarantee a polynomial-time complexity in n, one can use the algorithm proposed in [SPOG19] instead. In that case, the overall complexity of signature generation reduces to O(n 2 log q).

Security. Given that each gadget processing sensitive variable achieves at least t − NI security and the public variables are securely recombined, the whole signing procedure achieves, by composition, t-NIo security when the output signature σ is public.

Theorem 6 (t − NIo security of Sign). For any set of t intermediate variables, there exists a subset I ⊂ [1, n], with |I| ≤ t, such that these t intermediate variables can be perfectly simulated from s 1,|I and s 2,|I when the output σ is given to the simulator.

7 Implementation results

We have implemented the gadgets introduced in the previous sections in C and inte- grated them into the reference implementation of Dilithium, resulting in a fully masked implementation of Dilithium in C. We provide below the benchmark results obtained on a laptop with an Intel(R) Core(TM) i7-1065G7 @1.30GHz CPU. We observe that the performance of each gadget is similar to the operation count provided in the previous sections. However, we emphasize that our implementation is only a proof-of-concept and the actual performance in a real-life product would depend on the specific device targeted. To achieve optimal performance, an optimized implementation of the gadgets for the targeted architecture and mitigation of micro-architectural leakage would be necessary, but these steps are beyond the scope of this work. The plain C code is publicly available at

https://github.com/fragerar/Masked_Dilithium

### 7.1 Performance of individual gadgets

We provide below the performance results of individual gadgets. The randomness used is fetched from a simple XorShift PRNG. In practice, this would need to be replaced by a TRNG in a secure environment.

Arithmetic mod 2 k to Boolean conversion. Table 5 presents the performance of the arithmetic mod 2 k to Boolean conversion using the new ShiftMod gadget proposed in Section 3.1. The table shows that the empirical results are consistent with the theoretical

<!-- PDF_PAGE: 26 -->

## PDF page 26

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

135

operation counts in Table 1, although in practice, ShiftMod outperforms [CGV14] for orders slightly higher than expected.

Table 5: Cycle counts for a full arithmetic to Boolean conversion on 32-bit masked values.

A mod 2 32 → B

Security order t 1 2 3 4 5 6 7 8 9 [Gou01]/[CGV14] 50 1067 1649 3225 5176 6324 7392 10360 13248 Alg. 3 with ShiftMod 1262 2099 3179 4339 5375 6404 7655 9099 10650

Boolean to arithmetic mod q conversion. Table 6 compares various approaches for converting Boolean to arithmetic mod q to generate the coefficients of y within a given range, showing similar results to the operation counts presented in Table 2. The table shows that the newly proposed BtoAqApprox and BtoAqExact algorithms outperform the previously proposed algorithm in [SPOG19] for small orders. However, for higher orders, the main bottleneck arises from the Boolean to arithmetic conversion modulo 2 k proposed in [BCZ18], which has exponential complexity. As expected, the overhead for BtoAqApprox is lower than that for BtoAqExact.

Table 6: Cycle counts for a µ-bit Boolean to arithmetic mod q conversion for µ = 18 and q = 2 23 − 2 13 + 1.

k

B → A mod 2

Security order t 1 2 3 4 5 k B2Amod2 [BCZ18] 23 79 308 516 906 [SPOG19] 694 1307 2275 3395 4288 BtoAqApprox 24 80 310 518 908 BtoAqExact 351 445 979 1270 2133

B → A mod q

6 1961 6251 1963 3537

Comparison with the bitsliced approach. We provide a high-level comparison with the bitsliced approach of [BC22] for the high-order Boolean to arithmetic conversion modulo q. For such conversion, the authors of [BC22] provide a comparison between their bitsliced implementation of the Boolean to arithmetic conversion algorithm from [BBE + 18], and the non-bitsliced implementation of the [SPOG19] conversion algorithm. We denote by k the bitsize of the modulus q, and by µ the input Boolean size. The complexity of [BC22] is O(k) and independent of µ, while the complexity of [SPOG19] is O(µ) and independent of k. In [BC22, Fig. 6], for k = 12 and µ = 1, bitsliced [BC22] is 2.5 as slow as non-bitsliced [SPOG19], for security order t = 2. Based on this, we can estimate that for k = 23 and µ = 18, as in Dilithium, bitsliced [BC22] would be 3.7 times faster than non-bitsliced [SPOG19]. On the other hand, from Table 6 above, we observe that for security order t = 2, our non-bitsliced implementation is 2.9 times faster than [SPOG19]. Therefore, for the Boolean to arithmetic modulo q conversion, we expect [BC22] to be 1.3 times faster than our non-bitsliced implementation (and 2.4 times faster for security order t = 6). However, the timing estimates above do not take into account the change of represen- tation required for a bitsliced implementation, from the canonical representation where the inputs bits are stored contiguously in a given register, to the bitsliced representation where each input bit is stored in a different register for parallel evaluation, and vice versa (see Section 2.6 in [BC22]). While this change of representation has a linear complexity in the number of shares, it can impact the overall efficiency of a bitsliced approach for the full Dilithium algorithm.

<!-- PDF_PAGE: 27 -->

## PDF page 27

Improved Gadgets for the High-Order Masking of Dilithium

136

Table 7: Cycle counts for the Decompose gadgets, for security level 2 with γ 2 = (q − 1)/88, and security levels 3 and 5 with γ 2 = (q − 1)/32.

1 DecomposeComp 1814 γ 2 = (q − 1)/88 DecomposeMod 2280 DecomposeComp 1660 γ 2 = (q − 1)/32 DecomposeMod ([ABC + 22]) 1173

Security order t 2 3 4 5 6 2967 5425 8468 10859 13847 7594 12862 20514 25689 34012 2459 3619 5171 7348 8912 2787 4662 7285 10345 13602

Masking of Decompose. Table 7 compares the two methods proposed in Section 5.2 for performing the Decompose operation. As expected, the DecomposeComp approach is more efficient than the alternative DecomposeMod approach, since it only requires a sequence of arithmetic shifts using the ShiftMod operation instead of a full arithmetic mod q to Boolean conversion. However, when γ 2 = (q − 1)/32, which applies to security levels 3 and 5, the difference in efficiency between the two approaches is slightly smaller because the Boolean to arithmetic conversion can be avoided in Algorithm 11. We also provide in Appendix D the randomness consumption of the main gadgets.

### 7.2 Performance of fully-masked Dilithium

Table 8 presents the cycle counts for the full signature generation at security levels 2, 3, and 5, along with the time spent in each signature component for security level 3. The running time corresponds to the average total time spent in each component during multiple executions of the signature generation, including restarts due to rejection sampling.

The table highlights a common feature of high-order implementations of lattice-based schemes that were not initially designed with masking in mind: the slowest operations are often the ones that are trivial to compute in the unmasked case. We can see that the majority of the time is spent in Decompose and Reject, which are simple operations in the absence of masking. In contrast, polynomial arithmetic, which is the primary optimization target for unprotected implementations, only takes a small fraction of the runtime in masked implementations as it is a linear operation.

Table 8: Cycle counts for a full implementation of randomized Dilithium, with a breakdown of the time taken by each signature component for security level 3. Values are expressed in thousands of cycles. Average over 1000 executions of the signature at each order.

Security order t 0 1 2 3 4 5 6 506 26602 (×53) 54945 (×109) 101020 (×200) 155025 (×306) 231265 (×457) 296200 (×585) 853 36986 (×43) 83696 (×98) 130590 (×153) 205473 (×241) 273446 (×321) 395518 (×464) 989 38069 (×38) 87809 (×89) 137034 (×139) 201838 (×204) 315249 (×319) 404769 (×409)

Dilithium2 Dilithium3 Dilithium5

NTTs Sample y Compute Ay Decompose z = y + c · s 1 Reject w − c · s 2

- - - - - - -

304 3034 616 13088 355 18956 262

451 5135 916 32963 528 42856 390

598 7890 1121 52030 641 67281 487

732 13127 1515 84131 872 103840 635

838 19805 1704 110119 981 138584 746

1037 35884 2182 158275 1245 195207 932

<!-- PDF_PAGE: 28 -->

## PDF page 28

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

8 Conclusion

137

In this work, we presented improved high-order gadgets for the masking of Dilithium, a post-quantum lattice-based signature scheme standardized by NIST. Our new gadget called ShiftMod enables efficient arithmetic shifts modulo any integer 2q, which we used as a component in other masking gadgets. We also proposed a fast Boolean-to-arithmetic modulo q conversion algorithm that leverages ShiftMod, which is used in Dilithium for masking the generation of the random variable y modulo q. Additionally, we described improved techniques for masking the Decompose function in Dilithium, and we demonstrated the effectiveness of our countermeasures with a complete high-order masked implementation of Dilithium. We provided practical results of a C implementation and compared the performance improvement provided by the new gadgets with those from previous work.

A Mask refreshing

A.1 Linear mask refreshing

We recall the LinearRefresh algorithm from [RP10], working in any finite abelian group (G, +):

Algorithm 12 LinearRefresh Input: x 1 , . . . , x n ∈ G Output: y 1 , . . . , y n ∈ G such that y 1 + · · · + y n = x 1 + · · · + x n 1: y n ← x n 2: for j = 1 to n − 1 do 3: r j ← G 4: y j ← x j + r j 5: y n ← y n − r j 6: end for 7: return y 1 , . . . , y n

A.2 Full mask refreshing

We recall the RefreshMasks algorithm, where the operations are performed in any group G, for example the additive group Z q for any integer q. The algorithm was proven (n − 1)-SNI in [BBD + 16].

Algorithm 13 RefreshMasks Input: a 1 , . . . , a n P n P n Output: c 1 , . . . , c n such that i=1 c i = i=1 a i 1: For i = 1 to n do c i ← a i 2: for i = 1 to n do 3: for j = i + 1 to n do 4: r ← G, c i ← c i + r, c j ← c j − r 5: end for 6: end for 7: return c 1 , . . . , c n

The algorithm has complexity O(n 2 ), with a number of operations

T refresh (n) = 3n(n − 1)/2

<!-- PDF_PAGE: 29 -->

## PDF page 29

Improved Gadgets for the High-Order Masking of Dilithium

138

B Proof of Theorem 2

x 3

x 2

0

0

LR

×

LR

×

0

P 1

P 2

x 1

x n

0

×

LR

LR

×

P n−1

Figure 4: 1bitB2A algorithm

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 29]

In order to prove the free SNI 1bitB2A we split the algorithm in several part corresponding to the process of each share. As shown in Fig. 4, we denote by P i the core part of Alg. 2 that processes share x i+1 . More precisely, P i is an algorithm that takes as input i shares, processes x i+1 , and then applies a LinearRefresh on i + 1 shares with the last input share equal to 0. Eventually, the algorithm processes x 1 , and applies a LinearRefresh on the n shares, but by accumulating the randomness on the first column. The proof will focus first on proving by induction that the composition P n−1 ◦ · · · ◦ P 1 achieves free SNI. Then we will prove that the last iteration, processing x 1 , preserves the free SNI property.

We want to prove by induction that P i ◦ · · · ◦ P 1 , taking as input x 1 , . . . , x i+1 and outputting v 1 , . . . , v i+1 , satisfies the free-SNI property. This is initially true for P 1 . We assume that this is the case for P i−1 ◦ · · · ◦ P 1 , for i ≤ n − 1. We now prove that P i ◦ · · · ◦ P 1 satisfies free-SNI. We use the following notations (see Fig. 5):

• (v j ) 1≤j≤i : output of previous part P i−1 ◦ · · · ◦ P 1 ,

• (u j ) 1≤j≤i : result after processing x i+1 on v j ,

• (r j ) 1≤j≤i : randomness used in LinearRefresh,

• (w j ) 1≤j≤i+1 : output of LinearRefresh.

We have u 1 = (1 − 2x i+1 )v 1 + x i+1 and u j = (1 − 2x i+1 )v j for 2 ≤ j ≤ i. We also have w j = u j + r j (mod q) for 1 ≤ j ≤ i. We also denote by (w j,i+1 ) 1≤j≤i the accumulated randoms on the i + 1-th column of LinearRefresh, with w j,i+1 = −(r 1 + · · · + r j ) (mod q) for 1 ≤ j ≤ i, with eventually the last output share w i+1 = −(r 1 + · · · + r i ) (mod q).

Let W be any set of t intermediate variables in P i ◦ · · · ◦ P 1 . We split W in W 1 ∪ W 2 , corresponding to t 1 variables from P i−1 ◦ · · · ◦ P 1 and t 2 variables from P i , with t = t 1 + t 2 . We can assume t &lt; i. Otherwise, if t ≥ i, then we can let I = [2, i + 1]; in that case, we have |I| = i ≤ t and we can simulate all intermediate variables from inputs x |I since x 1 does not appear in any computation; additionally, any O ( [1, i + 1] \ I is empty and therefore the free-SNI property is satisfied.

<!-- PDF_PAGE: 30 -->

## PDF page 30

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

x i+1

x i

v i

P i−1 ◦ · · · ◦ P 1

x i−1

v i−1

(1 − 2x i+1 )v j

x j

v j

x 2

v 2

x 1

v 1

139

w 1,i+1 w j,i+1

w i+1

0

u i

w i

u i−1

w i−1

u j

w j

u 2

w 2

u 1

w 1

r 1 r j r i

LinearRefresh

Figure 5: Core part of 1bitB2A

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 30]

From the free-SNI property of P i−1 ◦ · · · ◦ P 1 with t 1 probes, we can construct a set U ⊂ [1, i], with |U | ≤ t 1 , such that the intermediate variables W 1 and outputs v |U can be perfectly simulated from inputs x |U . Additionally, for any subset O 0 ( [1, i] \ U , the outputs v |O 0 are uniformly and independently distributed, even conditioned on W 1 and v |U . We now extend the set U of input indices to a superset I ⊃ U to allow simulation of the remaining intermediate variables W 2 from P i . We initially set I = U . If x i+1 , 1 − 2x i+1 or any w j,i+1 belong to W 2 , we add i + 1 to to I; note that for the variables w j,i+1 this corresponds to a probe on the i + 1-th column. For 1 ≤ j ≤ i, if at least two variables in the j-th column belong to W 2 , namely any of (1 − 2x i+1 )v j , v j + x i+1 , u j + r j or r j , we add both i + 1 and j to I. If a single variable in the j-th column has been probed, we add j to I if j ∈ / U , otherwise we add i + 1 to I. By construction we must have |I| ≤ |U | + t 2 ≤ t 1 + t 2 = t. We consider any O ( [1, i + 1] \ I, and we now show that: 1. We can perfectly simulate W and outputs w |I from inputs x |I , 2. The outputs w |O are uniformly and independently distributed, even conditioned on W and w |I . For this, we distinguish 2 cases, depending on whether i + 1 ∈ I or i + 1 ∈ / I:

i + 1 ∈ I. Since we know x i+1 , the t 2 variables of W 2 and outputs w |I can be perfectly simulated from v |I\{i+1} and x i+1 , by propagating the simulation column by column. From the free-SNI of P i−1 ◦ · · · ◦ P 1 , we know outputs v |U can be perfectly simulated from x |U , and therefore from x |I . It remains to show how to simulate the outputs v |I\(U ∪{i+1}) , and to prove that the output variables w |O of P i ◦ · · · ◦ P 1 are uniformly distributed. For this, we construct a subset O 0 ( [1, i] \ U of indices on which we apply induction hypothesis, namely the free-SNI of P i−1 ◦ · · · ◦ P 1 , such that the outputs v |O 0 are uniformly distributed. We let: O 0 = O ∪ I \ (U ∪ {i + 1})

To apply the induction hypothesis, we must verify that O 0 ( [1, i] \ U . We have O ⊂ [1, i] \ I ⊂ [1, i] \ U and I \ (U ∪ {i + 1}) ⊂ [1, i + 1] \ {i + 1} \ U ⊂ [1, i] \ U , which gives O 0 ⊂ [1, i] \ U . To show the inclusion is strict, we show that [1, i] \ U \ O 0 is non-empty:

([1, i] \ U ) \ O 0 = [1, i] \ (U ∪ O 0 )

= [1, i] \ (U ∪ O ∪ (I \ (U ∪ {i + 1})))

= [1, i] \ (O ∪ (I \ {i + 1}))

= ([1, i] \ (I \ {i + 1})) \ O

= [1, i + 1] \ I \ O

U ⊂ I

i +1 ∈ I

<!-- PDF_PAGE: 31 -->

## PDF page 31

Improved Gadgets for the High-Order Masking of Dilithium

140

Since by assumption O ( [1, i + 1] \ I, the set [1, i + 1] \ I \ O is non-empty and so is [1, i] \ U \ O 0 . Hence from the free-SNI of P i−1 ◦ · · · ◦ P 1 , the outputs v |O 0 are uniformly and independently distributed. Therefore, we can perfectly simulate v |I\(U ∪{i+1}) with fresh randoms, and therefore all variables v |I\{i+1} can be simulated. As explained above, knowing x i+1 , the simulation can then be propagated to P i , and finally the intermediate variables W and outputs w |I can be perfectly simulated from inputs x |I . We now show that the outputs w |O are uniformly and independently distributed, where w j is the result of u j + r j for j ∈ O, for 1 ≤ j ≤ i; note that since i + 1 ∈ I, we must have i + 1 ∈ / O. We already know that the outputs v |O are uniformly and independently distributed and we remark that for j ∈ O, u j is a bijective transformation of v j . Namely u j = (1 − 2x i+1 )v j for j ≥ 1 and u 1 = (1 − 2x i+1 )v 1 + x i+1 . Therefore u |O are uniformly and independently distributed. Eventually u j acts as a one-time pad on w j = u j + r j and we conclude that the variables w |O are uniformly distributed, even conditioned on w |I and W.

i +1 ∈ / I. We first simulate outputs w |I and intermediate variables W. We consider j ∈ I. If j ∈ U , then by construction none of (1 − 2x i+1 )v j , u j , r j , w j , w j,i+1 belongs to W 2 , otherwise we would have i + 1 ∈ I. In particular, since r j is a fresh uniform random and not involved in the computation of any intermediate variable from W, it acts as a one-time pad on the value u j + r j . Therefore all outputs w |U can be perfectly simulated uniformly and independently. We now simulate outputs w |I\U . For this, we let O 0 = I \ U . We have O 0 ( [1, i] \ U . Indeed, we have assumed t &lt; i, and from |I| ≤ t &lt; i, we have I ( [1, i]; from U ⊂ I, we deduce O 0 = I \ U ( [1, i] \ U . From the induction hypothesis, we know that v |O 0 = v |I\U are uniformly and independently distributed. Since the application v 7→ (1 − x i+1 )v is a bijection, then (1 − 2x i+1 )v j is uniformly distributed. Moreover, for j ∈ I \ U , then by construction of I only one of (1 − 2x i+1 )v j , r j , u j + r j belongs to W 2 . Hence, we can perfectly simulate (1 − 2x i+1 )v j with uniform random without knowledge of x i+1 , since the distribution of v j is independent of W \ {(1 − 2x i+1 )v j }. Simulation of any of r j or u j + r j can also be made with fresh uniform random since r j acts as a one-time pad. Eventually, once the variable from W in the j-th column has been simulated, the simulation can be propagated in the rest of the column and eventually to w j . Therefore, we can perfectly simulate variables W and outputs w |I from inputs x |U ⊂ x |I . It remains to show that the outputs w |O are uniformly and independently distributed. For 1 ≤ j ≤ i, w j = u j + r j (mod q), where r j acts as a one-time pad (neither r j nor w j−1,i+1 − r j belongs to W). If i + 1 ∈ O, since O ( [1, i + 1] \ I, there exists j ? ∈ [1, i+1]\(I ∪O). We have that r j ? a uniform random independent from any P of intermediate variable W and outputs w |I∪(O\{i+1}) . Therefore the output w i+1 = − j6 = j ? r j − r j ? is uniformly distributed, even conditioned on W ∪ w |I∪(O\{i+1}) . Eventually, the outputs w |O are uniformly and independently distributed. We conclude that P i ◦ · · · ◦ P 1 is free-SNI, which achieves the induction. Therefore we have that P n−1 ◦ · · · ◦ P 1 is free-SNI.

It remains to show that the last part that processes x 1 preserves the free-SNI property. As previously, let W be any set of t intermediate variables, we split W = W 1 ∪ W 2 corresponding to variables from P n−1 ◦ · · · ◦ P 1 and the last part respectively, where |W 1 | = t 1 and |W 2 | = t 2 . If t 2 = 0, then there is nothing left to prove since P n−1 ◦ · · · ◦ P 1 is free−SNI and any set of ≤ n − 1 outputs is uniformly and independently distributed from the LinearRefreshMasks procedure. Hence, we assume t 2 &gt; 0. Additionally, we assume t &lt; n. Otherwise, we can take I = [1, n] and we can perfectly simulate all variables since we provide all inputs to the simulator. The proof is very similar to the previous part. First, from the free-SNI of P n−1 ◦ · · · ◦ P 1 , we deduce that there exists U ⊂ [1, n], with |U | ≤ t 1 , such that the intermediate variables W 1 and P n−1 ◦ · · · ◦ P 1 outputs v |U can be perfectly simulated from inputs x |U . Moreover

<!-- PDF_PAGE: 32 -->

## PDF page 32

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

141

for any subset O ( [1, n] \ U , outputs v |O are uniformly and independently distributed. We extend the set U as previously. Initially, we set I = U . As previously, we denote by (w j,1 ) 1≤j≤i the accumulated randoms on the first column of the last LinearRefresh. If any of x 1 , 1 − 2x 1 , w j,1 belongs to W 2 , we add 1 to I. Otherwise, for 2 ≤ j ≤ n, if at least two of v j , r j , w j belong to W 2 , we add both 1 and j to I. If only one of v j , r j , w j belongs to W 2 , we add j to I if j ∈ / U or 1 to I if j ∈ U . By construction, |I| ≤ |U | + t 2 ≤ t 1 + t 2 = t. Let O ( [1, n] \ I. We now show how to simulate variables W and outputs w |I from inputs x |I , and we show that outputs w |O are uniformly and independently distributed. We distinguish two cases whether 1 ∈ I or 1 ∈ / I:

1 ∈ I. By construction, any intermediate variable from W 2 and outputs w |I can be perfectly simulated from v |I , using the knowledge of x 1 . We let O 0 := O ∪(I \U ). Using O ( [1, n]\I, and since [1, n] \ I and I \ U have empty intersection, we deduce O 0 = O ∪ (I \ U ) ( ([1, n]\I)∪(I \U ) = [1, n]\U . Therefore, from the free-SNI of P n−1 ◦· · ·◦P 1 , the outputs v |O 0 are uniformly and independently distributed. Hence, v |I\U can be perfectly simulated with fresh randoms. Additionally, v |U and variables W 1 can be perfectly simulated from inputs x |U . Therefore, by propagating the simulation, we can perfectly simulate intermediate variables W and outputs w |I from inputs x |U ⊂ x |I . Eventually, following the same argument as above, the outputs w |O = u |O + r |O are uniformly distributed, following the fact that u |O are bijective transformation of the uniformly distributed v |O .

1 ∈ / I. We first simulate variables W and outputs w |I . For j ∈ U , by construction none of the variables (1 − 2x 1 )v j , u j , r j , w j , w j,1 belongs to W 2 , since otherwise we would have 1 ∈ I. In particular, r j is a uniform random independent from W and acts as a one time pad on w j = u j + r j (mod q). Hence, the output w j can be perfectly simulated with uniform random. As previously, to simulate the output variables w |I\U , we let O 0 := I \ U ( [1, n] \ U , as we assumed t &lt; n. From the free-SNI of P n−1 ◦ · · · ◦ P 1 , we have that the outputs v |O 0 are uniformly distributed. For j ∈ I \ U , then only one of (1 − 2x 1 )v j , r j , u j + r j belongs to W 2 . As previously, we can simulate any intermediate variables in column j ∈ I \ U with fresh uniform random and propagate the simulation to the output w j . Eventually, we conclude that intermediate variables and outputs w |I can be perfectly simulated from inputs x |U ⊂ x |I . It remains to show that outputs w |O have the uniform distribution. This holds because for j ∈ O and 2 ≤ j ≤ n, we have w j = u j + r j (mod q), where r j is a fresh uniform random independent from W and therefore acts as a one time P pad. Finally, if 1 ∈ O, there exists j ? ∈ [1, n] \ (O ∪ I), and we can write w 1 = (v 1 − j6 = j ? r j ) − r j ? (mod q), where r j ? is a fresh uniform random independent from W and other outputs; therefore it acts as a one-time-pad for w 1 .

Eventually, we have shown that the whole algorithm achieves free-SNI security.

C

Nonce generation with approximate Boolean to arith- metic conversion

In Section 4.2, we have described an approximate Boolean to arithmetic conversion algorithm such that y 1 + · · · + y n = x + e (mod q)

for some centered error |e| ≤ e max , with e max = bn/2c. We can ensure that x is uniformly distributed in the interval ]−γ 1 , γ 1 ], where γ 1 is a power-of-two. Therefore, the distribution of x 0 = x + e, conditioned on x 0 ∈] − γ 1 + e max , γ 1 − e max ], is uniform. This implies that the faster approximate Boolean to arithmetic conversion can also be used in the signature generation of Dilithium, by using a slightly stricter rejection sampling.

<!-- PDF_PAGE: 33 -->

## PDF page 33

Improved Gadgets for the High-Order Masking of Dilithium

142

More precisely, instead of performing the rejection sampling on z = y + cs 1 with kzk ∞ ≥ γ 1 − β, we perform the slightly stricter rejection sampling kzk ∞ ≥ γ 1 − β − e max . We show below that the conditional probability distribution of each coefficient of z remains uniform in an interval, which implies that no information is leaked about the secret-key. We also show that this induces only a very small increase in the number of repetitions to generate a valid signature.

Analysis without error. We start with no error (e = 0), following the reasoning in [BDK + 21, Section 3.4]. The probability that kzk ∞ &lt; γ 1 − β is computed by considering each coefficient separately. For each coefficient σ of cs 1 , the corresponding coefficient z = y + σ of z = y + cs 1 will be in the interval [−γ 1 + β + 1, γ 1 − β − 1] whenever the corresponding coefficient y of y is in [−γ 1 + β + 1 − σ, γ 1 − β − 1 − σ]. Since y is uniformly distributed in [−γ 1 + 1, γ 1 ] and |σ| ≤ β, this happens with probability (2(γ 1 − β) − 1)/(2γ 1 − 1), and moreover the conditional distribution of z is uniform in [−γ 1 + β + 1, γ 1 − β − 1], as required. Therefore the probability that every coefficient of y is in the good range is:

2(γ 1 − β) − 1 2γ 1 − 1

256·`

= 1 −

256·`

β γ 1 − 1/2

≃ exp(−256 · β`/γ 1 )

Similarly, the authors provide a (heuristic) estimate that kr 0 k ∞ &lt; γ 2 − β, and obtain a probability exp(−256 · βk/γ 2 ), so that the probability that the two conditions are satisfied is ≃ exp(−256 · β(`/γ 1 + k/γ 2 )) where (k, `) are the dimensions of A.

Analysis with centered error. We now consider the case of a centered error |e| ≤ e max , with e max = bn/2c, where we obtain for each coefficient z = y + σ + e, instead of z = y + σ. We now consider the stricter condition kzk ∞ &lt; γ 1 − β 0 with β 0 = β + e max . As previously, a coefficient z = y + σ + e will be in the interval [−γ 1 + β 0 + 1, γ 1 − β 0 − 1] whenever y is in [−γ 1 + β 0 + 1 − σ − e, γ 1 − β 0 − 1 − σ − e]. Since y is uniformly distributed in [−γ 1 + 1, γ 1 ] and |σ + e| ≤ β 0 , this happens with probability (2(γ 1 − β 0 ) − 1)/(2γ 1 − 1), and moreover the conditional distribution of z is still uniform in [−γ 1 + β 0 + 1, γ 1 − β 0 − 1], as required. As previously, the probability that every coefficient of y is in the good range is ≃ exp(−256 · β 0 `/γ 1 ) = exp(−256 · (β + e max )`/γ 1 ) and therefore the probability that the two conditions are satisfied is ≃ exp (−256 · ((β + e max )`/γ 1 + βk/γ 2 )) where e max = bn/2c. We obtain the following number of repetitions, which show only a very small increase with the security order.

Table 9: Number of repetitions for security level 2, with n = t + 1 shares

Security order t Repetitions

0 2 3 4 5 6 8 10 12 4.25 4.29 4.32 4.32 4.36 4.36 4.39 4.42 4.46

<!-- PDF_PAGE: 34 -->

## PDF page 34

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

D Randomness consumption

143

Table 10: Randomness usage for the gadgets in number of calls to rand32().

Security order t 1 2 3 4 5 6 CGV14 1 99 198 424 684 975 Alg. 3 with ShiftMod 64 160 288 448 640 864 DecomposeComp 52 154 306 508 760 1062 DecomposeMod 78 284 568 1030 1570 2238 [SPOG19] 18 54 108 180 270 378 BtoAqApprox 2 7 18 41 88 183 BtoAqExact 6 19 42 81 148 267 B2A mod 2 k [BCZ18] 2 7 18 41 88 183

### References

[ABC + 22] Melissa Azouaoui, Olivier Bronchain, Gaëtan Cassiers, Clément Hoffmann, Yulia Kuzovkova, Joost Renes, Markus Schönauer, Tobias Schneider, François- Xavier Standaert, and Christine van Vredendaal. Leveling dilithium against leakage: Revisited sensitivity analysis and improved implementations. Cryp- tology ePrint Archive, Paper 2022/1406, 2022. https://eprint.iacr.org/ 2022/1406.

[BBD + 15] Gilles Barthe, Sonia Belaïd, François Dupressoir, Pierre-Alain Fouque, Ben- jamin Grégoire, and Pierre-Yves Strub. Verified proofs of higher-order masking. In Advances in Cryptology - EUROCRYPT 2015 - Proceedings, Part I, pages 457–485, 2015.

[BBD + 16] Gilles Barthe, Sonia Belaïd, François Dupressoir, Pierre-Alain Fouque, Ben- jamin Grégoire, Pierre-Yves Strub, and Rébecca Zucchini. Strong non- interference and type-directed higher-order masking. In Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security, Vienna, Austria, October 24-28, 2016, pages 116–129, 2016. Publicly available at https://eprint.iacr.org/2015/506.pdf.

[BBE + 18] Gilles Barthe, Sonia Belaïd, Thomas Espitau, Pierre-Alain Fouque, Benjamin Grégoire, Mélissa Rossi, and Mehdi Tibouchi. Masking the GLP lattice-based signature scheme at any order. In Advances in Cryptology - EUROCRYPT 2018 - Proceedings, Part II, pages 354–384, 2018.

[BC22]

Olivier Bronchain and Gaëtan Cassiers. Bitslicing arithmetic/boolean masking conversions for fun and profit with application to lattice-based kems. IACR Trans. Cryptogr. Hardw. Embed. Syst., 2022(4):553–588, 2022. https://ia. cr/2022/158.

[BCZ18]

Luk Bettale, Jean-Sébastien Coron, and Rina Zeitoun. Improved high-order conversion from boolean to arithmetic masking. IACR Trans. Cryptogr. Hardw. Embed. Syst., 2018(2):22–45, 2018.

[BDE + 18] Jonathan Bootle, Claire Delaplace, Thomas Espitau, Pierre-Alain Fouque, and Mehdi Tibouchi. LWE without modular reduction and improved side-channel attacks against BLISS. In Thomas Peyrin and Steven D. Galbraith, editors,

<!-- PDF_PAGE: 35 -->

## PDF page 35

Improved Gadgets for the High-Order Masking of Dilithium

144

Advances in Cryptology - ASIACRYPT 2018 - 24th International Conference on the Theory and Application of Cryptology and Information Security, Brisbane, QLD, Australia, December 2-6, 2018, Proceedings, Part I, volume 11272 of Lecture Notes in Computer Science, pages 494–524. Springer, 2018.

[BDH + 21] Shivam Bhasin, Jan-Pieter D’Anvers, Daniel Heinz, Thomas Pöppelmann, and Michiel Van Beirendonck. Attacking and defending masked polynomial comparison for lattice-based cryptography. IACR Trans. Cryptogr. Hardw. Embed. Syst., 2021(3):334–359, 2021. https://eprint.iacr.org/2021/104.

[BDK + 21] Shi Bai, Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyuba- shevsky, Peter Schwabe, Gregor Seiler, and Damien Stehlé. Crystals- dilithium algorithm specifications and supporting documentation (version 3.1), 2021. https://pq-crystals.org/dilithium/data/ dilithium-specification-round3-20210208.pdf.

[BG14]

Shi Bai and Steven D. Galbraith. An improved compression technique for signatures based on learning with errors. In Josh Benaloh, editor, Topics in Cryptology – CT-RSA 2014, pages 28–47, Cham, 2014. Springer International Publishing.

[CGMZ22] Jean-Sébastien Coron, François Gérard, Simon Montoya, and Rina Zeitoun. High-order table-based conversion algorithms and masking lattice-based en- cryption. IACR Trans. Cryptogr. Hardw. Embed. Syst., 2022(2):1–40, 2022. https://ia.cr/2021/1314.

[CGMZ23] Jean-Sébastien Coron, François Gérard, Simon Montoya, and Rina Zeitoun. High-order polynomial comparison and masking lattice-based encryption. IACR Trans. Cryptogr. Hardw. Embed. Syst., 2023(1):153–192, 2023. https://ia. cr/2021/1615.

[CGTV15] Jean-Sébastien Coron, Johann Großschädl, Mehdi Tibouchi, and Praveen Ku- mar Vadnala. Conversion from arithmetic to boolean masking with logarithmic complexity. In Proceedings of FSE 2015, pages 130–149, 2015.

[CGV14]

Jean-Sébastien Coron, Johann Großschädl, and Praveen Kumar Vadnala. Secure conversion between boolean and arithmetic masking of any order. In Proceedings of CHES 2014, pages 188–205, 2014.

[Cor14]

Jean-Sébastien Coron. Higher order masking of look-up tables. In Proceedings of EUROCRYPT 2014, pages 441–458, 2014.

[CS21]

Jean-Sébastien Coron and Lorenzo Spignoli. Secure wire shuffling in the probing model. In Tal Malkin and Chris Peikert, editors, Advances in Cryptology - CRYPTO 2021 - 41st Annual International Cryptology Conference, CRYPTO 2021, Virtual Event, August 16-20, 2021, Proceedings, Part III, volume 12827 of Lecture Notes in Computer Science, pages 215–244. Springer, 2021.

[DFPS23] Julien Devevey, Pouria Fallahpour, Alain Passelègue, and Damien Stehlé. A detailed analysis of fiat-shamir with aborts. Cryptology ePrint Archive, Paper 2023/245, 2023. https://eprint.iacr.org/2023/245.

[GLP12]

Tim Güneysu, Vadim Lyubashevsky, and Thomas Pöppelmann. Practical lattice-based cryptography: A signature scheme for embedded systems. In Emmanuel Prouff and Patrick Schaumont, editors, Cryptographic Hardware and Embedded Systems – CHES 2012, pages 530–547, Berlin, Heidelberg, 2012. Springer Berlin Heidelberg.

<!-- PDF_PAGE: 36 -->

## PDF page 36

Jean-Sébastien Coron, François Gérard, Matthias Trannoy and Rina Zeitoun

[Gou01]

145

Louis Goubin. A sound method for switching between boolean and arithmetic masking. In Çetin Kaya Koç, David Naccache, and Christof Paar, editors, Cryptographic Hardware and Embedded Systems - CHES 2001, Third Interna- tional Workshop, Paris, France, May 14-16, 2001, Proceedings, volume 2162 of Lecture Notes in Computer Science, pages 3–15. Springer, 2001.

[ISW03]

Yuval Ishai, Amit Sahai, and David A. Wagner. Private circuits: Securing hardware against probing attacks. In CRYPTO 2003, Proceedings, pages 463–481, 2003.

[LS15]

Adeline Langlois and Damien Stehlé. Worst-case to average-case reductions for module lattices. Des. Codes Cryptogr., 75(3):565–599, 2015.

[Lyu09]

Vadim Lyubashevsky. Fiat-shamir with aborts: Applications to lattice and factoring-based signatures. In Advances in Cryptology–ASIACRYPT 2009: 15th International Conference on the Theory and Application of Cryptology and Information Security, Tokyo, Japan, December 6-10, 2009. Proceedings 15, pages 598–616. Springer, 2009.

[LZS + 21]

Yuejun Liu, Yongbin Zhou, Shuo Sun, Tianyu Wang, Rui Zhang, and Jingdian Ming. On the security of lattice-based fiat-shamir signatures in the presence of randomness leakage. IEEE Trans. Inf. Forensics Secur., 16:1868–1879, 2021.

[MGTF19] Vincent Migliore, Benoît Gérard, Mehdi Tibouchi, and Pierre-Alain Fouque. Masking Dilithium - efficient implementation and side-channel evaluation. In Applied Cryptography and Network Security - 17th International Conference, ACNS 2019, Bogota, Colombia, June 5-7, 2019, Proceedings, pages 344–362, 2019.

[MUTS22] Soundes Marzougui, Vincent Ulitzsch, Mehdi Tibouchi, and Jean-Pierre Seifert. Profiling side-channel attacks on dilithium: A small bit-fiddling leak breaks it all. Cryptology ePrint Archive, Paper 2022/106, 2022. https://eprint.iacr. org/2022/106.

[RP10]

Matthieu Rivain and Emmanuel Prouff. Provably secure higher-order masking of AES. In CHES 2010, Proceedings, pages 413–427, 2010.

[SPOG19] Tobias Schneider, Clara Paglialonga, Tobias Oder, and Tim Güneysu. Effi- ciently masking binomial sampling at arbitrary orders for lattice-based crypto. In PKC 2019, Proceedings, Part II, pages 534–564, 2019.
