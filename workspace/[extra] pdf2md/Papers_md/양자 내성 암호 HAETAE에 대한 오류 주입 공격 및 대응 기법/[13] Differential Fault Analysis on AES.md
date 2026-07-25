# [13] Differential Fault Analysis on AES

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 14
converted_at: "2026-07-26"
source_asset_id: "HAETAE-FIA-REF-13"
derived_asset_id: "HAETAE-FIA-REF-13-MD"
source_path: "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[13] Differential Fault Analysis on AES.pdf"
source_sha256: "915053e6bf30b0aa2a544ff19d521a02266be064a7a874356f3698b7fca2a937"
pages: 14
bbox_words: 6701
consumed_bbox_words: 6701
numeric_tokens: 1499
consumed_numeric_tokens: 1499
source_blocks: 242
consumed_source_blocks: 242
emitted_blocks: 213
embedded_raster_images: 0
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 14
glyph_chars_removed: 207
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

Diﬀerential Fault Analysis on A.E.S

Pierre Dusart 1 , Gilles Letourneux 2 , and Olivier Vivolo 2

1

LACO (URM CNRS n ◦ 6090), Faculté des Sciences &amp; Techniques, 123, avenue Albert THOMAS, 87060 Limoges, France dusart@unilim.fr, http://www.unilim.fr/laco 2 E.D.S.I. Atalis 1, 1, rue de Paris, 35510 Cesson-Sévigné, France development@edsi-smartcards.com.fr

Abstract. DFA is no new attack. It was ﬁrst used by Biham and Shamir who took unfair advantage of DES Feistel structure to carry it out. This structure is not present in AES. Nevertheless, is DFA able to attack AES another way? This article aims at setting out a means of applying DFA to AES that exploits AES internal structure. We can break an AES128 key with ten faulty messages within a few minutes.

1 Introduction

In September 1996, Boneh, Demillo, and Lipton [5] from Bellcore disclosed infor- mation about a new type of cryptanalytic attack which exploits computational errors to ﬁnd cryptographic keys. Their attack is applicable to public key cryp- tosystems such as RSA, excluding secret key algorithms. In [4], E. Biham &amp; A.Shamir extended this attack to various secret key cryptosystems such as DES, and called it Diﬀerential Fault Analysis (DFA). They applied the diﬀerential cryptanalysis to Data Encryption Standard (DES) within the frame of hardware fault model.

Since that time 56-bit key has been too short to be secure and worldwide competition between secret key cryptosystems has been raging. The standard which was to replace DES standard had to fulﬁll the following requirements: be a symmetric cryptosystem with 128 to 256 key sizes, easy to implement with hardware and resilient to linear and diﬀerential cryptanalyses. On Oct. 2, 2000, NIST chose Rijndael as Advanced Encryption Standard (AES).

We further assume that the attacker is in possession of a tamperproof-device, so that he can repeat the experiment with the same plaintext and key without applying external physical eﬀects. As a result, he obtains two ciphertexts derived from the same (unknown) plaintext and key, among which one is correct and the other the result of a computation corrupted by a single error occuring during the computation.

J. Zhou, M. Yung, Y. Han (Eds.): ACNS 2003, LNCS 2846, pp. 293–306, 2003. c Springer-Verlag Berlin Heidelberg 2003

<!-- PDF_PAGE: 2 -->

## PDF page 2

294 P. Dusart, G. Letourneux, and O. Vivolo

The major criticism of DFA was about its putting into practice possibilities until some authors [3] proved it to be possible. They introduced a fault while the program related to AES was running. A sealed tamperproof device when exposed to certain physical phenomena (e.g., ionizing or microwave radiation) is very likely to cause a fault to happen at a bit in any of the registers at an intermediate stage during the cryptographic computation. In practice, more than one bit can be altered. Whenever the attacker applies DFA attack to the DES, making the most of DES Feistel structure, he knows both diﬀerential input and output of the targeted SBox.

When applying DFA to DES, using the Feistel structure of DES, the attacker knows the diﬀerential input and output of the target SBox. It is necessary that the attacker should know these diﬀerentials to discover a round key byte. With AES, the situation is diﬀerent because only output diﬀerential is known to the attacker. There is no ﬁnding immediately the error that alters substitution input. On the other hand, the set of values possibly taken on by the error slipped in can be determined. Knowing that is still not enough. Given that the fault introduced can possibly take 127 values, the round key byte concerned can take as many as 256 values. Thus AES is immune to the classical diﬀerential analysis attack. We intend to reduce the set of values possibly taken on by the error introduced assuming that it spreads over at least two distinct bytes used in the SubBytes operation performed through the ciphering process. The error introduced in each SBox input, can possibly take 127 values. As they originate in the same error, only their intersection deserves further consideration. This way the number of possibly committed errors is reduced by half (for a generic case, these sets are diﬀerent). Either round key byte included in the target Sbox can then take 128 possible values. Key K N r value can be found by repeating an error at the same state byte. In the end, we proved that AES is vulnerable to diﬀerential fault analysis. We implemented the attack on a personal computer. Our analysis program extracted the full AES-128 key by analysing less than 50 ciphertexts.

