# [14] Differential Fault Analysis of the Advanced Encryption Standard Using a Single Fault

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 10
converted_at: "2026-07-26"
source_asset_id: "HAETAE-FIA-REF-14"
derived_asset_id: "HAETAE-FIA-REF-14-MD"
source_path: "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[14] Differential Fault Analysis of the Advanced Encryption Standard Using a Single Fault.pdf"
source_sha256: "ce1305b45492c119652a2412967e6d4df7be89f3de8491a2c580a491e72b2465"
pages: 10
bbox_words: 5367
consumed_bbox_words: 5367
numeric_tokens: 904
consumed_numeric_tokens: 904
source_blocks: 242
consumed_source_blocks: 242
emitted_blocks: 180
embedded_raster_images: 17
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 10
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

Diﬀerential Fault Analysis of the Advanced Encryption Standard Using a Single Fault

Michael Tunstall 1 , Debdeep Mukhopadhyay 2 , and Subidh Ali 2

1

Department of Computer Science, University of Bristol, Merchant Venturers Building, Woodland Road, Bristol BS8 1UB, United Kingdom tunstall@cs.bris.ac.uk 2 Computer Sc. and Engg, IIT Kharagpur, India {debdeep,subidh}@cse.iitkgp.ernet.in

Abstract. In this paper we present a diﬀerential fault attack that can be applied to the AES using a single fault. We demonstrate that when a single random byte fault is induced at the input of the eighth round, the AES key can be deduced using a two stage algorithm. The ﬁrst step has a statistical expectation of reducing the possible key hypotheses to 2 32 , and the second step to a mere 2 8 .

Keywords: Diﬀerential Fault Analysis, Fault Attack, Advanced Encryption Standard.

1 Introduction

The Advanced Encryption Standard (AES) [10] has been a de-facto standard for symmetric key cryptography since October 2000. Smart cards and secure microprocessors, therefore, typically include implementations of AES to protect the conﬁdentiality and the integrity of sensitive information. To satisfy the high throughput requirements of such applications, these implementations are typi- cally VLSI devices (crypto-accelerators) or highly optimized software routines (crypto-libraries). Several applications of DFA to AES have been reported in the literature. In [3], authors describe an analysis based on faults induced in one byte of the ninth round of AES that requires 250 faulty ciphertexts. An attack reported in [1] allows an attacker to recover the secret key with around 128 to 256 faulty ciphertexts. In [2], Dusart et al. show that using a fault which aﬀects one byte anywhere between the eighth round MixColumn and ninth round MixColumn, an attacker would be able to derive the secret key using 40 faulty ciphertexts. The authors of [12] describe an attack on AES with single byte faults that requires two faulty outputs, where a fault is induced in the input of the eighth or ninth round, extended to one 32-bit fault in the ninth round in [8]. We can note that when the assumptions are on the value of a byte (either it being faulty or uncorrupted) the number of faulty pairs is quite small. However, it is diﬃcult to be able to aﬀect a given value with any certainty. When numerous

C.A. Ardagna and J. Zhou (Eds.): WISTP 2011, LNCS 6633, pp. 224–233, 2011. c IFIP International Federation for Information Processing 2011

<!-- PDF_PAGE: 2 -->

## PDF page 2

Diﬀerential Fault Analysis of the Advanced Encryption Standard 225

faulty ciphertexts are required this problem is ampliﬁed, since an attacker needs to ﬁnd a method of determining which faulty ciphertexts correspond to the desired model. We can, therefore, state that the attacks that are most likely to be realizable require the least faulty ciphertexts and assumptions on the eﬀect of the fault. In [9] a fault attack against AES was proposed, which suggested that a secret key can be derived using a single byte fault induction at the input of the eighth round. The attack exploited the inter-relations between the fault values in the state matrix after the ninth round MixColumn operation and reduced the number of possible keys to around 2 32 . However it may be noted that this work, like the previous fault attacks on AES does not use the eﬀect of the fault maximally in an information theoretic sense [7]. The work proposed in this paper improves the previous fault analysis on AES-128 and reduces the key space to its minimal possible set of hypotheses attainable using a single byte fault. In this paper, we describe the extended version of this attack, where an attacker could reduce the exhaustive search to 2 8 .

