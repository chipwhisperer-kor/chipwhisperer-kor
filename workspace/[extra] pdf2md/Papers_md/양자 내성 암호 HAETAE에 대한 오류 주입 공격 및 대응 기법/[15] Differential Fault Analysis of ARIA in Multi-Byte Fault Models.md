# [15] Differential Fault Analysis of ARIA in Multi-Byte Fault Models

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 8
converted_at: "2026-07-26"
source_asset_id: "HAETAE-FIA-REF-15"
derived_asset_id: "HAETAE-FIA-REF-15-MD"
source_path: "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[15] Differential Fault Analysis of ARIA in Multi-Byte Fault Models.pdf"
source_sha256: "8f0e6e2c0fd29272bb1e1d7c4aa81f1561afea7faf6b375f2e9037ee6db1af5f"
pages: 8
bbox_words: 10090
consumed_bbox_words: 10090
numeric_tokens: 2070
consumed_numeric_tokens: 2070
source_blocks: 182
consumed_source_blocks: 182
emitted_blocks: 172
embedded_raster_images: 3
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

The Journal of Systems and Software 85 (2012) 2096– 2103

Contents lists available at SciVerse ScienceDirect

The Journal of Systems and Software

j ourna l ho me page: www.elsevier.com/locate/jss

Differential fault analysis of ARIA in multi-byte fault models

Chong Hee Kim

Information Security Group, ICTEAM Institute, Université catholique de Louvain, Place Sainte Barbe, 2, Louvain-la-Neuve, Belgium

a r t i c l e i n f o

a b s t r a c t

Article history: Received 21 December 2011 Received in revised form 15 March 2012 Accepted 7 April 2012 Available online 20 April 2012

Differential fault analysis exploits faults to ﬁnd secret information stored in a cryptographic device. It utilizes differential information between correct and faulty ciphertexts. We introduce new techniques to improve the previous differential fault analysis of ARIA. ARIA is a general-purpose involutional SPN (substitution permutation network) block cipher and was established as a Korean standard block cipher algorithm in 2004. While the previous method by Li et al. requires 45 faults, our method needs 13 faults to retrieve the 128-bit secret key of ARIA. If access to the decryption oracle is allowed, our method only needs 7 faults. We analyze the characteristics of the diffusion layer of ARIA in detail, which leads us to reduce the number of required faults to ﬁnd the key. © 2012 Elsevier Inc. All rights reserved.

Keywords: Cryptanalysis Security Differential fault analysis Block cipher ARIA

1. Introduction

Reliable computation is one of the main concerns in many devices. Especially faults occurred during the operations cause many problems such as performance deterioration, unreliable output, etc. Hence, a lot of works to minimize, detect, or pre- vent faults have been researched. Nowadays, we can easily ﬁnd cryptographic devices such as smart cards everywhere in our daily lives from banking cards to SIM cards for GSM. These devices are believed to be tamper-resistant. However, if a fault occurs, an adversary may ﬁnd the secret information stored in the device. Therefore, we are challenging a new type of fault problem. More precisely, an adversary can ﬁnd the key of a block cipher using differential information between correct and faulty cipher- texts. This kind of attack is called differential fault analysis (DFA). A block cipher is widely used in many cryptographic applications and has been studied extensively in the literature. Traditional crypt- analysis of block cipher targets a cipher’s design and architecture based on abstract and mathematical approaches. However, in prac- tice a cipher has to be implemented on a real device that is exposed to physical cryptanalysis such as side-channel attacks (Dhem et al., 1998; Kocher et al., 1999; Quisquater and Samyde, 2001) and fault attacks (Bar-El et al., 2004; Kim and Quisquater, 2007). An adversary gets faulty ciphertexts by giving external impact on a device with voltage variation, glitch, laser, etc. (Bar-El et al., 2004). The ﬁrst DFA presented by Biham and Shamir (1997) tar- geted DES (National Institute of Standard and Technology, 1993).

0164-1212/$ – see front matter © 2012 Elsevier Inc. All rights reserved. http://dx.doi.org/10.1016/j.jss.2012.04.009

The ways of exploiting faults to ﬁnd the key are different accord- ing to each algorithm. Therefore, ﬁnding an efﬁcient attack for each algorithm is main stream in the research of DFA. Up to now almost all cryptosystems, for example, Triple-DES (Hemme, 2004), RC4 (Biham et al., 2005; Hoch and Shamir, 2004), CLEFIA (Chen et al., 2007; Takahashi and Fukunaga, 2008), RSA (Coron et al., 2010), ElGamal (Bao et al., 1998), IDEA (Clavier et al., 2008), LUC and Demytko (Bleichenbacher et al., 1997), ECC (Blömer et al., 2005; Ciet and Joye, 2005), AES (Piret and Quisquater, 2003; Moradi et al., 2006; Kim and Quisquater, 2008; Takahashi et al., 2007; Barenghi et al., 2010; Kim, 2010), SMS4 and MacGuf- ﬁn (Li et al., 2009), DSA (Naccache et al., 2005), and ECDSA (Schmidt and Medwed, 2009; Barenghi et al., 2011) have been broken. The research of DFA can be further diversiﬁed into several directions: reducing the number of required faults, applying it to multi-byte fault models, extending to variants, if they exist, or exploring faults induced at an earlier round. In this article, we intro- duce new fault attacks on ARIA based on multi-byte fault models that needs less faults than the previous one. ARIA is a general-purpose involutional SPN (substitution permutation network) block cipher algorithm, optimized for lightweight environments and hardware implementation. The name ARIA was taken from the initials of Academia, Research Insti- tute and Agency, acknowledging the co-operative efforts of Korean researchers in designing ARIA. In 2004, ARIA was established as a Korean standard block cipher algorithm (KS X 1213) by the Ministry of Knowledge Economy (ARIA).

<!-- PDF_PAGE: 2 -->

## PDF page 2

C.H. Kim / The Journal of Systems and Software 85 (2012) 2096– 2103

Fig. 1. State of ARIA.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 2]

Several traditional cryptanalysis (Wu et al., 2007; Li and Song, 2008; Li et al., 2008; Fleischmann et al., 2009) and side-channel analysis of ARIA (Ha et al., 2005; Kim et al., 2008; Park et al., 2007; Yoo et al., 2006) have been proposed. However, there is only one result of DFA of ARIA (Li et al., 2008). While the pre- vious method by Li et al. (2008) requires 45 faults to retrieve the key, our method based on a two-byte fault model needs 13 faults. If access to the decryption oracle is allowed, our method needs 7 faults. Our generalized attack, working with faults corrupting a maximum of 4 bytes, can ﬁnd the key with 21 faults. This article is organized as follows: Section 2 introduces the ARIA algorithm. The next section brieﬂy describes the previous work by Li et al. and explains our new techniques. Section 4 dis- cusses possible countermeasures. Finally Section 5 concludes the article.

2. ARIA algorithm

ARIA is a 128-bit SPN block cipher 1 with 128-bit, 192-bit, or 256-bit key, where the number of rounds is 12, 14, and 16, respectively (ARIA, in press; Kwon et al., 2003). In the sequel, we will use the 128-bit key version of ARIA cipher, unless otherwise stated.

2.1. Structure of ARIA

