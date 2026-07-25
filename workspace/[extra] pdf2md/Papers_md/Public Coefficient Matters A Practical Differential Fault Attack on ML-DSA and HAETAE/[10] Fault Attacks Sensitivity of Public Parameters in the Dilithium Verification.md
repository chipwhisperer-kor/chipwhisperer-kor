# [10] Fault Attacks Sensitivity of Public Parameters in the Dilithium Verification

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 22
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-10"
derived_asset_id: "PCM-DFA-REF-10-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[10] Fault Attacks Sensitivity of Public Parameters in the Dilithium Verification.pdf"
source_sha256: "674b0b19a4fb6592312ff9e2ca6e1d85ead0b903d2990f75302eb7a20d8d7516"
pages: 22
bbox_words: 9286
consumed_bbox_words: 9286
numeric_tokens: 941
consumed_numeric_tokens: 941
source_blocks: 242
consumed_source_blocks: 242
emitted_blocks: 210
embedded_raster_images: 1
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 22
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

Fault Attacks Sensitivity of Public Parameters in the Dilithium Verification

Andersson Calle Viera 1,2( B ) , Alexandre Berzati 1 , and Karine Heydemann 1,2

1 Thales DIS, Meyreuil, France {andersson.calle-viera,alexandre.berzati, karine.heydemann}@thalesgroup.com 2 Sorbonne Université, CNRS, Inria, LIP6, 75005 Paris, France

Abstract. This paper presents a comprehensive analysis of the veriﬁca- tion algorithm of the CRYSTALS-Dilithium, focusing on a C reference implementation. Limited research has been conducted on its suscepti- bility to fault attacks, despite its critical role in ensuring the scheme’s security. To ﬁll this gap, we investigate three distinct fault models - ran- domizing faults, zeroizing faults, and skipping faults - to identify vulner- abilities within the veriﬁcation process. Based on our analysis, we pro- pose a methodology for forging CRYSTALS-Dilithium signatures without knowledge of the secret key. Instead, we leverage speciﬁc types of faults during the veriﬁcation phase and some properties about public param- eters to make these signatures accepted. Additionally, we compared dif- ferent attack scenarios after identifying sensitive operations within the veriﬁcation algorithm. The most eﬀective requires potentially fewer fault injections than targeting the veriﬁcation check itself. Finally, we intro- duce a set of countermeasures designed to thwart all the identiﬁed sce- narios rendering the veriﬁcation algorithm intrinsically resistant to the presented attacks.

Keywords: Dilithium · Digital signature · Fault Attacks · Side-channel attacks · Post-quantum cryptography · Lattice-based cryptography

1 Introduction

Shor’s algorithm [34], capable of breaking current cryptosystems [12,32], has underscored the urgency for post-quantum cryptography (PQC). As the third round of the National Institute of Standards and Technology (NIST) has con- cluded [1], four new post-quantum public key schemes are set to be standardized by 2024. Although estimates on the availability of suﬃciently large quantum computers remain uncertain, there is a concerted eﬀort by academia and indus- try to be ready when these algorithms are standardized. It is noteworthy that of the three digital signature schemes chosen, two are based on hard problems over structured lattices. This work focuses on CRYSTALS-Dilithium [3], here- after referred to as Dilithium, which is the NIST recommended standard for quantum-safe digital signatures [1].

c The Author(s), under exclusive license to Springer Nature Switzerland AG 2024 S. Bhasin and T. Roche (Eds.): CARDIS 2023, LNCS 14530, pp. 62–83, 2024. https://doi.org/10.1007/978-3-031-54409-5 _ 4

<!-- PDF_PAGE: 2 -->

## PDF page 2

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

63

The eﬀective and secure implementation of cryptographic algorithms on current hardware platforms poses a challenge, as it might be vulnerable to fault attacks (FA) and side-channel attacks (SCA). Securing embedded cryp- tographic applications against such attacks is essential but complex. It requires not only to consider a large set of attacks but also the potential impact on per- formances of the deployed protections. Although Dilithium has been designed to be resistant to timing attacks, recent work showed that its implementations are likely to leak secret informations [2,15,21,23,25,29,30]. Fault attacks signif- icantly threaten the security of cryptographic systems, potentially undermining the integrity and conﬁdentiality of sensitive data. In this paper, we focus on the analysis of Dilithium’s veriﬁcation algorithm - a crucial component of signature schemes - with a particular emphasis on its sensitivity to fault attacks. Unlike well-established signatures, like RSA or DSA and their variants, the veriﬁcation algorithm of Dilithium has yet to be precisely analyzed [7,27,33]. By exploring theoretical attack vectors on the veriﬁcation algorithm, we aim to provide a com- prehensive understanding of the vulnerabilities associated with this procedure.

Our Contributions. In this work, we present three properties allowing the genera- tion of forged Dilithium signatures that, when combined with appropriate faults, can bypass the veriﬁcation without requiring the knowledge of the secret key. To facilitate a deeper understanding of the veriﬁcation algorithm’s sensitivity to fault attacks, we meticulously investigate each identiﬁed operation and assess its sus- ceptibility to four common theoretical fault models. From this investigation, we detail three scenarios, the most realistic ones, but we also discuss other potential locations. We comprehensively summarize the analyzed locations and the required corresponding fault models in Table 1. In addition, we present a set of relevant ded- icated countermeasures aiming at mitigating the diﬀerent scenarios.

2 Preliminaries

In this section, we present the essential background on Dilithium to better under- stand the various attack paths presented. We also give a short summary of exist- ing fault attacks and signature forgery methods relative to Dilithium.

Notations: Let us note Z q the ring of integers modulo q and Z q [X] = (Z/qZ)[X] the set of polynomials with integer coeﬃcients modulo q. We deﬁne R = coeﬃcients, reduced by Z[X] (X n + 1) the ring of polynomials with integer the cyclotomic polynomial X n + 1 and R q = Z q [X] (X n + 1) when considering integer coeﬃcients modulo q. Elements in R q are denoted by lowercase letters, while elements in R q k or R q l are denoted by bold lowercase letters. Matrices with coeﬃcients in R q are denoted by bold uppercase letters. In this context, imple- mentations such as [13,17] represent a ∈ R q as a structure of n integers, often named poly, while an element a ∈ R q k (resp. b ∈ R q l ) is represented as a structure of k (resp. l) poly and is commonly named polyveck (resp. polyvecl). In the remainder, we perform polynomial operations in R q unless otherwise noted.

<!-- PDF_PAGE: 3 -->

## PDF page 3

64 A. Calle Viera et al.