Notation

In this paper, multiplications are considered to be polynomial multiplications over F 2 8 modulo the irreducible polynomial x 8 + x 4 + x 3 + x + 1. It should be clear from the context when a mathematical expression contains integer multi- plication.

Organization

The paper is organized as follows: In Section 2 we describe the background to this paper. In Section 3 we describe an attack based on one of the fault models given in Section 2. In Section 3 we extend this attack. In Section 4 we compare this paper to work described in the literature, and we conclude in Section 5.

2 Background

The Advanced Encryption Standard

2.1

The structure of the Advanced Encryption Standard (AES) , as used to per- form encryption, is illustrated in Algorithm 1. Note that we restrict ourselves to considering AES-128 and that the description above omits a permutation typically used to convert the plaintext P = (p 1 , p 2 , . . . , p 16 ) (256) and key K = (k 1 , k 2 , . . . , k 16 ) (256) into a 4 × 4 array of bytes, known as the state matrix. For example, the 128-bit plaintext input block P which produces fault free (CT ) and faulty ciphertexts (CT ) are arranged in the following fashion

⎛

⎛

⎞ x 1 x 5 x 9 x 13 ⎜ x 2 x 6 x 10 x 14 ⎟ ⎟ CT = ⎜ ⎝ x 3 x 7 x 11 x 15 ⎠ x 4 x 8 x 12 x 16

⎞ p 1 p 5 p 9 p 13 ⎜ p 2 p 6 p 10 p 14 ⎟ ⎟ P = ⎜ ⎝ p 3 p 7 p 11 p 15 ⎠ p 4 p 8 p 12 p 16

⎛ ⎞ x 1 x 5 x 9 x 13 ⎜ x 2 x 6 x 10 x 14 ⎟ ⎟ CT = ⎜ ⎝ x 3 x 7 x 11 x 15 ⎠ x 4 x 8 x 12 x 16

<!-- PDF_PAGE: 3 -->

## PDF page 3

226 M. Tunstall, D. Mukhopadhyay, and S. Ali

Algorithm 1. The AES-128 encryption function.

Input: The 128-bit plaintext block P and key K. Output: The 128-bit ciphertext block C.

X ← AddRoundKey(P, K) for i ← 1 to 10 do X ← SubBytes(X) X ← ShiftRows(X) if i = 10 then X ← MixColumns(X) end K ← KeySchedule(K) X ← AddRoundKey(X, K) end C ← X

return C

