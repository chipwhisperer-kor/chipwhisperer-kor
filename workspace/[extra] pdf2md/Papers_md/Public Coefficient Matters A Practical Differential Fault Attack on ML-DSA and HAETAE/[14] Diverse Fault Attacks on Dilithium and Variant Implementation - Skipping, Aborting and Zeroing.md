# [14] Diverse Fault Attacks on Dilithium and Variant Implementation - Skipping, Aborting and Zeroing

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 8
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-14"
derived_asset_id: "PCM-DFA-REF-14-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[14] Diverse Fault Attacks on Dilithium and Variant Implementation - Skipping, Aborting and Zeroing.pdf"
source_sha256: "bc23b5262b28b6330d008191258d9402e59835bbc9f91a7d8ca7a9f7f7f6a890"
pages: 8
bbox_words: 7521
consumed_bbox_words: 7521
numeric_tokens: 713
consumed_numeric_tokens: 713
source_blocks: 245
consumed_source_blocks: 245
emitted_blocks: 209
embedded_raster_images: 1
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 8
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

2025 IEEE 24th International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom)

Diverse Fault Attacks on Dilithium and Variant Implementation: Skipping, Aborting and Zeroing

1

Hao Yuan 1 , Yuejun Liu 1B , Jingdian Ming 1 , Yongbin Zhou 1,2B School of Cyber Science and Engineering, Nanjing University of Science and Technology, Nanjing, China 2 Institute of Information Engineering, Chinese Academy of Sciences, Beijing, China { y yuanhao, liuyuejun, mingjingdian, zhouyongbin } @njust.edu.cn

2025 IEEE 24th International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom) | 979-8-3315-6532-9/25/$31.00 ©2025 IEEE | DOI: 10.1109/Trustcom66490.2025.00354

Abstract—As one of the first post-quantum digital signature schemes standardized by NIST, Dilithium has gained significant attention due to its potential role in securing communication in the quantum era. However, ensuring the security of its practical implementations, particularly against fault attacks, remains a significant challenge. Despite various proposed countermeasures, their effectiveness remains inadequately explored. This paper presents a comprehensive analysis of fault attacks on Dilithium, introducing five distinct attack techniques across three fault types: instruction-skipping, loop-aborting, and zeroing, which target the polynomial structure and Number Theoretic Trans- form (NTT) operations in Dilithium. These attacks are shown to significantly reduce the number of faulty signatures required for private key recovery, with the most efficient technique requiring as few as one faulty signature. Our methods successfully com- promise both the reference and the protected implementation designed to resist skip-addition attacks. Experimental validation on an ARM Cortex-M4 platform demonstrates the effectiveness of these attacks, with success rates ranging from 29% to 63%, enabling full private key recovery in both deterministic and randomized Dilithium implementations. These findings under- score the need for more robust, fault-resilient post-quantum cryptographic implementations. Index Terms—Post-Quantum Cryptography, Dilithium, Fault Attack, Number Theoretic Transform, Embedded Security

### I. I NTRODUCTION

The advent of quantum computing poses a significant threat to classical public-key cryptography, as quantum algorithms like Shor’s can efficiently solve problems such as integer factorization and discrete logarithms in polynomial time [1]. This has driven the development of post-quantum cryptog- raphy (PQC), with the National Institute of Standards and Technology (NIST) leading the effort to standardize secure al- ternatives. Among the first post-quantum standards, Dilithium (now ML-DSA) [2], a lattice-based digital signature algorithm, is based on the hardness of the Modular Learning With Errors (MLWE) and Modular Short Integer Solution (MSIS) problems, which are widely believed to remain intractable intractable even against quantum adversaries. Although Dilithium is provably theoretically secure, prac- tical implementations are vulnerable to physical attacks [3], including side-channel attacks (SCAs) [4] and fault attacks [5]. Compared to SCAs, fault attacks are more devastating, actively inducing errors to produce faulty outputs that directly reveal sensitive data. With PQC schemes like Dilithium increas- ingly deployed in embedded devices, ensuring their resilience against fault attacks is crucial for real-world security.

2324-9013/25/$31.00 ©2025 IEEE DOI 10.1109/Trustcom66490.2025.00354

Recent studies have explored fault attacks on Dilithium target various components of its signing process, categorized into three types: skip-addition attacks [6]–[8], which skip masking polynomial additions to expose secret data; loop- abort attacks [9], [10], which halt loops early to induce zero coefficients for private key recovery via lattice reduction or integer linear programming; and NTT-specific attacks [11], which target twiddle factors in number-theoretic transform (NTT) to collapse them to zero. Despite these efforts, significant gaps remain. Most attacks focus on the reference and pqm4 implementations [12], [13], as well as the deterministic Dilithium [14], leaving randomized versions, designed to enhance fault resistance, underexplored. Additionally, existing attacks often require high fault pre- cision, numerous faulty signatures, or rely on challenging assumptions, limiting their practicality. Systematic evaluations across fault models, implementations, and variants are also lacking. Furthermore, systematic evaluations across different fault models and implementations are still lacking. This work addresses these gaps by analyzing fault vul- nerabilities in both deterministic and randomized Dilithium, targeting the reference implementation [12] and a variant implementation [13] designed to resist skip-addition attacks. We introduce novel fault models for polynomial addition and NTT operations in the signing algorithm, achieving key recovery with fewer faulty signatures. Our contributions are summarized as follows: • We propose two function-call skipping attacks on addi- tion subroutines, applicable to both the reference and the optimized NTT-protected implementations. These attacks enable recovery of the private key from as few as one faulty signature—down from the ℓ·n required by previous approaches of this kind [7], [8] (ℓ · n ≥ 1024). • We propose two loop-abort fault attacks targeting polynomial-level and coefficient-level additions. Impor- tantly, the polynomial-level attack is applicable to NTT- protected implementations as well. Unlike previous loop- abort techniques [9], [10], which often suffer from noise and shuffling, our methods yield clean, exploitable equa- tions, enabling recovery of the private key s 1 with fewer faulty signatures. • We propose a single-twiddle-factor zeroing attack on the NTT-protected implementation, achieved by skipping a single NTT assignment. This attack requires only two

