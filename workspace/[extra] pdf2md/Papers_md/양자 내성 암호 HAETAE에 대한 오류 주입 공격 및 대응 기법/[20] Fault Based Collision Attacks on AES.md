# [20] Fault Based Collision Attacks on AES

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 15
converted_at: "2026-07-26"
source_asset_id: "HAETAE-FIA-REF-20"
derived_asset_id: "HAETAE-FIA-REF-20-MD"
source_path: "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[20] Fault Based Collision Attacks on AES.pdf"
source_sha256: "9dcc4f22b1a8bcbe059013ed0fd158e6accab4829b42f30c9690b37ddd1ba9d1"
pages: 15
bbox_words: 8730
consumed_bbox_words: 8730
numeric_tokens: 874
consumed_numeric_tokens: 874
source_blocks: 167
consumed_source_blocks: 167
emitted_blocks: 142
embedded_raster_images: 18
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

Fault Based Collision Attacks on AES

Johannes Blömer and Volker Krummel

Faculty of Computer Science, Electrical Engineering and Mathematics University of Paderborn, Germany {bloemer, krummel}@uni-paderborn.de

Abstract. In this paper we present a new class of collision attacks that are based on inducing faults into the encryption process. We combine the classical fault attack of Biham and Shamir with the concept of collision at- tacks of Schramm et al. Unlike previous fault attacks by Blömer and Seifert our new attacks only need bit ﬂips not bit resets. Furthermore, the new at- tacks do not need the faulty ciphertext to derive the secret key. We only need the weaker information whether a collision has occurred or not. This is an improvement over previous attacks presented for example by Dusart, Letourneux and Vivolo, Giraud, Chen and Yen or Piret and Quisquater. As it turns out the new attacks are very powerful even against sophisti- cated countermeasures like error detection and memory encryption.

1 Introduction

A smartcard is a general purpose computer embedded in a plastic cover of a credit card’s size. The main building blocks of a smartcard are a CPU, a ROM that contains for example the operating system, an EEPROM containing among other things the secret key, and a RAM to store intermediate results of computations. To communicate with the outside world the smartcard has to be inserted into a so called smartcard reader that also provides the energy the smartcard needs for operating. Smartcards are perfectly suited for storing private information such as crypto- graphic keys because the corresponding cryptographic operations such as encryp- tion or digital signature are computed directly on the smartcard. Therefore the key never has to leave the smartcard and hence seems to be protected very well even in hostile environments. However, it is well known that physical instances of algorithms (in hardware or software) may leak information about the com- putation through so called side channels. Researchers identiﬁed several of those side channels and managed to use information obtained through side channels to determine secret keys of cryptographic applications. Kocher [13] was the ﬁrst who presented an attack based on timing measurements that successfully com- puted the secret key of RSA in 1996. This result was improved by Dhem et al. [8]. Koeune and Quisquater [15] adapted timing attacks to the symmetric cipher AES. In 1999 Kocher, Jaﬀe and Jun [14] presented a successful side channel attack based on the power consumption of a smartcard.

This work was partially supported by a grant from Intel Corporation, Portland.

### L. Breveglieri et al. (Eds.): FDTC 2006, LNCS 4236, pp. 106–120, 2006. c Springer-Verlag Berlin Heidelberg 2006

<!-- PDF_PAGE: 2 -->

## PDF page 2

Fault Based Collision Attacks on AES 107

In this paper we focus on so called fault attacks on the advanced encryption standard AES [7]. Boneh, DeMillo and Lipton [4] showed that faults induced into the encryption process of asymmetric ciphers can reveal the secret key. Biham and Shamir [1] combined fault attacks with the concept of diﬀerentials and mounted a diﬀerential fault attack (DFA) on DES. Skorobogatov and Anderson showed in [20] that fault attacks are realizable with suﬃcient precision in practice. See Blömer and Seifert [3] for an overview of the physics of inducing faults. There are several fault attacks on AES reported in the literature. The ﬁrst attacks were due to Blömer and Seifert [3] followed by improved attacks of Dusart, Letourneux and Vivolo [9], Giraud [10], Chen and Yen [6] and Piret and Quisquater [17]. All these publications demonstrate the power of fault at- tacks. However, these attacks either use the fault model of bit resets [3] in which case they do not need the faulty ciphertexts. Or the attacks only require the fault model of bit ﬂips, in which case, however, the attacks need the faulty ciphertexts [9],[10],[6],[17]. The attacks presented in this paper use bit ﬂips and, instead of faulty ciphertexts, the attacks only use so called collision information. This turns out to be a much weaker requirement than the requirement that an attacker gets complete faulty ciphertexts. To obtain our new attacks, we show how to combine fault attacks with so called collision attacks. In a collision attack the adversary tries to detect identical intermediate results during the encryption of diﬀerent plaintexts, e.g., by using side channel information, and use this information to derive the secret key. Basically this idea was due to Dobbertin. Schramm et al. developed collision attacks against DES [19] and AES [18] and showed how to detect collisions using power traces. We combine the concepts of fault and collision attacks by inducing faults to generate collisions. This approach allows to relax the requirement of getting faulty ciphertexts to the requirement of detecting collisions in the encryption process. First we explain the basic idea underlying our attacks by presenting an attack based on some rather strong assumptions. Then we present an attack utilizing the same basic ideas that successfully attacks a smartcard that is pro- tected by a memory encryption mechanism. To the best of our knowledge, this is the ﬁrst fault attack on smartcards protected by memory encryption. To defend against side channel attacks the manufacturer invented several countermeasures. One type of countermeasure is intended to protect the card, e.g., shields, sensors or error detection. Another type is designed to render side channel attacks useless using techniques to obfuscate the side channel informa- tion, e.g. by random masking [16],[11],[2]. Yet another more eﬃcient approach is to use a so called memory encryption mechanism (MEMO). Memory encryption mechanisms encrypt an intermediate result directly after it leaves the processor and decrypts data right before it enters the processor (see Figure 1). This guaran- tees that all data stored in the RAM is encrypted. The intention is that memory encryption makes it harder for an adversary to derive information about inter- mediate states of the encryption process by using side channels of the smartcard. In general, it is assumed that unlike the RAM the highly integrated processor is much to complicated to induce faults with some reasonable precision. Hence,