The 128-bit input block passes through a round function, which is iterated 12 times (see Fig. 2). The intermediate cipher result, called State, can be represented as a two-dimensional byte array i ) at round i is thus with 4 rows and 4 columns. The S i = (S 0 i , . . . , S 15 represented by an array as shown in Fig. 1. The encryption and decryption processes are identical except the use of round keys. Each round consists of the following three parts:

- Round key addition: the State is XORed with a 128-bit subkey. - Substitution layer (SL): the State goes through 16 S-boxes. There are 2 different substitutions, types 1 and 2, which alternate between the rounds. - Diffusion layer (DL): it is a function which maps an input (x 0 , x 1 , . . ., x 15 ) of 16 bytes into an output (y 0 , y 1 , . . ., y 15 ). The mapping can also be considered as a 16 × 16 binary matrix multiplication as follows:

1 ARIA has three versions according to slightly different key expansion methods: V0.8, V0.9 and V1.0. We use the latest standard version, V1.0 (ARIA).

2097

⎛ ⎞ ⎛

⎞ ⎛ ⎞

y 0 0 0 0 1 1 0 1 0 1 1 0 0 0 1 1 0 x 0 ⎜ y 1 ⎟ ⎜ 0 0 1 0 0 1 0 1 1 1 0 0 1 0 0 1 ⎟ ⎜ x 1 ⎟ ⎜ y ⎟ ⎜ 0 1 0 0 1 0 1 0 0 0 1 1 1 0 0 1 ⎟ ⎜ x ⎟ ⎜ 2 ⎟ ⎜ ⎟ ⎜ 2 ⎟ ⎜ y 3 ⎟ ⎜ 1 0 0 0 0 1 0 1 0 0 1 1 0 1 1 0 ⎟ ⎜ x 3 ⎟ ⎜ ⎟ ⎜ ⎟ ⎜ ⎟ ⎜ y 4 ⎟ ⎜ 1 0 1 0 0 1 0 0 1 0 0 1 0 0 1 1 ⎟ ⎜ x 4 ⎟ ⎜ ⎟ ⎜ ⎟ ⎜ ⎟ ⎜ y 5 ⎟ ⎜ 0 1 0 1 1 0 0 0 0 1 1 0 0 0 1 1 ⎟ ⎜ x 5 ⎟ ⎜ y ⎟ ⎜ 1 0 1 0 0 0 0 1 0 1 1 0 1 1 0 0 ⎟ ⎜ x ⎟ ⎜ 6 ⎟ ⎜ ⎟ ⎜ 6 ⎟ ⎜ y 7 ⎟ ⎜ 0 1 0 1 0 0 1 0 1 0 0 1 1 1 0 0 ⎟ ⎜ x 7 ⎟ ⎜ ⎟ = ⎜ ⎟ ⎜ ⎟ ⎜ y 8 ⎟ ⎜ 1 1 0 0 1 0 0 1 0 0 1 0 0 1 0 1 ⎟ ⎜ x 8 ⎟ ⎜ ⎟ ⎜ ⎟ ⎜ ⎟ ⎜ y 9 ⎟ ⎜ 1 1 0 0 0 1 1 0 0 0 0 1 1 0 1 0 ⎟ ⎜ x 9 ⎟ ⎜ y ⎟ ⎜ 0 0 1 1 0 1 1 0 1 0 0 0 0 1 0 1 ⎟ ⎜ x ⎟ ⎜ 10 ⎟ ⎜ ⎟ ⎜ 10 ⎟ ⎜ y 11 ⎟ ⎜ 0 0 1 1 1 0 0 1 0 1 0 0 1 0 1 0 ⎟ ⎜ x 11 ⎟ ⎜ ⎟ ⎜ ⎟ ⎜ ⎟ ⎜ y 12 ⎟ ⎜ 0 1 1 0 0 0 1 1 0 1 0 1 1 0 0 0 ⎟ ⎜ x 12 ⎟ ⎜ ⎟ ⎜ ⎟ ⎜ ⎟ ⎜ y 13 ⎟ ⎜ 1 0 0 1 0 0 1 1 1 0 1 0 0 1 0 0 ⎟ ⎜ x 13 ⎟ ⎝ y ⎠ ⎝ 1 0 0 1 1 1 0 0 0 1 0 1 0 0 1 0 ⎠ ⎝ x ⎠ 14 14 0 1 1 0 1 1 0 0 1 0 1 0 0 0 0 1 y 15 x 15

In the last round, instead of the diffusion layer, there is another key addition.

2.2. Key expansion of ARIA

The ARIA key expansion consists of two parts: initialization and subkey generation. In the initialization part, four 128-bit val- ues, W 0 , W 1 , W 2 , and W 3 , are generated from the master key by using a 3-round Feistel cipher. Then the subkeys are generated by a sequence of XOR, rotate-right and rotate-left operations as follows:

ek 1 = W 0 ⊕ W 1 ≫19 , ek 2 = W 1 ⊕ W 2 ≫19 , ek 3 = W 2 ⊕ W 3 ≫19 ,

ek 4 = W 0 ≫19 ⊕ W 3 , ek 5 = W 0 ⊕ W 1 ≫31 , ek 6 = W 1 ⊕ W 2 ≫31 ,

ek 7 = W 2 ⊕ W 3 ≫31 , ek 8 = W 0 ≫31 ⊕ W 3 , ek 9 = W 0 ⊕ W 1 ≪61 ,

ek 10 = W 1 ⊕ W 2 ≪61 , ek 11 = W 2 ⊕ W 3 ≪61 ,

ek 12 = W 0 ≪61 ⊕ W 3 , ek 13 = W 0 ⊕ W 1 ≪31 .

The subkeys for decryption are derived from the subkeys for encryption as follows:

dk 1 = ek 13 , dk 2 = DL(ek 12 ), . . . , dk 12 = DL(ek 2 ), dk 13 = ek 1 .

2.3. Notations

We use the following notations to describe ARIA. We denote by X ∈ ({0, 1} 8 ) 16 the plaintext and by Y ∈ ({0, 1} 8 ) 16 the ciphertext. The ith subkey is denoted by ek i ∈ ({0, 1} 8 ) 16 , 1 ≤ i ≤ 13. We denote by A i = (a 0,i , a 1,i , a 2,i , . . ., a 15,i ) and B i = (b 0,i , b 1,i , b 2,i , . . ., b 15,i ) the input and the output of the substitution layer at round i, 1 ≤ i ≤ 12, respectively. We denote by C i = (c 0,i , c 1,i , c 2,i , . . ., c 15,i ) the output of the linear layer at round i, 1 ≤ i ≤ 12 (see Fig. 2). We denote by A ∗ i = (a ∗ 0,i , a ∗ 1,i , a ∗ 2,i , . . . , a ∗ 15,i ) and B i ∗ = (b ∗ 0,i , b ∗ 1,i , b ∗ 2,i , . . . , b ∗ 15,i ) the faulty input and output of the substitution layer at round i, 1 ≤ i ≤ 12, respectively. The faulty output of the linear layer at round ∗ , c ∗ , c ∗ , . . . , c ∗ ), 1 ≤ i ≤ 12. i is denoted by C i ∗ = (c 0,i 1,i 2,i 15,i Let A i = (a 0,i , a 1,i , a 2,i , . . ., a 15,i ) be the difference between A i and A ∗ i , 1 ≤ i ≤ 12. We denote by B i and C i the dif- ference between B i and B i ∗ , and C i and C i ∗ , 1 ≤ i ≤ 12, respectively. We denote by SL(A i ) the output of 128-bit substitution layer for the input A i , 1 ≤ i ≤ 12. We denote by SL −1 (B i ) the output of the inversion of 128-bit substitution layer for the input B i , 1 ≤ i ≤ 12. Let DL(B i ) be the output of 128-bit diffusion layer for the input

<!-- PDF_PAGE: 3 -->

## PDF page 3

C.H. Kim / The Journal of Systems and Software 85 (2012) 2096– 2103

2098

Fig. 2. Encryption process of ARIA.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 3]