2986

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:06:55 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 2 -->

## PDF page 2

TABLE I: Comparison of Fault Attacks on ML-DSA/Dilithium

Fault Type Attack Scheme

Skip Addition Attack [7] Skip Fault Correction [8]

Skipping

Aborting Loop Abort Fault [9]

Random Fault NTT Twiddle Fault [11]

†

Polyvec-Level Addition Skip Poly-Level Addition Skip

Skipping

†

†

Poly-Level Loop Abort * Coeff-Level Loop Abort

Aborting

†

†

Zeroing Single-Twiddle-Factor Zeroing

* Impl.: ■ denotes the official reference implementation or pqm4 implementation,

▲ represents the implementation that reorders the additions in the computation of z.

* Poly-Level Loop Abort: Under this attack, the first polynomial of s

signature suffices to recover all of the remaining ℓ−1 polynomials. Denotes attack techniques proposed in this paper.

†

faulty signatures to recover a single polynomial from s 1 , relaxing the all-twiddle-zeroing requirement of [11] and making the attack more feasible in practice. • Through experiments on an ARM Cortex-M4 platform using ChipWhisperer-Lite, we validate the practicality of all proposed attacks, achieving success rates ranging from 29% to 63%, enabling full recovery of the private key s 1 in both deterministic and randomized Dilithium implementations.

Our attacks, compared with prior work in Table I, offer greater efficiency and broader applicability, highlighting the need for robust countermeasures in Dilithium deployments.

### II. B ACKGROUND

A. Notation

We denote the ring of integers modulo q as Z q , and define the polynomial ring R q = Z q [x]/(x n + 1). Elements in this ring are denoted using regular lowercase letters (e.g., f ∈ R q ). The coefficient of x i in a polynomial f is written as f i . Bold lowercase letters (e.g., f ∈ R q k ) represent vectors of polynomials, with f [i] denoting the i-th polynomial in the vector. Furthermore, f [i][j] denotes the coefficient of x j in the i-th polynomial. Bold uppercase letters (e.g., F ∈ R q k×ℓ ) represent matrices over R q . In Dilithium, all polynomial multiplications are performed in the NTT domain, where a single polynomial is the basic computational unit. Given two polynomials a, b ∈ R q , their product is computed as: a · b = NTT −1 (NTT(a) ◦ NTT(b)), where ◦ denotes coefficient-wise (pointwise) multiplication. For a vector of polynomials v ∈ R q k , we define v̂ = NTT(v) to denote component-wise NTT represetation. Multiplication of a polynomial a ∈ R q with a polynomial vector v ∈ R q k is defined as multiplying a with each component polynomial of v. In this paper, if a fault occurs in a variable such as a, we use a ′ to denote its faulted version.

Faulty Signatures Required

Impl. *

Fault Target

II III V

■ / ▲

1024 1024

1280 1280

1792 1792

z = y + c · s 1

▲

y←ExpandMask

4 5

7

■

• ■ / • ■ / • ■ / •

NTT(y)

4 5

7

1 4

1 5

1 7

z = y + c · s 1

2 4

2 5

2 7

■

•

NTT(y)

8 10 14

• indicates the NTT-protected implementation described in (II.1), and

1 is unrecoverable; therefore, one additional signature is required for it, while a single

B. Dilithium Dilithium operates over the polynomial ring R q , with fixed parameters n = 256 and q = 2 23 − 2 13 + 1. These choices enable efficient polynomial arithmetic using the Number The- oretic Transform (NTT). The scheme supports flexible module dimensions (k, ℓ), corresponding to the three NIST PQC security levels for Dilithium; specifically, Levels II, III, and V use (k, ℓ) = (4, 4), (6, 5), and (8, 7), respectively. Dilithium provides two signing versions: deterministic and randomized. The key distinction lies in the generation of the internal randomness used during the signing process. Specifi- cally, the randomized version generates a fresh random value rnd at line 4 of the signing algorithm II.2 to derive a unique per-signature seed. In contrast, the deterministic version sets rnd to a fixed zero value, resulting in identical signatures when signing the same message multiple times. The Dilithium signature scheme consists of three fundamen- tal procedures: key generation, signing, and verification, which are detailed as follows. Key Generation (Algorithm II.1): The key genera- tion begins by expanding a uniformly random seed using

Algorithm II.1 Dilithium.KeyGen() Output: Public key pk and private key sk 1: ξ ← {0, 1} 256 256 512 256 2: (ρ, ρ ′ , K) ← ← H ξ ∥ {0, 1} × {0, 1} × {0, 1} k ∥ ℓ, 1024 3: Â ∈ R q k×ℓ ← ExpandA(ρ) 4: (s 1 , s 2 ) ← ExpandS(ρ ′ ) 5: t ← NTT −1 Â ◦ NTT(s 1 ) + s 2 6: (t 1 , t 0 ) ← Power2Round(t) 7: pk ← pkEncode(ρ, t 1 ) 8: tr ← H(pk, 512) 9: sk ← skEncode(ρ, K, tr, s 1 , s 2 , t 0 ) 10: return (pk, sk)

2987

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:06:55 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 3 -->

## PDF page 3

