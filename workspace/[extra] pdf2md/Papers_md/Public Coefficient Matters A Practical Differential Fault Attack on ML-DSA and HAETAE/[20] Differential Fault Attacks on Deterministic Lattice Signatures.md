# [20] Differential Fault Attacks on Deterministic Lattice Signatures

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 23
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-20"
derived_asset_id: "PCM-DFA-REF-20-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[20] Differential Fault Attacks on Deterministic Lattice Signatures.pdf"
source_sha256: "713dcaf268d7499663591053bd054b1428502370e4dc4a3df29a04d56c75d240"
pages: 23
bbox_words: 12886
consumed_bbox_words: 12886
numeric_tokens: 1123
consumed_numeric_tokens: 1123
source_blocks: 419
consumed_source_blocks: 419
emitted_blocks: 355
embedded_raster_images: 0
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 23
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

Differential Fault Attacks on Deterministic Lattice Signatures

Leon Groot Bruinderink 1 and Peter Pessl 2

1

Technische Universiteit Eindhoven, The Netherlands, l.groot.bruinderink@tue.nl 2 Graz University of Technology, Austria, peter.pessl@iaik.tugraz.at

Abstract. In this paper, we extend the applicability of differential fault attacks to lattice-based cryptography. We show how two deterministic lattice-based signature schemes, Dilithium and qTESLA, are vulnerable to such attacks. In particular, we demonstrate that single random faults can result in a nonce-reuse scenario which allows key recovery. We also expand this to fault-induced partial nonce-reuse attacks, which do not corrupt the validity of the computed signatures and thus are harder to detect. Using linear algebra and lattice-basis reduction techniques, an attacker can extract one of the secret key elements after a successful fault injection. Some other parts of the key cannot be recovered, but we show that a tweaked signature algorithm can still successfully sign any message. We provide experimental verification of our attacks by performing clock glitching on an ARM Cortex-M4 microcontroller. In particular, we show that up to 65.2% of the execution time of Dilithium is vulnerable to an unprofiled attack, where a random fault is injected anywhere during the signing procedure and still leads to a successful key-recovery.

Keywords: Differential fault attacks · post-quantum cryptography · lattice-based cryptography · digital signatures

1 Introduction

Large-scale quantum computing is a major threat to currently used public-key cryptosys- tems. While it is uncertain when large-enough quantum computers will see the light of day, there is steady progress as, e.g., shown by the recent unveiling of a 72 qubit device [Kel18]. For this reason, the search for quantum-secure alternatives to discrete-logarithm and factoring-based solutions for public-key primitives is in full swing. This is demonstrated by the high interest in the NIST Post-Quantum Cryptography standardization process 1 [NIS]. In total 82 submissions were received at the very recent first-round deadline [Moo17]. This number trumps previous cryptographic competitions such as for AES and SHA-3 by far. A particularly interesting area of post-quantum research is lattice-based cryptography, as it appears to offer comparatively compact keys and ciphertexts as well as high computational performance. Possibly due to this reason, lattice-based cryptography is the largest category in terms of submissions.

∗ Author list in alphabetical order; see https://www.ams.org/profession/leaders/culture/ CultureStatement04.pdf. This work was supported by the Commission of the European Communi- ties through the Horizon 2020 program under project number 645622 (PQCRYPTO) and by the Austrian Research Promotion Agency (FFG) via the K-project DeSSnet, which is funded in the context of COMET – Competence Centers for Excellent Technologies by BMVIT, BMWFW, Styria and Carinthia. 1 NIST repeatedly stated that this process is not supposed to be a competition [Moo17].

Licensed under Creative Commons License CC-BY 4.0. IACR Transactions on Cryptographic Hardware and Embedded Systems ISSN 2569-2925, Vol. 2018, No. 3, pp. 21–43 DOI:10.13154/tches.v2018.i3.21-43

<!-- PDF_PAGE: 2 -->

## PDF page 2

Differential Fault Attacks on Deterministic Lattice Signatures

22

There are ongoing discussions on the black-box security of these submissions 2 . In addition, secure implementations are another important aspect of the standardization process. The proposals should be easy to implement both correctly (ideally also misuse resistant) and securely. Proposals that offer such characteristics on a wide variety of platforms, including PCs as well as constrained devices like smart cards, are more desirable. Naturally this requires analysis of many implementation attacks, such as passive side- channel attacks (cf. [MOP07]) as well as active fault attacks (cf. [BCN + 06]). The latter are a well-known threat to embedded devices. Rowhammer, a remote software-only fault attack [KDK + 14, GMM16], demonstrated that also high-performance PCs are vulnerable. As implementations are evaluated in terms of both security and performance, they should be made resistant to such attacks with minimal costs. In this regard, an interesting property of many lattice-based signature schemes is that they make use of the classic Fiat-Shamir transform [FS86]. Concretely, two NIST submissions, qTESLA [BAA + 17] and Dilithium [LDK + 17], use a variant of the transform called Fiat-Shamir with Aborts [Lyu09]. However, signature schemes built using the Fiat-Shamir transform, such as ECDSA, have a well-known caveat: signing requires a nonce and reuse for different messages leads to trivial key recovery. This requirement was sometimes violated in the past, as, e.g., shown by the infamous attack on the PlayStation3 console [bms10]. In order to sidestep this problem, the signature scheme can be made entirely deterministic. That is, the nonce is derived by hashing the message and the key, which leads to each input having a unique signature. Both Dilithium and qTESLA 3 use this approach and thus follow in the footsteps of proposals such as EdDSA [BDL + 11] and deterministic ECDSA [Por13]. This solution, however, creates problems when it comes to fault attacks. An attacker can let a victim sign the same message twice, but introduce a computational fault in one of the signature computations. This results in different signatures using the same nonce and thus in a key recovery. In fact, recent work [BP16, ABF + 18, PSS + 17, SB18] explored the vulnerability of elliptic-curve signatures against such differential fault attacks, including Rowhammer-based ones [PSS + 17]. The vulnerability of lattice-based deterministic signatures, however, is less clear. The possibility of such differential attacks was already hinted at [LDK + 17, BAA + 17], yet many questions remain open. Concretely, the abortion technique introduced by Lyuba- shevsky [Lyu09] and used by both qTESLA and Dilithium may hamper the attack. Furthermore, the different algebraic structure might open up new attack venues. Under- standing the possibilities of such fault attacks is relevant in the standardization process and possible deployment of these schemes.

Our contributions. In this paper, we show the applicability of differential fault attacks on deterministic lattice-based signature schemes. We focus on Dilithium, but all our attacks apply to qTESLA as well. We explore how and where these schemes are vulnerable to single random faults and show how fault-induced nonce reuse allows extracting the secret key. Furthermore, we show attacks that can easily create and then efficiently exploit a partial nonce-reuse. This scenario yields valid signatures and thus allows to bypass some generic countermeasures. In Dilithium and qTESLA, a unique signature vector z = y + cs is constructed out of a challenge c, a secret element s, and a deterministically computed nonce y. The attack is focused on faulting the computation of challenge c, leaving the nonce y untouched and thus creating a nonce reuse scenario. By carefully examining two signatures of the same

2 Official forum at https://groups.google.com/a/list.nist.gov/forum/#!forum/pqc-forum

3 Following the initial publication of this paper, a very recent update of the qTESLA specification added a mandatory countermeasure which makes the algorithm non-deterministic and prohibits our attacks. We refer to the originally submitted version of qTESLA for the remainder of the paper, and discuss the countermeasure and update in Section 6

<!-- PDF_PAGE: 3 -->

## PDF page 3

Leon Groot Bruinderink and Peter Pessl

23

message yet with a (due to a fault) different challenge c, s can be extracted using linear algebra. We identify multiple operations inside the Dilithium signing algorithm that are vulnerable, i.e., where a random fault can lead to nonce reuse. We say "can", as the use of the Fiat-Shamir with Aborts framework leads to not all faults being exploitable. We determine the success probabilities for all fault scenarios, they range from 14 % to 91 %. In addition to these scenarios, we also explore fault-induced partial nonce reuse. There, the fault attack is specifically focused on the computation of nonce y, but in such a way that only a portion of the computation is different. We exploit this by transforming key recovery into a unique shortest-vector problem, and show how to solve it using the BKZ lattice-reduction algorithm. While previous work already exploited such partial reuse scenarios for ECC [ABF + 18], our attacks are much less restrictive regarding injected faults. Successful extraction of s alone, however, does not directly allow to run the signing algorithm. This is due to Dilithium’s public-key compression, which causes that some additional elements of the secret key cannot be computed from just s. Thus, we show a tweaked signature algorithm that can still sign any new message despite lacking some parts of the key. We verified the vulnerabilities by performing clock glitching on an ARM Cortex-M4 microcontroller. In particular, we induced random faults during polynomial multiplication and in the SHAKE extendable output function. We show that an attacker with detailed knowledge of the executed code can easily inject faults at correct locations despite some non-constant time behavior. Still, an unprofiled attacker who injects a fault anywhere during the signing process still has a high chance of succeeding. Up to 65.2 % of the execution time of Dilithium is vulnerable to our attacks. We finally give a discussion on generic countermeasures against the attacks and reason about their applicability and implementation costs. We conclude that probably the simplest yet most effective countermeasure is a rerandomization of deterministic sampling, which, however, is not covered by the security proof of Dilithium.