where x i ∈ {0, . . . , 255} ∀i ∈ {1, . . . , 16}. We also deﬁne the key matrix for the subkeys used in the ninth and tenth round as K 10 = {k 1 , . . . , k 16 } and } that are arranged in a state matrix as described above. K 9 = {k 1 , . . . , k 16 The encryption itself is conducted by the repeated use of a number of round functions:

– The SubBytes function is the only non-linear step of the block cipher. It is a bricklayer permutation consisting of an S-box applied to the bytes of the state. Each byte of the state matrix is replaced by its multiplicative inverse, followed by an aﬃne mapping. Thus the input byte x is related to the output y of the S-Box by the relation, y = A x −1 + B, where A and B are constant matrices. In the remainder of this paper we will refer to the function S as the SubBytes function and S −1 as the inverse of the SubBytes function. – The ShiftRows function is a byte-wise permutation of the state. – The KeySchedule function generates the next round key from the previous one. The ﬁrst round key is the input key with no changes, subsequent round keys are generated using the SubBytes function and XOR operations. This is shown in Algorithm 2 which shows how the r th round key is computed from the (r − 1) th round key. The value h r is a constant deﬁned for the r th round, and &lt;&lt; is used to denote a bitwise left shift. – The MixColumn is a bricklayer permutation operating on the state column by column. Each column of the state matrix is considered as a 4-dimensional vector where each element belongs to F(2 8 ). A 4×4 matrix M whose elements are also in F(2 8 ) is used to map this column into a new vector. This operation is applied on all the 4 columns of the state matrix. Here M and its inverse M −1 are deﬁned as:

⎞ 2311 ⎜ 1 2 3 1 ⎟ ⎟ M = ⎜ ⎝ 1 1 2 3 ⎠ 3112

⎛

⎞ 14 11 13 9 ⎜ 9 14 11 13 ⎟ ⎟ M −1 = ⎜ ⎝ 13 9 14 11 ⎠ 11 13 9 14

⎛

<!-- PDF_PAGE: 4 -->

## PDF page 4

Diﬀerential Fault Analysis of the Advanced Encryption Standard 227

All the elements in M and M −1 are elements of F(2 8 ) expressed as a decimal digit. – AddRoundKey: Each byte of the array is XORed with a byte from a corre- sponding array of round subkeys.

Algorithm 2. The AES-128 KeySchedule function.

Input: (r − 1) th round key (X = x i for i ∈ {1, . . . , 16}). Output: r th round key X.

for i ← 0 to 3 do x (i&lt;&lt;2)+1 ← x (i&lt;&lt;2)+1 ⊕ S(x (((i+1)∧3)&lt;&lt;2)+4 ) ; end x 1 ← x 1 ⊕ h r ; for i ← 1 to 16 do if (i − 1) mod 4 = 0 then x i ← x i ⊕ x i−1 ; end end

return X

### 2.2 The Fault Model

The implementation of AES we target is an iterative one, i.e. where a round function is executed in a loop as described in Algorithm 1. An attacker can typically predict at what point in time certain events take place, e.g. when a particular round commences. Moreover, the time certain events take can often be determined by analyzing a suitable side channel. The fault model that we consider is the same as that used in many other papers, for example [9], where we assume that the eﬀect of an induced fault is to change one byte to a random value. For example, an attacker could attempt to use a glitch in the clock to create a fault at the input of a particular round with a certain probability. An iterative design helps in this regard, as the attacker is able to control the timing of fault induction by simply counting the number of clock edges from the start of an encryption.

3 The Fault Analysis

### 3.1 The First Step of the Fault Attack

If a fault is induced in a byte of the state matrix, which is then input to the eighth round, the MixColumn operation at the end of the round propagates this fault to the entire column of the state. The ShiftRow operation at the beginning of the following round will then shift these bytes to occupy diﬀerent columns. The next MixColumn operation will then propagate the fault to the remaining twelve bytes.

<!-- PDF_PAGE: 5 -->

## PDF page 5

228 M. Tunstall, D. Mukhopadhyay, and S. Ali

This process is shown in Figure 1 where we show the diﬀusion of a byte fault induced at the input of the eighth round. The XOR diﬀerence of the state matrices of the two results, one fault free and the other faulty, is shown. This is what we use as basis for a diﬀerential fault analysis.

f’

f

f’

Eighth Round Byte Sub

Eighth Round Shift Row

A A A

A 1

A A

A 1

A

2 3 4

2 3 4

A A A A

A A A A

6 7 8 5

5 6 7 8

A

A A A

A A A A

11 12 9 10

10

9 11 12

A A A A

A A A A

13 14 15

14

16

13 15 16

Tenth Round Shift Row Tenth Round Byte Sub

2f’

f’

f’

3f’

Eighth Round Mix Column F 1

Ninth Round Byte Sub

F2

F3

F4

Ninth Round Shift Row

2F 1 F4 F 3 3 F 2 F 1

F1 F 4 3 F 3 2 F2

F2

F 1 3 F 4 2 F3

F2

F3

3 F 1 2 F 4 F3 F2 F4

Ninth Round Mix Column

Fig. 1. Propagation of Fault Induced in the input of eighth round of AES

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

If, given a fault in the input to the eighth round, we consider the state of the diﬀerences after the ninth round shift row, we can obtain the following set of equations that include the values of the key bytes k 1 , k 8 , k 11 and k 14 , thus giving an expression for 32 bits of K 10 .

2 δ 1 = S −1 (x 1 ⊕ k 1 ) ⊕ S −1 (x 1 ⊕ k 1 )

δ 1 = S −1 (x 14 ⊕ k 14 ) ⊕ S −1 (x 14 ⊕ k 14 )

,

δ 1 = S −1 (x 11 ⊕ k 11 ) ⊕ S −1 (x 11 ⊕ k 11 )

3 δ 1 = S −1 (x 8 ⊕ k 8 ) ⊕ S −1 (x 8 ⊕ k 8 )

Where δ 1 , k 1 , k 8 , k 11 and k 14 are all unknown values ∈ {0, . . . , 255}. The above system of equations can be used to reduce the possibilities for these 32 bits of the key. An attacker would select a value for δ 1 and determine which values of k 1 , k 8 , k 11 and k 14 satisfy the equations using four independent exhaustive searches. Each equation will return 0, 2, or 4 hypotheses [11]. If any of the four equations cannot be satisﬁed, i.e. there is an impossible diﬀerential [6], then any hypotheses for that value of δ 1 can be discarded. As noted in [4, 8] one can apply the same technique to recover information on the remaining bytes of the last sub key. That is, information on the remaining key bytes can be derived by using the following sets of equations: In order to obtain information on k 2 , k 5 , k 12 and k 15 an attacker can use

<!-- PDF_PAGE: 6 -->

## PDF page 6

Diﬀerential Fault Analysis of the Advanced Encryption Standard 229

3 δ 2 = S −1 (x 5 ⊕ k 5 ) ⊕ S −1 (x 5 ⊕ k 5 )

2 δ 2 = S −1 (x 2 ⊕ k 2 ) ⊕ S −1 (x 2 ⊕ k 2 )

.

δ 2 = S −1 (x 15 ⊕ k 15 ) ⊕ S −1 (x 15 ⊕ k 15 )

δ 2 = S −1 (x 12 ⊕ k 12 ) ⊕ S −1 (x 12 ⊕ k 12 )

In order to obtain information on k 3 , k 6 , k 9 and k 16 an attacker can use the following equations:

δ 3 = S −1 (x 9 ⊕ k 9 ) ⊕ S −1 (x 9 ⊕ k 9 )

3 δ 3 = S −1 (x 6 ⊕ k 6 ) ⊕ S −1 (x 6 ⊕ k 6 )

2 δ 3 = S −1 (x 3 ⊕ k 3 ) ⊕ S −1 (x 3 ⊕ k 3 )

δ 3 = S −1 (x 16 ⊕ k 16 ) ⊕ S −1 (x 16 ⊕ k 16 )

Finally, in order to obtain information on k 4 , k 7 , k 10 and k 13 an attacker can use the following equations:

δ 4 = S −1 (x 13 ⊕ k 13 ) ⊕ S −1 (x 13 ⊕ k 13 )

δ 4 = S −1 (x 10 ⊕ k 10 ) ⊕ S −1 (x 10 ⊕ k 10 )

3 δ 4 = S −1 (x 7 ⊕ k 7 ) ⊕ S −1 (x 7 ⊕ k 7 )

2 δ 4 = S −1 (x 4 ⊕ k 4 ) ⊕ S −1 (x 4 ⊕ k 4 )

It can be noted that the equations have an identical structure, and, therefore, the solutions are of similar nature. An evaluation of each set of equations will be expected to return 2 8 unique hypotheses for the key bytes concerned. Therefore, an attacker would expect to have 2 32 key hypotheses for the secret key used.

Analysis of the First Step of the Fault Attack

3.2

The ﬁrst step of the fault attack uses four sets of equations to reduce the key space of AES. In this section we determine the expected number of key hypothe- ses that an attacker will have at each stage of an attack. In order to analyze the number of valid hypotheses in the ﬁrst stage of the attack we consider the ﬁrst set of equations given in Section 3.1. In this set of equations δ 1 is ∈ {1, . . . , 255}. If δ 1 is equal to zero then one could say that the expected fault has not been injected. If δ 1 is zero it would imply that x 1 is equal to x 1 and all 256 key hypotheses are possible. Let us ﬁrst consider the ﬁrst equation in this set:

2 δ 1 = S −1 (x 1 ⊕ k 1 ) ⊕ S −1 (x 1 ⊕ k 1 )

We know the values of x 1 and x 1 from the correct and faulty ciphertexts respectively. For a given value of 2 δ 1 there will 0, 2 or 4 valid key hypotheses. The mean hypotheses for all δ 1 ∈ {1, . . . , 255} is approximately one, and, therefore, 256 key hypotheses when all δ 1 ∈ {1, . . . , 255} are considered.

<!-- PDF_PAGE: 7 -->

## PDF page 7

230 M. Tunstall, D. Mukhopadhyay, and S. Ali

The same can be said for each of the four equations in the set given above. However, for a given value of δ 1 each of the four equations would be expected to return approximately one hypothesis for a key byte. These values will give one hypothesis for the quartet of key bytes {k 1 , k 8 , k 11 , k 14 }. Given that an attacker will have to take into account all the values in {0, . . . , 255} there will be 256 possible values for the quartet {k 1 , k 8 , k 11 , k 14 }. After an attacker has analyzed the four equations deﬁned in Section 3.1 there would be an expected 2 32 key hypotheses.

The Second Step of the Fault Attack

3.3

In order to further reduce the key hypotheses we use the relationship between the ninth round key and the tenth round key. We consider the key-scheduling algorithm (see Algorithm 2), the ninth round key, K 9 , generates the tenth round key, K 10 . The key schedule is invertible and K 9 can be expressed in terms of elements of K 10 . The value of K 9 can be expressed as

⎛

⎞ k 1 ⊕ S(k 14 ⊕ k 10 ) ⊕ h 10 k 5 ⊕ k 1 k 9 ⊕ k 5 k 13 ⊕ k 9 ⎜ k 2 ⊕ S(k 15 ⊕ k 11 ) k 6 ⊕ k 2 k 10 ⊕ k 6 k 14 ⊕ k 10 ⎟ ⎜ ⎟ . ⎝ k 3 ⊕ S(k 16 ⊕ k 12 ) k 7 ⊕ k 3 k 11 ⊕ k 7 k 15 ⊕ k 11 ⎠ k 4 ⊕ S(k 13 ⊕ k 9 ) k 8 ⊕ k 4 k 12 ⊕ k 8 k 16 ⊕ k 12

We can observe that the fault values in the ﬁrst column of the state matrix at the output of the eighth round MixColumn is (2 f , f , f , 3 f ), where f is a non-zero arbitrary value in F 2 8 . Using the InverseMixColumn operation and using the inter-relations between the fault values, we can deﬁne the following equation:

2 f = S −1 ( 14 ( S −1 (x 1 ⊕ k 1 ) ⊕ ((k 1 ⊕ S(k 14 ⊕ k 10 ) ⊕ h 10 )) ) ⊕ 11 ( S −1 (x 8 ⊕ k 8 )⊕

(k 2 ⊕ S(k 15 ⊕ k 11 )) ) ⊕ 13 ( S −1 (x 11 ⊕ k 11 ) ⊕ (k 3 ⊕ S(k 16 ⊕ k 12 )) ) ⊕

9 ( S −1 (x 8 ⊕ k 8 ) ⊕ (k 4 ⊕ S(k 13 ⊕ k 9 )) ) ) ⊕ S −1 ( 14 ( S −1 (x 1 ⊕ k 1 )

⊕ ((k 1 ⊕ S(k 8 ⊕ k 10 ) ⊕ h 10 )) ) ⊕ 11 ( S −1 (x 8 ⊕ k 8 ) ⊕ (k 2 ⊕ S(k 15 ⊕ k 11 ) ) ⊕

13 ( S −1 (x 11 ⊕ k 11 ) ⊕ (k 3 ⊕ S(k 16 ⊕ k 12 )) ) ⊕ 9 ( S −1 (x 8 ⊕ k 8 )⊕

(k 4 ⊕ S(k 13 ⊕ k 9 )) ) )

Similarly, we can deﬁne the following equations:

f = S −1 ( 9 ( S −1 (x 13 ⊕ k 13 ) ⊕ (k 13 ⊕ k 9 ) ) ⊕ 14 ( S −1 (x 10 ⊕ k 10 ) ⊕ (k 10 ⊕ k 14 )) ) ⊕

11 ( S −1 (x 7 ⊕ k 7 ) ⊕ (k 15 ⊕ k 11 ) ) ⊕ 13 ( S −1 (x 4 ⊕ k 4 ) ⊕ (k 16 ⊕ k 12 ) ) ) ⊕

S −1 ( 9 ( S −1 (x 13 ⊕ k 13 ) ⊕ (k 13 ⊕ k 9 ) ) ⊕ 14 ( S −1 (x 10 ⊕ k 10 ) ⊕ (k 10 ⊕ k 14 )) ) ⊕

11 ( S −1 (x 7 ⊕ k 7 ) ⊕ (k 15 ⊕ k 11 ) ) ⊕ 13 ( S −1 (x 4 ⊕ k 4 ) ⊕ (k 16 ⊕ k 12 ) ) )