SHAKE-256, which is used to derive both the public matrix A ∈ R q k×ℓ and the private key vector s 1 ∈ R q ℓ and s 2 ∈ R q k . The public component is computed as t = A · s 1 + s 2 . To reduce the size of the public key, the vector t is decomposed into high and low bits: the most significant d bits t 1 are retained, while the least significant bits t 0 are discarded. The public key consists of (ρ, t 1 ), where ρ is the seed used to expand A, and the private key includes (ρ, K, tr, s 1 , s 2 , t 0 ), where K is a secret seed for signing and tr = H(pk) is the hash of the public key. Signing (Algorithm II.2): To sign a message M , the signer first computes the message digest µ = H(tr ∥ M ). Then, a per-signature seed is derived as ρ ′ = H(K ∥ rnd ∥ µ), where rnd is either a random value (randomized version) or a zero vector (deterministic version). From this seed, a mask vector

Algorithm II.2 Dilithium sign(sk, M)

Input: message M , sk = (ρ, K, tr, s 1 , s 2 , t 0 ) Output: σ 1: Â ∈ R q k×l ← ExpandA(ρ) 2: µ ∈ {0, 1} 512 ← H(tr||M, 512) 3: κ := 0, (z, h) ←⊥ 4: rnd ← {0, 1} 256 (or rnd ← {0} 256 for the optional deterministic version) 5: ρ ′ ∈ {0, 1} 512 ← H(K||rnd||µ, 512) 6: while (z, h) ←⊥ do 7: y ∈ S γ ℓ 1 ← ExpandMask(ρ ′ , κ) 8: w ← NTT −1 ( Â ◦ NTT(y)) 9: w 1 ← HighBits(w) 10: c̃ ∈ {0, 1} 256 ← H(µ||w1Encode(w 1 ), λ/4) 11: c ∈ R q ← SampleInBall(c̃) 12: ĉ ← NTT(c) 13: z ← y + NTT −1 (ĉ ◦ ŝ 1 ) 14: r 0 ← LowBits q (w − cs 2 , 2γ 2 ) 15: if ∥z∥ ∞ ≥ γ 1 − β or ∥r 0 ∥ ∞ ≥ γ 2 − β then 16: (z, h) ←⊥ 17: else 18: h ← MakeHint q (−ct 0 , w − cs 2 + ct 0 , 2γ 2 ) 19: if ∥ct 0 ∥ ∞ ≥ γ 2 or |h| h j =1 &gt; ω then (z, h) :=⊥ 20: return σ ← sigEncode(z mod ± q, h, c̃)

Algorithm II.3 Dilithium verify(pk, M, σ)

Input: Public key pk, message M , signature σ 1: (ρ, t 1 ) ← pkDecode(pk) 2: (z, h, c̃) ← sigDecode(sk) 3: Â ∈ R q k×ℓ ← ExpandA(ρ) 4: µ ∈ {0, 1} 512 ← H(H(pk, 512)||M, 512) 5: c ∈ R q ← SampleInBall(c̃) ′ 6: w Approx ← NTT −1 ( Â ◦ NTT(z) − ĉ ◦ NTT(t 1 · 2 d )) ′ ′ 7: w 1 ← UseHint q (h, w Approx , 2γ 2 ) ′ 8: c̃ ← H(µ||w1Encode(w 1 ′ ), λ/4) 9: if c̃ = c̃ ′ and ∥z∥ ∞ &lt; γ 1 − β and # of 1’s in h ≤ ω then 10: accept

y is sampled with coefficients drawn uniformly at random from the integer interval [−γ 1 , γ 1 ] (with γ 1 ∈ {2 17 , 2 19 }); it is then transformed into the NTT domain and multiplied with Â to compute the commitment w 1 . The challenge c ∈ R q is then sampled by hashing µ ∥ w 1 , and the response vector is computed as z = y + NTT −1 (ĉ ◦ ŝ 1 ). A rejection check is performed to ensure z and a derived vector r 0 satisfy the norm bounds. If accepted, a hint vector h is generated to help the verifier reconstruct w 1 . The final signature is σ = (z, h, c̃). Verification (Algorithm II.3): To verify a signature σ = (z, h, c̃), the verifier first reconstructs the challenge c from c̃, and computes the commitment w 1 ′ = UseHint(h, A · z − c · t 1 · 2 d ). Then, the verifier recomputes µ and checks whether c̃ = H(µ ∥ w 1 ′ ), while also ensuring that ∥z∥ ∞ &lt; γ 1 − β and the number of nonzero entries in h does not exceed ω. If all checks pass, the signature is accepted as valid.

### C. NTT-protected Implementation

To counter addition-skipping fault attacks [7], [8], a de- fensive strategy was first proposed in [7]. Specifically, the standard implementation z = y + NTT −1 (NTT(c) ◦ NTT(s 1 )) (Algorithm II.2, Line 13) is replaced with the following alternative:

z = NTT −1 (NTT(y) + NTT(c) ◦ NTT(s 1 ))

(II.1)

In this implementation, all additions are performed in the NTT domain. If an addition-skipping behavior occurs in this domain, the resulting error propagates across all coefficients due to the log 2 n-stage butterfly network structure of the NTT, as shown in Fig. 1. Such skipped addition behavior is effectively equivalent to zeroing out one coefficient in ŷ, resulting in a modified polynomial denoted by ŷ ′ . The corresponding inverse transform, y ′ = NTT −1 (ŷ ′ ), is very likely to contain coefficients exceeding the rejection bound γ 1 , causing rejection(Algorithm II.2, Line 15), with a passing probability of about 2 −4320 [7]. As a result, this implemen- tation is resistant to addition-skipping fault attacks, and is referred to as the NTT-protected implementation. Moreover, in this implementation, y is stored only in its NTT form ŷ, reducing the memory overhead associated with retaining y in its normal form [11]. Compared to the reference

Stage 1 Stage 2 Stage 3

- Addition - Subtraction - Multiplication

Fig. 1: NTT Operation on a Polynomial x with Degree 8

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 3]