B i , 1 ≤ i ≤ 12. We denote by DL −1 (C i ) the output of the inversion of 128-bit diffusion layer for the input C i , 1 ≤ i ≤ 12.

3. New differential fault analysis on ARIA

3.1. Previous work

The ARIA diffusion layer propagates one single-byte fault to seven different bytes. That is, a single-byte fault induced before the diffusion layer at round 11 affects seven bytes of the cipher- text. Hence, one fault gives information on seven bytes of a subkey. Li et al. used this property and retrieved one subkey with 11 faulty ciphertexts on average and the master key with 45 faulty cipher- texts on average (Li et al., 2008). They directly applied “the method used to attack AES” in Piret and Quisquater (2003) to ARIA but did not analyze the characteristics of the ARIA diffusion layer that is different from the AES diffusion layer.

3.2. Fault models

We assume that an attacker induces a fault making 2 bytes corrupted (later it is generalized to a maximum of 4 bytes).

The corrupted bytes do not need to be consecutive. It is also assumed that the attacker obtains correct and faulty cipher- texts but does not know which bytes are corrupted. Furthermore, the faulty value is assumed to be random and uniformly dis- tributed. Our fault model is the same as that of Li et al. (2008) except the number of corrupted bytes. Instead of a single byte we assume that multiple bytes are corrupted. The multi-byte fault model has been applied to attack AES (Kim and Quisquater, 2008; Takahashi et al., 2007) and CLEFIA (Takahashi and Fukunaga, 2008; Zhao et al., 2010) and was shown to be practical by experi- ments (Fukunaga and Takahashi, 2009; Saha et al., 2009). In an 8-bit architecture one-byte fault model is desirable. However, depending on implementation, i.e., 16-bit/32-bit architecture or software implementation, multi-byte fault model can be much use- ful. As shown in Table 1, our model is similar to those used to attack AES and CLEFIA. While some models assume that the number of cor- rupted bytes is ﬁxed to 3 or 4 (Kim and Quisquater, 2008; Takahashi et al., 2007; Takahashi and Fukunaga, 2008), the others assume that the number of corrupted bytes is a maximum of 8, 12, or 16 (Saha et al., 2009; Zhao et al., 2010). In Section 3.9, we use a generalized fault model that exploits any fault corrupting one, two, three, or four bytes simultaneously. It is also assumed that the attacker does not know how many bytes are corrupted and where the corrupted bytes are positioned. Nor- mally the number of corrupted bytes varies each time a fault is induced (Saha et al., 2009). Therefore, we have to generate more faulty ciphertexts than expected in a fault model where the num- ber of corrupted bytes is ﬁxed. However, in our generalized fault model, we can exploit any fault corrupting a maximum of four bytes.

3.3. Basic idea

An attacker induces a random fault between C 10 and B 11 , and gets a faulty ciphertext. She obtains several pairs of cor- rect and faulty ciphertexts by repeating it. Then, she ﬁnds the subkey of the last round, ek 13 , (we will describe it in detail in Section 3.4) and computes A 12 from the ciphertext and ek 13 . She induces faults between C 9 and B 10 and gets faulty ciphertexts. And she computes the subkey, ek 12 . She repeats the procedure to the next round until she has enough subkeys to ﬁnd the mas- ter key. In ARIA, she needs at least four subkeys, ek 10 , ek 11 , ek 12 , and ek 13 , as a 3-round Feistel cipher is used in the key expansion. To help the readers understand our attack easily, we assume that 2 corrupted bytes are consecutive. We denote the errors induced on 2 bytes before the diffusion layer by (˛, ˇ). These errors propagate through the diffusion layer as shown in Table 2, where ˛ˇ presents that it is affected by both ˛ and ˇ. For example, let (b 0,i , b 1,i ) be two bytes at round i. Then (c 3,i , c 4,i , c 6,i , c 13,i , c 14,i ) are affected by b 0,i , (c 2,i , c 5,i , c 7,i , c 12,i , c 15,i ) are affected by b 1,i , and (c 8,i , c 9,i ) are affected by both b 0,i and b 1,i . The bytes are exploitable only if they are affected by the same error and the number of affected bytes is at least two. In the previous example, there are 12 exploitable bytes (5 bytes affected by ˛, 5 bytes by ˇ, and 2 bytes by both ˛ and ˇ). Hence, we can get information on 12 bytes of the subkey. However, if (b 3,i , b 4,i ) or (b 11,i , b 12,i ) are corrupted, we can get information on 10 bytes of the subkey. On average information on 11.73 bytes is available. We note that information on 7 bytes is available in the one-byte fault model of Li et al. Note. We note again that our attack still works even when two corrupted bytes are not consecutive. This assumption is just for easy explanation. If they are not, we can ﬁnd the subkeys by

<!-- PDF_PAGE: 4 -->

## PDF page 4

C.H. Kim / The Journal of Systems and Software 85 (2012) 2096– 2103

Table 1 Multi-byte fault models.

Ref.

Target

Kim and Quisquater (2008) Takahashi et al. (2007) Saha et al. (2009) Takahashi and Fukunaga (2008) Zhao et al. (2010)

AES AES AES CLEFIA CLEFIA

This article

ARIA

constructing another propagation tables according to the position of the corrupted bytes.

3.4. Finding the subkey of the last round

An attacker induces a random fault between C 10 and B 11 making two bytes at B 11 corrupted (see Fig. 2). Then she constructs three sets, T, U and V, of the positions of the bytes in A 12 affected by the same error. We denote the size of each set by m T , m U , and m V , respectively. For example, if (b 0,11 , b 1,11 ) are corrupted, T = {3, 4, 6, 13, 14}, U = {2, 5, 7, 12, 15} and V = {8, 9} (see the ﬁrst row of Table 2).

3.4.1. Finding m T + m U + m V bytes of ek 13 An attacker ﬁnds m T + m U + m V bytes of A 12 . Then she ﬁnds m T + m U + m V bytes of ek 13 from the ciphertext and A 12 . The input and output differences of the substitution layer of round 12 satisfy the following equation:

S(a j,12 ) ⊕ S(a j,12 ⊕ a j,12 ) = b j,12 ,

(1)

where 0 ≤ j ≤ 15. As the ciphertexts are known, b j,12 can be com- puted. For group T, (a t 1 ,12 , . . . , a t m ,12 ) can take only 255 values T among 255 m T candidates as all (a t 1 ,12 , . . . , a t m ,12 ) are affected by T the same error. Eq. (1) can be rewritten as follows:

a j,12 = a j,12 ⊕ S −1 (S(a j,12 ) ⊕ b j,12 ).

(2)

By guessing a j,12 , she computes a j,12 for j = t 1 , . . . , t m T and checks whether a t 1 ,12 = a t 2 ,12 = . . . = a t m ,12 . If the equa- T tion is satisﬁed, she adds the guessed a j,12 to the list L T of possible candidates. She repeats this for all possible values of (a t 1 ,12 , . . . , a t m ,12 ). For U and V, she repeats the procedure and T gets L U and L V , respectively. The complexity of computing L T , L U ,