Outline. In Section 2, we give the necessary background to understand the remainder of the paper. In Section 3, we explore the possibilities of differential fault attacks on Dilithium. In Section 4, we show how to modify the signature algorithm such that the secret key element extracted by our attacks suffices to compute valid signatures for any message. In Section 5 we verify the vulnerabilities with real experiments on an ARM Cortex-M4 microcontroller. In Section 6 we end the paper with a discussion on countermeasures.

2 Background

In this section, we introduce the necessary background on lattices and the Dilithium signature scheme. We also provide a summary of previous attacks on implementations of lattice-based cryptography.

### 2.1 Lattice-Based Cryptography

For any positive integer q, we define the polynomial ring R q = Z q [x]/(x n + 1). The elements in R are naturally represented as polynomials of degree less than n. For each polynomial f ∈ R q , we can define the corresponding vector of coefficients in Z q as f = (f 0 , f 1 , . . . , f n−1 ). Addition of polynomials f + g corresponds to addition of their coefficient vectors. Multiplication of two polynomials f · g mod (x n + 1) can be written in matrix-vector notation as f · g = gF = f G, where F, G ∈ Z n×n are matrices, whose q columns are nega-cyclic rotations of f , g. Two hard problems underlying many lattice-based cryptography schemes are Ring- LWE/Ring-SIS, which are defined over the ring R q . Given a public key (a, t) ∈ R 2 q , for

<!-- PDF_PAGE: 4 -->

## PDF page 4

Differential Fault Attacks on Deterministic Lattice Signatures

24

Algorithm 1 Dilithium Key Generation

Output: Keypair (pk, sk) 1: ρ ← {0, 1} 256 , K ← {0, 1} 256 2: (s 1 , s 2 ) ← S η l × S η k k×` := ExpandA(ρ) 3: A ∈ R q 4: t := As 1 + s 2 5: (t 1 , t 0 ) := Power2Round d (t) 6: tr ∈ {0, 1} 384 := CRH(ρ||t 1 ) 7: return (pk = (ρ, t 1 ), sk = (ρ, K, tr, s 1 , s 2 , t 0 ))

Ring-LWE an attacker is asked to find short polynomials s 1 , s 2 such that t ≡ a·s 1 +s 2 mod q. With short, we mean polynomials whose coefficients are small, i.e. in absolute value less or equal to some small η &gt; 0. Module-LWE/Module-SIS are generalizations of Ring- LWE/Ring-SIS, respectively. There the problems are defined over R k×` for some positive q k integers k, ` &gt; 1: given a matrix A ∈ R k×` and a vector t ∈ R , find two short elements q q ` k s 1 ∈ R q , s 2 ∈ R q such that t ≡ A · s 1 + s 2 mod q. For the attacks described in this paper, this means that an attacker needs to find multiple secret key elements.

Additional Notation. With := we denote deterministic assignments, with ← we refer to uniform probabilistic qP sampling from some set. We define the ` 2 and ` ∞ norm for n−1 2 w ∈ R q by ||w|| 2 = i=0 w i and kwk ∞ = max{|w 0 |, |w 1 |, . . . , |w n−1 |}, where all w i are

q−1 represented by an element in the interval [− q−1 2 , 2 ]. This definition can be naturally expanded to vectors of polynomials. S η denotes the subset of R q that includes all elements w that satisfy kwk ∞ ≤ η, i.e. the short polynomials described in the previous paragraph.

### 2.2 Deterministic Lattice Signatures

We now describe the two deterministic lattice-based signature schemes Dilithium [LDK + 17] and qTESLA [BAA + 17], both of which were submitted to the NIST call. For design rationale, associated security proofs, and more details (e.g., on various subroutines) we refer to the respective submission documents.

Dilithium. In this work we focus mainly on Dilithium, which is why we give a more in- depth description of this scheme. Dilithium is based on the Module-LWE/SIS assumption. It operates over the fixed base ring R q = Z q [x]/(x 256 + 1), q = 8380417 and allows for flexibility by allowing different module parameters (k, `). This means that code used for arithmetic in R q can be reused for any module R k×` , which makes an adaptation to other q security levels easier. Key generation is given in Algorithm 1. First, two random seeds ρ, K, and two key elements s 1 , s 2 are sampled. The function ExpandA deterministically expands the seed ρ into a matrix A ∈ R k×` using the extendable-output function (XOF) SHAKE128. This is q done to minimize public and private key sizes as only ρ needs to be stored instead of the full A. The public key t = As 1 + s 2 is compressed by feeding it into the Power2Round q function, which computes a pair (t 1 , t 0 ) such that t = t 1 · 2 d + t 0 . Only the upper part t 1 is published. The lower bits t 0 and a hash of the public key tr = CRH(ρ||t 1 ) are included in the private key sk. CRH is shorthand for Collision Resistant Hash, Dilithium uses SHAKE256 with an output length of 384 bits. Dilithium is based on the Fiat-Shamir with Aborts Framework [Lyu09]. Simply speaking, in this framework a signature σ is rejected and signing restarted if σ does not follow some fixed distribution. This rejection sampling statistically hides any secret information in

<!-- PDF_PAGE: 5 -->

## PDF page 5

Leon Groot Bruinderink and Peter Pessl

Algorithm 2 Dilithium Sign (simplified 4 )

25

. fA ρ , fA E

. fY . fW

Input: Message M , private key sk = (ρ, K, tr, s 1 , s 2 , t 0 ) Output: Signature σ = (z, h, c) k×` := ExpandA(ρ) 1: A ∈ R q 384 := 2: µ ∈ {0, 1} CRH(tr||M ) 3: κ := 0, (z, h) := ⊥ 4: while (z, h) = ⊥ do 5: y ∈ S γ l 1 −1 := DeterministicSample(K||µ||κ) 6: w := Ay 7: w 1 := HighBits(w) 8: c ∈ B 60 := H(µ||w 1 ) 9: z := y + cs 1 10: h := MakeHint(−ct 0 , w − cs 2 + ct 0 ) 11: (r 1 , r 0 ) := Decompose(w − cs 2 ) 12: if kzk ∞ ≥ γ 1 − β or kr 0 k ∞ ≥ γ 2 − β or r 1 6 = w 1 then (z, h) := ⊥ 13: κ := κ + 1 14: return σ = (z, h, c)

Algorithm 3 Dilithium Verify (simplified 4 )

. fH

Input: Public key pk = (ρ, t 1 ), message M , signature σ = (z, h, c) 1: A ∈ R q k×` := ExpandA(ρ) 2: µ ∈ {0, 1} 384 := CRH(CRH(ρ||t 1 )||M ) 3: w 1 := UseHint(h, Az − ct 1 ) 4: accept iff c = H(µ||w 1 )

the signature and thus provides the zero-knowledge property. The structure of rejection sampling can be easily seen in Algorithm 2, which shows a slightly simplified 4 version of the Dilithium signature algorithm. The comments in Algorithm 2 refer to our attack scenarios and can be ignored for now. Signature generation starts off by recomputing A and hashing the message M to- gether with the hashed public key tr. The abort loop starts off by using the function DeterministicSample to generate the noise y ∈ S γ ` 1 −1 . The product w = Ay is compressed to w 1 using HighBits. The hint h later allows the verifier to recompute this w 1 . The hash function H instantiates the random oracle needed in the proof. It returns a sparse ternary polynomial c ∈ B 60 , i.e., a polynomial with Hamming weight 60 and all non-zero coefficients in ±1. The function Decompose returns both HighBits and LowBits of its input. Finally, several checks are performed that determine if the current signature is accepted or rejected. Note that all operations in Algorithm 2 are completely deterministic and thus generate a unique signature for message M 5 . This property is also used in the proof of Dilithium in the Quantum Random Oracle Model (QROM) [KLS18]. The proof does allow a non- deterministic version, albeit at the cost of tightness and a loss in security proportional to the number of distinct signatures an adversary can observe per message. For completeness, we also provide a simplified version of the verification procedure (Algorithm 3). Throughout this paper we use the recommended Dilithium parameter set III shown in Table 1. It claims 128 bits of security against a Quantum adversary. Other parameter sets are given in Appendix A. They mainly differ in the used (k, `), so our later attacks are possible for all proposed sets.

4 Some additional checks and constant subroutine arguments are omitted.

5 A previous Dilithium description [DLL + 17] is probabilistic, but did not include a proof in the QROM.

<!-- PDF_PAGE: 6 -->

## PDF page 6

Differential Fault Attacks on Deterministic Lattice Signatures

26

Table 1: Dilithium Parameter Set III (recommended)

n q d weight(c) γ 1

256 8380417 14 60

γ 2 (k, `) η β

523776 261888 (5, 4) 5 325

qTESLA. Structurally, the signature scheme qTESLA [BAA + 17] is very similar to Dilithium. It also uses a variant of the Fiat-Shamir with Aborts framework and is deterministic. Unlike Dilithium, its proof in the QROM model [ABB + 17] allows for a non-deterministic version as well (without losing tightness). The main difference however is that qTESLA is based on the Ring-LWE/SIS assumptions instead of the module coun- terparts. Thus, it operates on R q = Z q [x]/(x n + 1) (so k = ` = 1) with n ≥ 1024. We will later demonstrate our attacks on the example of Dilithium. Still, with some minor modifications they all also apply to qTESLA. We defer the description of qTESLA to Appendix B, where we also highlight the similarities to Dilithium.