<!-- PDF_PAGE: 3 -->

## PDF page 3

108 J. Blömer and V. Krummel

memory encryption is widely believed to be a useful countermeasure against side channel attacks. Due to the limited computational power of smartcards the MEM has to be very fast. So the manufacturers of smartcards use some light encryption algo- rithms that are very fast but may not be secure against serious cryptanalysis. To increase the impact of the MEM the manufacturer like to keep their algorithms secret. However, many manufacturers do not analyze the impact of MEMs on security but simply present it as an improvement of security. The strategy is to implement as many good looking countermeasures as possible by not exceeding a certain cost threshold. Even a weak countermeasure should increase security. Our attack that works even in the presence of a MEM shows that the security improvement of the MEM as generally used is rather limited. In particular, we present an attack on an AES implementation protected by MEM that determines the full AES-Key by inducing only 285 faults and detecting collisions. The paper is organized as follows. In Section 2 we present our model for analyz- ing fault based collision attacks. In Section 3 we describe some fault based collision attacks and analyze their complexity. Unlike the classical fault attacks using bit ﬂips in [9],[10],[6] and [17] obtaining faulty ciphertexts is not essential for our at- tacks. Therefore our attacks are applicable in scenarios where classical fault attacks do not work. On the other hand, our new attacks need more faults than the classical fault attacks. We explain the basic idea in our ﬁrst attack. This attack is our basic attack and is based on rather strong assumptions. However, in the sequel we show how to strengthen it and how to adapt it to several other scenarios. The second attack we present is is our strongest attack. This attack shows how to successfully attack a smartcard that is protected by a MEM. To the best of our knowledge this is the ﬁrst successful attack against a smartcard protected by a MEM.

111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 ROM 111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 EEPROM 111111111111111111111111111111111111 000000000000000000000000000000000000 key 111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 Processor 111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 111111111111111111111111111111111111 000000000000000000000000000000000000 RAM

MEM

protected against faults

encrypted

Fig. 1. Model of an enhanced smartcard with memory encryption mechanism (MEM)

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 3]

2 Model

In our scenario we have a smartcard with an implementation of AES and a secret AES key K stored on it. We simplify the real world by assuming that only the RAM may leak some information and all other parts are well protected. An adversary

<!-- PDF_PAGE: 4 -->

## PDF page 4

Fault Based Collision Attacks on AES 109

A is able to input chosen plaintexts and induce faults in terms of bit ﬂips into the RAM in order to derive some information about the secret key K. To be more precise, A can ﬂip a single bit of some speciﬁed byte in the memory and derive so called collision information about an internal state of the encryption process. We regard the AES encryption as a bijective function AES K that maps a plaintext p on a ciphertext depending on the secret key K = (k 0 , . . . , k 15 ) 1 . To model faults mathematically we extend that function with a second variable b that speciﬁes a bit position during the computation of AES K . The set of all realizable functions via AES is extended by ﬂipping bit b during the computation of AES K . However, the extended function FAES K (p, b) is not bijective. So there exist collisions such that two intermediate states of computa- tions of FAES K (p, b) and FAES K (p , b ) with diﬀerent inputs (p, b) = (p , b ) are equal. An attacker wants to detect those collisions and then use them to derive the secret key K. We state three assumptions. First, A is able to feed chosen 2 plaintexts into the encryption algorithm. Second, A is able to induce faults in terms of bit ﬂips into a speciﬁc bit of the RAM. Our third assumption is that A is able to derive some information about an intermediate state of the encryption process. However, we do not assume that this information lets A determine (parts of) the secret key directly. Nevertheless it enables A to detect if a collision occurred or not. We call any kind of information that lets A detect collisions collision information of some intermediate state of FAES K (p, b). Later we will show examples how to derive collision information. We model collision information as the evaluation of an injective function f K that depends on the concrete implementation of AES K and the secret key K. It gets as input a plaintext p, the time t when a bit ﬂip occurs, the byte posi- tion x and the bit position b inside that byte. The output is some information f K (p, t, x, b) about an intermediate state of the encryption. Certainly it is also possible to derive the collision information without inducing a fault. Depending on the purpose of the smartcard f K can have diﬀerent realizations. Given the ciphertexts the detection of collisions is easy because the equality of ciphertexts implies equality of intermediate states. However, in many cases the output of an encryption is not available to the attacker. For example, if the smartcard computes a CBC-MAC or a hash value using AES as a building block f K (p, b) can simply be the MAC / hash value. Remember that the MAC is the ﬁnal result of a number of interlinked AES encryptions and not the result of a single AES encryption. The ﬁnal ciphertext could also be used as collision infor- mation if the smartcard computes multiple encryption with diﬀerent encryption algorithms. Finally, if the smartcard computes a single encryption but does not output faulty ciphertexts, f K could be the measurement of some side channel information, e.g., power consumption proﬁle, that allows to detect collisions.

1

For simplicity we only consider AES-128. However, all the attacks in this paper can easily be adapted to AES with larger key sizes. 2 The attacks presented in this paper can also be transformed to known plaintext attacks.