Table 2 Propagation of errors through the diffusion layer when two consecutive bytes are corrupted.

Errors before diff. layer

Propagated errors after diff. layer

˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ

0 0 ˇ ˛ ˛ ˇ ˛ ˇ ˛ˇ ˛ˇ 0 0 ˇ ˛ ˛ ˇ 0 ˇ ˛ 0 ˇ ˛ ˇ ˛ ˛ ˛ ˇ ˇ ˛ˇ 0 0 ˛ˇ ˇ ˛ 0 0 ˛ ˇ ˛ ˇ 0 0 ˛ˇ ˛ˇ ˛ ˇ ˇ ˛ ˛ˇ 0 ˇ 0 0 ˛ˇ 0 ˛ ˇ 0 ˛ ˛ˇ 0 ˛ ˛ˇ ˇ ˛ ˇ ˛ ˇ ˇ ˛ 0 0 ˛ ˇ ˇ ˛ 0 0 ˛ˇ ˛ˇ ˇ ˛ ˇ ˛ ˛ 0 0 ˇ 0 ˛ˇ ˛ˇ 0 ˇ ˇ ˛ ˛ ˛ ˇ ˛ ˇ 0 0 ˇ ˛ ˇ ˛ ˛ ˇ ˛ˇ ˛ˇ 0 0 ˇ ˛ˇ 0 ˛ ˇ 0 ˛ ˇ ˛ 0 ˇ ˛ ˛ ˛ˇ 0 ˇ ˛ˇ ˛ˇ 0 0 ˛ ˇ ˇ ˛ 0 0 ˛ ˇ ˇ ˛ ˇ ˛ ˛ ˛ ˇ ˇ 0 ˛ˇ ˛ˇ 0 ˇ 0 0 ˛ ˛ ˇ ˛ ˇ 0 0 ˛ˇ ˛ˇ ˇ ˛ ˛ ˇ ˛ ˇ 0 0 ˇ ˛ ˇ ˛ 0 ˇ ˛ˇ ˛ ˛ 0 ˇ ˛ˇ 0 ˛ˇ 0 ˇ ˛ˇ 0 ˛ 0 ˇ ˛ ˛ ˇ 0 0 ˛ˇ ˛ˇ ˇ ˛ ˇ ˛ ˛ ˇ 0 0 ˛ˇ 0 0 ˛ˇ ˇ ˇ ˛ ˛ ˛ ˇ ˛ ˇ 0 ˛ ˇ 0 ˛ ˇ ˇ ˛ ˛ˇ ˛ˇ 0 0 ˇ ˛ ˇ ˛ 0 0 ˛ ˇ

2099

Location

# of corrupted bytes

Round n − 1 of key expansion Round n − 1 of key expansion Between rounds n − 3 and n − 2 Round n − 2 Rounds n − 2, n − 1, and n

3 4 1–8, 12, or 16 4 1–8

Rounds n − 4, . . ., n − 1

1–4

or L V is about (2 8 ) m , m =2, 3, 4, or 5. Hence, the maximum com- plexity is 2 40 , which it is impractical. However, we can reduce the complexity by slightly modifying the attack as shown in Algorithm 1.

Find L T

Algorithm 1.

Input: T, b j,12 Output: L T

For each of the 2 16 candidates of (a t 1 ,12 , a t 2 ,12 ): Compute (a t 1 ,12 , a t 2 ,12 ) using Eq. (2). If a t 1 ,12 = a t 2 ,12 , add it to the list L T . For each l ∈ L T , try to extend it by one byte: Remove l from L T . For all 2 8 of a t 3 ,12 : Compute a t 3 ,12 . If a t 1 ,12 = a t 3 ,12 , add the newly extended (l, a t 3 ,12 ) to the list L T . Repeat Step 2 until elements of L T have a length of m T bytes.

Step 1.

Step 2.

Step 3.

The number of candidates in L T after N pairs of cipher- texts have been treated is about 256 m T /(255 m T −1 ) N . With one pair of correct and faulty ciphertexts on average 260 candi- dates remain. With two pairs, we have one candidate on average. The number of candidates in L T in each step of Algorithm 1 is about 2 8 . The complexity of Algorithm 1 is (2 16 ) × 2(m T − 1) and hence, 2 19 when m T = 5. Therefore, it is practical to implement.

3.4.2. Finding all bytes of ek 13 With a pair of correct and faulty ciphertexts we can ﬁnd 260 candidates for 11.73 bytes of A 12 on average. If we have more faulty ciphertexts, we can further reduce the number of candi- dates. Furthermore, we can ﬁnd more bytes of A 12 by changing the position of the faulty bytes. Once A 12 is found, the subkey is computed: ek 13 = SL(A 12 ) ⊕ C 12 . Algorithm 2 shows the procedure in detail.

#

12 12 12 10 12 12 12 12 12 12 12 10 12 12 12

<!-- PDF_PAGE: 5 -->

## PDF page 5

C.H. Kim / The Journal of Systems and Software 85 (2012) 2096– 2103

2100

Algorithm 2. Find ek 13

Output: ek 13

Step 0. Step 1.

Let k = 1. Induce a random fault between C 10 and B 11 making two bytes at B 11 corrupted. Find T k , U k , and V k . Compute the output difference, B 12 . Find L T k , L U k , and L V k using Algorithm 1. Reduce the number of candidates in L T k , L U k and L V k : If k &gt; 1: For each t i k ∈ T k : For each t j n ∈ T n with 1 ≤ n ≤ k − 1:

Step 2. Step 3. Step 4. Step 5.

Check whether t i k = t j n .

If yes, compare the candidates in L T k and L T n for a t k ,12 .

i

If the same candidate does not exist in both L T k and L T n , remove it from the lists. Repeat for U n and V n . Repeat for U k and V k . Construct a set W = T i U i V i for 1 ≤ i ≤ k and a list L W . Increase k by one. Repeat Step 1 to 7 until W has 16 elements and the number of candidates in L W is 1. Compute ek 13 : ek 13 = SL(A 12 ) ⊕ C 12 .

Step 6. Step 7. Step 8.

Step 9.