<!-- PDF_PAGE: 8 -->

## PDF page 8

Diﬀerential Fault Analysis of the Advanced Encryption Standard 231

f = S −1 ( 13 ( S −1 (x 9 ⊕ k 9 ) ⊕ (k 9 ⊕ k 5 ) ) ⊕ 9 ( S −1 (x 6 ⊕ k 6 ) ⊕ (k 10 ⊕ k 6 )) ) ⊕

14 ( S −1 (x 3 ⊕ k 3 ) ⊕ (k 11 ⊕ k 7 ) ) ⊕ 11 ( S −1 (x 16 ⊕ k 16 ) ⊕ (k 12 ⊕ k 8 ) ) ) ⊕

S −1 ( 13 ( S −1 (x 9 ⊕ k 9 ) ⊕ (k 9 ⊕ k 5 ) ) ⊕ 9 ( S −1 (x 6 ⊕ k 6 ) ⊕ (k 10 ⊕ k 6 )) ) ⊕

14 ( S −1 (x 3 ⊕ k 3 ) ⊕ (k 11 ⊕ k 7 ) ) ⊕ 11 ( S −1 (x 16 ⊕ k 16 ) ⊕ (k 12 ⊕ k 8 ) ) )

3 f = S −1 ( 11 ( S −1 (x 2 ⊕ k 2 ) ⊕ (k 2 ⊕ k 1 ) ) ⊕ 13 ( S −1 (x 5 ⊕ k 5 ) ⊕ (k 6 ⊕ k 5 )) ) ⊕