The document is organized as follows. After brieﬂy descripting AES, we will list a number of DFA-based attack models and then show how to quickly ﬁnd out the set of values the last round key is likely to take. In the appendix, we illustrate our attack with an example.

The authors thank Joan Daemen for his valuable comments on the article. We are grateful to Cédric Hasard for his help.

2 Brief Description of AES

In this article, we give a description of AES slightly diﬀerent from [1] as we use a matrix on GF (2 8 ) to describe a state. Nevertheless, we keep using the notations of [1].

<!-- PDF_PAGE: 3 -->

## PDF page 3

Diﬀerential Fault Analysis on A.E.S 295

The AES is a block cipher with block length to 128 bits, and support key lengths N k of 128, 192 or 256 bits. The AES is a key-iterated block cipher : it consists in repeating the application of a round transformation to the state. The number of rounds is represented by N r and depends on the key length (N r = 10 for 128 bits, N r = 12 for 192 bits and N r = 14 for 256 bits). The AES transforms a state, noted S ∈ M 4 (GF (2 8 )) , (i.e. S is a 4x4 matrix with its coeﬃcients in GF (2 8 )) into another state in M 4 (GF (2 8 )). The key K is used for generating N r + 1 round keys noted K i ∈ M 4 (GF (2 8 )) (i = 0, 1, . . . , N r ). With AES, a round of an encryption is composed of four main operations: AddRoundKey, MixColumns, SubBytes, ShiftRows.

Remark 1. The representation chosen in [1] of GF (2 8 ) is GF (2)[X]/ &lt; m &gt;, where &lt; m &gt; is the ideal generated by the irreducible polynomial m ∈ GF (2)[X], m = x 8 + x 4 + x 3 + x + 1.

Remark 2. We use three notations, equivalent to one another, to represent an element in GF (2 8 ):

– x 7 + x 6 + x 4 + x 2 , the polynomial notation – {11010100} b , the binary notation – ’D4’, the hexadecimal notation

AddRoundKey for i th Round

2.1

The AddRoundKey transformation consists in adding up matrices in M 4 (GF (2 8 )) between the state and the round key of the i th round. We rep- resent by S i,A the state after the i th AddRoundKey.

M 4 (GF (2 8 )) −→ M 4 (GF (2 8 )) S −→ S i,A = S + K i

SubBytes for i th Round

2.2

The SubBytes transformation consists in applying to each element of the matrix S an elementary transformation s. We represent by S i,Su the state after the i th SubBytes.

8 M 4 (GF (2 8  )) −→ M 4 (GF (2  ))  S[0] S[4] S[8] S[12] s(S[0]) s(S[4]) s(S[8]) s(S[12])  S[1] S[5] S[9] S[13]   s(S[1]) s(S[5]) s(S[9]) s(S[13])     S =   S[2] S[6] S[10] S[14]  −→ S i,Su =  s(S[2]) s(S[6]) s(S[10]) s(S[14])  S[3] S[7] S[11] S[15] s(S[3]) s(S[7]) s(S[11]) s(S[15])

where s is the non linear application deﬁned by

GF (2 8 ) −→ GF (2 8 )

x −→ s(x) =

a ∗ x −1 + b, if x = 0, b, if x = 0.

<!-- PDF_PAGE: 4 -->

## PDF page 4

296 P. Dusart, G. Letourneux, and O. Vivolo

a is a linear invertible application over GF (2), a ∈ M 8 (GF (2)), ∗ is the mul- tiplication of matrices over GF (2) and x −1 = {b 0 b 1 ...b 7 } b is seen as a GF (2)- vector equal to the transposition of the vector (b 0 , · · · , b 7 ). The value of b = ’63’∈ GF (2 8 ) and   10001111  1 1 0 0 0 1 1 1     1 1 1 0 0 0 1 1     1 1 1 1 0 0 0 1    . a =    1 1 1 1 1 0 0 0   0 1 1 1 1 1 0 0     0 0 1 1 1 1 1 0  00011111

### 2.3 MixColumns for i th Round

The MixColumns transformation consists in multiplying the state by a ﬁxed matrix A 0 of M 4 (GF (2 8 )). We represent by S i,M the state after the i th Mix- Columns. M 4 (GF (2 8 )) −→ M 4 (GF (2 8 )) S −→ S i,M = A 0 .S,

where A 0 is deﬁned by

 ’02’ ’03’ ’01’ ’01’  ’01’ ’02’ ’03’ ’01’   A 0 =   ’01’ ’01’ ’02’ ’03’  . ’03’ ’01’ ’01’ ’02’

### 2.4 ShiftRows for i th Round

The ShiftRows transformation is a byte transposition that cyclically shifts the rows of the state with diﬀerent oﬀsets. We represent by S i,Sh the state after the i th ShiftRows.