In Step 2, we can ﬁnd sets of the positions of the bytes in A 12 affected by the same error using Table 2. We know C 12 from a pair of correct and faulty ciphertexts and hence B 12 . However, we do not know A 12 (= C 11 ). If c j,11 is equal to 0, the corre- sponding a j,12 = b j,12 = c j,12 = 0, 0 ≤ j ≤ 15, and vice versa. We call the pattern of zero bytes at C 12 zero pattern. Then with zero pattern in C 12 , we can ﬁnd the position of the corrupted bytes. For example, if (b 0,11 , b 1,11 ) are corrupted at B 11 , we have a zero pattern of (0 0 - - - - - - - - 0 0 - - - -) at C 12 . Four cases have the same zero patterns: (b 0 , b 1 ) and (b 10 , b 11 ), (b 2 , b 3 ) and (b 8 , b 9 ), (b 4 , b 5 ) and (b 14 , b 15 ), and (b 6 , b 7 ) and (b 12 , b 13 ). For example, if C 12 = (0 0 - - - - - - - - 0 0 - - - -), the corrupted bytes are either (b 0 , b 1 ) or (b 10 , b 11 ). If an attacker induces a fault during the ﬁrst half of the operations in the layer, it is (b 0 , b 1 ). If she does during the second half, it is (b 10 , b 11 ). Hence, she can ﬁnd the location of a fault. So can she for the other 3 cases. Step 5 discards impossible candidates. We explain how Step 5 works with an example. We assume that the ﬁrst fault corrupts (b 0,11 , b 1,11 ). Then, T 1 = {3, 4, 6, 13, 14}, U 1 = {2, 5, 7, 12, 15} and V 1 = {8, 9}. After Step 4, L T 1 , L U 1 , and L V 1 have about 260 candidates respectively. We assume that the second fault corrupts (b 4,11 , b 5,11 ). Then T 2 = {0, 2, 5, 8, 11}, U 2 = {1, 3, 4, 9, 10}, and V 2 = {14, 15}. Step 5 ﬁrst ﬁnds elements included in both T 1 and T 2 . As T 1 T 2 = ∅, it compares T 1 and U 2 and T 1 U 2 = {3, 4}. Then, it compares the can- didates in L T 1 and those in L U 2 for a 3,12 and a 4,12 . If a candidate does not belong to both L T 1 and L U 2 simultaneously, it is removed from the lists. It continues the process and T 1 V 2 = {14}, U 1 T 2 = {2, 5}, U 1 U 2 = ∅, U 1 V 2 = {15}, V 1 T 2 = {8}, V 1 U 2 = {9}, and V 1 V 2 = ∅. As two pairs of correct and faulty ciphertexts allow retrieving a unique value, we can ﬁnd a unique candidate for a 3,12 and a 4,12 . We also have one candidate for T 1 U 2 . Hence, we can ﬁnd (a 1,12 , a 3,12 , a 4,12 , a 6,12 , a 9,12 , a 10,12 , a 13,12 , a 14,12 ). Similarly, we have one candidate for (a 0,12 , a 2,12 , a 5,12 , a 7,12 , a 8,12 , a 11,12 , a 12,12 , a 15,12 ) from U 1 and U 2 . Finally, we have W = {0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15} and one candidate in L W . Therefore, Algorithm 2 outputs a single candidate for ek 13 .

3.5. Finding the master key

We describe how to ﬁnd the ARIA master key using the method introduced in Section 3.4. Once we have found ek 13 , we can com- pute A 12 and remove the last round. Then we apply Algorithm 2

Fig. 3. Ratio of faulty ciphertexts to retrieve 1 subkey.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

to ﬁnd ek 12 . We repeat this until we have found 4 subkeys. In summary, we have the following steps:

Step 1.

Find ek 13 : - Induce a random error between C 10 and B 11 and get a pair of correct and faulty ciphertexts. - Get several pairs of correct and faulty ciphertexts by repeating it. - Find A 12 . - Compute ek 13 = SL(A 12 ) ⊕ C 12 , where C 12 = Y . Find ek 12 : - Induce a random error between C 9 and B 10 . - Get several pairs of correct and faulty ciphertexts by repeating it. - Find A 11 . - Compute ek 12 = DL(SL(A 11 )) ⊕ A 12 . Similarly ﬁnd ek 11 and ek 10 . Find the master key using the key expansion with ek 10 , ek 11 , ek 12 , and ek 13 .

Step 3.

Step 4. Step 5.

3.6. Simulation results

We implemented our attack on a PC with a 3.20 GHz Intel and 8 GB memory using Visual C++7.1 Compiler. The fault was simulated by a computer software. We ran the algorithm to 100 encryption units with randomly generated keys. Referring to Fig. 3, the number of required faulty ciphertexts to retrieve 1 subkey changes between 3 and 10 (see “Full recovery” in Fig. 3). Hence, we can retrieve a subkey with 3 faulty ciphertexts in the best case and with 10 faulty ciphertexts in the worst case, respectively. On average 4.98 ciphertexts are required. To recover the master key, we need 20 faulty ciphertexts on average. The com- plexity is about 2 24 ≃ 2 19 × 20. The time to complete the attack was a few seconds.

<!-- PDF_PAGE: 6 -->

## PDF page 6

C.H. Kim / The Journal of Systems and Software 85 (2012) 2096– 2103

Table 3 Propagation of errors through the diffusion layer when three consecutive bytes are corrupted.

Errors before diff. layer

Propagated errors after diff. layer

˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ

2101

#

15 15 11 11 15 15 11 11 15 15 11 11 15 15

0 ˇ ˛ ˛ ˇ ˛ ˇ ˛ˇ ˛ˇ ˇ ˛ ˛ ˇ ˇ ˛ 0 ˇ ˛ ˇ ˛ ˛ ˛ ˇ ˇ ˛ˇ ˛ˇ ˇ ˛ 0 ˛ ˇ ˛ ˇ 0 ˛ˇ ˛ˇ ˛ ˇ ˇ ˛ ˛ˇ ˇ ˛ˇ 0 ˛ ˇ ˛ ˛ˇ 0 ˛ ˛ˇ ˇ ˛ ˇ ˛ ˇ ˇ ˛ 0 ˛ ˇ ˇ ˛ ˛ˇ ˛ˇ ˇ ˛ ˇ ˛ ˛ 0 ˇ ˛ˇ ˛ˇ ˇ ˇ ˛ ˛ ˛ ˇ ˛ ˇ 0 ˇ ˛ ˇ ˛ ˛ ˇ ˛ˇ ˛ˇ 0 ˇ ˛ˇ 0 ˛ ˇ ˛ ˇ ˛ 0 ˇ ˛ ˛ ˛ˇ ˇ ˛ˇ ˛ˇ ˛ ˇ ˇ ˛ 0 ˛ ˇ ˇ ˛ ˇ ˛ ˛ ˛ ˇ ˇ ˛ˇ ˛ˇ ˇ 0 ˛ ˛ ˇ ˛ ˇ 0 ˛ˇ ˛ˇ ˇ ˛ ˛ ˇ ˛ ˇ 0 ˇ ˛ ˇ ˛ ˇ ˛ˇ ˛ ˛ 0 ˇ ˛ˇ ˛ˇ ˇ ˛ˇ ˛ 0 ˇ ˛ ˛ ˇ ˛ˇ ˛ˇ ˇ ˛ ˇ ˛ ˛ ˇ 0 ˛ˇ ˛ˇ ˇ ˇ ˛ ˛ ˛ ˇ ˛ ˇ 0 ˛ ˇ

3.7. Further reducing the number of faults

We need 20 faulty ciphertexts on average to ﬁnd the ARIA 128- bit key. In this section, we describe methods to further reduce the number of required faulty ciphertexts.

3.7.1. Partial search and brute-force attack We may stop searching candidates of the subkey before the number of candidates is equal to one, and ﬁnd the correct key by exhaustively searching the remaining candidates. This is done by changing “the number of candidates in L W is 1” for “the number of candidates in L W ≤ 2 4 , 2 6 , or 2 8 ” in Step 8 of Algorithm 2. Then Algorithm 2 outputs 2 4 , 2 6 , or 2 8 candidates instead of 1. The num- ber of required faulty ciphertexts for each case is shown in Fig. 3. We can see that the number of faulty ciphertexts reduces as the number of exhaustive search increases. On average 3.45, 3.38, and 3.19 ciphertexts are required, respectively. As 2 8 exhaustive searches are required to ﬁnd 1 subkey, 2 32 searches are required to ﬁnd the master key. The search of 2 32 can- didates is trivial from a cryptanalytic point of view, which means that the key is broken. For example, it took 8–35 min with a Core2 Duo 3.0 GHz PC (Fukunaga and Takahashi, 2009). Therefore, we can retrieve the master key with on average 13 faulty ciphertexts and 2 32 exhaustive searches.