For an even (resp. odd) positive integer α, we deﬁne r 0 = r mod ± α to be the &lt; r ≤ α−1 ) such unique element r in the range − α 2 &lt; r ≤ α 2 (resp. − α−1 2 2 + that r ≡ r mod α. For α ∈ N, we deﬁne r = r mod α to be the unique element r in the range 0 ≤ r &lt; α. For an element w ∈ Z q , we deﬁne w ∞ as |w mod ± q|. For an element w ∈ R, i.e., w = w 0 + w 1 X + . . . + w n−1 X n−1 , we deﬁne w ∞ as max w i ∞ and we i deﬁne w = w 0 2 ∞ + w 1 2 ∞ + . . . + w n−1 2 ∞ . Let S η = {w ∈ R : w ∞ ≤ η} and S̃ η the set {w mod ± 2η : w ∈ R}. For λ ∈ Z q and an element h of k vectors of n coeﬃcients. We deﬁne |h| h j =λ as the total number of coeﬃcients of h equal to λ. op represents the boolean evaluation of the operation op.

### 2.1 Presentation of Dilithium

In 2022 Dilithium [3] was selected alongside Falcon [35] and SPHINCS + [4], yet it is the recommended PQC signature scheme for most use cases. Dilithium is a lattice-based signature scheme based on the Fiat-Shamir with aborts principle [22] and proposed by the “Cryptographic Suite for Algebraic Lattices” (CRYS- TALS) team. Its security is derived from the hardness of solving the module learning with errors (M-LWE) [3], and SelfTargetMSIS [18] problems. For a given (k, l) ∈ N, it operates over the module R q k×l , with ﬁxed q = 8380417, a 23-bit integer and n = 256. There are three security levels, from NIST level 1 to level 5, with changes essentially in the (k, l) chosen for the module R q k×l . There are also two variants of the signing algorithm, one deterministic and one randomized, the only diﬀerence being how the randomness is sampled. For eﬃ- ciency, the scheme makes use of rounding sub-functions such as Power2Round, Decompose, HighBits, LowBits, MakeHint, UseHint whose latest speciﬁcation can be found in [3]. To reduce memory storage, polynomials are stored as a byte stream, using packing and unpacking functions speciﬁed in [3].

Algorithm 1. KeyGen

Output: pk = (ρ, t 1 ), sk = (ρ, K, tr, s 1 , s 2 , t 0 ) 1 ζ ← {0, 1} 256 2 (ρ, ρ , K) ∈ {0, 1} 256 × {0, 1} 512 × {0, 1} 256 := H(ζ) H instantiated as SHAKE-256 3 A ∈ R q k×l := ExpandA(ρ) A is generated and stored in NTT Representation as Â 4 (s 1 , s 2 ) ∈ S η l × S η k := ExpandS(ρ )

5 t := A s 1 + s 2 Compute As 1 as NTT −1 ( Â NTT(s 1 )) 6 (t 1 , t 0 ) := Power2Round q (t, d) 7 tr ∈ {0, 1} 256 := H(ρ || t 1 ) 8 return pk = (ρ, t 1 ), sk = (ρ, K, tr, s 1 , s 2 , t 0 )

<!-- PDF_PAGE: 4 -->

## PDF page 4

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

65

Key Generation. The key generation in Algorithm 1 expands a matrix A ∈ R q k×l from a public seed ρ via a function ExpandA [3]. It then samples random secret vectors s 1 and s 2 . Elements of these vectors belong to R q with small coeﬃcients of size at most η, a small integer. The second part of the public key, denoted pk, is computed as t = A s 1 + s 2 but, for eﬃciency, only the higher bits t 1 are made public while the lower part t 0 is kept secret. Finally, tr is the hash of the pk and is added to the secret key, sk.

Algorithm 2. Sign

Input : sk = (ρ, K, tr, s 1 , s 2 , t 0 ) Output: σ = (c̃, z, h) 1 A ∈ R q k×l := ExpandA(ρ) A is generated and stored in NTT representation as Â 2 μ ∈ {0, 1} 512 := H(tr || M ) 3 κ := 0, (z, h) :=⊥ 4 ρ ∈ {0, 1} 512 := H(K || μ) (or ρ ← {0, 1} 512 for randomized signing) 5 while (z, h) =⊥ do Pre-compute ŝ 1 := NTT(s 1 ), ŝ 2 := NTT(s 2 ) and t̂ 0 := NTT(t 0 )

y ∈ S̃ γ l 1 := ExpandMask(ρ , κ)

6

7 8

w := A y w 1 = HighBits q (w, 2 γ 2 )

κ is increased by 1 at each call

w := NTT −1 ( Â · NTT(y))

9 c̃ ∈ {0, 1} 256 := H(μ || w 1 ) Store c in NTT representation as ĉ = NTT(c) 10 c ∈ B τ := SampleInBall(c̃) Compute cs 1 as NTT −1 (ĉ · ŝ 1 ) 11 z := y + c s 1 Compute cs 2 as NTT −1 (ĉ · ŝ 2 ) 12 r 0 := LowBits q (w − cs 2 , 2 γ 2 ) 13 if z ∞ ≥ γ 1 − β or r 0 ∞ ≥ γ 2 − β then 14 (z, h) :=⊥ 15 else 16 h := MakeHint q (−c t 0 , w − cs 2 + c t 0 , 2 γ 2 ) Compute c t 0 as NTT −1 (ĉ · t̂ 0 ) 17 if ||c t 0 || ∞ ≥ γ 2 or |h| h j =1 &gt; ω then 18 (z, h) :=⊥ 19 return σ = (c̃, z, h)

Signature. The signature, described in Algorithm 2, consists of a rejection sam- pling loop, generating a new signature until it satisﬁes some security and cor- rectness properties. The rejection loop starts by generating a masking vector y 1 with coeﬃcients below γ 1 . Then, the signer computes w = Ay and compresses it into high-order bits w 1 and low-order bits w 0 . The message is hashed with w 1 to sample a speciﬁc ternary challenge c with ﬁxed weight τ and the rest 0’s. The potential signature is computed, using s 1 as z = y + c s 1 . Because the veriﬁer does not know t 0 , the signature includes a vector h that keeps track of the coeﬃcients that overﬂow onto the high part of w 1 . Checks are performed in

1

This vector is essentially used as a random mask of the secret s 1 line 11 in Algo- rithm 1.

<!-- PDF_PAGE: 5 -->

## PDF page 5

66 A. Calle Viera et al.

lines 13 and 17 to ensure that no information about the secret key leaks and for correctness. If any of these checks fails, a new signature candidate is generated.

Signature Verification. The veriﬁcation algorithm, described in Algorithm 3, involves computing the high-order bits of A z − c t 1 2 d using the signature and the public key, pk. The result is then corrected by the hint vector h. If the sig- nature is correct, this is equal to w 1 , which allows to recompute the challenge c. To verify a signature, a ﬁnal check ensures that all the coeﬃcients of z are less than γ 1 − β and that the number of hints in h are less than ω.

Algorithm 3. Verify

Input : pk = (ρ, t 1 ), σ = (c̃, z, h) Output: T rue or F alse 1 A ∈ R q k×l := ExpandA(ρ) 2 μ ∈ {0, 1} 512 := H(H(ρ || t 1 ) || M ) 3 c := SampleInBall(c̃) 4 w 1 := UseHint q (h, Az − ct 1 2 d , 2γ 2 ) 5 return ||z|| ∞ &lt; γ 1 − β and c̃ = H(μ || w 1 ) and |h| h j =1 ≤ ω

### 2.2 Fault Models

Over the past two decades, fault injection attacks have emerged as a power- ful method of compromising devices, even secured ones [39]. These attacks use a variety of techniques, including laser beam and electromagnetic (EM) pulse, which allow precise control over space and time. Extensive research has focused on characterizing the eﬀects of fault injection in order to identify fault mod- els at a given abstraction (circuit level, hardware logical level, assembly code, source code). Such models serve as a framework for categorizing and studying the potential fault attacks on systems and sub-systems such as cryptographic ones. A fault model at hardware logical level includes the width of the fault (mono- bit, multi-bits, byte, or word) and the induced change (bit set, bit reset, bit-ﬂip, random changes). The feasibility and cost of a fault model are related to the required equipment, the time, and the level of expertise needed. At software level, faults impact the data and computations, the control ﬂow and executed instructions, or both. At this level, common fault models cover eﬀects such as instruction skipping or conditional branch inversion. A threat (or attacker) model deﬁnes both the fault models and the number of faults needed to study the security of a system. Note that achieving a precise fault multiple times generally requires a strong attacker and means increased diﬃculty in real-life scenarios. In this paper, we consider four fault models at C level, two on instruction ﬂow and two on data, namely skipping faults, test inversion faults, randomization faults, and zeroizing faults. For each we explain how they can be achieved.

<!-- PDF_PAGE: 6 -->

## PDF page 6

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

67

Skipping fault involves deliberately skipping selected lines of code within the execution of a program. It amounts to not executing speciﬁc program instruc- tions or intentionally manipulating the program counter. Skipping faults can be achieved with many fault injection techniques such as CPU clock or voltage glitching [19,36,40], EM pulse injection [24] or laser beam [14]. Skipping faults can have severe consequences, such as bypassing critical security checks or essen- tial cryptographic steps. The practical demonstration of higher-order skipping faults has recently underscored the signiﬁcance of this type of fault attack [9], highlighting the potential security risks they pose.

Test inversion fault corresponds to the inversion of a conditional branch out- come (if-then or if-then-else constructs). It can be achieved by inverting the condition in the corresponding conditional jump instruction or by corrupting an instruction involved in the condition’s computation, all of which can be achieved by several injection means [11,20,26]. It can also be the result of skipping the branch instruction. Test inversion enables bypassing security veriﬁcation.

Zeroizing fault assumes that the attacker can set a variable, a constant or a portion thereof, to zero. While the realism of this attack scenario has been ques- tioned, instances of zeroizing faults have been successfully executed in practice as it amounts to resetting or ﬂipping some bits [6]. State-of-the-art fault injection allows controlling the fault aﬀecting up to a dozen bits [10]. Therefore, zeroing less than a dozen bits can be considered as realistic. Zeroizing faults can also be a consequence of skipping faults, or instruction or operand corruption [26,37].

Randomization fault introduces random changes to data or computations within a targeted program, causing unexpected behavior. This means that after the injection, the attacker remains unaware of the exact result of the computation, but gains an advantage by knowing that it has been altered within a speciﬁc range. Randomization faults can lead to incorrect output, bypassing security checks, or compromising the integrity of the cryptographic operation.

In the remainder, we only consider the type and number of faults for each scenarios from which one can deduce the corresponding attacker model.

### 2.3 Related Works

In this section, we ﬁrst give an overview of the state of the art in fault attacks on Dilithium. Then, we explain how one can forge signatures with partial infor- mation about the secret key.

Fault Attacks on Dilithium. For its PQC competition, NIST put an empha- sis on security against side-channel and fault attacks. In this regard, Dilithium already has some constant-time properties to an extent. Still, several practical fault injection attacks leading to the key recovery have already been published. Among them, Bruinderink and Pessl [8] demonstrated the applicability of diﬀer- ential fault attacks on the deterministic Dilithium through multiple paths.

<!-- PDF_PAGE: 7 -->

## PDF page 7

68 A. Calle Viera et al.

In contrast to the extensive research on fault injection attacks on the sig- nature algorithm, the veriﬁcation process has received less attention. The main reason is that only public information are handled during the veriﬁcation process. Fault attacks on the veriﬁcation procedure primarily target the comparison in line 5 of Algorithm 3, which is usually carefully implemented on secure devices to prevent acceptance of corrupted signatures. The algebraic parts of the veriﬁ- cation process are often considered less sensitive, given the diﬃculty of forging a signature. Nonetheless, exploitable vulnerabilities can make these algebraic parts an attractive attack surface for fault injection. It is the case for the RSA signature scheme where manipulating the modulus N , which is sensitive to faults, allows an attacker to pass the veriﬁcation with false signatures [33]. Although there have been eﬀorts to explore fault injection attacks in the context of the veriﬁcation procedure, such research remains scarce. One notable study conducted by Bindel et al. [5] highlighted the potential consequences of zeroizing the challenge c within the veriﬁcation process of other lattice-based signature schemes. They demonstrated that such zeroization could enable successful veriﬁcation of invalid signatures for any message, all without needing the secret key. Furthermore, they showed that skipping the correctness check or the size check on z in line 5 of Algorithm 3 could have the same eﬀect. Achieving zeroization in practice is not a trivial task, and concerns have been raised regarding the practicality of this speciﬁc theoretical attack scenario. How- ever, recently, Ravi et al. [31] presented the ﬁrst practical zeroization fault attack on an implementation of the Dilithium signature veriﬁcation. They showed that zeroizing the twiddle constants, a ﬁxed table of coeﬃcients, in the NTT reduces its entropy, thus achieving the same eﬀect as Bindel et al. who zeroized the challenge c. They practically demonstrated this by noticing that zeroizing the starting address of the the twiddle constant’s table is suﬃcient to set them all to zero. Given the critical role of the veriﬁcation algorithm in upholding the security of digital systems, it is essential to dedicate more attention to comprehensively evaluating its susceptibility to fault injection attacks.

Dilithium Signature Forgery. In the following, we present how to forge Dilithium signatures, assuming that only the s 1 part of the secret key is known. The veriﬁcation algorithm essentially recomputes the value of w 1 using only public information to accept a signature. To sign a message, the sk used is composed of (ρ, K, tr, s 1 , s 2 , t 0 ). The seed ρ needed to expand the matrix A is also part of the public key and tr is the hash of pk, so they can be both retrieved from public information. The nonce K is used to generate the vector y, but no check on the veriﬁcation allows to determine if this particular value was used. Thus, it can be replaced by a random value. The s 2 part of the secret key is only used for rejection checks and in intermediate values. Regarding t 0 , the security proof considers it as public [3], but in practice it remains secret. In the signing algorithm, if we assume that y is randomly chosen, as in the randomized version of Dilithium, then, with the knowledge of the public key and

<!-- PDF_PAGE: 8 -->

## PDF page 8

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

69

s 1 , an attacker can proceed up to the computation of z, in line 11 of Algorithm 2. From this step, there are basically two diﬀerent methods to forge a signature. Bruinderink and Pessl [8] presented a modiﬁed signing procedure to perform signature forgery with only public information and the knowledge of s 1 . They ﬁrst compute with known values the value u := A s 1 − t 1 2 d = t 0 − s 2 . Given s 2 ’s small coeﬃcients, the quantity u approximates t 0 . It allows them to compute an alternative h with u. They cannot check the rejections based on s 2 and t 0 , so they remove them because this will not impact the correctness of the signature with high probability. Ravi et al. [30] also showed an alternative signature forgery procedure. They start in the same way as Bruinderink and Pessl up to line 11 of Algorithm 2. They showed that the UseHint procedure can be inverted and used to compute the high bits of w − c s 2 . But, because LowBits q (A z − c s 2 , 2γ 2 ) ∞ &lt; γ 2 − β with probability very close to 1, they can be sure to recompute the correct w 1 .

Public Parameters Sensitivity Analysis of Verify

3

In this section, we present the main idea allowing the acceptance of random signatures by Algorithm 3 through the exploitation of speciﬁc faults. Then, we conduct a comprehensive analysis of one implementation of the veriﬁcation algo- rithm. The goal is to identify sensitive operations and explain how to forge signatures that would be accepted, in the presence of the corresponding fault. To our knowledge, this is the ﬁrst extensive study of the veriﬁcation algorithm. Finally, we summarize the sensitivity of each location regarding our fault models.

### 3.1 Main Idea

The attacker’s goal, here, is to produce a message-signature pair that will be accepted by Algorithm 3. The main idea behind the signature veriﬁcation of Dilithium is that computing the value A z − c t 1 2 d will be equal to the high bits of A y plus some bounded small values. These small values can sometimes slightly overﬂow onto the high part w 1 , so the signing algorithm computes a speciﬁc vector h of hints that will be used to compensate for this eﬀect. Given this hint, one can retrieve the same w 1 as in the signing procedure but with only public values. Let us remember that a Dilithium signature is composed of (c, z, h), given that z = y + c s 1 and t = A s 1 + s 2 , we have

A z − c t = A y − c s 2 .

(1)

By replacing w = A y and t = t 1 2 d + t 0 2 in Eq. 1, we get

A z − c t 1 2 d − c t 0 = w − c s 2 ,

2

The vector w is computed line 7 in Algorithm 2 and t is computed line 5 in Algo- rithm 1.

<!-- PDF_PAGE: 9 -->

## PDF page 9

70 A. Calle Viera et al.

and by rewriting this equation, we obtain

A z − c t 1 2 d = w − c s 2 + c t 0 .

(2)

Equation 2 is exactly the quantity computed for the veriﬁcation line 4 of Algorithm 3. Remember that h = MakeHint q (−c t 0 , w − c s 2 + c t 0 , 2 γ 2 ). Then, from Lemma 1.1 in [3], we know that

(3)

UseHint q (h, w − c s 2 + c t 0 , 2γ 2 ) = HighBits q (w − cs 2 , 2γ 2 ).

Since c s 2 ∞ ≤ β and LowBits q (w − cs 2 , 2γ 2 ) ∞ &lt; γ 2 − β 3 , according to Lemma 2 [3] we have

(4)

HighBits q (w − cs 2 , 2γ 2 ) = HighBits q (w, 2γ 2 ) = w 1 ,

which shows how to retrieve the value w 1 from the public key and the signature. From line 4 in Algorithm 3 and the equations above, we can see that, at the top level, w 1 is only dependant on A, z, c, t 1 and h which are known. The matrix A can be considered as a ﬁxed value, like the constant d. The values z and h are essentially random values on their respective intervals, and an attacker can choose them freely. Given this information, we show how to bound the value c t 1 2 d so that it doesn’t impact too much the high bits of A z.

Proposition 1. Let z ∈ S̃ γ l 1 −β be a random vector. If at least one of the follow- ing conditions is satisfied:

P1. c t 1 2 d = 0 P2. c t 1 2 d ∞ ≤ β and LowBits q (A z − c t 1 2 d , 2γ 2 ) ∞ &lt; γ 2 − β P3. c t 1 2 d ∞ ≤ γ 2 and h = MakeHint q (c t 1 2 d , A z − c t 1 2 d , 2 γ 2 )

Then, HighBits q (A z − c t 1 2 d , 2γ 2 ) = HighBits q (A z, 2γ 2 ).

Proof.

P1. If c t 1 2 d = 0, the result is straightforward. P2. Direct application of Lemma 2 in [3]. P3. If c t 1 2 d ∞ ≤ γ 2 then from Lemma 1.1 in [3], we know that UseHint q MakeHint q (c t 1 2 d , A z − c t 1 2 d , 2 γ 2 ), A z − c t 1 2 d , 2 γ 2

= HighBits q (A z − c t 1 2 d + c t 1 2 d , 2γ 2 ).

3

If σ is a valid signature then we know that this condition is fulﬁlled thanks to the check on r 0 on line 13 of Algorithm 2.

<!-- PDF_PAGE: 10 -->

## PDF page 10

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

71

If we can fault some operations of Algorithm 3 and have one of these three condi- tions, then we can carefully construct signatures that will pass the veriﬁcation.

– Even though at ﬁrst glance P1 seems like a strong hypothesis to realize, Ravi et al. [31] recently showed the practical realization of a fault attack involving the challenge c that has the same eﬀect. – P2 is perhaps the hardest hypothesis to use because we need both conditions for the fault to have the desired eﬀect. – P3 seems convenient because the hint vector h is part of the signature, and γ 2 is not too small.

To illustrate the sensitivity analysis, we use the C implementation of Dilithium from the PQclean library [17], which is identical to the reference one [13] but more portable. The code structure is also reused in other implementa- tions [16]. The function PQCLEAN DILITHIUM2 CLEAN crypto sign verify will be referred to as verify to simplify notations and is given in Fig. 1. In the fol- lowing, we describe three relevant scenarios resulting from the analysis of the C code. For each scenario, we identify which fault model, as presented in Sect. 2.2, allows us to exploit propositions P1 and P3 to forge a signature. We provide two algorithms Algorithm 4 for P1 and Algorithm 5 for P3, to forge signatures given the corresponding faults. Each algorithm has been implemented in SageMath. We have veriﬁed that such carefully forged signatures using these algorithms, paired with speciﬁc fault eﬀects, enable us to pass the veriﬁcation.

### 3.2 Preliminary Analysis

A natural target is the corruption of the value returned by the veriﬁcation pro- cess. An attacker must then force the return value to 0, corresponding to a valid signature. However, zeroizing 32 bits may be relatively hard for an attacker to accomplish in practice. Alternatively, the attacker can try to pass all of the three checks lines 14, 16, and 54 of verify in Fig. 1, necessitating three test inversion faults at minimum. These sensitive tests are typically hardened in secure appli- cations [38], making such fault eﬀects potentially hard to achieve. The analysis below focuses on arithmetic parts that might be less carefully implemented since they do not handle secure parameters.

<!-- PDF_PAGE: 11 -->

## PDF page 11

72 A. Calle Viera et al.

Fig. 1. PQClean Dilithium verify code snippet.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 11]