2988

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:06:55 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 4 -->

## PDF page 4

implementation, this design offers both memory efficiency and enhanced structural resilience against fault attacks. It is therefore a strong candidate for adoption at the implementation level by engineers. In this paper, we consistently refer to the implementation in (II.1) as the protected implementation.

### D. Related Work

a) Skip Addition Fault Attacks: The skip addition fault attack was first introduced in [6] targeting lattice-based signa- ture schemes. The authors described a fault model in which the attacker skips the addition operation such as z = y +c·s. As a result, the masking polynomial y is omitted, thereby exposing the secret-dependent term c · s in the output signature z. While this work demonstrated the risk of secret leakage under such faults, it remained theoretical and did not involve actual fault injection. Building on this idea, a more practical and fine- grained fault model applied to coefficient-level additions in Dilithium was proposed in [7]. Each faulty signature leaks a single coefficient of c · s 1 , and by collecting ℓ · n faulty signatures, the full s 1 can be recovered. This attack was further extended in [8], which analyzed its effectiveness in the randomized Dilithium. In particular, it was shown that if the fault causes z ′ [i][j] to equal y[i][j], the missing compo- nent (c · s 1 )[i][j] can be recovered using signature correction techniques [15], thereby enabling recovery of s 1 . b) Loop-Abort Fault Attacks: Loop-abort fault attacks form another class of threats. In [9], such an attack was first applied to Dilithium by aborting the sampling loop for the mask vector y, resulting in a large number of consecutive zero coefficients. Although the resulting signature remains valid, it leaks substantial information about the private key. The induced zeros in the high-degree coefficients of y effectively reduce its degree, enabling lattice reduction techniques to recover s 1 . However, this approach is vulnerable to shuffling countermeasures, which randomize the order of coefficients and prevent low-degree y even after loop abortion. Moreover, while the small norm of c · s 1 enables partial inference of its coefficients from z, directly identifying equations like z i,j = (c · s 1 ) i,j by observing small-norm entries tends to produce noisy and unreliable systems. To address this, an ILP- based approach was proposed in [10], which tolerates noisy equations and still enables accurate recovery of s 1 . c) NTT-Specific Fault Attacks: The first fault attack di- rectly targeting the NTT operations in Dilithium was intro- duced in [11]. By injecting random faults into the twiddle pointers used in the NTT computation, the attacker proba- bilistically causes all twiddle factors to become zero. This attack was applied to the protected implementation described in Section II-C, enabling the attacker to obtain a large portion of the cs 1 vector and subsequently recover the private key s 1 .

### III. A TTACK O VERVIEW

A. Adversary Model

Our attack adopts the single-instruction skip fault model, which is well studied and practical across various hardware platforms. It can be induced using standard techniques such

as clock glitching, voltage manipulation, electromagnetic in- terference, and laser injection. We assume the existence of a physical device capable of performing multiple runs of the Dilithium signing routine. This device possesses an unknown private key but exposes its corresponding public key. The attacker is assumed to be capable of triggering a targeted fault during each signing routine and collecting the resulting faulty signatures. We inject the fault during the first iteration of the internal rejection sampling loop. This eliminates timing uncertainty caused by the Fiat–Shamir with aborts structure [16]. To ensure that a faulty signature is output by the device, it must pass the rejection check in the first round. The probability of this happening for Dilithium-II, III, and V is approximately 0.22, 0.19, and 0.25, respectively. For clarity in theoretical analysis, we assume this condition always holds. Moreover, since all proposed attacks cause multiple coefficients in the sampled vector y to be zeroed, the actual success probabilities tend to be slightly higher in practice.

B. Attack Strategies

We propose three targeted categories of fault attack strate- gies, summarized as follows:

Strategy I: Skipping Polynomial-Level Addition. Skipping the critical function call in the vector addition for computing z disrupts the addition structure, causing a large number of additions to be skipped. As a result, polynomials within the secret vector c · s 1 may become directly exposed in the faulty signature z ′ . • Strategy II: Loop-Abort in Vector Addition. This strategy targets the loop structure within the vector addition for computing z. By injecting a fault that prema- turely aborts the loop, only a partial sum of coefficients is computed, exposing certain coefficients of the secret vector c · s 1 in the resulting faulty signature z ′ . • Strategy III: Zeroing Twiddle Factors in NTT. This strategy targets the NTT computation of polynomi- als. By deliberately zeroing a carefully chosen minimal subset of twiddle factors used in the NTT, it causes more coefficients in the polynomial to become zero. Applied to NTT-protected implementations, this enables the leakage of c · s 1 coefficients through the faulty signature z ′ .

•

All the proposed attacks in this work aim to recover the coefficients of the secret vector c · s 1 . For each leaked coefficient (c · s 1 )[i][j], we define rot(c, j) = {c j , c j−1 , . . . , c 0 , −c 1 , . . . , −c j+1 }, and construct a linear equation with the coefficients of s 1 as unknowns:

⟨rot(c, j), s 1 [i]⟩ = (c · s 1 )[i][j]

By collecting ℓ · n such equations, the private key s 1 can be recovered by solving the resulting system of linear equations. The following subsections present concrete attacks based on these strategies and demonstrate how they can be effectively realized under the single-instruction skip fault model.

2989

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:06:55 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 5 -->

## PDF page 5

### IV. C ONCRETE FA M ETHODS

A. Function-Call Skipping Attacks

1) Polyvec-Level Addition Skip Attack: As shown in List- ing 1, in all known implementations of Dilithium—including both the deterministic and randomized reference versions as well as the pqm4 implementation—the computation of z = y + c · s 1 in the signing procedure follows a consistent pattern: the secret vector c · s 1 is first stored in z, and then z = z + y is performed to compute the final result. In this attack, skipping the function call on line 4 of Listing 1—which invokes the vector addition routine and corresponds to the bl instruction on line 6 in Listing 2—ef- fectively eliminates the entire addition process. As a result, the faulted z ′ is guaranteed to pass the norm check at Line 15 of Algorithm II.2, and is subsequently output as the signature:

z ′ = c · s 1

Fault injection is considered successful if all coefficients of the faulty signature z ′ have small magnitude, indicating that the addition of y was skipped. This is justified by the bounds ∥c · s 1 ∥ &lt; β and ∥y∥ &lt; η, where β ≪ η. Further, the private key vector s 1 can be recovered using the following relation:

s 1 = z ′ · c −1

Since the only difference between the reference and pro- tected implementation lies in whether the operand y is rep- resented in the NTT domain, both implementations perform the same vector addition operation. Therefore, this attack is effective against both implementations. With only a single faulty signature, it enables full recovery of the private key vector s 1 , thereby easily breaking the security of Dilithium. 2) Poly-Level Addition Skip Attack: As shown in Listing 3, the reference implementation of the polyvecl_add function performs vector addition by invoking the poly_add function ℓ times. The protected implementation adopts the same struc- ture. Listing 4 presents the correspondi assembly code. In both the reference and protected implementations, the ℓ polynomial additions invoked by poly_add are independent of each other. Therefore, skipping the bl instruction on line 3, which calls poly_add, effectively omits one polynomial addition without affecting the others in the vector. Depending on the fault injection timing, it is possible to selectively skip any one of the ℓ polynomial additions in the

Listing 1: Official C Code Calling polyvecl_add

... polyvecl_pointwise_poly_montgomery(&amp;z, &amp;cp, &amp;s1); polyvecl_invntt_tomont(&amp;z); polyvecl_add(&amp;z, &amp;z, &amp;y); ...

1

2

3

4

5

Listing 2: Corresponding Assembly Code Snippet

... add.w adds mov add.w bl

1 2 3 4 5 6

r1 , sp , #11264 r1 , #32 r0 , r1 r2 , sp , #7200 &lt;dilithium_polyvecl_add&gt;

Listing 3: Official C Code for Polynomial Vector Addition

1

void polyvecl_add (polyvecl *w, const polyvecl *u, const polyvecl *v) { unsigned int i; for(i = 0; i &lt; L; ++i){ poly_add(&amp;w-&gt;vec[i], &amp;u-&gt;vec[i], &amp;v-&gt;vec[i]); }}

2

3

4

5

6

Listing 4: Assembly Code Snippet for Polynomial Vector Addition

... add.w bl cmp.w bne.n

1 2 3 4 5

r4 , r4 , #1024 &lt;dilithium_poly_add&gt; r4 , #4096 &lt;dilithium_polyvecl_add+0xa&gt;

vector addition process. Suppose the fault causes the k-th polynomial addition in the vector to be omitted. The resulting faulty output z ′ [i] can thus be uniformly described by (IV.1). In this context, S 1 represents the index set of polynomials un- affected by the fault, while S 2 contains the index of the faulty polynomial. For this case, we have S 1 = {0, 1, . . . , ℓ−1}\{k} and S 2 = {k}. Therefore, (c · s 1 )[k] can be directly obtained by the attacker and used to construct linear equations for recovering s 1 [k]. ( y[i] + (c · s 1 )[i], i ∈ S 1 ′ z [i] = (IV.1) (c · s 1 )[i], i ∈ S 2

B. Loop-Abort Attacks in Addition Routines

Vector addition consists of element-wise operations and is typically implemented using loops. In Dilithium, the operands are polynomials over a ring, and polynomial addition is inherently coefficient-wise, also relying on loops. This makes the vector addition step a natural target for loop-abort fault attacks. 1) Polynomial-Level Loop Abort: As shown in Listing 3, the polyvecl_add function performs one polynomial ad- dition per iteration. Suppose the loop is aborted during the (k−1)-th iteration (0-based indexing), specifically by skipping the conditional branch instruction bne.n at line 5 in Listing 4. This prevents control from returning to the loop body and results in early termination. The resulting faulty output z ′ can be characterized by (IV.1). Under this attack model, the sets in that equation take the following values:

S 1 = {0, 1, . . . , k−1}, S 2 = {k, k+1, . . . , ℓ−1}, k ≥ 1

Depending on the point at which the loop aborts, all polyno- mials of the secret vector c · s 1 —except the first one—may be exposed in the faulty signature z ′ . Notably, this attack typically fails to recover the first polynomial of the private key vector s 1 . However, when polynomial-level shuffling is applied as a countermeasure, the randomized polynomial addition order may lead to the first polynomial being leaked in the faulty sig- nature. In such cases, only two faulty signatures are sufficient to recover the full s 1 . This behavior is consistent across both deterministic and randomized Dilithium and applies to both the reference and protected implementations.

2990

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:06:55 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 6 -->

## PDF page 6