3.7.2. Access to the decryption oracle If access to the decryption oracle is allowed, the attack can be transposed into the initial rounds of the cipher (Rivain, 2009). In fact, an attacker may obtain a faulty ciphertext Y ∗ from a plaintext X by inducing a fault at the end of the ﬁrst round. The plaintext X can then be viewed as the faulty result of a decryption of Y ∗ for which a fault has been induced at the beginning of the last round. She then asks for the decryption of Y ∗ which provides her with a

Table 4 Propagation of errors through the diffusion layer when four consecutive bytes are corrupted.

Errors before diff. layer

Propagated errors after diff. layer

˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı 0 0 0 0 0 0 0 0 0 0 0 0 0 ˛ ˇ ı

plaintext X ∗ . The pair (X, X ∗ ) thus constitutes a pair of correct and faulty results of the decryption algorithm with respect to an error induced at the beginning of the last round. Therefore, we can ﬁnd dk 13 with 4 faults as described in the previous section. We can also ﬁnd ek 13 with additional 4 faults without accessing the decryption oracle. Then from ARIA key expansion, we know that

ek 1 = dk 13 , ek 1 = W 0 ⊕ W 1 ≫19 , ek 13 = W 0 ⊕ W 1 ≪31 .

The 128-bit master key can be easily computed from ek 1 and ek 13 (for the detailed explanation we refer to Ha et al. (2005)). Therefore, we need 7 faults to ﬁnd the master key if an attacker can access to the decryption oracle.

3.8. Analysis when three or four bytes are corrupted

We know that we can get information on 7 bytes of a subkey with a one-byte fault and 11.73 bytes with a two-byte fault. We compute how many information we can get with a three-byte or a four-byte fault (see Tables 3 and 4, respectively.) To be exploited, at least two bytes should be affected by the same error. Furthermore, the location of the fault should be traceable from the output difference. For example, if (b 2,i , b 3,i , b 4,i , b 5,i ) are four corrupted bytes at round i (see the third row of Table 4), they are useless since there is no zero pattern and hence it is impossible to ﬁnd the location of the corrupted bytes. Finally, the information we can get with a three-byte fault is 13.29 bytes on average. That with a four-byte fault is 3.23 bytes on average.

3.9. Generalized fault model

Until now we have assumed that two bytes are corrupted. We loosen this constraint and assume that a maximum of four bytes

#

0 7 0 7 0 7 0 7 0 7 0 7 0

ı ˇ ˛ ˛ ˇı ˛ ˇı ˛ˇ ˛ˇ ı ı ˇ ˛ı ˛ı ˇ ı ˇ ˛ı 0 ˇ ˛ı ˇ ˛ ˛ı ˛ ˇ ˇı ˛ˇ ı ˛ˇı ˇ ˛ı ı ˛ı ˇ ˛ ˇ ı ˛ˇı ˛ˇ ˛ ˇ ˇı ˛ı ˛ˇı ˇı ˛ˇ 0 ˛ı ˇ ı ˛ı ˛ˇ ı ˛ı ˛ˇ ˇ ˛ ˇı ˛ ˇı ˇ ˛ ı ˛ı ˇ ˇ ˛ı ı ı ˛ˇ ˛ˇ ˇı ˛ı ˇ ˛ ˛ı 0 ˇı ˛ˇ ˛ˇı ˇ ˇı ˛ ˛ı ˛ı ˇı ˛ ˇ ı ˇı ˛ ˇ ˛ ˛ ˇı ˛ˇı ˛ˇ ı ˇ ˛ˇ ı ˛ı ˇ ı ˛ı ˇ ˛ı 0 ˇ ˛ ˛ ˛ˇı ˇı ˛ˇ ˛ˇ ı ı ˛ı ˇ ˇ ˛ı ı ˛ ˇ ˇı ˛ ˇı ˛ ˛ ˛ı ˇı ˇ ˛ˇ ˛ˇı ı ˇ ı 0 ˛ı ˛ı ˇ ˛ ˇ ı ˛ˇ ˛ˇı ˇ ˛ ˛ı ˇı ˛ı ˇ ı ˇ ˛ı ˇ ˛ ı ˇ ˛ˇ ˛ı ˛ı ı ˇ ˛ˇ ˛ˇı ˇı ˛ˇ ˛ı 0 ˇ ˛ı ˛ı ˇ ı ı ˛ˇ ˛ˇ ˇı ˛ ˇı ˛ ˛ ˇ ı

<!-- PDF_PAGE: 7 -->

## PDF page 7

C.H. Kim / The Journal of Systems and Software 85 (2012) 2096– 2103

2102

Fig. 4. Number of faulty ciphertexts to recover one subkey.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 7]

are corrupted. Furthermore, it is assumed that an attacker does not know the number of corrupted bytes. Then we can ﬁnd the subkeys and the master key by slightly modifying Algorithm 2. In Step 2, we ﬁrst ﬁnd the number and the location of corrupted bytes, and the sets of the positions of the bytes affected by the same error with the fault distribution tables (we can easily ﬁnd them from the zero pattern at the output with Tables 1–3). Once we have found the sets, we follow the other steps but need to modify some parts according to the number of sets. Fig. 4 and Table 5 show the simulation results. We ﬁrst tried to ﬁnd the number of faulty ciphertexts required to retrieve all 16 bytes of a subkey (we call it full recovery). Then we found the num- ber of faulty ciphertexts required for a partial search remaining 2 8 exhaustive searches (hence, overall exhaustive search to ﬁnd the master key becomes 2 32 ). The number of required faulty cipher- texts for full recovery when one byte is corrupted is 9.72. We need 6.38 faulty ciphertexts if 2 8 exhaustive searches are allowed. Our simulation results show a better performance than that of Li et al. (2008) in a one-byte fault model as the comparison-and-reduction process (Step 5 of Algorithm 2) removes impossible candidates. Algorithm 2 eliminates wrong candidates quickly as the size of the sets of the positions of the bytes affected by the same error is bigger. Therefore, a three-byte fault is less efﬁcient than a two-byte fault even if the number of useful bytes, 13.29, is bigger than that of the two-byte fault, 11.73. While 58 % of the sets have a size of 5 and 29% have a size of 3 in a two-byte fault model, 36% have a size of 3 and 55% have a size of 2 in a three-byte fault model. When an attacker does not know the number and the position of faulty bytes (we call it random-byte fault model), the number of required faulty ciphertexts to retrieve the master key is 5.26 on average allowing 2 8 exhaustive searches. Therefore, we need 21 faulty ciphertexts on average with 2 32 exhaustive searches to ﬁnd the 128-bit master key. The number of corrupted bytes varies

Table 5 Number of faulty ciphertexts to ﬁnd a subkey for each fault model.

# of faulty bytes 1 2 3 4 Random

Full recovery 2 8 exhaustive search

### 9.72 6.38

### 4.98 3.19

### 5.61 4.09

### 36.82 22.65

### 7.53 5.26

depending on the structure of the implementation, type of injected faults, etc. A fault should corrupt only single byte in the previous work by Li et al. (2008). However, our attack based on a random- byte fault model works if a fault corrupts a maximum of four bytes. Furthermore, it requires less faulty ciphertexts.