The SHAKE Extendable Output Function

2.3

Dilithium makes heavy use of the SHAKE Extendable Output Function (XOF). It is also an important target of our fault attack, which is why we now very briefly describe it. SHAKE uses the sponge construction [BDPV07]. The sponge construction has two internal parameters r and c called the rate and the capacity, where the capacity is chosen such that the sponge construction meets a desired level of security. We call the internal state of the sponge x, consisting of r + c bits, with all bits initialized to zero. The sponge starts with the absorb phase. Any input to the sponge function is first padded, using some injective padding function, resulting in k ≥ 1 input blocks m 1 ||m 2 || . . . ||m k . These message blocks are then XORed with the first r bits of the state x, interleaved with applications of a permutation f : {0, 1} r+c → {0, 1} r+c . In SHAKE, the Keccak-f permutation is used. After all message blocks are processed, the squeeze phase starts. Depending on the desired output length, the function iteratively returns the first r bit blocks of the internal state x, interleaved with applications of the permutation f . In Figure 1, we show an example for three input blocks and three output blocks. Note that this construction allows for any number of input and output blocks.

m 0 m 1 m 2

⊕ ⊕ ⊕

0 r 0 c

f f f

Absorb

H 0 H 1 H 2

...

f f f

Squeeze

Figure 1: Sponge construction with three block input m 0 ||m 1 ||m 2 and three block output H 0 ||H 1 ||H 2 . With 0 r , 0 c we denote the all-zero bit string of length r, c. The application of the padding function is not shown.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 6]

In the context of fault attacks, the important thing to note is that any manipulations in f corrupt the state x and thus affect all subsequent operations. For instance, faulting the first application of f in the squeeze phase leads to a correct H 0 but faulty H 1 , H 2 , . . ..

Implementation Security of Lattice-Based Cryptography

2.4

Since lattice-based cryptography has gained traction in recent years, interest in its implementation-security aspect is also increasing. For the case of passive side-channel

<!-- PDF_PAGE: 7 -->

## PDF page 7

Leon Groot Bruinderink and Peter Pessl

27

attacks, previous works showed, e.g., the applicability of cache attacks to lattice-based signa- tures [GBHLY16, PBY17, BBK + 17] and specialized power analysis of lattice-based cryptog- raphy [PPM17]. Countermeasures, such as masked implementations [OSPG18, RRVV15] as well as shuffling and other randomization techniques [Saa18], are also being proposed. Many lattice-based schemes require high-precision sampling from a discrete Gaussian distribution. However, it appears to be difficult to implement discrete Gaussian samplers securely. In fact, previous attacks [GBHLY16, Pes16, PBY17, EFGT17] exploited the non-constant time nature of samplers. While there do exist first approaches to imple- menting discrete Gaussian samplers securely [MW17, HLS18, KRR + 18], both Dilithium and qTESLA opt to use samples from the uniform distribution for signing instead. This does not only allow much easier (constant-time) sampling, but also drastically simplifies the signature rejection step. In fact, non-constant time rejection was also exploited in previous work [EFGT17]. The downside of using the uniform distribution is slightly larger signatures. Compared to a Gaussian-based instantiation of Dilithium described in [DLL + 17], signatures of the uniform version are larger by approximately 10 %. Active implementation attacks on lattice-based cryptography also received some prior attention. Two concurrent works [BBK16, EFGT16] investigated fault attacks on non- deterministic lattice-based signature schemes, such as BLISS [DDLL13], GLP [GLP12], PASSSign [HPS + 14], and ring-TESLA [ABB + 16]. Espitau et al. [EFGT16] investigated loop-abort faults in the generation of the noise-polynomial y ∈ R q . This means that the sampling algorithm for this polynomial is cut off after the m’th noise coefficient, i.e. y = (y 0 , . . . , y m−1 , 0, . . . , 0). A key-recovery is possible if m n. The target distribution of y is not relevant; the general attack framework applies to both BLISS (which uses the discrete Gaussian distribution) and the other previously mentioned schemes (which all use the uniform distribution). Like Dilithium and qTESLA, the above mentioned lattice-based signatures compute z = y + cs, where c, z are part of the signature σ and s ∈ R q is a small secret key element. We can rewrite this equation as:

c −1 z ≡ c −1 y + s mod q

(1)

where we assume that c ∈ R q is invertible (which is true with very high probability). As s is a small element, the target t = c −1 z is close to a point in the lattice generated by the vectors {w i = c −1 x i mod q |i ∈ {0, . . . , m − 1}} and qZ n , and the difference is exactly s. This means that the closest-vector problem in (1) can be solved by, e.g., a lattice reduction followed by application of Babai’s nearest plane algorithm. As this sub-lattice is of full dimension and too hard to solve at once, one can reduce the size of the problem to solve (1) for a subset I ⊆ {0, . . . , n − 1} of indices, using the projection ψ I : Z n → Z I given by ψ I ((u i ) 0≤i&lt;n ) = (u i ) i∈I . It can be shown that if the cardinality of any subset I is slightly larger than m (see the analysis in [EFGT16]), then (1) is solvable for subset I. By repeating this for multiple subsets, the complete secret key element s can be recovered. With knowledge of s the full secret key could be recovered using linear algebra.

### 2.5 Differential Fault Attacks on ECC

In this work we concentrate on differential fault attacks, in which the difference between a faulty and a correct output is used to determine information about the secret key. Previous work [BP16, ABF + 18, PSS + 17, SB18] explored such attacks on two deterministic elliptic curve signature schemes: EdDSA and deterministic ECDSA. Both of these signature schemes use the Fiat-Shamir transform, thus requiring the usage of a unique nonce per message. The fault attacks mainly focus on achieving nonce reuse, as this leads to a very efficient key-recovery. Concretely, Poddebniak et al. [PSS + 17] exploit the fact that the message is hashed twice in EdDSA. By manipulating the message in between these hashing operations with

<!-- PDF_PAGE: 8 -->

## PDF page 8

Differential Fault Attacks on Deterministic Lattice Signatures

28

Rowhammer, one can induce a nonce reuse and thus key recovery. Ambrose et al. [ABF + 18] inspect a wider range of scenarios. They show that even random faults in certain operations can allow attacks. Additionally, they show that faults affecting the nonce itself are also usable. However, for this they require a very restrictive fault model. They need that the resulting error is limited to a few bits, as an exhaustive search is required to find the exact difference between the faulty and correct nonce.

Differential Faults on Deterministic Lattice Signatures

3