<!-- PDF_PAGE: 12 -->

## PDF page 12

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

73

Fig. 2. PQClean unpack pk code snippet

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 12]

Fig. 3. PQClean unpack t 1 code snippet

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 12]

For instance, the unpacking of t 1 is a potential location for fault injection. To avoid aﬀecting other public variables, such as A, the only feasible target is the constant 0x3FF lines 4 to 7 of the function polyt1 unpack Fig. 3. Zeroizing this constant sets every coeﬃcient of t 1 to zero and we can use P1 through Algorithm 4, detailed in Scenario 1. However, this approach requires a total of K × N repeated faults, which can be challenging in practice. Yet, it is worth noting that t 1 could be sensitive if declared as a global variable. Then, as by default it is initialized to 0, faulting the call to the function polyt1 unpack, line 9 in Fig. 2, could set t 1 to 0 with just K repeated faults. Alternatively, one test inversion fault, line 8 Fig. 2, can force zero iterations of the loop.

Fig. 4. PQClean NTT −1 code snippet

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 12]

<!-- PDF_PAGE: 13 -->

## PDF page 13

74 A. Calle Viera et al.

Our attention also turns to lines 34, 36, and 41 of Fig. 1 involving the NTT and NTT −1 conversions, given in Fig. 4 . Notably, Ravi et al. [31] already cover the conversion of c in line 34. At the end of the inverse conversion of A z−c t 1 2 d each coeﬃcient undergoes multiplication by the squared Montgomery factor divided by 256 in a for loop, line 18 Fig. 4. This 32-bit integer constant plays a critical role. It is used at each of the N iterations so it can potentially be stored in a register. Zeroizing this value once can set all polynomial A z − c t 1 2 d to 0. However, this fault must be repeated K times, once for each polynomial of the vector processed by the NTT −1 . We can exploit this fault to sample the challenge c with w 1 = 0 and forge valid signatures with Algorithm 4. We notice that even if we ﬁrst perform the NTT −1 of A z and c t 1 2 d separately, and then subtract the two, it would also be vulnerable. This is because we can apply the same fault to the NTT −1 of c t 1 2 d to zeroize the result, enabling the exploitation of P1.