4. Possible countermeasures

Several countermeasures to detect faults have been proposed in the literature. Especially, three techniques – redundancy-based, code-based, and pattern-based techniques – are mentioned in Li et al. (2008). In this section, we examine whether these counter- measures can prevent our attacks in multi-byte fault models. Redundancy-based technique is to perform additional encryp- tion (or decryption), and then check whether the result is the same (or the original data). As all DFA exploit faults induced at the ﬁrst or the last few rounds, this solution may compute the ﬁrst and the last few rounds again instead of re-encrypting the full rounds. Code- based solutions are divided into coding method and error detection code (EDC). Coding method encodes message before encryption and checks errors after decryption. EDC approach is often used in each rounds’ inner parts with the implementation of parity-based EDC. Li et al. proposed pattern-based technique that utilizes the ciphertext difference (Li et al., 2008). It checks pattern of zero and non-zero bytes in the ciphertext difference after assuming that one byte is corrupted. Redundancy-based and code-based techniques are independent of the adopted fault model. Hence, these techniques are applicable to prevent our attacks. Li et al.’s pattern-based technique can also be used to prevent our attacks as we can construct pattern of zero and non-zero bytes in the ciphertext difference as shown in Tables 2–4. However, we note that pattern-based technique is not so much efﬁcient because it should store many ciphertexts. An attacker may give a fault after several iterations of encryptions. Hence, in order to detect a fault it needs the XOR result of all possible combination of two ciphertexts during certain period.

5. Conclusions and discussion

We introduced new differential fault attacks on ARIA. By assum- ing that an attacker induces a fault corrupting two bytes, we need 13 faults on average to recover the ARIA 128-bit secret key. If access to the decryption oracle is allowed, we need 7 faults. The attacker does not need to know the position and value of the corrupted bytes in advance. Furthermore, we proposed a generalized technique that works even if a fault corrupts a maximum of four bytes. The attacker can ﬁnd the key with 21 faulty ciphertexts without knowing the num- ber of corrupted bytes. This improvement comes from our analysis of the characteristics of the ARIA diffusion layer that has not been carried out before. One interesting point we have found is that the enhancement in terms of security against traditional cryptanalysis may be helpful in differential fault analysis. ARIA has very similar structure to AES except the diffusion layer. AES diffusion layer diffuses one byte to four bytes. However, ARIA diffusion layer does one byte to seven bytes in order to amplify the diffusion effect, which leaks more information on the key in differential fault analysis. This is the case for faults induced at one round earlier. The best known DFA on AES exploits faults induced at two rounds earlier, hence the affected bytes after two rounds become 16 bytes. In ARIA, the analysis of faults induced at two rounds ear- lier is more complicated due to complex key expansion as well as asymmetric structure of the diffusion layer. AES has a simple key scheduling method so that knowing the last round key allows to

<!-- PDF_PAGE: 8 -->

## PDF page 8

C.H. Kim / The Journal of Systems and Software 85 (2012) 2096– 2103

ﬁnd the previous round key. Hence, the key space for the consecu- tive two rounds is 2 128 . However, ARIA has 2 256 key space for two consecutive round keys. Anyhow, the analysis of faults induced at two rounds earlier will be good research direction for future work.

Acknowledgements

The author thanks the reviewers for their helpful comments. This work has been partially funded by the Walloon Region Mar- shall Plan through the SPW DG06 Project TRASILUX.

### References

ARIA, Korean standard block cipher algorithm. Available from: http://210.104.33.10/ARIA/index-e.html. Bao, F., Deng, R.H., Han, Y., Jeng, A.B., Narasimhalu, A.D., Ngair, T.-H.,1998. Breaking public key cryptosystems on tamper resistant devices in the presence of tran- sient faults. In: The 5th International Workshop on Security Protocols, vol. 1361 of Lecture Notes in Computer Science. Springer, pp. 115–124. Bar-El, H., Choukri, H., Naccache, D., Tunstall, M., Whelan, C., 2004. The sorcerer’s apprentice guide to fault attacks. In: Fault Diagnosis and Tolerance in Cryptog- raphy in association with the International Conference on Dependable Systems and Networks (DSN 2004), pp. 330–342. Barenghi, A., Bertoni, G., Breveglieri, L., Pellicioli, M., Pelosi, G.,2010. Low voltage fault attacks to AES. In: IEEE International Symposium on Hardware-Oriented Security and Trust – HOST 2010. IEEE Computer Society, pp. 7–12. Barenghi, A., Bertoni, G., Palomba, A., Susella, R.,2011. A novel fault attack against ECDSA. In: IEEE International Symposium on Hardware-Oriented Security and Trust – HOST 2011. IEEE Computer Society, pp. 161–166. Biham, E., Granboulan, L., Nguyen, P.Q.,2005. Impossible fault analysis of RC4 and differential fault analysis of RC4. In: Fast Software Encryption: 12th International Workshop, FSE 2005, vol. 3557 of Lecture Notes in Computer Science. Springer, pp. 359–367. Biham, E., Shamir, A.,1997. Differential fault analysis of secret key cryptosystems. In: Advances in Cryptology – CRYPTO ’97, 17th Annual International Cryptol- ogy Conference, vol. 1294 of Lecture Notes in Computer Science. Springer, pp. 513–525. Blömer, J., Otto, M., Seifert, J.-P., 2005. Sign change fault attacks on elliptic curve cryp- tosystems. In: The 2nd International Workshop on Fault Diagnosis and Tolerance in Cryptography – FDTC 2005, pp. 25–40. Bleichenbacher, D., Joye, M., Quisquater, J.-J.,1997. A new and optimal chosen- message attack on RSA-type cryptosystems. In: Information and Communica- tion Security, First International Conference, ICICS’97, vol. 1334 of Lecture Notes in Computer Science. Springer, pp. 302–313. Chen, H., Wu, W., Feng, D.,2007. Differential fault analysis on CLEFIA. In: Information and Communications Security, 9th International Conference, ICICS 2007, vol. 4861 of Lecture Notes in Computer Science. Springer, pp. 284–295. Ciet, M., Joye, M., 2005. Elliptic curve cryptosystems in the presence of permanent and transient faults. Designs, Codes and Cryptography 36 (1), 33–43. Clavier, C., Gierlichs, B., Verbauwhede, I.,2008. Fault analysis study of IDEA. In: Topics in Cryptology – CT-RSA 2008, The Cryptographer’s Track at RSA Con- ference 2008, vol. 4964 of Lecture Notes in Computer Science. Springer, pp. 274–287. Coron, J.-S., Giraud, C., Morin, N., Piret, G., Vigilant, D.,2010. Fault attacks and counter- measures on Vigilant’s RSA-CRT algorithm. In: Fault Diagnosis and Tolerance in Cryptography, 7th International Workshop, FDTC 2010. IEEE Computer Society, pp. 89–96. Dhem, J.-F., Koeune, F., Leroux, P.-A., Mestré, P., Quisquater, J.-J., Willems, J.-L.,1998. A practical implementation of the timing attack. In: Smart Card Research and Applications, This International Conference, CARDIS ’98, vol. 1820 of Lecture Notes in Computer Science. Springer, pp. 167–182. Fleischmann, E., Gorski, M., Lucks, S., 2009. Attacking reduced rounds of the ARIA block cipher. IACR Eprint Archive 200, 9–334. Fukunaga, T., Takahashi, J.,2009. Practical fault attack on a cryptographic LSI with ISO/IEC 18033-3 block ciphers. In: 6th International Workshop on Fault Diag- nosis and Tolerance in Cryptography, FDTC 2009. IEEE Computer Society, pp. 84–92. Ha, J., Kim, C., Moon, S.-J., Park, I., Yoo, H.,2005. Differential power analysis on block cipher ARIA. In: HPCC, vol. 3726 of Lecture Notes in Computer Science. Springer, pp. 541–548. Hemme, L.,2004. A differential fault attack against early rounds of (triple-)DES. In: Cryptographic Hardware and Embedded Systems – CHES 2004: 6th Interna- tional Workshop, vol. 3156 of Lecture Notes in Computer Science. Springer, pp. 254–267. Hoch, J.J., Shamir, A.,2004. Fault analysis of stream ciphers. In: Cryptographic Hard- ware and Embedded Systems – CHES 2004: 6th International Workshop, vol. 3156 of Lecture Notes in Computer Science. Springer, pp. 240–253.