2) Coefficient-Level Loop Abort: As shown in Listing 5, the poly_add function implements the addition of two polyno- mials of degree n−1 by looping to perform coefficient-wise addition. Suppose a fault is injected into the i-th polynomial component of the vector, and the addition loop is aborted after the (k−1)-th coefficient has been processed. This is achieved by skipping the bne.n instruction on line 8 in Listing 6 within the corresponding loop. For the reference implementation, the resulting faulty output z ′ [i] can be expressed as: ( y[i][j] + (cs 1 )[i][j], j ∈ {0, . . . , k−1} ′ z [i][j] = (IV.2) (cs 1 )[i][j], j ∈ {k, . . . , n−1}

Again, the number of leaked coefficients in c · s 1 depends on the abort point k. Since y[i][j] is drawn uniformly from [−γ 1 , γ 1 ] and (cs 1 )[i][j] ≈ N (0, σ 2 ) with γ 1 ≫ β &gt; σ, we have Pr |z[i][j]| ≤ β ≲ β/γ 1 ≤ 1.50 × 10 −3 . Hence, even if k is unknown, the faulty output z ′ exhibits a contiguous run of small–norm coefficients (&lt; β) for j ≥ k, which allows us to localize k and extract a linear system in cs 1 . Only two faulty signatures are required to recover any polynomial of s 1 when k ≤ n/2. When k attains its minimum value (i.e., k = 1), only (c·s 1 )[i][0] remains unknown; since the coefficients are approximately Gaussian and ∥c·s 1 ∥ ≤ β, we enumerate {0, ±1, ±2, . . . } outward from the mean and solve the resulting linear system. We then validate the candidate by checking whether the recovered s 1 satisfies ∥s 1 ∥ ∞ ≤ η (with η ∈ {2, 4}); incorrect guesses typically yield solutions whose ℓ ∞ -norm far exceeds η. To accommodate imprecise loop–abort faults (which may introduce a few noisy equations) or very small k, an Integer Linear Programming (ILP) formulation can also recover one polynomial of s 1 from a single faulty signature, following [10].

### C. Single-Twiddle-Factor Zeroing Attack

In the first stage of the Cooley–Tukey NTT (CT-NTT) [17] implementation, all butterfly operations belong to the same butterfly group and therefore use a shared twiddle factor, which in this group is given by ψ 4 · ω 0 , as shown in Fig. 1. Consequently, faulting this single twiddle factor affects all n/2 butterfly operations within the stage. Moreover, the normal- domain coefficients of the polynomial directly participate in the first-stage computation, making the fault effects more predictable and easier to control.

Listing 5: Official C Code of Polynomial Addition

1

void poly_add (poly *c, const poly *a, const poly *b) { unsigned int i; for(i = 0; i &lt; N; i++){ c-&gt;coeffs[i] = a-&gt;coeffs[i] + b-&gt;coeffs[i];}}

2

3

4

Listing 6: Assembly Code Snippet of Polynomial Addition

1 2 3 4 5 6 7 8

... ldr.w ldr.w add str,w adds cmp.w bne.n

r4 , [r1, r3, lsl #2] r5 , [r2, r3, lsl #2] r4 , r5 r4 , [r0, r3, lsl #2] r3 , #1 r3 , #256 &lt;dilithium_poly_add+0x4&gt;

Forward NTT (CT-NTT) Forward NTT (CT-NTT) Inverse NTT (GS-NTT)

Fig. 2: Illustration of Twiddle Factor Zeroing in the Butterfly Operation

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 6]

Let a (k) denote the output after the k-th stage of the CT- NTT. Assuming that the shared twiddle factor of a butterfly group in the k-th stage is zero, all butterfly operations within that group produce identical outputs at both branches; that is, for each butterfly pair (i, j), the two output branches satisfy a (k+1) [i] = a (k+1) [j]. This is functionally equivalent to replacing the a j input branch of each butterfly with zero, as illustrated in Fig. 2. Based on this observation, we propose a novel fault model in which the twiddle factor used in the first-stage butterfly group is faulted to zero. Under this model, the first-stage output satisfies: h h n i n i a (2) [j] = a (2) j + , for j ∈ 0, − 1 , n = 256 2 2 which effectively zeroes out the coefficients in degrees n/2 through n − 1 of the polynomial that has undergone a faulted NTT computation. We refer to this as the single-twiddle-factor zeroing fault model. Notably, we do not constrain the specific fault injection technique used to achieve this zeroing effect; the proposed fault model is designed to remain independent of any particular implementation. Nevertheless, we propose an implementation-aware strategy that achieves the desired zeroing effect by skipping a single instruction. Specifically, as illustrated in Listing 7, we skip the assignment to zeta at line 5, without affecting the increment of k, thereby causing zeta to retain its original memory value instead of being assigned the expected twiddle factor. In our key-recovery attack model, we assume that the uninitialized zeta variable is read as zero—an assumption widely adopted in the fault-attack literature. For example, in loop-abort attacks [9], the unsampled coefficients of y are typically treated as zeros. Recent work [18] carried out several attacks based on the same assumption. In practice, uninitialized memory tends to contain zero with non-negligible probability. For instance, [11] shows that, in 10,000 random- ized memory access tests, a 1KB memory region entirely filled with zeros appeared with a probability of 20–25%. Furthermore, zero-initialization is both a safe and widely adopted software practice, lending credibility to our model assumption. Following this assumption, the single-twiddle-factor zeroing fault is injected during the NTT computation of y, as shown in line 8 of Algorithm II.2. This fault corrupts the i-th polynomial of the vector y as follows:

y ′ [i] = (y 0 , y 1 , . . . , y 127 , 0, 0, . . . , 0), i ∈ {0, . . . , ℓ − 1}.

Under the protected implementation described by (II.1), where the computation of the vector z is performed entirely in the NTT domain, the process becomes directly dependent

2991

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:06:55 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 7 -->

## PDF page 7

Listing 7: Official C Source Code of NTT

1

void ntt(int32_t a[N]){ ... for(len=128; len&gt;0; len&gt;&gt;=1){ for(start = 0; start &lt; N; start = j+len){ zeta = zetas[++k]; for(j = start; j &lt; start + len; ++j){ t=montgomery_reduce((int64_t)zeta*a[j+len]) ; a[j+len]=a[j]-t; a[j]=a[j]+t; }} }}

2

3

4

5

6

7

8

9

10

on the faulted NTT-domain representation ŷ ′ . The resulting faulty signature z ′ can be described by (IV.2), where k = 128 denotes the number of unaffected coefficients. As a result, half of the coefficients of (c · s 1 )[i] are directly exposed in the faulty polynomial z ′ [i] within the faulty signa- ture. Consequently, only 2ℓ faulty signatures are sufficient to recover ℓ · n independent linear equations, which is enough to reconstruct the full private key vector s 1 .

### V. E XPERIMENT

Our experiment is divided into two main phases: the fault injection phase and the private key recovery phase.

A. Experimental Setup

1) Fault Injection Phase: The fault injection phase is conducted on the ChipWhisperer-Lite platform, as illustrated in Fig. 3. We take the reference implementation of Dilithium-2, as well as a corresponding protected implementation, which is obtained by making minor modifications to directly per- form additions on the NTT-domain representations of poly- nomials, as a case study, where the signing program is compiled using arm-none-eabi-gcc with the flags -Os, -mcpu=cortex-m4, -mfloat-abi=soft, and -DF_- CPU=7372800, and executed on an ARM Cortex-M4 target board equipped with an STM32F405 microcontroller. We em- ploy clock glitching as the fault injection technique to precisely skip individual instructions during execution. A trigger flag is inserted immediately before and after the vector addition operation shown in Listing 1, line 4, to set the fault injection window and synchronize the injection timing.