<!-- PDF_PAGE: 5 -->

## PDF page 5

110 J. Blömer and V. Krummel

To analyze the cost of an attack we simply count the number of faults we have to induce. The evaluation of f K without inducing a fault is for free. We also neglect the complexity of additional computations that can be performed oﬄine since in our cases they are obviously easy.

3 New Fault Attacks

### 3.1 Notation

(r),(o)

to be the ith byte of the encryption For simplicity and clarity we deﬁne p i state of plaintext p after the operation o of round r. The operation o is one of the following:

B SubBytes R ShiftRows C MixColumns K AddRoundkey

(3),(R)

For example, p 5 is the 5th byte of the encryption state of plaintext p after the ShiftRows operation of round 3. The ith byte of the round key of round r is (r) called k i . We denote the transformation of SubBytes applied on a single byte x of the state simply as the application of the sbox on x and write it as S[x]. To simplify notation we deﬁne Δ(p i , q i ) = p i + q i to be the diﬀerence of two (0) (0) plaintext bytes p i and q i . Then Δ in (p i , q i ) = (p i + k i ) + (q i + k i ) = p i + q i is the input diﬀerence of (p i , q i ) before the ﬁrst application of the sbox and (0) (0) Δ out (p i , q i ) = (S[p i + k i ] + S[p i + k i ]) is the output diﬀerence of (p i , q i ) after the ﬁrst application of the sbox. To simplify notation further we denote the collision information of encrypting plaintext p and inducing a bit ﬂip into bit e of byte 0 of the state after the application of SubBytes in round 1 by (1),(B) , e). We denote the evaluation of f K without inducing a fault in the f K (p 0 (1),(B) , −). From the context it will always be clear encryption process by f K (p 0 which plaintext is meant.

### 3.2 Scenarios

Below we describe some attacks that are based on the detection of collisions. For simplicity, we only show how to compute byte 0 of the secret key. Similar approaches can be used to compute the other key bytes. We describe how to mount and analyze each attack in diﬀerent scenarios. Each scenario is characterized by abilities of the adversary and/or the environment. The ﬁrst characteristic deﬁnes the precision of the fault induction. We look at the two cases that the adversary is able to ﬂip a speciﬁc bit of an intermediate state and that each possible bit ﬂip occurs with probability 1/8. The second characteristic speciﬁes whether the smart card is protected by a MEM (memory encryption mechanism) or not. The MEM encrypts every in- termediate result that leaves the processor and decrypts a value right before it enters the processor (see Figure 1). Since a smart card has only restricted

<!-- PDF_PAGE: 6 -->

## PDF page 6

Fault Based Collision Attacks on AES 111

computational power and memory most manufacturers choose a byte oriented encryption function with a ﬁxed key that is used for encryption and decryption. In our approach we simply model the memory encryption as an unknown but ﬁxed function h : {0, 1} 8 → {0, 1} 8 . That means that we do not rely on a weak- ness in the memory encryption itself. In particular, we do not assume to have any information of how bit ﬂips eﬀect further processing of that byte. The last characteristic deﬁnes whether collision information remains valid for a long period of time or not. If collision information does not remain valid there is no reason for A to store collision information since he cannot use it later in the attack. A is only able to compare collision information of two recently taken measurements and store the result. This eﬀect could be caused by environments that are frequently changed such that collision information taken at diﬀerent times is hardly comparable, e.g., due to some countermeasure that induces noise into the collision information. If, however, collision information remains valid over the time segment used for the attack it maybe useful for A to store this information in a preprocessing step to have it available once and for all. As we will see later stored information is useful as it helps to reduce the number of faults.

### 3.3 First Attack

First, we describe the scenario in which the attack takes place. We assume that A can ﬂip a speciﬁc bit e of the intermediate state p (1),(B) . We also assume that collision information remains valid over the time span of the attack. Finally, we assume that the smartcard is not protected by a MEM. In a preprocessing step the adversary computes an array T e of length 256. In position T e [y], y ∈ {0, . . . , 255} the array stores the following information: T e [y] := {s, t} s + t = y, S[s] + S[t] = 2 e ,

i.e., T e [y] stores all (unordered) pairs of bytes with Δ in (s, t) = y and Δ out (s, t) = S[s] + S[t] = 2 e . Furthermore, by C e [y] denote the union of sets in T e [y]. The sets C e [y] are pairwise disjoint. As it turns out, for every e ∈ {0, 1, . . . , 7} we have that 129 sets C e [y] are empty, 126 sets C e [y] contain exactly two elements, and one set C e [y] contains exactly four elements. (1)(B) Next, A collects a set T of collision information f K (p 0 , −) for all 256 diﬀerent values of p 0 and arbitrary but ﬁxed p 1 , . . . , p 15 . Then A chooses an arbitrary value q 0 and encrypts the corresponding plaintext ﬂipping an arbitrary (1),(B) (1),(B) (1),(B) bit e of q 0 . If f K has the property that f K (p 0 , −) = f K (q 0 , e) A is able to ﬁnd the corresponding plaintext p 0 satisfying S[p 0 + k 0 ] = S[q 0 + k 0 ] + 2 e by comparing the collision information with the elements of T . Given the pair p 0 , q 0 the adversary knows the diﬀerence p 0 + k 0 + q 0 + k 0 = p 0 + q 0 . Using array T e the adversary A now concludes {p 0 + k 0 , q 0 + k 0 } ∈ T e [p 0 + q 0 ]. Hence, A knows that the correct key byte k 0 satisﬁes (1) k 0 ∈ p 0 + s s ∈ C e [p 0 + q 0 ] .

<!-- PDF_PAGE: 7 -->

## PDF page 7

112 J. Blömer and V. Krummel

As mentioned above, C e [y] ≤ 4 for all y, and C e [y] = 2 for all but one y. Hence, at this point A has reduced the number of possible values for key byte k 0 to at most 4. Next, the adversary repeats the experiment described above with some value q 0 , such that q 0 + s ∈ C e [p 0 + q 0 ] for all s ∈ {p 0 + s̄ s̄ ∈ C e [p 0 + q 0 ]}. Using the collision information in set T , the adversary determines p 0 such that S[p 0 +k 0 ] = S[q 0 + k 0 ] + 2 e . As before A concludes that the key byte k 0 satisﬁes k 0 ∈ p 0 + s s ∈ C e [p 0 + q 0 ] . (2)

that By choice of q 0 , the adversary A is guaranteed p 0 + q 0 = p 0 + q 0 . By elementary arithmetic it follows that if C e [p 0 + q 0 ] = C e [p 0 + q 0 ] = 2, then (1) and (2) uniquely determine the key byte k 0 . As it turns out, the same is true if one of the sets has size four. However, to verify this, one has to perform a tedious case analysis based on the exact structure of the arrays T e . We omit this in this extended abstract.

Cost Analysis To determine a single AES key byte A has to induce two faults. Thus 32 faults are enough to determine the full 128-bit AES key.

### 3.4 Second Attack

The scenario for this attack is as follows. We assume that A can ﬂip a speciﬁc bit e of the intermediate state p (0),(K) . We also assume that collision information remains valid over the time span of the attack. Finally, we assume that the smartcard is protected by a MEM modelled as a function h : {0, 1} 8 → {0, 1} 8 . This implies that after a ﬂip of bit e the encryption continues using the value h −1 (h(p i + k i ) + 2 e ) instead of p i + k i . Therefore, we assume that we have no information about the impact of bit ﬂips on the encryption process. The attack is divided into two steps. In the ﬁrst step A collects the necessary information to compute a function g 0 that is equal to h up to some constant coeﬃcient. To do so A selects a set S of 256 plaintexts p that take on all diﬀerent values in byte p 0 and that are equal in each other byte. A uses the smartcard to derive the collision information for each of these plaintexts by evaluating (0)(K) ), −) and stores it in the table T . Then A encrypts plaintexts p of f K (h(p 0 (0),(K) the set S and induces a bit fault into bit 0 ≤ e ≤ 7 of h(p 0 ) and compares (0),(K) ), e) with the entries of table T to ﬁnd the the collision information f K (h(p 0 corresponding plaintext p 0 . So A knows the diﬀerence

h(p 0 + k 0 ) + h(p 0 + k 0 ) = 2 e

and stores the triple (p 0 , p 0 , e) in a diﬀerence table DT . This step is repeated for diﬀerent plaintexts p and for diﬀerent faulty bit positions until A has enough information to compute the diﬀerences

h(p 0 + k 0 ) + h(p 0 + k 0 )

of one byte p 0 with all other bytes p 0 . The details are given in the following lemma.

<!-- PDF_PAGE: 8 -->

## PDF page 8

Fault Based Collision Attacks on AES 113

Lemma 1. Let m : {0, 1} q → {0, 1} q be an unknown function deﬁned over F 2 q . There exists a set D of 2 q − 1 pairs (u, v) ∈ F 2 q × F 2 q with the following property: If for all (u, v) ∈ D we have that m(u) + m(v) = 2 e for some known e ∈ {0, . . . , q − 1}, then one can determine a function g such that g + c = m for some constant c ∈ F 2 q .

Proof. Given some set D ⊆ F 2 q × F 2 q we construct a graph G whose set of vertices is F 2 q as follows. We connect two vertices u, v with an edge of weight e if (u, v) ∈ D. If in G there exists a path between two vertices x, y then the diﬀerence m(x)+ m(y) is determined by the diﬀerences of pairs in D. Furthermore, if the graph G is connected we can compute the diﬀerence m(x)+m(y) for all (x, y) ∈ F 2 q ×F 2 q . In particular, we can determine all diﬀerences of the form m(u) + m(u 0 ) for an arbitrary but ﬁxed input u 0 . Then using Lagrange interpolation we can now compute the function g(u) = m(u) + m(u 0 ). Setting c := m(u 0 ) proves the lemma. Next we describe a set D of pairs (u, v) with known diﬀerences m(u)+ m(v) = 2 e , such that the graph G as deﬁned above is in fact connected. First we ﬁx an arbitrary e 1 ∈ {0, . . . , q − 1}. Then there exists a set D 1 of 2 q−1 distinct pairs (u, v) ∈ F 2 q × F 2 q such that m(u) + m(v) = 2 e 1 . All pairs in D 1 will be elements of D. If we consider the graph whose edges are deﬁned by pairs in D 1 we get a graph G 1 on the vertex set F 2 q that consists of 2 q−1 connected components each consisting of exactly 2 vertices. Next we choose e 2 = e 1 . Then there exists a set D 2 of 2 q−2 pairs of vertices (u, v) with m(u) + m(v) = 2 e 2 such that each pair in D 2 connects diﬀerent connected components of G 1 . We call the resulting graph G 2 . The set D will also contain all elements from D 2 . Continuing in this way with all possible e i ∈ {0, . . . , q − 1} we get sets of pairs D 1 , D 2 . . . , D q and graphs G 1 , G 2 , . . . , G q such that G i has 2 q−i connected components. In particular, q G q is connected. Moreover, the edges of G q are given by the pairs in D := i=1 D i . The size of D is 2 q − 1. This proves the lemma.

We want to apply Lemma 1 to the function h(x + k 0 ). It is easy to see that A can compute exactly the set of diﬀerences D described in the proof of Lemma 1 since he is able to ﬂip a speciﬁc bit. Hence, knowing D the adversary A can compute a function g 0 : {0, 1} 8 → {0, 1} 8 such that for all x ∈ F 256 the diﬀerence g 0 (x)+ h(x+ k 0 ) is some constant c 0 ∈ F 256 . Since A does not know the constant c 0 he does not get any information about the key byte k 0 at this point. A continues by computing for all other byte positions i a function g 1 , . . . , g 15 such that for all x ∈ F 256 the function g i : {0, 1} 8 → {0, 1} 8 has the property that g i (x) + h(x + k i ) = c i for some unknown constant c i ∈ F 256 . Each of the g i ’s does not reveal any information about the involved key byte k i because the constant c i can take on all possible values and is unknown to A. To derive information about the key A proceeds as follows. He guesses two k i for the keybytes k 0 , k i , respectively. To test this hypothesis on candidates k 0 , the key A selects several bytes x uniformly at random and computes

<!-- PDF_PAGE: 9 -->

## PDF page 9

114 J. Blömer and V. Krummel

g 0 (x + k 0 ) = h(x + k 0 + k 0 ) + c 0

and

k i ) = h(x + k i + k i ) + c i . g i (x +

Depending on the hypothesis ( k 0 , k i ) the diﬀerence t 0,i := g 0 (x + k 0 ) + g i (x + k i ) computes to

(3)

0 + k 0 = k i + k i h(x) + c 0 + h(x) + c i = c 0 + c i ,if k 0 + k 0 ) + c 0 + h(x + k i + k i ) + c i ,if k 0 = k 0 and k i = k i h(x + k h(x) + c 0 + h(x + k i + k i ) + c i ,if k 0 = k 0 and k i = k i

(4)

(5)

h(x + k 0 + k 0 ) + c 0 + h(x) + c i ,if k 0 = k 0 and k i = k i

(6)

Now we assume that the function h has the following property. There do not exist constants a, c ∈ F 256 such that h(x) + a = h(x + c) for all x. Note that this assumption does not restrict the choice of h for two reasons. First, a function used for memory encryption that does not have this property contains too much structure and is probably easier to attack. Secondly, most functions have this property. In fact, a random function has the property with probability at least 1 − 2 −127 . This assumption implies that unlike in case (3) in cases (4),(5),(6) the diﬀer- 0 , k i was correct that is k 0 = k 0 ence t 0,i is not constant. Moreover, if the guess k and k i = k i then A will always be in case (3). Now A can easily test the hypothe- sis ( k 0 , k 1 ) by computing t 0,i for several bytes x. If t 0,i varies for several diﬀerent 0 , k 1 ) cannot x then A knows that he is not in case (3). It follows that the pair ( k be correct. On the other hand if t 0,i remains constant A concludes to be in case (3) and keeps the pair ( k 0 , k 1 ) as a potentially correct candidate. 0 the adversary A obtains a This implies that for every possible key byte k k 0 the single candidate k i for 1 ≤ i ≤ 15 that fulﬁlls condition (3). Guessing 1 , . . . , k 15 ) composed of unique candidates adversary A can compute a vector ( k k i that only depend on k 0 . To uniquely determine the correct key A simply mounts an exhaustive search attack on the 256 possible values of k 0 .

Cost Analysis. A has to induce 255 faults to compute a function g i according to Lemma 1. To test a hypothesis of the key A does not need to induce faults. So the overall number of faults is 16 · 255 = 4080.

Improvement. The previous attack can be improved with respect to the number of induced faults as shown below. In the ﬁrst step A computes the function g 0 such that g 0 (x) = h(x + k 0 ) + c 0 , where c 0 ∈ F 256 is unknown, as above. To determine the other functions g 1 , . . . , g 15 A uses the fact that each g i is related to g 0 by the following equation

g i (x) = h(x + k i ) + c i = g 0 (x + k i + k 0 ) + c i + c 0 .

s i

<!-- PDF_PAGE: 10 -->

## PDF page 10

Fault Based Collision Attacks on AES 115

So knowing g 0 (determined as above) A computes a list of all 256 functions g 0,s := g 0 (x + s), s ∈ F 256 . To determine which of these functions equals g i (0),(K) the adversary A chooses arbitrary p i , q i and evaluates f K (h(p i ), −) and (0),(K) f K (h(q i ), e) at byte position i. Using this information A computes some diﬀerences g i (p i ) + g i (q i ) as described in the computation of g 0 above. To determine the correct function g i = g 0,s i A simply checks which of the function g 0,s fulﬁlls these diﬀerences simultaneously until only one function re- mains. See below for the required number of experiments. Then A knows the sum s i = k 0 + k i of two AES key bytes. A repeats this procedure for all other byte positions 0 ≤ i ≤ 15. As before guessing k 0 the adversary A can determine k 1 , . . . , k 15 ) with ﬁxed a unique candidate k i . That means that A has a vector ( candidates k i for each of the 256 candidates k 0 . Like in the original version of this attack this reduces the set of possible AES keys to only 256 candidates. An exhaustive search reveals the full AES key.

Cost Analysis. To compute g 0 the adversary A has to induce 255 faults like in the original version. To determine further g i ’s A has to collect a set of diﬀerences g i (p)+ g i (q) that is fullﬁlled by only one of the 256 functions g 0,s simultaneously. Notice that if the function g 0,s fulﬁlls a diﬀerence, i.e., g 0 (p + s) + g 0 (q + s) = g i (p) + g i (q) then because of symmetry the function g 0,s given by s := p + q + s also fulﬁlls this diﬀerence since

g 0 (p + (p + q + s)) + g 0 (q + (p + q + s) = g 0 (q + s) + g 0 (p + s) = g i (q) + g i (p).

Assuming that the 256 functions g 0,s behave like random permutations (except for the symmetry) we expect that A needs 2 diﬀerences to uniquely identify the correct one with high probability. We tested this assumption by various experiments and in our experiments it proved to be correct. Hence, we expect that A needs 255 + 15 · 2 = 285 faults to determine the full AES key. As mentioned before we do not consider the complexity of the oﬄine calculations like Lagrange interpolation etc. since all these calculations are easy to perform.

### 3.5 Third Attack

First, we describe the scenario in which the attack takes place. We assume that A can ﬂip a speciﬁc bit e of the intermediate state p (1),(B) . We do not assume that collision information remains valid over the time span of the attack. Hence, A is only able to compare collision information of two recently obtained measurements. Finally, we assume that the smartcard is not protected by a MEM. Because it is always clear from the context we simplify notation by identifying elements of F 256 with their canonical representation as elements of the set {0, . . . , 255}. As a basis for his attack A ﬁxes some input diﬀerence Δ in and output dif- ference Δ out of the application of the sbox in round 1. To be able to detect collisions with a single bit ﬂip we restrict Δ out to be a power of 2. The analysis of the sbox shows that there are a lot of suitable values for Δ in and Δ out (see technical analysis in the full version of the paper). E.g. A chooses Δ in = 10 and Δ out = 4. Only the two pairs

<!-- PDF_PAGE: 11 -->

## PDF page 11

116 J. Blömer and V. Krummel

Z 1 := (p 0 + k 0 = 0, q 0 + k 0 = 10)

and

Z 2 := (p 0 + k 0 = 244, q 0 + k 0 = 254)

together with their commuted counterparts fulﬁll the chosen requirements. A (1),(B) fault that is induced into bit 2 of q 0 after the application of the sbox results in a collision for one of these pairs. In order to detect such a collision the collision information f K should have the property that

(1),(B)

f K (p 0

(1),(B)

, −) = f K (q 0

, 2).

If A ﬁnds such a collision he can conclude that the key byte k 0 is an element of the set K = {p 0 + 0, p 0 + 10, p 0 + 244, p 0 + 254}

More precisely, the attack using f K with the property deﬁned above works as follows. First, the adversary A generates all 128 pairs of plaintexts (p, q) (without symmetry) that have diﬀerence 10 in byte 0 (p 0 = q 0 + 10) and are equal in the other bytes, i.e., 10, if i=0 Δ(p i , q i ) = 0, otherwise

A knows that exactly two of these pairs have output diﬀerence 4 in byte 0. The input diﬀerence of the sbox is the same as the diﬀerence of p 0 and q 0 since AddRoundKey does not change it. A checks all 128 pairs (p, q) until

(1),(B)

f K (p 0

, −) = f K (q 0

(1),(B)

, 2).

Taking the symmetry into account it follows that either p 0 +k 0 = 0, p 0 +k 0 = 10, p 0 + k 0 = 244 or p 0 + k 0 = 254. So there are only 4 candidates for k 0 left. A can repeat this attack for all byte positions of the state. This leaves 2 2·16 = 2 32 possible keys. To determine the complete 128-bit AES key A mounts an exhaustive search attack.

Cost Analysis In the ﬁrst step A examines 128 pairs of plaintexts with diﬀerence 10. Two of these pairs result in a collision so the expected number of faults A has to induce is (2/128) −1 = 64. To compute a 128 bit AES key A expects to induce 16 ∗ 64 = 1024 faults and a brute force attack of size 2 32 .

Alternative To determine the correct candidate of the key byte A could also repeat the same procedure as above with another diﬀerence. We assume that f K lets A detect collisions when ﬂipping bit 3, i.e.

f K (p 0

(1),(B)

, −) = f K (q 0

(1),(B)

, 3).

If we look at all pairs at all pairs (p , q ) such that

Δ(p i , q i ) =

5, if i=0 0, otherwise

<!-- PDF_PAGE: 12 -->

## PDF page 12

Fault Based Collision Attacks on AES 117

an analysis of the sbox shows that Z 3 := (p 0 + k 0 = 0, q 0 + k 0 = 5) and Z 4 := (p 0 + k 0 = 122, q 0 + k 0 = 127) are the only pairs with Δ in = 5 and Δ out = 8. Detecting one of these pairs using f K yields again a set of 4 candidates for k 0 . Next, A computes the diﬀerence of plaintexts p 0 and p 0 . The diﬀerence must be one of the diﬀerences listed in Table 1. Since all possible diﬀerences are distinct A can determine p 0 + k 0 and hence k 0 .

Table 1. All possible diﬀerences of p 0 ,p 0

p 0 + k 0 p 0 + k 0 0 10 244 254 0 0 10 244 254 5 15 241 251 5 122 122 112 142 132 127 127 117 139 129

Cost Analysis. Following the cost analysis as above this method determines the correct candidate of each key byte with 1024 faults as in the previous method plus additional 1024 faults.

### 3.6 Fourth Attack

First, we describe the scenario in which the attack takes place. We assume that A can ﬂip a bit of a speciﬁc byte of the intermediate state p (1),(B) . However, he has no control over the bit position. Instead, we assume that all of the 8 possible bit ﬂips occur with the same probability 1/8. We also assume that collision information remains valid over the time span of the attack. Finally, we assume that the smartcard is not protected by a MEM. The attack works as follows. In a ﬁrst step A selects a set S of 256 plaintexts p that take on all diﬀerent values in byte p 0 and are equal in each other byte. (1),(B) A collects the collision information f K (p 0 , −) for all elements of S. Then he chooses an arbitrary q 0 and encrypts the corresponding plaintext inducing a (1),(B) (1),(B) fault into bit e of q 0 . By comparing the collision information f K (q 0 , e) with the collision information collected in the ﬁrst step A can determine the corresponding plaintext p 0 such that S[p 0 + k 0 ] = S[q 0 + k 0 ] + 2 e . Note that e is unknown to A since he does not have any inﬂuence on the bit position. A can k 0 ] + S[q 0 + k 0 ] is a power test all candidates k 0 of k 0 by simply checking if S[p 0 + 0 as a possible key value and discard it of 2. If this condition is true A stores k otherwise. Analysis of the AES sbox shows that after checking all candidates a set of at most 16 candidates will remain. A repeats this procedure with diﬀerent q 0 until only one candidate is left. Using a reﬁned method similar to the attack in Section 3.3 using several diﬀerent q 0 we can determine the correct key.

### 3.7 Fifth Attack

First, we describe the scenario in which the attack takes place. We assume that A can ﬂip a bit of a speciﬁc byte of the intermediate state p (1),(B) . However, he

<!-- PDF_PAGE: 13 -->

## PDF page 13

118 J. Blömer and V. Krummel

has no control over the bit position. Instead, we assume that all of the 8 possible bit ﬂips occur with the same probability 1/8. We do not assume that collision information remains valid over the time span of the attack. Hence, A is only able to compare collision information of two recently obtained measurements. Finally, we assume that the smartcard is not protected by a MEM. A chooses Δ in of the sbox in round 1 in such a way that the number of pairs that have diﬀerence Δ in and output diﬀerence with Hamming weight 1 is maximal. This choice reduces the number of faults A has to induce as we will see later. Analysis of the sbox shows that Δ in = 216 is the best choice since 8 is the maximum number of pairs that fulﬁll the requirements. (1)(B) A single bit ﬂip induced into q 0 may produce a collision if and only if p 0 + k 0 is one of the following values:

0, 2, 8, 28, 29, 41, 111, 117, 173, 183, 196, 197, 208, 216, 218, 241.

To detect the collision f K should have the property that

(1)(B)

f K (p 0

, −) = f K (q 0

(1)(B)

, b)

(7)

A collision implies that k 0 is an element of the set of 16 candidates

K = { p 0 , p 0 + 2, p 0 + 8, p 0 + 28, p 0 + 29, p 0 + 41, p 0 + 111, p 0 + 117, p 0 + 173,

p 0 + 183, p 0 + 196, p 0 + 197, p 0 + 208, p 0 + 216, p 0 + 218, p 0 + 241}.

To determine p 0 the adversary A ﬁrst builds a list of all 128 pairs (p 0 , q 0 ) of plaintexts with diﬀerence 216 in byte 0 and diﬀerence 0 in all other bytes. Then A (1)(B) , b) of the corresponding plaintext and selects an arbitrary q 0 , derives f K (q 0 (1)(B) , −) of the corresponding compares it with the collision information f K (p 0 plaintext of p 0 . A repeats this procedure until he detects a collision. At his point A knows that k 0 is an element of the set K. To identify the correct candidate A could start an exhaustive search or repeat the procedure with a diﬀerent combination of input and output diﬀerences. For example A chooses input diﬀerence 4 and output diﬀerence 32. Since (88, 92) is the only such pair A can use f K as a special case of (7) having the property

(1)(B)

f K (p 0

, −) = f K (q 0

(1)(B)

, 5)

to test each candidate k 0 ∈ K of k 0 . To check whether a candidate k 0 ∈ K is equal to k 0 , A derives the collision (1)(B) (1)(B) 0 + 92 and q 0 = k 0 + 88. information f K (p 0 , −) and f K (q 0 , b) for p 0 = k Since (92, 88) is the only pair with input diﬀerence 4 and Hamming weight of the k 0 = k 0 the output diﬀerence 1 A can check his hypothesis k 0 . More precisely if Hamming weight of the output diﬀerence will always be greater than 1 except for (0)(K) (0)(K) the case that p 0 = 88 and q 0 = 92. But this case implies that k 0 +4 = k 0 which is impossible since every diﬀerence of two of the sixteen candidates is diﬀerent from 4. So a wrong hypothesis cannot create a collision. On the other k 0 + k 0 = 92 and q + k 0 = 88 + k 0 + k 0 = 88 hand if k 0 = k 0 then p + k 0 = 92 + is the demanded pair and A will detect a collision using f K .

<!-- PDF_PAGE: 14 -->

## PDF page 14

Fault Based Collision Attacks on AES 119

Cost Analysis. The success probability of ﬁnding one of the 8 pairs in part one 8 1 of the attack choosing p 0 uniformly at random is 128 · 18 = 128 . Hence 128 is the expected number of faults A has to induce. The success probability in the second step is (1/8) · (1/16) = 1/128. So we expect that A needs additional 128 faults. Hence the total number of faults to determine a key byte is 2 · 128 = 256. To compute a complete 128 bit AES key we expect that A needs 16·256 = 4096 faults.

4 Concluding Remarks

In this paper we introduced the concept of fault based collision attacks that is a combination of collision attacks with fault attacks. We also showed how to mount fault based collision attacks on AES. Thereby we considered so called memory encryption mechanisms (MEM), a widely used countermeasure to protect against side channel attacks. We showed that using MEM in a straightforward manner does not increase security as much as one would expect. E.g., we presented a fault based collision attack that breaks an implementation protected by a MEM by inducing only about 285 faults. To thwart our attack one has to be more careful. For example using diﬀerent MEM functions for diﬀerent bytes of a state obviously renders our attack useless. An alternative and more general approach is to use a general randomization strategy such as [2] based on [5].

### References

1. Eli Biham and Adi Shamir. Diﬀerential fault analysis of secret key cryptosys- tems. In Burton S. Kaliski Jr., editor, CRYPTO, volume 1294 of Lecture Notes in Computer Science, pages 513–525. Springer, 1997. 2. Johannes Blömer, Jorge Guajardo, and Volker Krummel. Provably secure masking of AES. In H. Handschuh and M. Anwar Hasan, editors, Proceedings Selected Areas in Cryptography (SAC), Lecture Notes in Computer Science Volume 3357, pages 69–83. Springer-Verlag, 2004. 3. Johannes Blömer and Jean-Pierre Seifert. Fault based cryptanalysis of the ad- vanced encryption standard (AES). In Financial Cryptography’03, Lecture Notes in Computer Science Volume 2742, pages 162–181. Springer-Verlag, 2003. 4. Dan Boneh, Richard A. DeMillo, and Richard J. Lipton. On the importance of checking cryptographic protocols for faults (extended abstract). In EUROCRYPT, pages 37–51, 1997. 5. Suresh Chari, Charanjit S. Jutla, Josyula R. Rao, and Pankaj Rohatgi. Towards sound approaches to counteract power-analysis attacks. In Wiener [21], pages 398– 412. 6. Chien-Ning Chen and Sung-Ming Yen. Diﬀerential fault analysis on AES key schedule and some countermeasures. In Reihaneh Safavi-Naini and Jennifer Se- berry, editors, ACISP, volume 2727 of Lecture Notes in Computer Science, pages 118–129. Springer, 2003.

<!-- PDF_PAGE: 15 -->

## PDF page 15

120 J. Blömer and V. Krummel

7. Joan Daemen and Vincent Rijmen. The Design of Rijndael. Information Security and Cryptography. Springer Verlag, 2002. 8. Jean-François Dhem, François Koeune, Philippe-Alexandre Leroux, Patrick Mestré, Jean-Jacques Quisquater, and Jean-Louis Willems. A practical imple- mentation of the timing attack. In Jean-Jacques Quisquater and Bruce Schneier, editors, CARDIS, volume 1820 of Lecture Notes in Computer Science, pages 167– 182. Springer, 1998. 9. Pierre Dusart, Gilles Letourneux, and Olivier Vivolo. Diﬀerential fault analysis on A.E.S. In Jianying Zhou, Moti Yung, and Yongfei Han, editors, ACNS, volume 2846 of Lecture Notes in Computer Science, pages 293–306. Springer, 2003. 10. Christophe Giraud. DFA on AES. In Hans Dobbertin, Vincent Rijmen, and Alek- sandra Sowa, editors, AES Conference, volume 3373 of Lecture Notes in Computer Science, pages 27–41. Springer, 2004. 11. Jovan Dj. Golic and Christophe Tymen. Multiplicative masking and power analysis of AES. In Kaliski Jr. et al. [12], pages 198–212. 12. Burton S. Kaliski Jr., Çetin Kaya Koç, and Christof Paar, editors. Cryptographic Hardware and Embedded Systems - CHES 2002, 4th International Workshop, Red- wood Shores, CA, USA, August 13-15, 2002, Revised Papers, volume 2523 of Lec- ture Notes in Computer Science. Springer, 2003. 13. Paul C. Kocher. Timing attacks on implementations of Diﬃe-Hellman, RSA, DSS, and other systems. In Neal Koblitz, editor, CRYPTO, volume 1109 of Lecture Notes in Computer Science, pages 104–113. Springer, 1996. 14. Paul C. Kocher, Joshua Jaﬀe, and Benjamin Jun. Diﬀerential power analysis. In Wiener [21], pages 388–397. 15. François Koeune and Jean-Jacques Quisquater and. A timing attack against Rijn- dael. Technical Report CG-1999/1, Université Catholique de Louvain, 1999. 16. Thomas S. Messerges. Securing the AES ﬁnalists against power analysis attacks. In Bruce Schneier, editor, FSE, volume 1978 of Lecture Notes in Computer Science, pages 150–164. Springer, 2000. 17. Gilles Piret and Jean-Jacques Quisquater. A diﬀerential fault attack technique against SPN structures, with application to the AES and KHAZAD. In Colin D. Walter, Çetin Kaya Koç, and Christof Paar, editors, CHES, volume 2779 of Lecture Notes in Computer Science, pages 77–88. Springer, 2003. 18. Kai Schramm, Gregor Leander, Patrick Felke, and Christof Paar. A collision-attack on AES: Combining side channel- and diﬀerential-attack. In Marc Joye and Jean- Jacques Quisquater, editors, CHES, volume 3156 of Lecture Notes in Computer Science, pages 163–175. Springer, 2004. 19. Kai Schramm, Thomas J. Wollinger, and Christof Paar. A new class of collision attacks and its application to DES. In Thomas Johansson, editor, FSE, volume 2887 of Lecture Notes in Computer Science, pages 206–222. Springer, 2003. 20. Sergei P. Skorobogatov and Ross J. Anderson. Optical fault induction attacks. In Kaliski Jr. et al. [12], pages 2–12. 21. Michael J. Wiener, editor. Advances in Cryptology - CRYPTO ’99, 19th Annual International Cryptology Conference, Santa Barbara, California, USA, August 15- 19, 1999, Proceedings, volume 1666 of Lecture Notes in Computer Science. Springer, 1999.