In this section, we present our differential fault attacks on Dilithium. As previously mentioned, these attacks apply to qTESLA as well, as we provide the attacks for general `, k. First, we briefly describe our fault model. Then we explain the main intuition of our attacks. We identified multiple vulnerable operations, for each of them we finally describe how faulting can lead to key recovery. We also discuss additional properties, such as ease of fault injection, for the scenarios.

Fault Model. In this work we assume the possibility of injection a single random fault. These can encompass instruction skips, arithmetic faults, glitches in storage, and more. The faults are not restricted to specific operations but can be applied during a large section of execution time. This model is also used for some of the previously mentioned attacks on EdDSA [ABF + 18] (some scenarios require a more restrictive fault model). In contrast, previous active attacks on lattice-based signatures required more control, such as the ability to abort a loop [EFGT16].

### 3.1 Intuition

The intuition behind our fault attacks is as follows. We let the signer sign the same message M twice. In the first invocation we do not inject any fault and receive a valid and proper signature σ = (z, h, c). We inject a fault in the second run; we use 0 , e.g., z 0 , to denote variables in this faulted invocation. More concretely, we inject a fault such that y 0 is undisturbed and due to the determinism equal to y, yet c 0 6 = c and thus z 0 = y + c 0 s 1 . Thus, the fault induces a nonce-reuse scenario. When defining ∆z = z − z 0 (and ∆c, ∆y analogously), we have ∆z = ∆y + ∆c · s 1 = ∆c · s 1 . Thus, under the requirement that ∆c is invertible, which is true with very high probability, then s 1 = ∆c −1 · ∆z. The Fiat-Shamir with Abort structure, however, introduces an additional hurdle. We require that both the valid as well as the faulty signature computation terminate in the same iteration of the abortion loop. In other words, when using κ f to denote the final value of the loop counter κ, we need that ∆κ f = κ f − κ 0 f = 0. Observe that in Algorithm 2, loop counter κ is input to DeterministicSample. Hence, to achieve y = y 0 we have the requirement that ∆κ f = 0. Due to faulty intermediates and the influence of the rejection tests, this is obviously not guaranteed. In the remainder of this section we discuss concrete fault scenarios. That is, we explain which operations in Algorithm 2 can be faulted such that key-recovery is possible. For each scenario we will give the exploitation technique as well as state its success probability, i.e., the chance that it terminates in the same loop iteration and thus ∆κ f = 0. This probability was estimated using at least 10 000 fault simulations per scenario. An overview of the scenarios is given in Table 2, they are listed in order of appearance in Algorithm 2. The order of description will be different.

<!-- PDF_PAGE: 9 -->

## PDF page 9

Leon Groot Bruinderink and Peter Pessl

29

Table 2: Fault scenarios discussed in this paper

Name Section Description

Corrupt ρ during import of sk Random fault in expansion A := ExpandA(ρ) Random fault in sampling y := DeterministicSample(·) Random fault in polynomial multiplication w := Ay Random fault in call to H

fA ρ fA E fY fW fH

### 3.4 3.4 3.5 3.3 3.2

### 3.2 Scenario: fH

Probably the most intuitive way to achieve a nonce-reuse is the fH scenario, where a random fault is injected into the computation c ∈ B 60 := H(µ||w 1 ). This can be achieved by either manipulating one of the inputs µ, w 1 immediately before they are being used in H, or by directly injecting a fault into the hash function H itself. We will show in Section 5.1 that it is a very reasonable assumption that an attacker can inject a fault in the correct iteration κ f , i.e., the last one in the non-faulty computation. If the rejection step is then passed with the different c 0 , secret element s 1 can be recovered as described in Section 3.1. Since c is a sparse ternary polynomial and s 1 ∈ S η l has small coefficients, their product is also small. We depict its coefficient-wise probability distribution in Figure 2, it can be approximated with a (discretized) Gaussian distribution having zero mean and σ ≈ 24.3. As kcsk 2 kyk 2 , kwk 2 , the rejection conditions for z and r 0 are likely to hold for a different c as well. This results in a high success probability of over 90 %.

0.02

Prob(cs = v)

0.01

0 -100

-50

0 50 100

v

Figure 2: Coefficient-wise probability distribution of cs

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 9]

Determining Success. There are two ways to test if ∆κ f = 0 and thus key recovery is successful. The first method is to simply recover s 1 and then test if it is small, i.e., s 1 ∈ S η l . If ∆y 6 = 0 then the recovered key will be a random vector in R `q which will not fulfill the bound on the ` ∞ norm. Alternatively, one can also exploit the small norm of cs by computing k∆zk 2 (or also k∆zk ∞ ) and test if it is below a certain threshold. Again, ∆y 6 = 0 will lead to a very large value of k∆zk 2 . Apart from ∆κ f = 0, we also require that ∆c is invertible. This is true with very high probability. The fraction of invertible polynomials in R q is (1 − 1/q) n [LPR13], which is about 1 − 2 −15 for the Dilithium parameters. In the remainder of this paper, we assume this fraction also holds for the polynomials described by ∆c (i.e. the difference of two random sparse ternary polynomials c, c 0 ∈ B 60 ). We test for invertibility and consider the attack to have failed in the rare case that ∆c is not invertible.

<!-- PDF_PAGE: 10 -->

## PDF page 10

Differential Fault Attacks on Deterministic Lattice Signatures

30

### 3.3 Scenario: fW

Instead of directly faulting the hash function H, it is also possible to alter c := H(µ||w 1 ) by manipulating the computation of its inputs µ, w 1 . The message/public key hash µ is also used as seed for DeterministicSample, hence faults in the computation µ := CRH(tr||M ) are not exploitable. Faults in the computation of w := Ay which lead to an incorrect w 1 , however, can be exploited. The required polynomial multiplications in R q can be efficiently implemented using the Number Theoretic Transform (NTT). Still, the runtime of multiplication is higher than that of hashing, thus it can be a more viable target for fault attacks. An NTT is essentially an FFT-like transform over a prime field and uses similar implementation techniques, i.e., butterfly networks. Due to these techniques, the number of coefficients in w affected by a single random fault can range from 1 to all n · k.

As unaffected coefficients of w clearly pass rejection and a single altered one is sufficient to achieve ∆c 6 = 0, minimizing the number of faulty coefficients increases the success probability. Thus, unlike in our other scenarios the concrete fault position has a much stronger impact. To give a sense of possible success probabilities, we evaluated the two most extreme cases. First, we inject a fault in the forward-NTT of y. Such a fault spreads to all n · k coefficients of w and thus leads to a low success probability (25.3 %). Second, we fault the inverse-NTT applied to w such that only two coefficients are affected. With a success probability of over 90 %, this sub-scenario is similar to directly faulting H. Note that while single-coefficient faults are also possible, they are slightly less likely to lead to a successful key-recovery. This is due to the chance that a faulty coefficient w 0 still rounds to the correct w 1 0 = w 1 , which results in ∆c = 0 and the fault not being exploitable.

### 3.4 Scenarios: fA ρ , fA E

Another possibility to achieve a faulty w = Ay is to manipulate the expansion of seed ρ into the matrix A. As seen in Algorithm 2, this is done before entering the abort loop and is thus always executed at the same time. Furthermore, ExpandA is a major contributor to overall runtime (cf. Section 5.2). Both these properties drastically simplify fault injection for this scenario. Also, A has a larger footprint (20 kB in Dilithium-III) than other variables and is potentially kept in memory for a prolonged time, i.e., by caching it one does not need to re-run ExpandA for every singing operation. These properties make A a particularly interesting target for memory-based faults, such as Rowhammer.

When focusing on more traditional faulting techniques, then differences in A can be achieved by either manipulating the seed ρ, e.g., during loading of the private key (scenario := ExpandA(ρ) (scenario fA E ). fA ρ ), or by inserting a glitch into the expansion A ∈ R k×` q On first glance these scenarios might seem identical. There are, however, some major differences. Observe that in Algorithm 4, which sketches the method for expanding ρ into A, the k · ` polynomials comprising A are generated using independent calls to SHAKE. Thus, any single fault in the SHAKE permutation leads to just one corrupted polynomial. Consequently, after the matrix-vector multiplication Ay we have n differing coefficients of w. This leads to a success probability of approximately 54 %.

Directly faulting ρ, either during import or in storage, obviously results in an all different A and thus w. This decreases the success probability to just 14 %. However, this type of fault has a major advantage when it comes to defeating countermeasures. It is potentially (semi-)permanent and can thus, at least under certain circumstances, not be detected by the generic double-computation or verification-after-sign countermeasures. In Section 6 we discuss this in more detail.

<!-- PDF_PAGE: 11 -->

## PDF page 11

Leon Groot Bruinderink and Peter Pessl

Algorithm 4 ExpandA(ρ)

Input: Seed ρ Output: uniform A ∈ R k×` q 1: for i := 0 . . . k − 1 do 2: for j := 0 . . . ` − 1 do 3: A i,j := SamplePoly(ρ||i||j) 4: return A

5: function SamplePoly(s) 6: t ∈ {0, 1} 5·SHAKErate := SHAKE128(s) 7: u := 0 8: while u &lt; n do

v := next dlog 2 qe bits of t if v &lt; q then a i := v u := u + 1 return a

9: 10: 11: 12:

13:

### 3.5 Scenario: fY

31

So far, we have only discussed fault-induced nonce-reuse scenarios, i.e. the case where y 0 = y. For our final scenario, we will switch to partial nonce-reuse. Unlike all previous scenarios, inducing a partial reuse still leads to valid signatures and is thus not detectable with a signature verification. We introduce some additional notation for element t ∈ R `q : we define t u ∈ R q to be q−1 the u’th element of t and (t u ) v ∈ [− q−1 2 , 2 ] to be its v’th coefficient, for 0 ≤ u &lt; ` and 0 ≤ v &lt; n. We define e j for 0 ≤ j &lt; n to be the j-th unit vector, i.e. the vector with a 1 at position j and zero otherwise.

Simple Example. First, let us assume the following. We inject a fault in y 0 ∈ S γ ` 1 −1 such that only a single coefficient (y 0 u ) v ∈ y (with index u ∈ {0, . . . , `−1} and v ∈ {0, . . . , n−1}) is changed to a random value (while preserving |(y 0 u ) v | ≤ γ 1 − 1). Still, this leads to a completely different w 1 , and therefore to a different c 0 and z 0 = y 0 + c 0 s 1 . We then compute s 1 = ∆c −1 · ∆z and determine u by simply using the one index for which s 1,u ∈ / S η . For all i 6 = u we have that ∆y i = 0, thus recovery of these key polynomials succeeds. If we now compute the difference ∆z u , we will notice the following: for indices i 6 = v we see |∆z i | ≤ 2δ for some threshold δ chosen such that kcs 1 k ∞ ≤ δ holds for any c and s 1 . Concretely, we can set δ = 60η. The injected fault in (y 0 u ) v can cause any difference to the value, but on average it will be large. On expectation |(y 0 u ) v − (y u ) v | will be 2γ 1 3 −1 , as both of these coefficients are random values in [−(γ 1 − 1), (γ 1 − 1)] (by our assumption). Since kcs 1 k ∞ ≤ δ 2γ 1 3 −1 , we can detect index v and thus the position of the fault by using the index of maximum |∆z u |. We finally recover s 1,u as follows. Simply speaking, we eliminate row v of the linear system s 1,u = ∆c −1 · ∆z u , guess the value of (s 1,u ) v (exhaustive search), solve for the full s 1,u and test if it is in S η . Note that similarly we could also directly guess the value of (∆y u ) v (instead of (s u ) v ), albeit there the search-space is much larger. This latter scenario is the direct counterpart to the partial nonce reuse fault attack on elliptic curve signatures (as described in [ABF + 18] and mentioned in Section 2.5): an exhaustive search is used to determine the exact error in the faulted nonce. We will show next that for lattice-based signatures these partial-reuse attacks are way more powerful. The exhaustive search can be replaced with solving a lattice problem,

<!-- PDF_PAGE: 12 -->

## PDF page 12

Differential Fault Attacks on Deterministic Lattice Signatures

32

Algorithm 5 DeterministicSample γ 1 −1 (s) (simplified 6 )

Input: Seed s Output: y ∈ S γ ` 1 −1 1: for u := 0 . . . ` − 1 do 2: t ∈ {0, 1} 5·SHAKErate := SHAKE256(s||u) 3: v := 0 4: while v &lt; n do 5: r := next 2dlog 2 γ 1 e bits of t 6: if r ≤ 2(γ 1 − 1) then 7: (y u ) v := q + γ 1 − 1 − r 8: v := v + 1 9: return a

. Sample ` nonce polynomials

. Rejection sampling

which is much more efficient. The far larger number of tolerable errors allows replacing the very restrictive fault model (influencing a small number of bits of the nonce) with random faults in SHAKE.

Efficient Partial Nonce Reuse Attack. The nonce y ∈ S γ ` 1 −1 is generated by function DeterministicSample, a simplified 6 version is given in Algorithm 5. Note that input seed s changes whenever a signature is rejected (Algorithm 2), and the counter u will change the individual elements of y. The idea is that we now fault SHAKE (Line 2), but in such a way that it only changes a few coefficients of y u for some u ∈ {0, . . . , ` − 1}. Since all coefficients of (y u ) are sampled sequentially, a fault that only affects the last few bytes of t 0 will only change the last few coefficients of (y u ). As mentioned in Section 2.3, SHAKE operates on a state x of r + c bits and consists of an absorb phase and a squeeze phase. If a fault is injected during the absorb phase, the output of SHAKE will be completely different. However, if the fault is injected near the end of the squeeze phase, only the last few applications of f will operate on a faulty state x and thus return an erroneous output (cf. Section 2.3). In particular, as DeterministicSample requests 5 output blocks of SHAKE (Line 2), an injected fault in, e.g., the last or second-to-last application of Keccak-f during the squeeze phase will cause changes in the last few bytes of t 0 . Thus, only the last few coefficients of y u 0 will differ i.e. ∆y u = (0, . . . , 0, ζ v , ζ v+1 , . . . , ζ n−1 ) for some index v ∈ {0, . . . , n − 1}. Note that the index v for which the values start to differ will vary depending on how many elements were accepted from the first few output blocks of SHAKE. We can again detect index v similarly as mentioned previous: by taking the first index where |∆z u | ≥ 2δ. However, we cannot apply the brute-force search for the corresponding elements in (s 1,u ) v≤i&lt;n anymore: the search-space will be too large. Instead, we will transform the search for these n − v secret coefficients to a lattice problem similarly as described in Section 2.4. Thus, when writing:

t = ∆c −1 ∆z u = ∆c −1 ∆y u + s 1,u

we have a target t and want to determine the closest point on the lattice generated by ∆c −1 . The difference between t and its closest lattice point is exactly s 1,u . Solving this closest-vector problem is made possible by using that the first v coefficients of ∆y u are 0. We use the lattice generated by basis vectors {w i = ∆c −1 x i mod q |i ∈ {v, v +1, . . . , n−1}} and qZ n . Take I = {m, m + 1, . . . , n − 1} to be the target subset of indices, where m &lt; v and apply ψ I to these basis vectors, where ψ I as defined in Section 2.4. We then cast the

6 For example, with very small probability the 5 · SHAKErate bits are not enough to generate enough values for any y i . In that case, another call to SHAKE and more rejection sampling is done.

<!-- PDF_PAGE: 13 -->

## PDF page 13

Leon Groot Bruinderink and Peter Pessl

33

Table 3: Results of injecting faults in DeterministicSample

Squeeze phase iteration

Average running time lattice reduction

Average number of errors in y u

1P (last) 2P (second to last)

39 93

2.3s 35.8s

Table 4: Fault-attack success probability in percent

fA ρ

fA E fY-1P

### 14.3 54.4 24.8

fY-2P fW

fH

### 23.9 25.4 - 90.3 91.0

problem at hand to a unique shortest-vector problem as, e.g., described by Albrecht et al. [AFG13], and then apply a lattice-reduction algorithm (like LLL or BKZ). If successful, we retrieve a small n − m dimensional vector s guess , whose coefficients correspond to the last n − m coefficients of s 1,u . To get the full s 1,u , we replace the last n − m coefficients of ∆z u by the coefficients of s guess , transform rotation-matrix ∆C of ∆c into C by replacing the last n − m columns by the identity columns e m , e m+1 , . . . , e n−1 and compute the full

−1

s guess = ∆zC . We can verify correctness by checking that s guess ∈ S η . In our experiments, we injected a random fault in the last (denoted by 1P) or second-to- last (denoted by 2P) application of Keccak-f inside SHAKE (called in Algorithm 5, line 2). Since the input to SHAKE is shorter than the rate r, out of the total five applications of Keccak-f these are the fourth (2P) and fifth (1P), respectively. Faults in the 3 earlier applications of Keccak-f did not yield a solvable lattice problem. We performed 1000 experiments for both 1P and 2P and determined the average number of errors (so n − v) and the average running time for BKZ (on an Intel Xeon E5-4669 v4 @ 2.20GHz). In our experiments, we took m such that the cardinality of I is about 1.4(n − v). For the lattice reduction, we used BKZ with block-size 25 but included an early abort, i.e., we abort reduction as soon as a potential key-candidate (a vector in S η ) is found. The results are shown in Table 3. The success probability of the lattice reduction was 100%. Thus, if a fault is correctly injected and ∆κ f = 0, then the key s 1 can always be recovered. The probability that ∆κ f = 0 is between 24 and 25 % (Table 4).

### 3.6 Summary of Scenarios

We now give a summary of the different fault scenarios. In Table 4 we restate the success probability of all fault scenarios. Recall that in scenario fW a large number of outcomes is possible, but we analyzed the best and worst possible outcomes. For scenarios fY, fH, and fW we assume that the fault is injected in the last iteration κ f . fH is the most intuitive scenario and also achieves the highest success probability. However, it is also the smallest of all targets (cf. Section 5.2). The lowest success probability is achieved for fA ρ , yet with the huge advantage of being potentially permanent. Faulting the expansion of A offers both a large and fixed-time target. Finally, scenario fY lead to valid yet still exploitable signatures.

4 Signing with the Recovered Key

In the previous sections we showed how to recover s 1 after a successful fault injection. However, s 1 is only one component of the private key sk = (ρ, K, tr, s 1 , s 2 , t 0 ). The seed ρ, which is used for generating the matrix A, is also part of the public key. tr can be

<!-- PDF_PAGE: 14 -->

## PDF page 14

Differential Fault Attacks on Deterministic Lattice Signatures

34

trivially recomputed as CRH(ρ||t 1 ) (cf. Algorithm 1). K is used as a secret input to the deterministic sampler and cannot be recovered with our attack. However, an attacker can just choose any random K and still produce valid signatures. The only downside here is that the owner of the full private key can test whether or not a signature is forged. He simply runs the signature algorithm and tests for equivalence, a new K will obviously result in a different yet still valid signature. The situation for the two remaining components, namely s 2 and t 0 , is less clear. Recall that t := As 1 + s 2 (cf. Algorithm 1). If t is known, then recovering s 2 boils down to simple linear algebra. However, for compression one computes a pair (t 1 , t 0 ) satisfying t 1 · 2 d + t 0 = t and includes only the upper part t 1 in the public key. Thus, the equation t 1 · 2 d + t 0 = As 1 + s 2 cannot be directly solved. Note also that during signature computation s 2 and t 0 are only used for hint generation and rejection purposes. Thus, there are no simple equations that can be exploited for recovering this part of the private key. This obviously does not imply that there is no information on s 2 present. For instance, in a valid signature we have that kr 0 k ∞ &lt; γ 2 − β, with (r 1 , r 0 ) := Decompose(w − cs 2 ). As w is recoverable since s 1 is already known, an attacker will get constraints for the possible values for s 2 . A large number of such constraints could result in a fully determined s 2 . However, we expect that a very large number of valid signatures and high computational effort is needed to perform such a recovery. Instead, we now present a modified signing procedure (Algorithm 6) that does not require knowledge of s 2 . Thus, the property that only a single valid/faulty signature pair is needed for the attack is preserved. Algorithm 6 starts off by recomputing tr and sampling a random K, as described earlier. Then we compute u := As 1 − t 1 · 2 d , which is exactly the difference of the unknown quantities, i.e., u = t 0 − s 2 . Signature generation then continues as usual up until the computation of the hint h. In the original signing algorithm we have h := MakeHint(−ct 0 , w − cs 2 + ct 0 ). The second argument to MakeHint can be trivially rewritten as w − cs 2 + ct 0 = w + cu. The first argument −ct 0 cannot be computed without knowledge of t 0 . We get around this by exploiting the fact that t 0 is vastly larger than s 2 , with coefficients in the intervals [±2 d−1 ] and [±η], respectively. Thus, we have that u = t 0 − s 0 ≈ t 0 and simply substitute −ct 0 with −cu. We then skip all rejection conditions that cannot be tested without knowing s 2 or t 0 . Essentially, we just test that if kzk ∞ ≥ γ 1 − β and reject the signature if this is the case. Finally, we perform a verification of the signature to catch the very improbable case that MakeHint(−cu, w + cu) 6 = MakeHint(−ct 0 , w + cu). Due to the removal of rejection conditions, this modified signing algorithm potentially leaks secret information. Thus, anyone being aware of the fact that signatures are computed by our modified algorithm could maybe also recover the secret key. Since all produced signatures are valid, there is no trivial way to test for this condition (without already knowing the key, as explained earlier).

5 Experimental Verification

In this section, we back up our previous theoretical expositions and simulations by running our attack on an actual device. After discussing our platform, we show how an attacker can inject a fault in the iteration κ f without determining the concrete value. This requires at least some knowledge of the implementation. For this reason, we also demonstrate that a random fault anywhere during the signing procedure has a high chance of being exploitable.

<!-- PDF_PAGE: 15 -->

## PDF page 15

Leon Groot Bruinderink and Peter Pessl

Algorithm 6 Dilithium Sign with Recovered Key s 1

35

Input: Message M , private key part s 1 , public key pk = (ρ, t 1 ) Output: Signature σ = (z, h, c) 1: tr ∈ {0, 1} 384 := CRH(ρ||t 1 ) . Recompute tr from public information 2: K ← {0, 1} 256 . Sample a random seed 3: u := As 1 − t 1 · 2 d . As 1 − t 1 · 2 d = t 0 − s 2 k×` := ExpandA(ρ) 4: A ∈ R q 5: µ ∈ {0, 1} 384 := CRH(tr||M ) 6: κ := 0, (z, h) := ⊥ 7: while (z, h) = ⊥ do 8: y ∈ S γ l 1 −1 := DeterministicSample(K||µ||κ) 9: w := Ay 10: w 1 := HighBits(w) 11: c ∈ B 60 := H(µ||w 1 ) 12: z := y + cs 1 13: h := MakeHint(−cu, w + cu) . MakeHint(−c(s 2 − t 0 , ), w − cs 2 + ct 0 ) 14: if kzk ∞ ≥ γ 1 − β then . Remove rejection conditions 15: (z, h) := ⊥ 16: else 17: if not Verify(pk, M, (z, h, c)) then (z, h) := ⊥ . Test for correctness 18: κ := κ + 1 19: return σ = (z, h, c)

Platform. For our experiments, we use an STM32F405 microcontroller (ARM Cortex- M4F) running on a ChipWhisperer CW308 side-channel evaluation board. We run the Dilithium C reference implementation 7 (compiled with -O3) and clock our device at 30 MHz. For attack evaluation, we signal the start and end of signing with a trigger pin. As faulting method we make use of clock glitches. We mounted attacks for all scenarios except fA ρ , all with success. For the scenarios targeting the SHAKE XOF, i.e., fA E , fY, and fH, the ability to precisely time clock glitches and thus to attack very specific instructions is not needed. A single such permutation takes approximately 40 000 clock cycles and we only require that its output is different, thus any random fault suffices. In fact, we did not determine the exact location or effect of the fault. Attacks on the polynomial multiplication (scenario fW) can benefit from more precise fault injection (see Section 3.3). However, even random faults yield a high success rate (Section 5.2).

Injecting a Fault in the Correct Iteration

5.1

Recall that a fault is only exploitable if both the faulted and the non-faulted execution of the signing algorithm terminate in the same iteration of the abort loop, i.e., ∆κ f = 0. Clearly, in the scenarios fY, fW, and fH, an attacker can maximize the success probability by injecting the fault in this last iteration κ f . The Dilithium reference implementation is constant (read: key-independent) time. The individual rejection conditions (line 12 of Algorithm 2) are still tested as soon as possible. This minimizes the runtime of failed iterations but does not leak sensitive information on the key. Quite on the contrary, this non-constant-time behavior somewhat complicates the fault attack. Even an attacker knowing κ f cannot exactly pinpoint the time of execution of vulnerable operations and thus the best time to inject a fault.

7 Reference implementation available at https://pq-crystals.org/dilithium/software.shtml

<!-- PDF_PAGE: 16 -->

## PDF page 16

Differential Fault Attacks on Deterministic Lattice Signatures

36

Table 5: Runtime-percentage of vulnerable code

fA E fY

κ f = 1 Overall

### 47.4 24.3

### 3.8 2.0

fW fH Sum

### 11.2 5.7

### 2.9 1.5

### 65.2 33.5

We get around this by using the observation that the last loop iteration κ f is, unlike the previous ones, constant time. Only there all operations are guaranteed to be performed and apart from the rejections the code is constant time. Thus, we determine the time of execution of vulnerable operations as follows. First, we perform the undisturbed signing and measure its runtime. And second, we simply subtract a fixed offset (depending on the to-be-faulted operation) from this overall runtime. We used this method for our attacks in the scenarios fY, fH, and fW, and were successful for any κ f .

### 5.2 Unprofiled Attacks

The above method is highly accurate, yet requires some device/code profiling. Concretely, an attacker needs to determine the time offsets (either from the start or finish of the signing operation) of the vulnerable code. This might not always be a realistic assumption. For this reason, we now show that an attacker injecting a random fault anywhere in the signing process still has a high chance of succeeding. We do so by measuring the runtime (in cycles) of the vulnerable code and relating it to the overall execution time (Table 5). In the best-case scenario for such an attacker, the signing algorithm terminates in the first iteration (κ f = 1). In this case, 65.2 % of execution time are vulnerable. In the general case (no restriction to κ f = 1), the success probability goes down to one-third of the total execution time. In both cases, sampling of the matrix A takes by far the most time. Additionally, it is performed at a fixed time in the execution, shortly after the invocation of the signing algorithm. Thus, in reality an unprofiled attacker faulting somewhere in this region has a much higher chance of hitting ExpandA than stated in Table 5. In Figure 3, we further visualize the general case and compare runtime to success probability for different scenarios. Recall that depending on the concrete fault position, the success probability of scenario fW varies drastically (see Table 4). For the case of the unprofiled attacker, we narrowed down this probability by performing 1000 fault attacks on our target device, with faults at random positions inside fW. Approximately 62 % of these faults were exploitable. Faulting the call to H yields the highest success probability (Table 4), but also has the smallest footprint. As discussed in Section 3.5, 2/5 of the time spent on the SHAKE call by DeterministicSample is vulnerable to the attack. This makes it a slightly larger target compared to fH, but also with a much lower success probability. In total, a fault inside the vulnerable portions can be exploited with a probability of 56 %. These cover 33.5 % of execution time, thus approximately 19 % of random faults anywhere during signing lead to key recovery.

6 Countermeasures

When presenting new attacks, a discussion on potential countermeasures should never be missing. For this reason, we present the applicability and effectiveness of three generic countermeasures against the fault attacks described in this work. For each of these methods, we give the runtime costs and state which fault scenarios will be mitigated by it. A summary of the latter is shown in Table 6.

<!-- PDF_PAGE: 17 -->

## PDF page 17

Leon Groot Bruinderink and Peter Pessl

1

fH

Success probability

0.8

fW

0.6

0.4

fY

0.2

0

0 0.05 0.1 0.15

37

Total

fA E

0.15

0.10

### 0.05 0.01

### 0.2 0.25 0.3 0.35 0.4

Portion of total signing time

Figure 3: Comparison of scenarios regarding runtime as portion of total signing time (from Table 5) vs. success probability (from Table 4). Lines of constant product are drawn in solid gray.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 17]

Double computation. While determinism leads to the applicability of differential fault attacks in the first place, it can also be used as a countermeasure against such attacks. Concretely, many faults can be detected by running the signature algorithm twice and testing the output for equality. This obviously doubles execution time. The countermeasure can be defeated by either injecting an identical fault twice, which can be challenging, or by using a permanent fault, e.g., in scenario fA ρ with the seed ρ.

Verification-after-sign. Many of the presented attack scenarios lead to signatures being invalid. Thus, performing signature verification after signing is an effective countermeasure. As runtime costs of verification are less than one-third of signing (see [LDK + 17]), this option is also much more efficient than double computation. As a downside, however, it cannot detect faults injected into the sampling of y as this yields valid signatures. Permanent faults in ρ can be detected if tr = CRH(ρ||t 1 ) is computed during key generation and then stored as part of the private key (as described in Algorithm 1). If tr is recomputed in the signing algorithm using the public key, then faults in ρ are not detectable.

Additional randomness. A final and very simple countermeasure is to re-randomize the deterministic sampling of the noise y. One can simply sample a random r ← 0, 1 256 and then invoke y := DeterministicSample(K||µ||κ||r). This effectively mitigates the differential fault attack as the faulted call to the signing algorithm uses different y and thus ∆y 6 = 0. Whats more, this method might also hamper further side-channel attacks coming as side-effects of determinism. As observed by Seuschek et al. [SHS16] and Samwell et al. [SBB + 18], mixing the known message µ with the secret seed K in a hash function (in Dilithium this is SHAKE in DeterministicSample) opens the gates for DPA-like attacks. Hash functions are hard to protect against such attacks; using an additional random input can be a cheap alternative. How r needs to be introduced to maximize the protection while keeping the necessary size of r small likely depends on the used hash function, further investigations are needed to answer this question for the case of SHAKE. The added protection against implementation attacks does not negate the protection against incorrect implementation and resulting nonce reuse (using the same y for different messages). For instance, using a constant r effectively reverts signing to its deterministic version. Additional upsides of this countermeasure are its simplicity and negligible runtime overhead. Furthermore, unlike straight-forward implementations of the two previous

<!-- PDF_PAGE: 18 -->

## PDF page 18

Differential Fault Attacks on Deterministic Lattice Signatures

38

Table 6: Applicable countermeasures

fA ρ

Double computation Verification-after-sign Additional randomness †

7 3/7 ∗ 3

∗

Under certain conditions. Not supported by proof of Dilithium [KLS18].

†

fA E fY fW fH

3 3 3

3 7 3

3 3 3

3 3 3

countermeasures, it is single-pass and so does not require to keep a copy of the message in memory. Note that this countermeasure was already proposed in the context of EdDSA [ABF + 18, SBB + 18], but it can also be applied to lattice-based signatures. In fact, a very recent update of the qTESLA specification made use of this countermeasure mandatory and cites the presented attacks as reason. There are, however, also considerable downsides of this countermeasure. First, unlike the two previous countermeasures, this countermeasure is probabilistic and requires some source of entropy, i.e., a true random number generator. Such a generator might not be available on all devices, especially low-resource ones. And second, this countermeasure violates the security proof of Dilithium. Kiltz, Lyubashevksy, and Schaffner [KLS18] present a tight proof in the quantum random oracle model (QROM) based on the hardness of MLWE, MSIS, and a new problem called SelfTargetMSIS. They require the signature scheme to be deterministic. They do give an alternative proof for a probabilistic version of Dilithium, yet it is not tight and loses security linearly in the number of observed unique signatures per message. Thus, introducing this countermeasure voids provable security guarantees, albeit no concrete attack is known. The Dilithium authors "still recommend using deterministic signatures except in environments that may be vulnerable to the aforementioned side-channel attacks" [LDK + 17]. However, determining whether or not an environment is vulnerable is not easy, as clearly shown by the Rowhammer bug.

### References

[ABB + 16]

Sedat Akleylek, Nina Bindel, Johannes A. Buchmann, Juliane Krämer, and Giorgia Azzurra Marson. An Efficient Lattice-Based Signature Scheme with Provably Secure Instantiation. In AFRICACRYPT, volume 9646 of LNCS, pages 44–60. Springer, 2016.

[ABB + 17]

Erdem Alkim, Nina Bindel, Johannes A. Buchmann, Özgür Dagdelen, Edward Eaton, Gus Gutoski, Juliane Krämer, and Filip Pawlega. Revisiting TESLA in the Quantum Random Oracle Model. In PQCrypto, volume 10346 of LNCS, pages 143–162. Springer, 2017. Full version available at https://ia.cr/ 2015/755.

[ABF + 18]

Christopher Ambrose, Joppe W. Bos, Björn Fay, Marc Joye, Manfred Lochter, and Bruce Murray. Differential Attacks on Deterministic Signatures. In CT-RSA, volume 10808 of LNCS, pages 339–353. Springer, 2018.

[AFG13]

Martin R. Albrecht, Robert Fitzpatrick, and Florian Göpfert. On the Efficacy of Solving LWE by Reduction to Unique-SVP. In ICISC, volume 8565 of LNCS, pages 293–310. Springer, 2013.

<!-- PDF_PAGE: 19 -->

## PDF page 19

Leon Groot Bruinderink and Peter Pessl

[BAA + 17]

39

Nina Bindel, Sedat Akleylek, Erdem Alkim, Paulo S. L. M. Barreto, Johannes Buchmann, Edward Eaton, Gus Gutoski, Juliane Krämer, Patrick Longa, Harun Polat, Jefferson E. Ricardini, and Gustavo Zanon. qTESLA. Submission to the NIST Post-Quantum Cryptography Standardization [NIS], 2017. https: //qtesla.org.

[BBK16]

Nina Bindel, Johannes A. Buchmann, and Juliane Krämer. Lattice-Based Signature Schemes and Their Sensitivity to Fault Attacks. In FDTC, pages 63–77. IEEE Computer Society, 2016.

[BBK + 17]

Nina Bindel, Johannes A. Buchmann, Juliane Krämer, Heiko Mantel, Johannes Schickel, and Alexandra Weber. Bounding the Cache-Side-Channel Leakage of Lattice-Based Signature Schemes Using Program Semantics. In FPS, volume 10723 of Lecture Notes in Computer Science, pages 225–241. Springer, 2017.

[BCN + 06]

Hagai Bar-El, Hamid Choukri, David Naccache, Michael Tunstall, and Claire Whelan. The Sorcerer’s Apprentice Guide to Fault Attacks. Proceedings of the IEEE, 94(2):370–382, 2006.

[BDL + 11]

Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe, and Bo-Yin Yang. High-Speed High-Security Signatures. In CHES, volume 6917 of LNCS, pages 124–142. Springer, 2011.

[BDPV07]

Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche. Sponge functions. ECRYPT Hash Workshop, 2007.

[bms10]

"bushing", "marcan", and "sven". PS3 epic fail. 27th Chaos Communica- tion Congress, 2010. https://events.ccc.de/congress/2010/Fahrplan/ events/4087.en.html.

[BP16]

Alessandro Barenghi and Gerardo Pelosi. A Note on Fault Attacks Against Deterministic Signature Schemes. In IWSEC, volume 9836 of LNCS, pages 182–192. Springer, 2016.

[DDLL13]

Léo Ducas, Alain Durmus, Tancrède Lepoint, and Vadim Lyubashevsky. Lattice Signatures and Bimodal Gaussians. In CRYPTO (1), volume 8042 of LNCS, pages 40–56. Springer, 2013.

[DLL + 17]

Léo Ducas, Tancrède Lepoint, Vadim Lyubashevsky, Peter Schwabe, Gregor Seiler, and Damien Stehlé. CRYSTALS – Dilithium: Digital signatures from module lattices. Cryptology ePrint Archive, Report 2017/633, 2017. Publication to [LDK + 17].

[EFGT16]

Thomas Espitau, Pierre-Alain Fouque, Benoît Gérard, and Mehdi Tibouchi. Loop-Abort Faults on Lattice-Based Fiat-Shamir and Hash-and-Sign Signa- tures. In SAC, volume 10532 of LNCS, pages 140–158. Springer, 2016.

[EFGT17]

Thomas Espitau, Pierre-Alain Fouque, Benoît Gérard, and Mehdi Tibouchi. Side-Channel Attacks on BLISS Lattice-Based Signatures: Exploiting Branch Tracing against strongSwan and Electromagnetic Emanations in Microcon- trollers. In CCS, pages 1857–1874. ACM, 2017.

[FS86]

Amos Fiat and Adi Shamir. How to Prove Yourself: Practical Solutions to Identification and Signature Problems. In CRYPTO, volume 263 of LNCS, pages 186–194. Springer, 1986.

<!-- PDF_PAGE: 20 -->

## PDF page 20

Differential Fault Attacks on Deterministic Lattice Signatures

40

[GBHLY16] Leon Groot Bruinderink, Andreas Hülsing, Tanja Lange, and Yuval Yarom. Flush, Gauss, and Reload - A Cache Attack on the BLISS Lattice-Based Signature Scheme. In CHES, volume 9813 of LNCS, pages 323–345. Springer, 2016.

[GLP12]

Tim Güneysu, Vadim Lyubashevsky, and Thomas Pöppelmann. Practical Lattice-Based Cryptography: A Signature Scheme for Embedded Systems. In CHES, volume 7428 of LNCS, pages 530–547. Springer, 2012.

[GMM16]

Daniel Gruss, Clémentine Maurice, and Stefan Mangard. Rowhammer.js: A remote software-induced fault attack in JavaScript. In DIMVA, volume 9721 of LNCS, pages 300–321. Springer, 2016.

[HLS18]

Andreas Hülsing, Tanja Lange, and Kit Smeets. Rounded Gaussians. In PKC, volume 10770 of LNCS, pages 728–757. Springer, 2018.

[HPS + 14]

Jeffrey Hoffstein, Jill Pipher, John M. Schanck, Joseph H. Silverman, and William Whyte. Practical Signatures from the Partial Fourier Recovery Problem. In ACNS, volume 8479 of LNCS, pages 476–493. Springer, 2014.

[KDK + 14]

Yoongu Kim, Ross Daly, Jeremie Kim, Chris Fallin, Ji-Hye Lee, Donghyuk Lee, Chris Wilkerson, Konrad Lai, and Onur Mutlu. Flipping bits in memory without accessing them: An experimental study of DRAM disturbance errors. In ISCA, pages 361–372. IEEE Computer Society, 2014.

[Kel18]

Julian Kelly. A Preview of Bristlecone, Google’s New Quan- tum Processor, 2018. https://research.googleblog.com/2018/03/ a-preview-of-bristlecone-googles-new.html.

[KLS18]

Eike Kiltz, Vadim Lyubashevsky, and Christian Schaffner. A Concrete Treat- ment of Fiat-Shamir Signatures in the Quantum Random-Oracle Model. In EUROCRYPT (3), volume 10822 of LNCS, pages 552–586. Springer, 2018.

[KRR + 18]

Angshuman Karmakar, Sujoy Sinha Roy, Oscar Reparaz, Frederik Vercauteren, and Ingrid Verbauwhede. Constant-time Discrete Gaussian Sampling. IEEE TC, 2018.

[LDK + 17]

Vadim Lyubashevsky, Léo Ducas, Eike Kiltz, Tancrède Lepoint, Peter Schwabe, Gregor Seiler, and Damien Stehlé. CRYSTALS-Dilithium. Submis- sion to the NIST Post-Quantum Cryptography Standardization [NIS], 2017. https://pq-crystals.org/dilithium.

[LPR13]

Vadim Lyubashevsky, Chris Peikert, and Oded Regev. A Toolkit for Ring- LWE Cryptography. In EUROCRYPT, volume 7881 of Lecture Notes in Computer Science, pages 35–54. Springer, 2013.

[Lyu09]

Vadim Lyubashevsky. Fiat-Shamir with Aborts: Applications to Lattice and Factoring-Based Signatures. In ASIACRYPT, volume 5912 of LNCS, pages 598–616. Springer, 2009.

[Moo17]

Dustin Moody. The Ship has Sailed - The NIST Post-Quantum Crypto "Competition". Invited Talk at ASIACRYPT 2017, 2017. https: //csrc.nist.gov/CSRC/media//Projects/Post-Quantum-Cryptography/ documents/asiacrypt-2017-moody-pqc.pdf.

[MOP07]

Stefan Mangard, Elisabeth Oswald, and Thomas Popp. Power analysis attacks - revealing the secrets of smart cards. Springer, 2007.

<!-- PDF_PAGE: 21 -->

## PDF page 21

Leon Groot Bruinderink and Peter Pessl

[MW17]

41

Daniele Micciancio and Michael Walter. Gaussian Sampling over the Integers: Efficient, Generic, Constant-Time. In CRYPTO (2), volume 10402 of LNCS, pages 455–485. Springer, 2017.

[NIS]

https:

NIST. Post-Quantum Cryptography Standardization. //csrc.nist.gov/projects/post-quantum-cryptography/ post-quantum-cryptography-standardization.

[OSPG18]

Tobias Oder, Tobias Schneider, Thomas Pöppelmann, and Tim Güneysu. Practical CCA2-Secure and Masked Ring-LWE Implementation. TCHES, 2018(1):142–174, 2018.

[PBY17]

Peter Pessl, Leon Groot Bruinderink, and Yuval Yarom. To BLISS-B or not to be: Attacking strongSwan’s Implementation of Post-Quantum Signatures. In CCS, pages 1843–1855. ACM, 2017.

[Pes16]

Peter Pessl. Analyzing the Shuffling Side-Channel Countermeasure for Lattice- Based Signatures. In INDOCRYPT, volume 10095 of LNCS, pages 153–170, 2016.

[Por13]

T. Pornin. Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA). RFC 6979, 2013. https://tools.ietf.org/html/rfc6979.

[PPM17]

Robert Primas, Peter Pessl, and Stefan Mangard. Single-Trace Side-Channel Attacks on Masked Lattice-Based Encryption. In CHES, volume 10529 of LNCS, pages 513–533. Springer, 2017.

[PSS + 17]

Damian Poddebniak, Juraj Somorovsky, Sebastian Schinzel, Manfred Lochter, and Paul Rösler. Attacking Deterministic Signature Schemes using Fault Attacks. Cryptology ePrint Archive, Report 2017/1014, 2017.

[RRVV15]

Oscar Reparaz, Sujoy Sinha Roy, Frederik Vercauteren, and Ingrid Ver- bauwhede. A Masked Ring-LWE Implementation. In CHES, volume 9293 of LNCS, pages 683–702. Springer, 2015.

[Saa18]

Markku-Juhani O. Saarinen. Arithmetic coding and blinding countermeasures for lattice signatures - Engineering a side-channel resistant post-quantum signature scheme with compact signatures. J. Cryptographic Engineering, 8(1):71–84, 2018.

[SB18]

Niels Samwel and Lejla Batina. Practical Fault Injection on Deterministic Signatures: The Case of EdDSA. In AFRICACRYPT, volume 10831 of LNCS, pages 306–321. Springer, 2018.

[SBB + 18]

Niels Samwel, Lejla Batina, Guido Bertoni, Joan Daemen, and Ruggero Susella. Breaking Ed25519 in WolfSSL. In CT-RSA, volume 10808 of Lecture Notes in Computer Science, pages 1–20. Springer, 2018.

[SHS16]

Hermann Seuschek, Johann Heyszl, and Fabrizio De Santis. A Cautionary Note: Side-Channel Leakage Implications of Deterministic Signature Schemes. In CS2@HiPEAC, pages 7–12. ACM, 2016.

<!-- PDF_PAGE: 22 -->

## PDF page 22

Differential Fault Attacks on Deterministic Lattice Signatures

42

A Dilithium Parameter Sets

Table 7 shows all parameter sets specified by the Dilithium authors [LDK + 17]. Parameters (n, q, weight(c), γ 1 , γ 2 ) are identical across all sets and thus allow for simpler implementation and switching of security levels.

Table 7: Dilithium Parameter Sets

I weak

II medium

n q d weight(c) γ 1 γ 2 (k, `) η β ω