2103

Kim, C., Schlaffer, M., Moon, S., 2008. Differential side channel analysis attacks on FPGA implementation of ARIA. ETRI Journal 30 (2), 315–325. Kim, C.H.,2010. Differential fault analysis against AES-192 and AES-256 with mini- mal faults. In: Fault Diagnosis and Tolerance in Cryptography, 7th International Workshop, FDTC 2010. IEEE Computer Society, pp. 3–9. Kim, C.H., Quisquater, J.-J., 2007. Faults, injection methods, and fault attacks. IEEE Design and Test of Computers 24 (6), 544–545. Kim, C.H., Quisquater, J.-J.,2008. New differential fault analysis on AES key schedule: Two faults are enough. In: Smart Card Research and Advanced Applications, 8th IFIP WG 8.8/11.2 International Conference, CARDIS 2008, vol. 5189 of Lecture Notes in Computer Science. Springer, pp. 48–60. Kocher, P.C., Jaffe, J., Jun, B.,1999. Differential power analysis. In: Advances in Cryp- tology – CRYPTO ’99, 19th Annual International Cryptology Conference, vol. 1666 of Lecture Notes in Computer Science. Springer, pp. 388–397. Kwon, D., Kim, J., Park, S., Sung, S.H., Sohn, Y., Song, J.H., Yeom, Y., Yoon, E.-J., Lee, S., Lee, J., Chee, S., Han, D., Hong, J.,2003. New block cipher: ARIA. In: 6th Inter- national Conference on Information Security and Cryptology – ICISC 2003, vol. 2971 of Lecture Notes in Computer Science, pages. Springer, pp. 432–445. Li, R., Sun, B., Zhang, P., Li, C., 2008. New impossible differential cryptanalysis of ARIA. IACR Eprint Archive 200, 8–227. Li, S., Song, C., 2008. Improved impossible differential cryptanalysis of ARIA. In: International Conference on Information Security and Assurance, ISA 2008, pp. 129–132. Li, W., Gu, D., Li, J., 2008. Differential fault analysis on the ARIA algorithm. Information Sciences 178 (19), 3727–3737. Li, W., Gu, D., Wang, Y., 2009. Differential fault analysis on the contracting UFN struc- ture, with application to SMS4 and Macgufﬁn. Journal of Systems and Software 82 (2), 346–354. Moradi, A., Shalmani, M.T.M., Salmasizadeh, M.,2006. A generalized method of dif- ferential fault attack against AES cryptosystem. In: Cryptographic Hardware and Embedded Systems – CHES 2006, 8th International Workshop, vol. 4249 of Lecture Notes in Computer Science. Springer, pp. 91–100. Naccache, D., Nguyen, P.Q., Tunstall, M., Whelan, C.,2005. Experimenting with faults, lattices and the DSA. In: Public Key Cryptography – PKC 2005, 8th Interna- tional Workshop on Theory and Practice in Public Key Cryptography, vol. 3386 of Lecture Notes in Computer Science. Springer, pp. 16–28. National Institute of Standard and Technology, 1993. Data Encryption Standard, NIST FIPS PUB 46-2. Park, J., Lee, H., Ahn, M.,2007. Side-channel attacks against ARIA on active RFID device. In: International Conference on Convergence Information Technology, ICCIT 2007. IEEE Computer Society, pp. 2163–2168. Piret, G., Quisquater, J.-J.,2003. A differential fault attack technique against SPN structures, with application to the AES and KHAZAD. In: Crypto- graphic Hardware and Embedded Systems – CHES 2003, 5th International Workshop, vol. 2779 of Lecture Notes in Computer Science. Springer, pp. 77–88. Quisquater, J.-J., Samyde, D.,2001. Electromagnetic analysis (EMA): Measures and counter-measures for smart cards. In: Smart Card Programming and Security, International Conference on Research in Smart Cards, E-smart 2001, vol. 2140 of Lecture Notes in Computer Science. Springer, pp. 200–210. Rivain, M.,2009. Differential fault analysis on DES middle rounds. In: Cryptographic Hardware and Embedded Systems – CHES 2009: 11th International Workshop, vol. 5747 of Lecture Notes in Computer Science. Springer, pp. 457–469. Saha, D., Mukhopadhyay, D., RoyChowdhury, D., 2009. A diagonal fault attack on the advanced encryption standard. IACR Eprint Archive 200, 9–581. Schmidt, J.-M., Medwed, M.,2009. A fault attack on ECDSA. In: 6th Fault Diagnosis and Tolerance in Cryptography, Third International Workshop – FDTC 2009. IEEE Computer Society, pp. 93–99. Takahashi, J., Fukunaga, T.,2008. Improved differential fault analysis on CLEFIA. In: Fifth International Workshop on Fault Diagnosis and Tolerance in Cryptography, 2008, FDTC 2008. IEEE Computer Society, pp. 25–34. Takahashi, J., Fukunaga, T., Yamakoshi, K.,2007. DFA mechanism on the AES key schedule. In: 4th International Workshop on Fault Diagnosis and Tolerance in Cryptography, FDTC 2007. IEEE Computer Society, pp. 62–74. Wu, W.-L., Zhang, W.-T., Feng, D.-G., 2007. Impossible differential cryptanalysis of reduced-round ARIA and Camellia. Journal of Computer Science and Technology 22 (3), 449–456. Yoo, H., Herbst, C., Mangard, S., Oswald, E., Moon, S.-J.,2006. Investigations of power analysis attacks and countermeasures for ARIA. In: 7th International Workshop on Information Security Applications, WISA 2006, vol. 4298 of Lecture Notes in Computer Science. Springer, pp. 160–172. Zhao, X.-J., Wang, T., Gao, J.-Z., 2010. Multiple bytes differential fault analysis on CLEFIA. IACR Eprint Archive, 2010–2078.

Chong Hee Kim received his B.S. from Kyungpook National University, Republic of Korea in 1997, M.S. and Ph.D. from POSTECH (Pohang University of Science and Tech- nology), Republic of Korea in 1999 and 2004, respectively. He worked for Samsung Electronics Co., LTD and NXP Semiconductors N.V. He is currently senior researcher at Universite Catholique de Louvain, Belgium. His recent research interests include RFID secure protocols and security of the embedded systems such as side channel analysis and fault attacks.