9 ( S −1 (x 12 ⊕ k 12 ) ⊕ (k 10 ⊕ k 9 ) ) ⊕ 14 ( S −1 (x 15 ⊕ k 15 ) ⊕ (k 14 ⊕ k 13 ) ) ) ⊕

S −1 ( 11 ( S −1 (x 2 ⊕ k 2 ) ⊕ (k 2 ⊕ k 1 ) ) ⊕ 13 ( S −1 (x 5 ⊕ k 5 ) ⊕ (k 6 ⊕ k 5 )) ) ⊕

9 ( S −1 (x 12 ⊕ k 12 ) ⊕ (k 10 ⊕ k 9 ) ) ⊕ 14 ( S −1 (x 15 ⊕ k 15 ) ⊕ (k 14 ⊕ k 13 ) ) )

The second stage of the attack is coupled with the ﬁrst stage, and can be used to further reduce the number of key hypotheses.

Analysis of the Second Step of the Fault Attack

3.4

The expected number of hypotheses produced by the second step of the attack follows a similar reasoning to the analysis of the ﬁrst step, given in Section 3.2. If we consider the second equation deﬁned in Section 3.3, it can be rewritten as f = A ⊕ B ,

where A and B are deﬁned as

A = S −1 ( 9 ( S −1 (x 13 ⊕ k 13 ) ⊕ (k 13 ⊕ k 9 ) ) ⊕

14 ( S −1 (x 10 ⊕ k 10 ) ⊕ (k 10 ⊕ k 14 )) ) ⊕ 11 ( S −1 (x 7 ⊕ k 7 ) ⊕

(k 15 ⊕ k 11 ) ) ⊕ 13 ( S −1 (x 4 ⊕ k 4 ) ⊕ (k 16 ⊕ k 12 ) ) )