256 8380417 14 60 523776 261888 (3, 2) 7 375 64

B Description of qTESLA

III recommended

IV high

256 8380417 14 60 523776 261888 (4, 3) 6 325 80

256 8380417 14 60 523776 261888 (5, 4) 5 275 96

256 8380417 14 60 523776 261888 (6, 5) 3 175 120

In this section we briefly describe the qTESLA signature scheme [BAA + 17]. Please note that we give the originally submitted version of qTESLA. Following the initial publication of this paper, in a very recent update of the qTESLA specification the additional randomness countermeasure was incorporated as part of the algorithm description. As the security proof of qTESLA allows for a probabilistic version, this countermeasure can be used without violating any security guarantees. Hence the attacks are no longer applicable. In Algorithms 7, 8, and 9, we give slightly simplified versions of key generation, signing, and verification, respectively. Note its similarity to Dilithium, we highlight this similarity by stating the corresponding variable and function names in Table 8. The main difference between Dilithium and qTESLA is that the latter is based on Ring-LWE and thus operates on polynomials in Z q [x]/(x n + 1) with n ≥ 1024. Dilithium is based on the Module-LWE assumption and uses vectors/matrices of polynomials in a fixed base ring Z q [x]/(x 256 + 1).

Algorithm 7 qTESLA Key Generation