### 3.3 Scenario 1: Sampling of c̃

Fig. 5. PQClean sampling of c code snippet

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 13]

For eﬃciency, the veriﬁcation algorithm only compares the recomputed seed c̃ with the one from the signature, line 54 Fig. 1. In our investigation, we identify the procedure, in Fig. 5, for sampling the challenge c from its seed c̃ as sensitive.

<!-- PDF_PAGE: 14 -->

## PDF page 14

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

75

This process involves setting all N coeﬃcients of the challenge to zero using a ﬁrst for loop, followed by another for loop setting τ coeﬃcients as 1 or −1. By exploiting skipping or test-inversion faults, an attacker can target the for loop, line 16 Fig. 5, abort it prematurely, and zeroize all coeﬃcients of c with just one correctly targeted fault. Similarly, the same eﬀect can be achieved by faulting the loop’s termination condition, such as zeroizing the constant TAU. Suppose the challenge c has been successfully manipulated to be zero. We present an algorithm enabling an attacker to exploit this eﬀect, resulting in the acceptance of false signatures without needing the secret key.

Algorithm 4. Sign based on P1

Input : pk = (ρ, t 1 ) Output: σ = (c̃, z, h) 1 A ∈ R q k×l := ExpandA(ρ) A is generated and stored in NTT representation Â 2 μ ∈ {0, 1} 512 := H(H(ρ || t 1 ) || M ) 3 z ∈ S̃ γ l 1 −β 4 w := A z 5 h := SampleInBall ω () 6 w 1 = UseHint q (h, w, 2 γ 2 ) 7 c̃ ∈ {0, 1} 256 := H(μ || w 1 ) 8 return σ = (c̃, z, h)