and

B = S −1 ( 9 ( S −1 (x 13 ⊕ k 13 ) ⊕ (k 13 ⊕ k 9 ) ) ⊕

14 ( S −1 (x 10 ⊕ k 10 ) ⊕ (k 10 ⊕ k 14 )) ) ⊕ 11 ( S −1 (x 7 ⊕ k 7 ) ⊕ .

(k 15 ⊕ k 11 ) ) ⊕ 13 ( S −1 (x 4 ⊕ k 4 ) ⊕ (k 16 ⊕ k 12 ) ) )

We can consider A and B to be random values in F 2 8 . For a given values of f the diﬀerence between A and B will be equal to f with a probability of 2 1 8 . Using the same reasoning, the probability of all four equations being valid is 1 4 = 2 1 32 . 2 8 We have to consider all the possible values of f , i.e. {0, . . . , 255}. A given key hypothesis will, therefore, be valid for some arbitrary value of f with a probability of 2 8 × 2 1 32 = 2 1 24 . The ﬁrst step of the attack is expected to return 2 32 hypotheses each of which still be under consideration at the end of the second step with a probability of 2 1 24 . One would, therefore, expect the second step of the attack to produce 2 8 possible key hypotheses.

<!-- PDF_PAGE: 9 -->

## PDF page 9