8 )) −→ M 4 (GF (2 M 4 (GF (2 8   ))  S[0] S[4] S[8] S[12] S[0] S[4] S[8] S[12]  S[1] S[5] S[9] S[13]   S[5] S[9] S[13] S[1]     S =   S[2] S[6] S[10] S[14]  −→ S i,Sh =  S[10] S[14] S[2] S[6]  . S[3] S[7] S[11] S[15] S[15] S[3] S[7] S[11]

Attacks on Computation of AES

3

We describe a list of possible DFA attacks on AES. The attacker is able to intro- duce a fault into the AES computation process and ﬁnd out the cryptographic operation output. In all of those attack patterns, one fault means any error pos- sibly several bits long, standing at a byte of the state The goal of these attacks is to ﬁnd out the key K N r (and K N r−1 in the case of AES 192 and 256 bits) and hence the key K ([1] for interested readers).

<!-- PDF_PAGE: 5 -->

## PDF page 5

### 3.1 Models of Attack

Diﬀerential Fault Analysis on A.E.S 297

All these attacks are based on the basic attack pattern.

Basic attack after the N r − 2 th MixColumns and before the N r − 1 th MixColumns. We introduce a random fault into a deﬁnite byte in the state known to the attacker between N r − 2 th MixColumns and the N r − 1 th Mix- Columns. The fault introduced into the state hits four bytes through last Mix- Columns. Through SubBytes operation, these four bytes interact with four bytes in N r th round key and result in four diﬀerential faults ε . From each of the four diﬀerential faults, we deﬁne the set S c,ε of values possibly taken on by the initial fault. As the four faults originated in the same initial fault, its real value be- longs to the set made up by the intersection of the four previous sets. According to proposition 5, 63 elements at the most constitute that intersection. It stems from proposition 6 that each of the 4 bytes of key K N r may possibly take 128 values. By iterating the introduction of a fault, the set of values possibly taken on by the keys is reduced by half. After having introduced ﬁve faults running, we discover four bytes of the round key. Applying this technique to another row or column, we can manage to discover for other bytes of the last round key. In using about 20 pairs (distorted ciphered output and correct ciphered output), we extract the AES key in full.

Main attack after the N r − 2 th MixColumns and before the N r − 1 th MixColumns. We introduce a random fault into the state at a point unknown to the attacker. That is a generalization of the previous attack. Assuming that the fault may occur at four diﬀerent places allows us to ﬁnd out the key K N r . We thus put ourselves under the conditions of the previous attack so as to determine four sets of Key K N r possible values. It is necessary that the attack should be repeated using from 40 to 50 distinct pairs (distorted ciphered output and correct ciphered output) for the complete key to be extracted.

Attack after the N r − 3 th MixColumns and before the N r − 2 th Mix- Columns. We introduce a random fault into the state at a point unknown to the attacker. N r − 2 th ShiftRows spreads each of the four faults over another column of the state. The last MixColumns propagates each fault contained in a column to the whole of it. We can apply the result of the basic attack to every fault contained in a column in order or determine the sets of values pos- sibly taken on by every byte of the last round key. In such a case ten faults are required to get key K N r .

Attack on hardware device. It is possible to apply the previous patterns of attack to hardware device. Suppose that you can physically modify a hardware AES device. Firstly, compute the outputs from around ten random plaintexts with an AES device. Secondly, modify for instance the component design by

<!-- PDF_PAGE: 6 -->

## PDF page 6

298 P. Dusart, G. Letourneux, and O. Vivolo

cutting wires lying between two bytes and grounding them (or Vcc) temporarily two rounds before the process ends. It amounts to having a byte of round N r − 2 with a ’00’ (or ’FF’) value. Compute another time the same plaintexts as previously with the tampered device. When the input is a random plaintext, the error generated is a random one. Proceeding along as set out in the previous paragraph, we can extract key K N r .

### 3.2 Basic Principle of Attacks

Let us analyse basic attack, we denote by F the erroneous state. Now we are going to describe each step of the state from the N r − 1 th MixColumns to the end. Assume that we replace the ﬁrst element of the state by an unknown value. Let ε ∈ GF (2 8 ) − {0}, and get

F N r −1,Sh [0] = S N r −1,Sh [0] + ε.   ε 000  0 0 0 0   F N r −1,Sh = S N r −1,Sh +   0 0 0 0  . 0000

   ε 000 ’02’.ε 0 0 0  0 0 0 0   ε 0 0 0     F N r −1,M = S N r −1,M + A 0 .   0 0 0 0  = S N r −1,M +  ε 0 0 0  . 0000 ’03’.ε 0 0 0   ’02’.ε 0 0 0  ε 0 0 0   F N r −1,A = S N r −1,A +   ε 0 0 0  . ’03’.ε 0 0 0

We can deﬁne ε 0 , ε 1 , ε 2 , ε 3 (the diﬀerential faults) by the equations  s(x 0 + ’02’.ε) = s(x 0 ) + ε 0    s(x 1 + ε) = s(x 1 ) + ε 1 s(x 2 + ε) = s(x 2 ) + ε 2    s(x 3 + ’03’.ε) = s(x 3 ) + ε 3

Consequently

(1)

  ε 0 0 0 0  ε 1 0 0 0   F N r ,Su = S N r ,Su +   ε 0 0 0  . 2 ε 3 0 0 0   ε 0 0 0 0  0 0 0 ε 1   F N r ,Sh = S N r ,Sh +   0 0 ε 0  .

2

0 ε 3 0 0

<!-- PDF_PAGE: 7 -->

## PDF page 7

Diﬀerential Fault Analysis on A.E.S 299

  ε 0 0 0 0  0 0 0 ε 1   F N r ,A = S N r ,A +   0 0 ε 0  .

2

0 ε 3 0 0

F N r ,A is the erroneous output of a cipher. Comparing the states F N r ,A with S N r ,A , the values of ε 0 , ε 1 , ε 2 and ε 3 can be easily found.

The only operation that could give a clue about the key K N r is the last SubBytes transformation. Consequently we have four equations where x 0 , x 1 , x 2 , x 3 , ε are unknown variables. We want to solve the system of equa- tions (in x i and ε) (1). All these equations belong to a generalized equation :

s(x + c.ε) + s(x) = ε ,

where c =’01’, ’02’ or ’03’. Let us analyse it.

(2)

Remark 3. The map deﬁned by x → x −1 in GF (2 8 ) is diﬀerentially 2 or 4 uni- form [7]. This map has other favorable cryptographic properties: large distance from aﬃne functions, high non-linear order and eﬃcient computability.

Deﬁnition 1. Consider the linear application in GF (2):

l : GF (2 8 ) −→ GF (2 8 ) x −→ x 2 + x

Let us represent by E 1 = Im(l) the GF (2)-vector space image of l. We have dim GF (2) (E 1 ) = 7. If θ ∈ E 1 , then there are two solutions x 1 , x 2 ∈ GF (2 8 ) to the equation x 2 + x = θ, and the solutions satisfy the equation x 2 = x 1 + 1.

Deﬁnition 2. Let λ ∈ GF (2 8 ), λ = 0 and deﬁne φ λ a GF (2)-vector spaces isomorphism: φ λ : GF (2 8 ) −→ GF (2 8 ) x −→ λ.x

and let E λ = Im(φ λ | E 1 ) be the GF (2)-vector space image of φ λ restricted to E 1 . Moreover dim GF (2) (E λ ) = 7.

Proposition 1. There is a bijective application φ between E 1 ∗ (= E 1 − {0}) and S c,ε . φ : E 1 ∗ −→ S c,ε t −→ (c(a −1 ∗ ε ).t) −1 .

S c,ε have 127 elements.

Proof. Let ε ∈ S c,ε , then ∃x ∈ GF (2 8 ) such that (2) holds. Let us assume x = 0 and x = c.ε, we get

x 2 + c.ε.x = (a −1 ∗ ε ) −1 .c.ε.

<!-- PDF_PAGE: 8 -->

## PDF page 8

300 P. Dusart, G. Letourneux, and O. Vivolo

We represent by t = x.(c.ε) −1 ∈ GF (2 8 ) − {0}, then we have

t 2 + t = (a −1 ∗ ε ) −1 .(c.ε) −1 .

(3)

Therefore (a −1 ∗ ε ) −1 (c.ε) −1 ∈ E 1 ∗ . Reciprocally for θ ∈ E 1 ∗ we can deﬁne (a −1 ∗ ε ) −1 .(c.θ) −1 ∈ S c,ε . Let us assume x = 0 or x = c.ε, (2) becomes a ∗ (c.ε) −1 = ε . We obtain ε = ((a −1 ∗ ε ).c) −1 . This case is included in the previous one because 1 ∈ E 1 ∗ . We observe that when θ = 1, four solutions in x to the equation (2) can be found. In brief, a bijection map exists between E 1 ∗ and S c,ε :

φ λ

E 1 ∗ −→ E λ − {0} −→ S c,ε t −→ λ.t −→ (λ.t) −1 .

where λ = c(a −1 ∗ ε ).

Proposition 2. The following statements hold for λ 1 , λ 2 ∈ GF (2 8 ) − {0}: 7 If λ 1 = λ 2 dim GF (2) (E λ 1 ∩ E λ 2 ) = 6 Otherwise

Proof. Proving that following lemma 1 holds true is enough to prove Proposition 2 holds true too.

Lemma 1. For λ 1 , λ 2 ∈ GF (2 8 ) − {0}, we get

E λ 1 = E λ 2 ⇐⇒ λ 1 = λ 2 .

Proof. This lemma is equivalent to this proposition: for λ ∈ GF (2 8 ) − {0},

E λ = E 1 ⇐⇒ λ = 1.

Let us prove this statement and assume that λE 1 = E 1 . Remark that E 1 = {t = {t 7 t 6 · · · t 0 } b ∈ GF (2 8 ) − {0} : t 7 = t 5 }. Hence {1, x, x 2 , x 3 , x 4 , x 6 , x 5 + x 7 } is a basis of E 1 . Let us multiply the basis vectors v i of E 1 by λ = {λ 7 · · · λ 0 } b . As λv i ∈ E 1 , we have (λv i ) 7 = (λv i ) 5 . We obtain 7 relations (λ 7 = λ 5 , λ 6 = λ 4 , λ 5 = λ 3 + λ 7 , λ 4 = λ 6 + λ 2 + λ 7 , λ 7 + λ 3 = λ 5 + λ 1 + λ 6 , λ 5 + λ 1 = λ 3 + λ 4 , λ 6 + λ 5 = λ 7 + λ 3 ). We solve this system to obtain λ 7 = λ 6 = λ 5 = λ 4 = λ 3 = λ 2 = λ 1 = 0. The solution λ = 0 is not right. We can infer that λ = 1.

Proposition 3. For λ 1 , λ 2 , λ 3 ∈ GF (2 8 ) − {0}, we get:   7 If λ 1 = λ 2 = λ 3 −1 −1 dim GF (2) (E λ 1 ∩ E λ 2 ∩ E λ 3 ) = 6 If rank GF (2) {λ −1 1 , λ 2 , λ 3 } = 2  5 Otherwise

Proof. It follows from proposition 2 and this following lemma

<!-- PDF_PAGE: 9 -->

## PDF page 9

Diﬀerential Fault Analysis on A.E.S 301

Lemma 2. For λ 1 , λ 2 , λ 3 ∈ GF (2 8 ) − {0}, we get

−1 −1 E λ 1 ∩ E λ 3 = E λ 2 ∩ E λ 3 ⇐⇒ λ −1 3 = λ 1 + λ 2 or λ 1 = λ 2 .

Proof. 1. ⇐ Let x ∈ E λ 1 ∩ E λ 3 , then ∃y, t ∈ E 1 such that x = λ 1 .y = λ 3 .t.

−1 y = λ −1 1 .λ 3 .t = λ 2 .λ 3 .t + t,

y − t = λ −1 2 .λ 3 .t ∈ E 1 ,

and

x = λ 3 .t = λ 2 .(y − t) ∈ E λ 2

2. ⇒ −1 Let us assume that λ 1 = λ 2 , and show that ∀t ∈ E 1 , λ 3 .(λ −1 1 + λ 2 ).t ∈ E 1 . Let x = λ 3 .t ∈ E λ 3 : – If x ∈ E λ 1 then x ∈ E λ 2 and ∃s 1 , s 2 ∈ E 1 so that x = λ 1 .s 1 = λ 2 .s 2 and −1 we get λ 3 .(λ −1 1 + λ 2 ).t = s 1 + s 2 ∈ E 1 . / E λ 2 and we get λ −1 / E 1 and λ −1 / E 1 . We – If x ∈ / E λ 1 then x ∈ 1 .x ∈ 2 .x ∈ −1 −1 −1 −1 / E 1 and have λ 3 .(λ 1 + λ 2 ).t = λ 1 .x + λ 2 .x ∈ E 1 (because ∀u ∈ ∀v ∈ / E 1 then u + v ∈ E 1 ). = We showed that E λ 3 .(λ −1 +λ −1 ) = E 1 and with the lemma 1 we get λ −1 3

1 2

−1 λ −1 1 + λ 2 .

Proposition 4. Finally for λ 1 , λ 2 , λ 3 , λ 4 ∈ GF (2 8 ) − {0}, we get:  7 If λ 1 = λ 2 = λ 3 = λ 4    −1 −1 −1 6 If rank GF (2) {λ −1 1 , λ 2 , λ 3 , λ 4 } = 2 dim GF (2) (E λ 1 ∩ E λ 2 ∩ E λ 3 ∩ E λ 4 ) = −1 −1 −1 5 If rank GF (2) {λ 1 , λ 2 , λ 3 , λ −1  4 } =3   4 Otherwise

Deﬁnition 3. We deﬁne the set of solutions to (2) in ε by

S c,ε = ε ∈ GF (2 8 ) : ∃x ∈ GF (2 8 ), s(x + c.ε) + s(x) = ε .

Deﬁnition 4. We considered four equations in a diﬀerent way, but the fault introduced is common to these four equations. This is the reason why we introduce the set of possibly introduced faults S: Π = S 2,ε 0 S 1,ε 1 S 1,ε 2 S 3,ε 3 .

Π has a smaller cardinal than S c,ε . This allows one to specify more accurately the set of values possibly taken on the faults. Thus the key can be found out by introducing fewer faults.

<!-- PDF_PAGE: 10 -->

## PDF page 10

302 P. Dusart, G. Letourneux, and O. Vivolo

Proposition 5. If two of the four following values 2 −1 .ε 0 , ε 1 , ε 2 , 3 −1 .ε 3 are not equal, we get S 1,ε 1 S 1,ε 2 S 3,ε 3 ≤ 63. Card S 2,ε 0

Proposition 6. For a diﬀerential fault ε , let ε ∈ Π ∩ S c,ε be a fault value, θ = ((a −1 ∗ε ).c.ε) −1 ∈ E 1 ∗ and α, β the two solutions (in GF (2 8 )) to the equation t 2 + t = θ. The possible values of key K N r [i] (for a certain i, being the index of element in the state) are

– If θ = 1 then K N r [i] can possibly take on two values

K N r [i] = s(c.ε.α) + F N r ,A [i] or K N r [i] = s(c.ε.β) + F N r ,A [i]

– If θ = 1 then K N r [i] can possibly take on four values

K N r [i] = s(c.ε.α) + F N r ,A [i] or K N r [i] = s(c.ε.β) + F N r ,A [i]

or K N r [i] = b + F N r ,A [i] or K N r [i] = s(c.ε) + F N r ,A [i]

Proof. – If θ = 1 then we know that θ ∈ E 1 , and there are two solutions α, β to t 2 + t = θ. We can deduce two solutions from (2) noted {x 1 , x 2 }, where x 1 = c.ε.α and x 2 = c.ε.β. – If θ = 1, we know that 1 ∈ E 1 , and there are two solutions α, β to t 2 + t = 1. We can deduce two solutions from (2) noted {x 1 , x 2 }, where x 1 = c.ε.α and x 2 = c.ε.β. Moreover there are also two trivial solutions to (2): x 3 = 0 and x 4 = c.ε. Once we get a solution x to (2), K N r [i] value can be easily inferred.

By applying this proposition to the four erroneous elements of the state, we can deduce four sets of values that K N r [0], K N r [7], K N r [10] and K N r [13] can taken on. By introducing repeatedly a fault into a computation, and considering the intersection of those four sets we soon get the true value for K N r [0], K N r [7], K N r [10] and K N r [13].

### 3.3 Probability Complexity

We want to know how many pairs we need to crack the cipher. Proposition 7. In average, 9 pairs are required to ﬁnd 4 bytes of the K N r round key. Alike, 11 pairs are required for the Basic attack, 9 for the Extended ones and 34 for the main one.

Proof. Denote by Card K the cardinal of possible values taken on by any byte of K N r . Under propositions 4 and 6, supposing they have been distributed at random, probabilities are as follows:

– 256·255·254·253 that Card K = 32 256 4

C 4 2 ·256·255·254 that Card K = 64 256 4

–

<!-- PDF_PAGE: 11 -->

## PDF page 11

(C 3 +C 2 /2)·256·255

4 4 – that Card K = 128 256 4 256 – 256 4 that Card K = 256

Diﬀerential Fault Analysis on A.E.S 303

On average, Card K = 32.75146103 when the position of the fault is known. In general, such information is not available so the four possibilities have to be tried: Card K = 4 · 32.75146103 = 131.0058441. Each time, the set of possible values 256 ≈ 1.954111298. To bring the number of possibilities is divided by 131.0058441 down to one, ln 256/ ln 1.954111298 ≈ 8.277180940 pairs are required. Hence, nine faulty ciphertexts have to be used to ﬁnd 4 bytes of the K N r round key. In the Extended attacks, 16/4=4 more pairs are required but the four errors are treated simultaneously. Hence in these cases, nine faulty ciphertexts have to be used to ﬁnd the whole K N r round key. In the basic attack, the errors have to be distribued all over the other bytes; 16/4=4 more pairs are required:

4

ln 256 ≈ 10.78707691. 256 ln 32.75146103

A Example

We will be using the same example as in Appendix B of [1]. The following diagram shows the values in the ﬁnal states for a block length and a Cipher Key length of 16 bytes each (i.e., N b = 4 and N k = 4).

Input= ’32 43 F6 A8 88 5A 30 8D 31 31 98 A2 E0 37 07 34’ Cipher Key= ’2B 7E 15 16 28 AE D2 A6 AB F7 15 88 09 CF 4F 3C’ Output= ’39 25 84 1D 02 DC 09 FB DC 11 85 97 19 6A 0B 32’

The spreading of the fault is highlighted:

After ShiftRows 9 Fault injected 1E

After MixColumns

K 9

87 F2 4D 97 99 F2 4D 97 7B 40 A3 4C AC 19 28 57 6E 4C 90 EC 6E 4C 90 EC 29 D4 70 9F ⊕ 77 FA D1 5C 46 E7 4A C3 46 E7 4A C3 8A E4 3A 42 66 DC 29 00 A6 8C D8 95 A6 8C D8 95 CF A5 A6 BC F3 21 41 6E

After AddRoundKey 9 After SubBytes 10

After ShiftRows 10 value of K 10

D7 59 8B 1B 0E CB 3D AF 0E CB 3D AF D0 C9 E1 B6 5E 2E A1 C3 58 31 32 2E 31 32 2E 58 ⊕ 14 EE 3F 63 EC 38 13 42 CE 07 7D 2C 7D 2C CE 07 F9 25 0C 0C 3C 84 E7 D2 EB 5F 94 B5 B5 EB 5F 94 A8 89 C8 A6

Output with Faults

DE 02 DC 19 25 DC 11 3B 84 09 C2 0B 1D 62 97 32

<!-- PDF_PAGE: 12 -->

## PDF page 12

304 P. Dusart, G. Letourneux, and O. Vivolo

The error injected into the state, generates four further errors (diﬀerential faults) in the ﬁnal state.

Output with faults

Output without fault Error

DE 02 DC 19 39 02 DC 19 E7 00 00 00 25 DC 11 3B ⊕ 25 DC 11 6A = 00 00 00 51 84 09 C2 0B 84 09 85 0B 00 00 47 00 1D 62 97 32 1D FB 97 32 00 99 00 00

The diﬀerential faults are ε 0 = ’E7’, ε 1 = ’51’, ε 2 = ’47’ and ε 3 = ’99’. The following four equations have now to be worked out:

s(x 0 ⊕ ’02’.ε) = s(x 0 ) ⊕ ’E7’

s(x 1 ⊕ ε) = s(x 1 ) ⊕ ’51’ s(x 2 ⊕ ε) = s(x 2 ) ⊕ ’47’

s(x 3 ⊕ ’03’.ε) = s(x 3 ) ⊕ ’99’

As deﬁned previously,

E 1 ∗ = {’01’..’1F’,’40’..’5F’,’A0’..’BF’,’E0’..’FF’}.

Let

λ 0 = ’02’.(a −1 ∗ ’E7’) = ’12’

λ 1 = ’01’.(a −1 ∗ ’51’) = ’7C’

λ 2 = ’01’.(a −1 ∗ ’47’) = ’65’

λ 3 = ’03’.(a −1 ∗ ’99’) = ’B0’

−1 We have a single linear relation over GF (2) between λ 0 , λ 1 , λ 2 , λ 3 : λ −1 0 ⊕ λ 3 = −1 λ 2 . Therefore we get card S 2,’E7’ S 1,’51’ S 1,’47’ S 3,’99’ = 2 5 − 1 = 31.

Using the relation S c,ε = {(c.(a −1 ∗ ε ).t) −1 , quickly!) compute S 2,’E7’ S 1,’51’ S 1,’47’ S 3,’99’

t ∈ E 1 ∗ }, we can easily (and

= {’01’, ’04’, ’13’, ’1E’, ’21’, ’27’, ’33’, ’3B’, ’48’, ’4D’, ’50’, ’53’, ’55’, ’5D’, ’64’, ’65’,’7E’, ’7F’, ’80’, ’83’, ’8D’, ’8F’, ’93’, ’A7’, ’A8’, ’A9’, ’AB’, ’B3’, ’B8’, ’C9’, ’F6’}

Using the proposition 6, we get a set of values possibly taken on by K 10 [0] (the true value is ’D0’):

<!-- PDF_PAGE: 13 -->

## PDF page 13

Diﬀerential Fault Analysis on A.E.S 305

K 10 [0] ∈ {’03’, ’06’, ’09’, ’0C’, ’10’, ’15’, ’1A’, ’1F’, ’21’, ’24’, ’2B’, ’2E’, ’32’, ’37’, ’38’, ’3D’, ’43’, ’46’, ’49’, ’4C’, ’50’, ’55’, ’5F’, ’61’, ’64’, ’6B’, ’6E’, ’72’, ’77’, ’78’, ’7D’, ’83’, ’86’, ’89’, ’8C’, ’90’, ’95’, ’9A’, ’9F’, ’A1’, ’A4’, ’AB’, ’AE’, ’B2’, ’B7’, ’B8’, ’C3’, ’C6’, ’C9’, ’CC’, ’D0’, ’D5’, ’DA’, ’DF’, ’E1’, ’E4’, ’EB’, ’EE’, ’F2’, ’F7’, ’F8’, ’FD’}

By introducing a second fault into the very same place in the state, we reduce by half the set of values possibly taken on by K 10 [0]. Introducing a fault ﬁve times over, we can ﬁnd out the one and only true value of K 10 [0]. Of course, we can also analyse the other three bytes K 10 [7], K 10 [10] and K 10 [13] as we analyse the ﬁrst one. Doing so, we can ﬁnd out the true values of 4 bytes in key K 10 . In order to determine the other 4 bytes of the key K 10 , we have to introduce a fault into any other place in the state and repeat the above described process.

B Example 2

We compute ten pairs of (correct/faulty) ciphertexts with an AES-128 program. We know that we injected a fault into a byte between the MixColumn7 and MixColumn8 operations. Still we know neither its position nor its value (for the readers interesting in repeating those computations, the fault injected replaces State[0] by ’FF’ just before MixColumn8 in the following examples).

Correct CipherText Faulty CipherText

’467A7363D54E58BB25B135FABFA0EA49’ ’4F41429299FFBE374514034F07BF4B19’

’9EEE064F55D3B0F5DDC0002E33CDCBEE’ ’DF0C7EBA22B9131D83ADE91D223ADD6F’

’5EB4F21A7493ED8EA431B8E6B73FA924’ ’2A2B37C7B08482E43063040D357E7F92’

’1A6FC7471E2A43460AE4F29296CCB731’ ’A83C77CE284BCAF64DDE12DF58D8B9DB’

’7711043CE69C252E7219FBB12371CD66’ ’B7FF53C4D24FF23DF8618B229F8522CB’

’3253954160E455152D77F8A0748B0CEB’ ’CA499E9FB8BC82E3120C489FACDC654D’

’538FFA5AD396AE973EDB8C50B44EC54C’ ’5C655A7BDE74DED49BE0D36BF27662B8’

’1663332626442DA55F3362384FF1144B’ ’51116D1D351518FC7021931A20AC49A0’

’F9CC9D6B31BC0EA27D4E239DBBC943CD’ ’75EC4D4F1122E1B7F3F8AD578AA2CD11’

’8C7D0ABC6CDD13D0BD268469ED34FADB’ ’672A2B22556974C304C8C7DCD499ABAD’

The ﬁrst pair shows an diﬀerential error result, which can be split into four matrices. When every column preceding MixColumn9 is injected with a fault, the matrices show as follows:

 

’09’ ’4C’ ’60’ ’B8’

’F1’ ’8C’ ’B5’ ’50’

 

’00’ ’4C’ ’00’ ’00’  ’00’ ’00’    ’00’ ’A1’   ’00’ ’8C’ ’00’ ’00’ ’00’ ’00’ ’B5’ ’00’     ’00’ ’00’ ’60’ ’00’ ’00’ ’00’ ’00’ ’B8’      ’00’ ’B1’ ’00’ ’00’   ’00’ ’00’ ’A5’ ’00’     ⊕    ⊕    ’31’ ’00’ ’00’ ’00’   ’00’ ’E6’ ’00’ ’00’      ’00’ ’00’ ’00’ ’50’ ’F1’ ’00’ ’00’ ’00’

’09’ ’00’ ’00’ ’00’

      ’00’ ’00’ ’00’ ’1F’   ’3B’ ’00’  ’3B’ ’B1’ ’A5’ ’1F’        =   ⊕    ’00’ ’00’ ’36’ ’00’   ’00’ ’00’  ’31’ ’E6’ ’36’ ’A1’      

<!-- PDF_PAGE: 14 -->

## PDF page 14

306 P. Dusart, G. Letourneux, and O. Vivolo

By considering the ﬁrst matrice, the possible values of the key can be reduced (for the ﬁrst matrice, the error belongs to the ﬁrst column). If the error lies in the ﬁrst line: we have to compute the following L ε (1) = S 2,’09’ S 1,’1F’ S 1,’36’ S 3,’8C’

We have Card L ε (1) = 15, hence, using CipherT ext[0] =’46’ and Proposition 6, we get the ﬁrst set P K 1 [0] of values possibly taken on by K 10 [0]. If the error lies in the second line: we have to compute the following L ε (2) = S 3,’09’ S 2,’1F’ S 1,’36’ S 1,’8C’

We have Card L ε (2) = 15, hence, using CipherT ext[0] =’46’ and Proposition 6, we get the second set P K 2 [0] of values possibly taken on by K 10 [0]. We go over the same steps in the cases where the error lies in the third or in the fourth line. We refer to the resulting sets by P K 3 [0] and P K 4 [0]. Finally, K 10 [0] lies in

P K 1 [0] ∪ P K 2 [0] ∪ P K 3 [0] ∪ P K 4 [0]

which have 96 elements altogether. So we reduce the 256 values of K 10 [0] to only 96 possibilities. We go over the same steps applied to the second, third and fourth matrices (which impact on the other bytes of K 10 ) and ﬁnd

K 10 = ’D014F9A8C9EE2589E13F0CC8B6630CA6’

with ten faulty ciphertexts.

### References

1. FIPS PUB 197 : Avanced Encryption Standard, http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf 2. Joan Daemen and Vincent Rijmen, The Design of Rijndael, AES – The Advanced Encryption Standard, Springer-Verlag 2002, (238 pp.). 3. Ross J. Anderson, Markus G. Kuhn: Tamper Resistance – a Cautionary Note, The Second USENIX Workshop on Electronic Commerce Proceedings, Oakland, California, November 18–21, 1996, pp 1–11, ISBN 1-880446-83-9. 4. E. Biham and A.Shamir, Diﬀerential Fault Analysis of Secret Key Cryptosystems, CS 0910, Proceedings of Crypto’97. 5. Boneh, DeMillo, and Lipton, On the Importance of Checking Cryptographic Pro- tocols for Faults, Lecture Notes in Computer Science, Advances in Cryptology, proceedings of EUROCRYPT’97, pp. 37–51, 1997. 6. Joan Daemen, Annex to AES Proposal Rijndael, http://www.esat.kuleuven.ac.be/˜rijmen/rijndael/PropCorr.PDF,1998. 7. K. Nyberg, Diﬀerentially uniform mappings for cryptography, Advances in Cryp- tology, Proceedings Eurocrypt’93, LNCS 765, T. Helleseth, Ed., Springer-Verlag, 1994, pp. 55–64. 8. G. Letourneux, Rapport de stage EDSI : Etude et implémentation de l’AES, At- taques DPA et DFA, August 30, 2002.