Algorithm 4 utilizes the fact that if c = 0, then c t 1 2 d = 0, therefore leverag- ing P1. We begin by sampling the vector z within the appropriate range. Similar to [31], our algorithm generates a random h satisfying its corresponding condi- tion. Using the UseHint function, we compute the corresponding w 1 to sample the resulting c̃. As observed earlier, we exploit faults that set c to 0 in the ver- iﬁcation algorithm, meaning that the same seed c̃ is sampled as in Algorithm 4. Unlike [31], we don’t perform a rejection on the ﬁrst coeﬃcient of c because the fault in the veriﬁcation does not use this condition. As a variation of Algorithm 4, we can directly set h to zero and use only the high bits of A z to derive the seed c̃. It is worth noting that while h being com- pletely null is a situation that could arise in practice, its probability is negligible. In current versions of Dilithium, this check is neither speciﬁed nor implemented. A thorough analysis is required to determine if adding the h = 0 check to the veriﬁcation algorithm would reject valid signatures. Furthermore, this scenario relies on the ability to set all coeﬃcients of c to zero. Whereas, the challenge c should have precisely τ coeﬃcients equal to 1 or −1. However, there are no checks in place to verify this in practice.

<!-- PDF_PAGE: 15 -->

## PDF page 15

76 A. Calle Viera et al.

### 3.4 Scenario 2: Shift by d

Fig. 6. PQClean polyvec shift code snippet

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 15]

Fig. 7. PQClean poly code snippet

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 15]