Output: Keypair (pk, sk) 1: seed a ← {0, 1} 256 , seed y ← {0, 1} 256 2: a ∈ R q := GenA(seed a ) 3: do 4: s ∈ R q ← D σ , e ∈ R q ← D σ . Discrete Gaussian distribution D σ 5: while s and e do not fulfill certain criteria 6: t := as + e mod q 7: return (pk = (seed a , t), sk = (s, e, seed y , seed a )

<!-- PDF_PAGE: 23 -->

## PDF page 23

Leon Groot Bruinderink and Peter Pessl

Algorithm 8 qTESLA Sign (simplified)

43

Input: Message M , private key sk = (s, e, seed y , seed a ) Output: Signature σ = (c, z) 1: a ∈ R q := GenA(seed a ) 2: counter := 0 3: rand := PRF 1 (seed y , M ) 4: do 5: y := PRF 2 (rand, counter) 6: v := ay mod q 7: c := H(Round(v), M ) 8: z := y + sc 9: counter := counter + 1 10: while Reject(z, v, c, sk) 11: return σ = (c, z)

Algorithm 9 qTESLA Verify (simplified)

Input: Public key pk = (seed a , t), message M , signature σ = (c, z)) 1: a ∈ R q := GenA(seed a ) 2: w := az − tc mod q 3: return c = H(Round(w), M )