Fig. 3: Chipwhisperer-Lite Platform

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 7]

TABLE II: Fault Injection Parameters for the Proposed Attacks

Attack Offset Width Ext Offset Success Rate

Polyvecl-Addition Skip -48.75 -3.25 7 57%

Poly-Additon Skip

13 40%

-47.75 -1.5

2843 29%

Poly-Level Loop Abort

-49 -3.25 34 + 11k 34%

Coeff-Level Loop Abort

-47.75 -1.5 19 63%

Twiddle Factor Zeroing

The host PC communicates with the DUT via UART. A Python script running on the host coordinates trigger genera- tion, glitch parameter tuning, and data collection. 2) Private Key Recovery Phase: In this phase, the coeffi- cients of c·s 1 extracted from the collected faulty signatures are used to construct a linear system, which is then solved using the Z3 solver to recover the private key s 1 . The recovery is performed on a host machine equipped with an Intel Core i7-12700 CPU running Ubuntu 20.04.

B. Experimental Results

The fault injection framework provided by the ChipWhis- perer-Lite platform supports three key parameters for precise clock glitch injection: offset, width, and ext_offset. The offset parameter defines the temporal shift of the glitch within the target clock cycle. The width specifies the width of the glitch cycle. The ext_offset determines the number of clock cycles between the trigger signal and the target instruction, allowing synchronization of the injection point with a specific operation. These parameters are crucial for accurately targeting and skipping specific instructions during execution. Table II presents the results of fault injection experiments conducted on signature operations over 1,000 randomly generated messages. It summarizes the glitch parameters used in all our proposed attacks, along with their corresponding success rates. Notably, the results from our practical experiments on function-call skipping and loop-abort attacks show that both the reference and protected implementations share identical clock glitch parameters and exhibit very similar success rates. This can be naturally explained by the fact that the target operations requiring faults are exactly the same in both implementations under these attacks. The ext_offset values in the table represent the parameters used during the addition of the first polynomial in the vector, where k ∈ {0, 255} denotes the index of the coefficient-wise addition. In the single-twiddle-factor zeroing attack, a minor mod- ification was made by zero-initializing the memory region storing zeta, similar to the practice in [8], which instead zero-initializes the memory region of Â in the signing process. The code was compiled with the -O0 flag to disable compiler optimizations, while all other compilation settings remained unchanged. A trigger flag was inserted before and after line 5 of Listing 7. Under precisely tuned fault injection parameters (as shown in Table II), a total of 567 clock glitches were

2992

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:06:55 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 8 -->

## PDF page 8

injected. In 358 of these attempts, the instruction that stores the twiddle factor into zeta was successfully skipped, yielding a fault success rate of 63.2%.

### VI. B YPASSING S HUFFLING C OUNTERMEASURES

For attacks mounted at the polynomial level, the norm of the term c · s 1 is bounded by β (with β ≤ 196), and thus the faulty polynomial z—which consists of n small- norm coefficients—can be identified simply by inspecting its coefficients. This allows the attacker to locate the target poly- nomial affected by the skip fault and subsequently construct a system of linear equations for private key recovery. As a result, both coefficient-level and polynomial-level shuffling countermeasures are ineffective against attacks such as the polyvec-level addition attack, the poly-level addition attack, and the polynomial-level loop abort attack. The effect of the coefficient-level loop abort attack is anal- ogous to that of the loop-abort attack targeting the generation of y-coefficients in [9]. Although that attack is susceptible to coefficient-level shuffling, which was proposed as an effective countermeasure in [9], this defense strategy has been success- fully bypassed in [10] using integer linear programming (ILP)- based methods. Therefore, such attacks remain effective and can successfully bypass shuffling countermeasures. As for the single-twiddle-factor zeroing attack, it targets the first stage of the NTT, which contains only a single butterfly group. Since there is no inter-group shuffling at this stage, and intra-group shuffling does not affect the outcome—because all the faulted coefficients are zeroed out regardless of the butterfly operation order—making shuffling at any granularity [19] ineffective against this type of attack. In summary, all the fault attacks proposed in this work can effectively bypass shuffling countermeasures.

### VII. C ONCLUSION

In this work, we systematically investigate skip addition- based fault attacks and extend the attack granularity from the coefficient level to the polynomial level. This transition significantly reduces the number of required faulty signatures and improves the efficiency and practicality of private key recovery. We further explore the fault vulnerability of storage- optimized protected implementation and propose a novel fault model targeting the Number Theoretic Transform, which ef- fectively zeroes out multiple coefficients in a polynomial. Our experimental results demonstrate that the proposed attacks achieve full private key recovery across all security levels and various Dilithium implementations, highlighting the broad applicability and practical relevance of our approach.