In this scenario, we focus on line 35 of verify given in Fig. 1. At this point, t 1 has been unpacked, and the challenge c has been sampled from the seed c̃. Faulting either the shift of t 1 by d or the multiplication of c with t 1 can inﬂuence the magnitude of the product c t 1 2 d . It is important to note that the result of the multiplication of c with t 1 2 d , stored in the same location as t 1 2 d , already contains coeﬃcients outside the exploitable range of Proposition 1. Thus, faulting this operation does not yield usable outcomes. Now, let us analyze the multiplication of t 1 by 2 d . By considering skipping faults, an attacker can target the call to the polyveck shiftl function on line 35 of verify by skipping the corresponding jump instruction with one fault. Another potential target is line 3 of Fig. 6, where faulting the loop counter terminates the function prematurely. Alternatively, the call to poly shiftl on line 4 can be targeted during each of the K iterations. However, this approach requires K repeated faults and can be more challenging to achieve. The loop line 3 of Fig. 7 can be a potential target for a single fault. Similarly, we can target line 4 but this approach also requires K repeated faults. Regarding zeroization faults, the constant d can be targeted to zeroize a bit or a byte of its value. It is worth noting that, in practice, for all versions of Dilithium, d = 13 = 0b1101, which is 3 bits to set to zero. Considering randomization faults on d, the diﬀerence is that this time there is no control over the value d so most of the random faults are not usable. Our aim is to determine the suitable d such that c t 1 2 d ∞ ≤ γ 2 which allows us to utilize P3. Let us compute such a d by bounding the product

c t 1 2 d ∞ ≤ 2 d c 1 t 1 ∞ ,

since c 1 = τ and t 1 ∞ ≤ 2 10 − 1 4

≤ 2 d τ (2 10 − 1).

(5)

γ 2 . τ (2 10 − 1)

We want 2 d τ (2 10 − 1) ≤ γ 2 . Therefore d ≤ log 2

4

We must have this condition fulﬁlled in Sign for a signature to be valid.

<!-- PDF_PAGE: 16 -->

## PDF page 16

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

77

Example: For Dilithium-2 we have d = 1, while for Dilithium-3 and 5 we have d = 2. In practice, however, the maximum erroneous d tolerated for any version is 3. This is explained by the fact that we have analyzed the worst possible case, and so in practice the bound can be tightened.

Algorithm 5. Sign based on P3

Input : pk = (ρ, t 1 ) Output: σ = (c̃, z, h) 1 A ∈ R q k×l := ExpandA(ρ) A is generated and stored in NTT representation Â 2 μ ∈ {0, 1} 512 := H(H(ρ || t 1 ) || M ), (h) :=⊥ 3 while (h) =⊥ do 4 z ∈ S̃ γ l 1 −β 5 w := A z 6 w 1 = HighBits q (w, 2 γ 2 )

7 c̃ ∈ {0, 1} 256 := H(μ || w 1 ) 8 c ∈ B τ := SampleInBall(c̃) 9 h := MakeHint q (−c t 1 2 d , w + c t 1 2 d , 2 γ 2 ) 10 if |h| h j =1 &gt; ω then 11 (h) :=⊥ 12 return σ = (c̃, z, h)

Assuming we have eﬀectively manipulated t 1 2 d so that c t 1 2 d ∞ ≤ γ 2 , we present an algorithm, Algorithm 5 enabling an attacker to exploit this with P3 and achieve the acceptance of false signatures without requiring the secret key. Algorithm 5 closely resembles the correct signing algorithm employed in Dilithium, although lacking some rejection checks that we can’t verify. It oper- ates with the vector z sampled within the appropriate range and leverages the hint vector computed using c t 1 2 d . Using P3, supposing we managed to produce the corresponding fault, we can assure that c t 1 2 d remains suﬃciently small to prevent excessive overﬂow into the higher bits. However, we still need to keep the rejection criterion based on the maximum value of non-zero coeﬃcients within h for successful veriﬁcation of such signatures. Our practical implementation of this algorithm, using SageMath library, has demonstrated low rejection rate for every security level of Dilithium, with no more than 3 on average.

### 3.5 Scenario 3: Subtraction

Fig. 8. PQClean polyveck sub code snippet

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 16]

<!-- PDF_PAGE: 17 -->

## PDF page 17

78 A. Calle Viera et al.

Fig. 9. PQClean poly sub code snippet

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 17]

To conclude our analysis, we direct our attention to line 39 of verify in Fig. 1. Notably, in current implementations, the result of the subtraction of A z by c t 1 2 d is stored in the same variable as A z. Introducing a fault in the subtraction, allows us to exploit this observation and leverage P1. First, one can skip the call to the function polyveck sub on line 39 of verify, Fig. 1, to fault the subtraction. Similarly, line 3 of Fig. 8 can be targeted to exit the for loop early. Since the result is stored in the same location as the ﬁrst operand, skipping the call to poly sub on line 4 of Fig. 8 at each of the K iterations yields the same outcome. However, this approach necessitates K repeated faults, which can be harder to do. Within the poly sub function given in Fig. 9, we can focus on skipping the loop on line 3. Alternatively, we can target line 4 of Fig. 9, although this requires K × N repeated faults. In this scenario, once we achieved to fault the subtraction, we leverage P1 and Algorithm 4 remains applicable. It allows an attacker to produce a valid message-signature pair for veriﬁcation. It is important to note that targeting this location has the same outcome as zeroizing the t 1 or zeroizing the challenge c in Scenario 1.

### 3.6 Experimental Validation

Our primary objective is to evaluate the functionality of Algorithm 4 and Algo- rithm 5 under the conditions speciﬁed by P1 and P3, respectively. To achieve this, we have chosen to model faults exclusively at the algorithmic level. This decision is based on the following reasons:

– Within the C code, there are multiple potential locations and various types of exploitable faults that can lead to the three scenarios discussed in Sects. 3.3, 3.4, and 3.5. – As outlined in Sect. 2.2, there are numerous ways to achieve the desired out- comes. – The speciﬁc faults required will depend heavily on the target platform and binary code, which depends on the source code, and both the compiler and compilation options used.

Therefore, to cover a broad range of possible faults, we have developed three modiﬁed versions of Dilithium in Python that correspond to each scenario, and ensure the desired algorithmic eﬀects.

<!-- PDF_PAGE: 18 -->

## PDF page 18

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

79

– Version 1 for Scenario 1, where we arbitrarily set c to 0. – Version 2 for Scenario 2, where we set d to match the value of d . – Version 3 for Scenario 3, where we removed the subtraction operation entirely.

We have validated that the signatures generated by Algorithm 4 are accepted when using the versions 1 and 3. Likewise, we have veriﬁed that the signatures generated by Algorithm 5 are accepted when using version 2.

4 Countermeasures