232 M. Tunstall, D. Mukhopadhyay, and S. Ali

### 3.5 Attacking other Bytes

In the previous sections we describe an attack where we base our Diﬀerential Fault Analysis on the knowledge that a fault has been induced in the ﬁrst byte of the state matrix. However, we can note that the analysis returns a very small number of hypotheses. We can, therefore, conduct 16 independent analyses under the assumption that a fault is induced each of the 16 bytes of of the state at the beginning of the eighth round. An attacker would expect this to produce 2 4 × 2 8 = 2 12 valid key hypotheses, which is still a trivial exhaustive search.

Comparison with Previous Work

4

There are several versions of fault-based diﬀerential cryptanalysis that are able to reduce the number of key hypotheses from two faults injected into an imple- mentation of AES, as described in [5, 9, 12]. However, the analysis proposed in this paper is more eﬀective, since the resulting exhaustive search can be reduced to a trivial size using one fault. The number of key hypotheses returned by pre- vious work would be somewhat time consuming. The advantage of the proposed attack is that it does not need to reproduce a successful attack in order to able to determine a secret key. Acquiring multiple faulty ciphertexts can be problem- atic as faults are only successful with a certain probability, and the eﬀect cannot always be predetermined. This would mean that an attacker could potentially have to search among numerous faulty ciphertexts to ﬁnd a pair that both have the desired fault.

5 Conclusion

This paper proposes a fault-based diﬀerential cryptanalysis of AES, that is an extended version of the attack described in [9]. An attacker would expect to be able to reduce the number of key hypotheses from 2 128 to 2 8 with one well placed fault. As noted in [8], these attacks can be conducted without any knowledge of the plaintext being enciphered, as an attacker would just need to know the plaintexts were the same. There are many descriptions of a fault-based diﬀerential cryptanalysis of AES that could be prevented by repeating the last two or three rounds of an implemen- tation of AES, to verify that no exploitable fault has been inserted [1,2,3,12,13]. However, to prevent the attack described in this paper the last four rounds would need to be repeated to check no fault was injected. Moreover, given how much information can be gleaned from one fault, one would expect there are attacks that require more faulty ciphertexts that would be able to make use of faults in earlier rounds. One would, therefore, suggest that in order to protect an implementation of AES the last ﬁve rounds should be protected against fault injection.