Applicability of our attacks. All attacks for Dilithium described in Section 3 can easily be adapted to the original deterministic version of qTESLA, with obviously differing success probabilities due to different parameter sets, rejection conditions, and algebraic structure. In particular, the major fault scenario (a random fault in SHAKE) would be the same: SHAKE is used in qTESLA in a similar way to build the functions described in Table 8. A subtle difference however is that Dilithium samples multiple smaller polynomials, e.g., y ∈ R `q , using independent calls to SHAKE, whereas qTESLA uses just one call to SHAKE to sample a single but larger polynomial. This affects success rates and also the available time for fault injection. For instance, in scenario fY in Dilithium one can inject a fault in the last 2 permutations in any one of the ` independent SHAKE calls, whereas in qTESLA only the last permutations of the single SHAKE call can be faulted. After faulting, key recovery is exactly the same, i.e., computing s = ∆c −1 · ∆z. Note that in qTESLA the public key t is not compressed, thus recovering e (which corresponds to s 2 in Dilithium) is trivial as soon as s (corresponds to s 1 ) is known. No adapted signature algorithm (as described in Section 4) is needed.

Table 8: Comparison of variable/parameter names and function names for Dilithium and qTESLA. Only differing names are listed. Variables: Dilithium ρ K s 1 s 2 κ µ w qTESLA seed a seed y s e counter rand v

Dilithium qTESLA

ExpandA GenA

Functions: CRH PRF 1

DeterministicSample PRF 2

HighBits Round