It is essential to implement the scheme thoughtfully, to minimize potential attacks, identifying and securing vulnerable operations within it. We outline sev- eral countermeasures to address the sensitive locations identiﬁed in this section. For example, line 39 of verify, storing the result of A z minus c t 1 2 d in the same memory location as c t 1 2 d prevents the exploitation of this subtraction in Scenario 3. Even if an attacker attempts to fault the subtraction, the subsequent computation of the high bits of c t 1 2 d at line 45 of verify renders them unusable for accepting false signatures. Thus protecting this location with no extra cost. Proposition P1 relies on the fact that all K × N coeﬃcients of c t 1 2 d are smaller than they should be. Therefore, if we can prevent even a single coeﬃcient from being changed in size, the presented scenarios will not work. A ﬁrst set of commonly used countermeasures aims to make it more diﬃcult for the attacker to induce faults or reproduce them [38]. There are also mecha- nisms that can detect and prevent fault injections targeting loops [28]. This can ensure data is handled correctly throughout the process. However, these coun- termeasures are fragile and complex to deploy, as we must ensure their presence in the ﬁnal code. Consequently, it is more advantageous to have a Dilithium veriﬁcation algo- rithm that is intrinsically resistant to propositions P1 and P3. Let us introduce speciﬁc countermeasures tailored for the identiﬁed sensitive operations.

Distribution Check of the value c t 1 2 d before the subtraction. By verifying if it is the expected one, we can eﬀectively detect the faults used in Scenario 1 and 2. However, in practice, this means computing some statistical test on the values which can be computationally expensive

Verify d. Alternatively, we can check the correctness of the value d before using it. One way to do this veriﬁcation is by ﬁrst noticing that (2 d ) −1 = 1 − 2 10 mod q, which can be computed easily and only with shift operations. Therefore, checking that 2 d × (2 d ) −1 = 1 mod q before using the value d could ensure that it is the correct one used. However, this method only detects the faults of Scenario 2.

<!-- PDF_PAGE: 19 -->

## PDF page 19

80 A. Calle Viera et al.

Split d. Another equivalent implementation would be to do the multiplication by 2 d in two times, with little overhead. If we set d 1 &gt; 3 and d 2 &gt; 3 such that d = d 1 + d 2 , we can ensure that even if we fault one of the intermediate d, the result will be too big to use P3 in Scenario 2.

Alternative implementation. We can remark that by computing z := z (2 d ) −1 , d d −1 at the d beginning of the veriﬁcation, we can write A z − c t 1 2 = A z (2 ) − c t 1 2 . This time, the signatures will always be invalid if an attacker can skip the multiplication by (2 d ) −1 or by 2 d thus completely preventing Scenario 2. We give in Algorithm 6 a possible implementation of this countermeasure.

Algorithm 6. Verify Alternative

Input : pk = (ρ, t 1 ), σ = (c̃, z, h) Output: T rue or F alse 1 A ∈ R q k×l := ExpandA(ρ) 2 μ ∈ {0, 1} 512 := H(H(ρ || t 1 ) || M ) 3 c := SampleInBall(c̃) 4 z := z (2 d ) −1 5 temp 1 := A z 6 temp 2 := −ct 1 7 temp 2 := temp 2 + temp 1 8 w 1 := UseHint q (h, temp 2 2 d , 2γ 2 ) 9 return ||z|| ∞ &lt; γ 1 − β and c̃ = H(μ || w 1 ) and |h| h j =1 ≤ ω

Norm Check. One last possible countermeasure would be to only accept a sig- nature as valid if the check c t 1 2 d ∞ &gt; γ 2 passes. The idea behind this check we introduce is that all three possibilities for Proposition 1 are based on the fact that c t 1 2 d is smaller than it should be. By verifying if it is not too small, one can completely prevent its use. One thing to note is that the probability for every of the K × N coeﬃcients to be naturally less than γ 2 is negligible. Thus, it should not change the veriﬁcation algorithm of Dilithium. If this check doesn’t aﬀect the veriﬁcation, it could prevent the faults used in Scenario 1 and 2. Here, we give a summary of the previous two sections in the form of a table with the diﬀerent scenarios, the type of fault that can be exploited for each, and the countermeasure associated.

<!-- PDF_PAGE: 20 -->

## PDF page 20

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

81

Table 1. Summary of the vulnerable locations of the veriﬁcation algorithm to the corre- sponding fault models. (✓: easy exploitation, ✓: possible exploitable, –: not applicable), together with the applicable countermeasures

Skipping Test-Inv Randomization Zeroizing Countermeasures

Versions

✓ ✓

Scenario 1 for

TAU

– –

✓ ✓

Scenario 2 polyvec for

✓ ✓

poly for

✓

d

–

✓ ✓

Scenario 3 polyvec for

✓ ✓

poly for

function call ✓ –

5 Conclusion

✓

–

Distribution Check,

✓

✓ Norm Check

✓

–

Distribution Check,

✓

–

Norm Check,

✓

✓ Verify d, Split d

✓

–

Alternative

✓

–

implementation

✓

–

This works aims at proving that, similarly to RSA, Dilithium veriﬁcation shall be implemented carefully even if it does not handle secret data. Hence, we presented a comprehensive analysis of the veriﬁcation algorithm of Dilithium, focusing on a common implementation in C and considering four common fault models: skip- ping faults, test inversion faults, randomization faults, and zeroizing faults. For each of them we establish a methodology for forging Dilithium signatures based on the speciﬁc type of fault employed during the veriﬁcation process. Further- more, our analysis provides valuable insights into the vulnerabilities and sensitive operations within the Dilithium veriﬁcation algorithm. Building upon these ﬁnd- ings, we propose a set of novel countermeasures covering the various scenarios introduced, and designed to mitigate the risks associated with these sensitive operations.

### References

1. Alagic, G., et al.: Status report on the third round of the NIST post-quantum cryptography standardization process (2022) 2. Azouaoui, M., et al.: Protecting dilithium against leakage: revisited sensitivity analysis and improved implementations. In: CHES (2023) 3. Bai, S., et al.: CRYSTALS – Dilithium. National Institute of Standards and Technology (2022). https://csrc.nist.gov/Projects/post-quantum-cryptography/ selected-algorithms-2022 4. Bernstein, D., Hülsing, A., Kölbl, S., Niederhagen, R., Rijneveld, J., Schwabe, P.: The SPHINCS+ signature framework. In: CCS (2019) 5. Bindel, N., Buchmann, J., Krämer, J.: Lattice-based signature schemes and their sensitivity to fault attacks. In: FDTC (2016) 6. Breier, J., Hou, X.: How practical are fault injection attacks, really? IEEE Access 10, 113122–113130 (2022) 7. Brier, E., Chevallier-Mames, B., Ciet, M., Clavier, C.: Why one should also secure RSA public key elements. In: CHES (2006)

<!-- PDF_PAGE: 21 -->