A CKNOWLEDGMENT

This work is supported in part by the National Natural Science Foundation of China (No. U2336205, No. 62202230, No. 62202231, No. 62302224, No. 62302226).

R EFERENCES

[1] P. W. Shor, “Algorithms for quantum computation: Discrete logarithms and factoring,” Proceedings of the 35th Annual Symposium on Founda- tions of Computer Science (FOCS), pp. 124–134, 1994. [2] National Institute of Standards and Technology (NIST), “FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA),” U.S. Department of Commerce, Aug. 13, 2024. [Online]. Available: https: //doi.org/10.6028/NIST.FIPS.204 [3] P. Ravi, A. Chattopadhyay, J.-P. D’Anvers, and A. Baksi, “Side-channel and fault-injection attacks over lattice-based post-quantum schemes (Kyber, Dilithium): Survey and new results,” ACM Trans. Embedded Comput. Syst., vol. 23, no. 2, pp. 35:1–35:54, 2024. [4] M. Randolph and W. Diehl, “Power side-channel attack analysis: A review of 20 years of study for the layman,” Cryptography, vol. 4, no. 2, p. 15, 2020. [5] A. Barenghi, L. Breveglieri, I. Koren, and D. Naccache, “Fault injection attacks on cryptographic devices: Theory, practice, and countermea- sures,” Proceedings of the IEEE, vol. 100, no. 11, pp. 3056–3076, Nov. 2012. [6] N. Bindel, J. Buchmann, and J. Krämer, “Lattice-based signature schemes and their sensitivity to fault attacks,” in Proc. Fault Diagnosis and Tolerance in Cryptography (FDTC), 2016, pp. 63–77. [7] P. Ravi, M. P. Jhanwar, J. Howe, A. Chattopadhyay, and S. Bhasin, “Ex- ploiting determinism in lattice-based signatures: Practical fault attacks on pqm4 implementations of NIST candidates,” in Proc. ACM Asia Conf. Comput. Commun. Secur. (AsiaCCS), Auckland, New Zealand, Jul. 2019, pp. 427–440. [8] E. Krahmer, P. Pessl, G. Land, and T. Güneysu, “Correction fault attacks on randomized CRYSTALS-Dilithium,” IACR Trans. Cryptogr. Hardw. Embed. Syst., vol. 2024, no. 3, pp. 174–199, 2024. [9] T. Espitau, P.-A. Fouque, B. Gérard, and M. Tibouchi, “Loop-abort faults on lattice-based Fiat-Shamir and Hash-and-Sign signatures,” in Proc. Sel. Areas Cryptogr. (SAC), vol. 10532, St. John’s, NL, Canada, Aug. 2016, pp. 140–158. [10] V. Q. Ulitzsch, S. Marzougui, A. Bagia, M. Tibouchi, and J.-P. Seifert, “Loop aborts strike back: Defeating fault countermeasures in lattice signatures with ILP,” IACR Trans. Cryptogr. Hardw. Embed. Syst., vol. 2023, no. 4, pp. 367–392, 2023. [11] P. Ravi, B. Yang, S. Bhasin, F. Zhang, and A. Chattopadhyay, “Fiddling the twiddle constants: Fault injection analysis of the number theoretic transform,” IACR Trans. Cryptogr. Hardw. Embed. Syst., vol. 2023, no. 2, pp. 447–481, 2023. [12] R. Avanzi, J. Bos, L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, J. Schanck, P. Schwabe, M. Seiler, and D. Stehlé, “Reference im- plementation of Dilithium,” GitHub repository, [Online]. Available: https://github.com/pq-crystals/dilithium, accessed Nov. 1, 2024. [13] M. J. Kannwischer, R. Petri, J. Rijneveld, P. Schwabe, and K. Stof- felen, “PQM4: Post-quantum crypto library for the ARM Cortex-M4,” [Online]. Available: https://github.com/mupq/pqm4, 2020. [14] L. Groot Bruinderink and P. Pessl, “Differential fault attacks on de- terministic lattice signatures,” IACR Transactions on Cryptographic Hardware and Embedded Systems, vol. 2018, no. 3, pp. 21–43, 2018. [15] S. Islam, K. Mus, R. Singh, P. Schaumont, and B. Sunar, “Signature cor- rection attack on Dilithium signature scheme,” in Proc. IEEE European Symposium on Security and Privacy (EuroS&amp;P), 2022, pp. 647–663. [16] V. Lyubashevsky, “Fiat-Shamir with Aborts: Applications to Lattice and Factoring-Based Signatures,” in Advances in Cryptology – ASIACRYPT 2009, vol. 5912, M. Matsui, Ed. Berlin, Heidelberg: Springer, 2009, pp. 598–616. [17] J. W. Cooley and J. W. Tukey, “An algorithm for the machine calculation of complex Fourier series,” Mathematics of Computation, vol. 19, no. 90, pp. 297–301, 1965. [18] S. Amer, Y. Wang, H. Kippen, T. Dang, D. Genkin, A. Kwong, A. Nel- son, and A. Yerukhimovich, “PQ-Hammer: End-to-End Key Recovery Attacks on Post-Quantum Cryptography Using Rowhammer,” in Proc. IEEE Symp. Security and Privacy (S&amp;P), 2025, pp. 3567–3582. [19] P. Ravi, R. Poussier, S. Bhasin, and A. Chattopadhyay, “On configurable SCA countermeasures against single trace attacks for the NTT – a performance evaluation study over Kyber and Dilithium on the ARM Cortex-M4,” in Proc. 10th Int. Conf. Security, Privacy and Applied Cryptography Engineering (SPACE), 2020, pp. 123–146.

2993

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:06:55 UTC from IEEE Xplore. Restrictions apply.