<!-- PDF_PAGE: 10 -->

## PDF page 10

Diﬀerential Fault Analysis of the Advanced Encryption Standard

Acknowledgements

233

The work described in this paper has been supported in part by the European Commission IST Programme under Contract ICT-2007-216676 ECRYPT II and EPSRC grant EP/F039638/1 “Investigation of Power Analysis Attacks”. The second author would like to acknowledge the support of Department of Science and Technology (DST) India under the Fast Track Proposals for Young Scientists for the proposal entitled ”Design and Analysis of Side Channel Attack Resistant Symmetric Key Cryptosystems”.

### References

1. Blömer, J., Seifert, J.-P.: Fault based cryptanalysis of the advanced encryption standard (AES). In: Wright, R.N. (ed.) FC 2003. LNCS, vol. 2742, pp. 162–181. Springer, Heidelberg (2003) 2. Dusart, P., Letourneux, G., Vivolo, O.: Diﬀerential fault analysis on A.E.S. In: Zhou, J., Yung, M., Han, Y. (eds.) ACNS 2003. LNCS, vol. 2846, pp. 293–306. Springer, Heidelberg (2003) 3. Giraud, C.: DFA on AES. In: Dobbertin, H., Rijmen, V., Sowa, A. (eds.) AES 2005. LNCS, vol. 3373, pp. 27–41. Springer, Heidelberg (2005) 4. Giraud, C., Thillard, A.: Piret and Quisquater’s DFA on AES revisited. Cryptology ePrint Archive, Report 2010/440 (2010), http://eprint.iacr.org/ 5. Kim, C.H., Quisquater, J.-J.: New diﬀerential fault analysis on AES key schedule: Two faults are enough. In: Grimaud, G., Standaert, F.-X. (eds.) CARDIS 2008. LNCS, vol. 5189, pp. 48–60. Springer, Heidelberg (2008) 6. Knudsen, L.: Deal — a 128-bit block cipher. Technical report no. 151. Department of Informatics, University of Bergen, Norway (1998) 7. Li, Y., Gomisawa, S., Sakiyama, K., Ohta, K.: An information theoretic perspective on the diﬀerential fault analysis against aes. Cryptology ePrint Archive, Report 2010/032 (2010), http://eprint.iacr.org/ 8. Moradi, A., Shalmani, M.T.M., Salmasizadeh, M.: A generalized method of diﬀer- ential fault attack against AES cryptosystem. In: Goubin, L., Matsui, M. (eds.) CHES 2006. LNCS, vol. 4249, pp. 91–100. Springer, Heidelberg (2006) 9. Mukhopadhyay, D.: An improved fault based attack of the advanced encryption standard. In: Preneel, B. (ed.) AFRICACRYPT 2009. LNCS, vol. 5580, pp. 421– 434. Springer, Heidelberg (2009) 10. National Institute of Standards and Technology (NIST). Advanced Encryp- tion Standard (AES). FIPS Publication 197 (2001), http://www.itl.nist.gov/ fipspubs/ 11. Nyberg, K.: Diﬀerentially uniform mappings for cryptography. In: Helleseth, T. (ed.) EUROCRYPT 1993. LNCS, vol. 765, pp. 55–64. Springer, Heidelberg (1994) 12. Piret, G., Quisquater, J.-J.: A diﬀerential fault attack technique against SPN struc- tures, with application to the AES and KHAZAD. In: Walter, C.D., Koç, Ç.K., Paar, C. (eds.) CHES 2003. LNCS, vol. 2779, pp. 77–88. Springer, Heidelberg (2003) 13. Takahashi, J., Fukunaga, T., Yamakoshi, K.: DFA mechanism on the AES schedule. In: Fault Diagnosis and Tolerance in Cryptography 2007 — FDTC 07, pp. 62–72 (2007)