## PDF page 21

82 A. Calle Viera et al.

8. Bruinderink, L.G., Pessl, P.: Diﬀerential fault attacks on deterministic lattice sig- natures. CHES 2018(3), 21–43 (2018) 9. Claudepierre, L., Péneau, P., Hardy, D., Rohou, E.: TRAITOR: a low-cost evalu- ation platform for multifault injection. In: ASSS (2021) 10. Colombier, B., et al.: Multi-spot laser fault injection setup: new possibilities for fault injection attacks. In: CARDIS (2021) 11. Colombier, B., Menu, A., Dutertre, J., Moëllic, P., Rigaud, J., Danger, J.: Laser- induced single-bit faults in ﬂash memory: instructions corruption on a 32-bit micro- controller. In: IEEE HOST (2019) 12. Diﬃe, W., Hellman, M.: New directions in cryptography. IEEE Trans. Inf. Theory 22(6), 644–654 (1976) 13. Ducas, L., et al.: PQ-CRYSTALS, Dilithium (2022). gitHub repository. Accessed 15 Dec 2022 14. Dutertre, J., Riom, T., Potin, O., Rigaud, J.: Experimental analysis of the laser- induced instruction skip fault model. In: NordSec (2019) 15. Islam, S., Mus, K., Singh, R., Schaumont, P., Sunar, B.: Signature correction attack on dilithium signature scheme. In: EuroS&amp;P (2022) 16. Kannwischer, M., Petri, R., Rijneveld, J., Schwabe, P., Stoﬀelen, K.: PQM4: post- quantum crypto library for the ARM Cortex-M4. Accessed 15 Dec 2022 17. Kannwischer, M.J., Schwabe, P., Stebila, D., Wiggers, T.: PQClean (2022). https:// github.com/PQClean/PQClean. GitHub repository Accessed 15 Sep 2023 18. Kiltz, E., Lyubashevsky, V., Schaﬀner, C.: A concrete treatment of Fiat-Shamir signatures in the quantum random-oracle model. In: Nielsen, J., Rijmen, V. (eds.) Advances in Cryptology – EUROCRYPT 2018. EUROCRYPT 2018. LNCS, vol. 10822, pp. 552–586. Springer, Cham (2018). https://doi.org/10.1007/978-3-319- 78372-7 18 19. Korak, T., Hoeﬂer, M.: On the eﬀects of clock and power supply tampering on two microcontroller platforms. In: FDTC (2014) 20. Kumar, D., Beckers, A., Balasch, J., Gierlichs, B., Verbauwhede, I.: An in-depth and black-box characterization of the eﬀects of laser pulses on atmega328p. In: CARDIS (2019) 21. Liu, Y., Zhou, Y., Sun, S., Wang, T., Zhang, R., Ming, J.: On the security of lattice-based Fiat-Shamir signatures in the presence of randomness leakage. IEEE Trans. Inf. Forensics Secur. 16 (2021) 22. Lyubashevsky, V.: Fiat-Shamir with aborts: applications to lattice and factoring- based signatures. In: Matsui, M. (eds.) Advances in Cryptology – ASIACRYPT 2009. ASIACRYPT 2009. LNCS, vol. 5912, pp. 598–616. Springer, Berlin, Heidel- berg (2009). https://doi.org/10.1007/978-3-642-10366-7 35 23. Marzougui, S., Ulitzsch, V., Tibouchi, M., Seifert, J.: Proﬁling side-channel attacks on dilithium: a small bit-ﬁddling leak breaks it all. ePrint (2022) 24. Menu, A., Dutertre, J., Potin, O., Rigaud, J., Danger, J.: Experimental analysis of the electromagnetic instruction skip fault model. In: DTIS (2020) 25. Migliore, V., Gérard, B., Tibouchi, M., Fouque, P.A.: Masking dilithium. In: ACNS (2019) 26. Moro, N., Dehbaoui, A., Heydemann, K., Robisson, B., Encrenaz, E.: Electromag- netic fault injection: towards a fault model on a 32-bit microcontroller. In: FDTC (2013) 27. Muir, A.: Seifert’s RSA fault attack: simpliﬁed analysis and generalizations. In: Ning, P., Qing, S., Li, N. (eds.) ICICS 2006. LNCS, vol. 4307, pp. 420–434. Springer, Heidelberg (2006). https://doi.org/10.1007/11935308 30

<!-- PDF_PAGE: 22 -->

## PDF page 22

Fault Attacks Sensitivity of Public Parameters in the Dilithium Veriﬁcation

83

28. Proy, J., Heydemann, K., Berzati, A., Cohen, A.: Compiler-assisted loop hardening against fault attacks. ACM 2017 (2017) 29. Qiao, Z., Liu, Y., Zhou, Y., Ming, J., Jin, C., Li, H.: Practical public template attacks on CRYSTALS-dilithium with randomness leakages. IEEE Trans. Inf. Forensics Secur. 18, 1–14 (2023). https://doi.org/10.1109/TIFS.2022.3215913 30. Ravi, P., Jhanwar, M.P., Howe, J., Chattopadhyay, A., Bhasin, S.: Side-channel assisted existential forgery attack on dilithium - a NIST PQC candidate. ePrint 31. Ravi, P., Yang, B., Bhasin, S., Zhang, F., Chattopadhyay, A.: Fiddling the twiddle constants - fault injection analysis of the number theoretic transform. CHES (2023) 32. Rivest, R., Shamir, A., Adleman, L.: A method for obtaining digital signatures and public-key cryptosystems. ACM Commun. (1978) 33. Seifert, J.P.: On authenticated computing and RSA-based authentication. In: CCS (2005) 34. Shor, P.: Algorithms for quantum computation: discrete logarithms and factoring. In: FOCS (1994) 35. Soni, D., Basu, K., Nabeel, M., Aaraj, N., Manzano, M., Karri, R.: FALCON, pp. 31–41. Springer, Cham (2021). https://doi.org/10.1007/978-3-030-57682-0 3 36. Timmers, N., Spruyt, A., Witteman, M.: Controlling pc on arm using fault injec- tion. In: FDTC (2016) 37. Trouchkine, T., Bouﬀard, G., Clédière, J.: EM fault model characterization on SoCs: from diﬀerent architectures to the same fault model. In: FDTC (2021) 38. Witteman, M.: Secure application programming in the presence of side channel attacks. https://www.riscure.com/publication/secure-application-programming- presence-side-channel-attacks/ 39. Yuce, B., Schaumont, P., Witteman, M.: Fault attacks on secure embedded soft- ware: threats, design and evaluation. CoRR (2020) 40. Zussa, L., Dutertre, J.M., Clédière, J., Robisson, B., Tria, A.: Investigation of timing constraints violation as a fault injection means. In: DCIS (2012)
