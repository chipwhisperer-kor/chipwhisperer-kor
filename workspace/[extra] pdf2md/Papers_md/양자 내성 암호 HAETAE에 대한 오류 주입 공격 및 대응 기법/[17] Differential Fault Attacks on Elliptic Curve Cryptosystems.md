# [17] Differential Fault Attacks on Elliptic Curve Cryptosystems

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 16
converted_at: "2026-07-26"
source_asset_id: "HAETAE-FIA-REF-17"
derived_asset_id: "HAETAE-FIA-REF-17-MD"
source_path: "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[17] Differential Fault Attacks on Elliptic Curve Cryptosystems.pdf"
source_sha256: "8cac85cacf93bd60bdd101ab943f07c5ba6426f6aa4c246b8183f7aa602944d9"
pages: 16
bbox_words: 9141
consumed_bbox_words: 9141
numeric_tokens: 552
consumed_numeric_tokens: 552
source_blocks: 140
consumed_source_blocks: 140
emitted_blocks: 129
embedded_raster_images: 0
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 16
glyph_chars_removed: 5
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

Diﬀerential Fault Attacks on Elliptic Curve Cryptosystems

(Extended Abstract)

Ingrid Biehl 1 , Bernd Meyer 2 , and Volker Müller 3

1

University of Technology, Computer Science Department, Alexanderstraße 10, 64283 Darmstadt, Germany, biehl@informatik.tu-darmstadt.de 2 Siemens AG, Corporate Technology, 81730 München, Germany, bernd.meyer@mchp.siemens.de 3 Universitas Kristen Duta Wacana, Jl. Dr. Wahidin 5–19, Yogyakarta 55224, Indonesia, vmueller@ukdw.ac.id

Abstract. In this paper we extend the ideas for diﬀerential fault at- tacks on the RSA cryptosystem (see [4]) to schemes using elliptic curves. We present three diﬀerent types of attacks that can be used to derive information about the secret key if bit errors can be inserted into the elliptic curve computations in a tamper-proof device. The eﬀectiveness of the attacks was proven in a software simulation of the described ideas.

Key words: Elliptic Curve Cryptosystem, Diﬀerential Fault Attack.

1 Introduction

Elliptic curves have gained especially much attention in public key cryptography in the last few years. Standards for elliptic curve cryptosystems (ECC) and signature schemes were developed [7]. The security of ECC is usually based on the (expected) diﬃculty of the discrete logarithm problem in the group of points on an elliptic curve. In many practical applications of ECC the secret key (the solution to a discrete logarithm problem) is stored inside a tamper-proof device, usually a smart card. It is considered to be impossible to extract the key from the card without destroying the information. For security reasons the decryption or signing process is usually also done inside the card. Three years ago a new kind of attack on smart card implementations of cryp- tosystems became public, the so called diﬀerential fault attack (DFA), which has been successful in attacking RSA [4], DES [3], and even helps reverse-engineering unknown cryptosystems. The basic idea of DFA is the enforcement of bit errors into the decryption or signing process which is done inside the smart card. Then information on the secret key can leak out of the card. In RSA implementations for example this information can be used to factor the RSA modulus (at least with some non-negligible probability), which is equivalent to computing the se- cret RSA key. So far there is no method known to extend the ideas of [4] to

### M. Bellare (Ed.): CRYPTO 2000, LNCS 1880, pp. 131–146, 2000. c Springer-Verlag Berlin Heidelberg 2000

<!-- PDF_PAGE: 2 -->

## PDF page 2

Ingrid Biehl, Bernd Meyer, and Volker Müller

132

cryptosystems based on the discrete logarithm problem over elliptic curves. In this paper we investigate how DFA techniques can be used to compute the secret key of an ECC smart card implementation. Our attacks can be used for elliptic curves deﬁned over arbitrary ﬁnite ﬁelds. We consider the following scenario: a cryptographically strong elliptic curve is publicly known as part of the public key. The secret key d ∈ ZZ is stored inside a tamper-proof device, unreadable for outside users. On input of some point P on the chosen elliptic curve, the device computes and outputs the point d · P . We assume that we have access to the tamper-proof device such that we can compute d · P for arbitrary input points P . The main common idea behind the attacks in Sect. 4 is the following: by inserting (in the ﬁrst mentioned attack) or by disturbing the representation of a point by means of a random register fault we enforce the device to apply its point addition resp. multiplication algorithm to a value which is not a point on the given but on some diﬀerent curve. It is a crucial observation as we will show in Sect. 3 that the result of this computation is a point on the new prob- ably cryptographically less strong curve which can be exploited to compute d. Thus these attacks work by misusing the tamper-proof device to execute its computation steps on group structures not originally intended by the designer of the cryptosystem. Similar ideas have been previously described in [10] where small order subgroups in (ZZ/pZZ) ∗ are exploited to compute part of the secret key and in [5] for attacks against identiﬁcation schemes. It is shown in [5] how identiﬁcation schemes can be used to prove knowledge of logarithms and roots which do not even exist in the subgroup where the cryptosystem should make its computations. Moreover, we present a DFA-like attack in Sect. 5 which is similar to at- tacks against RSA in [4]. There so called register faults are used to attack RSA smart card implementations. Register faults are transient faults that aﬀect cur- rent data inside a register. All the circuitry is not inﬂuenced by these faults and works properly. For a more detailed discussion of that fault model, we refer to [4, Sect. 3]. We use the same fault model and assume that we can enforce ran- dom register faults in the decryption or signing process. Incorrect output values caused by random register faults are used to compute possible intermediate val- ues of the computation and parts of the secret key. The intermediate values are not necessarily unique and one has to repeat the attack to get successively all bits of the secret key. The analysis of the probability of non-uniqueness and so of the costs of the computation of the secret key is the technically most compli- cated part of the analysis in the considered ECC case and cannot be based on the ideas presented in [4]. We sketch it in the appendix. We know no widespread applications of smart cards for signature generation or decryption where complete points are the output of the used tamper-proof de- vice. Therefore, we consider additionally as a more realistic scenario the situation that the tamper-proof device implements El-Gamal decryption. For El-Gamal decryption we can show that the attacks from Sect. 4.1 and 5 have expected polynomial running time. Furthermore, it is shown that the attack of Sect. 4.2

<!-- PDF_PAGE: 3 -->

## PDF page 3

Diﬀerential Fault Attacks on Elliptic Curve Cryptosystems 133

can be used against El-Gamal decryption and the elliptic curve digital signature scheme in expected subexponential running time. The fault models of DFA attacks have been criticized for being purely the- oretical. In [2] it is argued that a random one-bit error would be more likely to crash the processor of the tamper-proof device or yield an uninformative error than to produce a faulty ciphertext. Instead, glitch attacks which have already been used in the pay-TV hacking community, are presented in [2,1,8] as a more practical approach for diﬀerential fault analysis. The attacker applies a rapid transient in the clock or the power supply of the chip. Due to diﬀerent delays in various signal paths, this aﬀects only some signals and by varying the parameters of the attack, the CPU can be made to execute a number of wrong instructions. By carefully choosing the timing of the glitch, the attacker can possibly enforce register faults in the decryption or signing process and apply our attacks. The paper is structured as follows: Section 2 gives an introduction to the well known theory of elliptic curves. Section 3 examines pseudo-addition, an operation which will play a crucial part in the DFA attacks. Sections 4 and 5 describe three diﬀerent attacks on ECC systems and show how faults can be used to determine the secret key d. We close with comments on possible countermeasures.

2 Elliptic Curves

In this section we review several well known facts about elliptic curves. Let K be a ﬁnite ﬁeld of arbitrary characteristic, and let a 1 , a 2 , a 3 , a 4 , a 6 ∈ K be elements such that the discriminant of the polynomial given in (1) is not zero (the formula for the discriminant can be found in, e.g., [6]). Then the group of points E(K) on the elliptic curve E = (a 1 , a 2 , a 3 , a 4 , a 6 ) is given as (x, y) ∈ K 2 : y 2 + a 1 xy + a 3 y = x 3 + a 2 x 2 + a 4 x + a 6 ∪ O , (1)

where O := (∞, ∞). Pairs of elements of K 2 which satisfy the polynomial equa- tion (1) are denoted as points on E. In the following we use subscripts like P E to show that P is a point on the elliptic curve E. We deﬁne the following operation:

(2)

– for all P E ∈ E(K), set P E + O E = O E + P E := P E , – for P E = (x, y) E , set −P E := (x, −y − a 1 x − a 3 ) E , – for x 1 = x 2 and y 2 = −y 1 − a 1 x 1 − a 3 , set (x 1 , y 1 ) + (x 2 , y 2 ) := O E , – in all other situations, set (x 1 , y 1 ) E + (x 2 , y 2 ) E := (x 3 , y 3 ) E , where

x 3 = λ 2 + a 1 λ − a 2 − x 1 − x 2

y 3 = −y 1 − (x 3 − x 1 ) λ − a 1 x 3 − a 3

with

 2   3 x 1 + 2 a 2 x 1 + a 4 − a 1 y 1 2 y 1 + a 1 x 1 + a 3 λ =   y 1 − y 2 x 1 − x 2

if x 1 = x 2 and y 1 = y 2 ,

otherwise.

<!-- PDF_PAGE: 4 -->

## PDF page 4

Ingrid Biehl, Bernd Meyer, and Volker Müller

134

As shown in [6], this operation makes E(K) to an abelian (additive) group with zero element O E . For any positive integer m we deﬁne m · P E to be the result of adding P E m − 1 times to itself. A crucial point that we will use in further sections is the fact that the curve coeﬃcient a 6 is not used in any of the addition formulas given above, but follows implicitly from the fact that the point P E is assumed to be on the curve E. In almost all practical ECC systems the discrete logarithm (DL) problem in the group of points on an elliptic curve is used as a trapdoor one-way function. The DL problem is deﬁned as follows: given an elliptic curve E and two points P E , d · P E on E, compute the minimal positive multiplier d. A cryptographically strong elliptic curve is an elliptic curve such that the discrete logarithm problem in the group of points is expected (up to current knowledge) to be diﬃcult. ECC system implementations should always use cryptographically strong curves. We will show in the following sections that random register faults can be used to compute information about a secret key d which is stored inside a tamper- proof device that computes d · P for some input point P . Thus our scenario becomes applicable if the device is used for the computation of the trapdoor one-way function d · P in a larger protocol. In practice however neither EC sig- nature generation nor EC cryptosystems use tamper-proof devices which output complete points. Consider for example the following EC El-Gamal cryptosystem (without point compression): Let E be a cryptographically strong elliptic curve. Given a point P ∈ E assume that Q = d · P is the public key and 1 ≤ d &lt; ord(P ) the secret key of some user. For a point R let x(R) denote the x-coordinate. The EC El-Gamal cryptosystem (without point compression) is given as follows:

Encryption Input: message m, public key

choose 1 &lt; k &lt; ord(P ) randomly return (k · P, x(k · Q) ⊕ m)

Decryption Input: (H, m ), secret key d

compute d · H return m ⊕ x(d · H)

If we combine the input and the output of the decryption process, then we can consider El-Gamal decryption as a black box that computes on input of some point H the x-coordinate of d · H. Using the curve equation corresponding to the input point H we can determine the points d · H and −(d · H). But we have to stress that one cannot distinguish which one of this pair of points is d · H.

Pseudo-addition and Pseudo-multiplication

3

Let E be a ﬁxed cryptographically strong elliptic curve deﬁned over a ﬁnite ﬁeld K. We start with the following question: what happens when we use the operation deﬁned in (2) for arbitrary pairs in K 2 instead for points on E? In this section we will answer this question and deduce some properties of this new operation.

<!-- PDF_PAGE: 5 -->

## PDF page 5

Diﬀerential Fault Attacks on Elliptic Curve Cryptosystems 135

Let a 1 , a 2 , a 3 , a 4 ∈ K be the coeﬃcients of E with the exception of a 6 . It should be noted that a 6 does not occur in the addition formulas (2) and is therefore not needed. Then it is easy to see that the operation (2) is also well- deﬁned for arbitrary elements in P := K 2 ∪{(∞, ∞)} (assuming that division by zero has the result ∞). For two arbitrary pairs P i ∈ P, i = 1, 2, we denote this operation as pseudo-addition and write P 1 ⊕ P 2 . Pseudo-subtraction is deﬁned as pseudo-addition with the negative point and denoted with P 1 P 2 = P 1 ⊕(−P 2 ). Moreover, for any positive integer n ∈ IN and any pair P 1 ∈ P, we deﬁne a pseudo-multiplication n ⊗ P 1 as the result of (· · · ((P 1 ⊕ P 1 ) ⊕ P 1 ) ⊕ · · · ) ⊕ P 1 , where pseudo-addition ⊕ is used exactly n − 1 times. We present a few facts on the operation ⊕. Testing a few random example pairs in P, it becomes obvious that pseudo-addition ⊕ is in general no longer as- sociative. We can however prove the following weaker results on pseudo-addition.

Theorem 1. Let two elements (x i , y i ) ∈ P, i = 1, 2, be given. Pseudo-addition is

1. commutative, i.e. (x 1 , y 1 ) ⊕ (x 2 , y 2 ) = (x 2 , y 2 ) ⊕ (x 1 , y 1 ), 2. “weakly associative”: if x 1 = x 2 or (x 1 , y 1 ) = ±(x 2 , y 2 ) (x 1 , y 1 ) ⊕ (x 2 , y 2 ) (x 2 , y 2 ) = (x 1 , y 1 ).

Proof. The ﬁrst assertion of the theorem follows directly from the symmetry of the formulas given in (2), testing all cases for the second assertion is a minor exercise for a computer algebra system.

The discrete logarithm problem for elliptic curves is deﬁned after multiplication of a point with a scalar. The following theorem describes a property of pseudo- multiplication.

Theorem 2. Let the number of elements in the ﬁeld K be q. For at least q 2 +1− 4q elements P ∈ P and all positive integers n, m, pseudo-multiplication satisﬁes

1. 2.

n ⊗ (m ⊗ P ) = (n · m) ⊗ P , (n ⊗ P ) ⊕ (m ⊗ P ) = (n + m) ⊗ P .

Proof. Note ﬁrst that the assertions are trivial for the pair O. Let therefore P = (x, y) ∈ P. Deﬁne a 6 = y 2 +a 1 xy+a 3 y−x 3 −a 2 x 2 −a 4 x. If (a 1 , a 2 , a 3 , a 4 , a 6 ) deﬁnes an elliptic curve, then obviously P is a point on this curve, and the result of the theorem follows directly from the associativity of point addition. The number of exceptional pairs (x, y) that do not lead to elliptic curves can easily be bounded by 4q since for given coeﬃcients a 1 , a 2 , a 3 , a 4 there are only two possibilities for a 6 such that the discriminant becomes zero.

Finally, we examine how a fast multiplication algorithm behaves when used with pseudo-addition instead of ordinary point addition. A direct consequence of Theorem 2 is the following theorem.

<!-- PDF_PAGE: 6 -->

## PDF page 6

Ingrid Biehl, Bernd Meyer, and Volker Müller

136

Theorem 3. Given a pair P = (x, y) ∈ P and a positive integer m. Assume that the tuple (a 1 , a 2 , a 3 , a 4 , y 2 + a 1 xy + a 3 y − x 3 − a 2 x 2 − a 4 x) deﬁnes an el- liptic curve E over K. Then any fast multiplication type algorithm with input (m, P, a 1 , a 2 , a 3 , a 4 ) computes the result m⊗P accordingly to the addition deﬁned in Sect. 2. Moreover, we have the equality m ⊗ P = m · P E , where P E = P and m · P E are points on E and the latter is computed with “ordinary” point additions.

Remark 1. The crucial idea of pseudo addition is the fact that one of the curve coeﬃcients is not used in the addition formulas. However a diﬀerent point rep- resentation, so called projective coordinates, is also often used in practice. The addition formulas for such representations (see, e.g., [7, A.10.4]) have the same property. Therefore, the ideas presented in this paper can be adapted to other point representations typically used in practical applications.

Faults at the Beginning of the Multiplication

4

We start with the description of elliptic curve fault attacks. The ﬁrst type of attacks however does not need the generation of any fault; it is an attack on “bad” implementations of ECC systems.

No Correctness Check for Input Points

4.1

The ﬁrst attack is applicable when the device neither explicitly checks whether an input point P nor the result of the computation really is a point on the cryptographically strong elliptic curve E which is a parameter of the system. The attack is simple and should not be applicable to a well designed system, but nevertheless such a “bug” might happen in practice. Let E = (a 1 , a 2 , a 3 , a 4 , a 6 ) be a given cryptographically strong elliptic curve, which is part of the setup of the ECC system. In this situation we input a pair P ∈ P into the tamper-proof device which is not a point on E, but a point on some other elliptic curve E . We choose the input pair P = (x, y) carefully, such that with a 6 = y 2 + a 1 xy + a 3 y − x 3 − a 2 x 2 − a 4 x the tuple (a 1 , a 2 , a 3 , a 4 , a 6 ) deﬁnes an elliptic curve E whose order has a small divisor r and such that ord(P ) = r. With Theorem 3 we know that the output of the tamper-proof device with input P is then d · P on E . Therefore, we end up with a discrete logarithm problem in the subgroup of order r generated by P ∈ E , namely given points P, d · P on E , ﬁnd d mod ord(P ). We can repeat this procedure with a diﬀerent choice of P and use the Chinese Remainder Theorem to compute the correct value of d. This algorithm is quite eﬃcient if we do not choose P , but the curve E ﬁrst and compute P . The construction of such an elliptic curve E can be done in essentially the same way as in the elliptic curve construction method described in [7]. First we try to ﬁnd an integer m in the Hasse interval such that (q + 1 − m) 2 − 4q has a large square factor and m a small factor. Then we can determine

<!-- PDF_PAGE: 7 -->

## PDF page 7

Diﬀerential Fault Attacks on Elliptic Curve Cryptosystems 137

the j-invariant of an elliptic curve deﬁned over K which has group order m. Finally, we have to check whether there exists an elliptic curve with coeﬃcients a 1 , . . . , a 4 , a 6 that has the given j-invariant. The latter test can be solved by factoring a polynomial of degree 2 and yields a 6 . We check for a few random values of x whether y 2 + a 1 xy + a 3 y − x 3 − a 2 x 2 − a 4 x − a 6 = 0 is solvable for y. The pair P E = (x, y) is chosen as input. Since m has a small divisor, given d · P E we can then determine the secret key modulo this small divisor (at least when this small divisor divides the order of P E on E ). If we apply this attack to the device computing the El-Gamal decryption as described in Sect. 2 we cannot determine the y-coordinate of the resulting point uniquely. Given its x-coordinate w we can compute values z, z such that (w, z), (w, z ) ∈ E and (w, z 1 ) = −(w, z 2 ), but we cannot decide which of these points is d · P on E . By computation of the discrete logarithms of (w, z) and (w, z ) we therefore get values c, c with c ≡ −c mod ord(P ) and either d ≡ c mod ord(P ) or d ≡ c mod ord(P ). Thus we get d 2 ≡ c 2 mod ord(P ). To com- pute d we have to choose suﬃciently many points P i with small order such that lcm(ord(P 1 ), . . . , ord(P s )) ≥ d 2 . Then we get equations d 2 ≡ c 2 i mod ord(P i ) for 1 ≤ i ≤ s and can compute the value d 2 as an integer using the Chinese Remainder Theorem. The integer square root is the secret key d.

### 4.2 Placing Register Faults Properly

In the second attack we assume that we can enforce register faults inside the “tamper-proof” device at some precise moment at the beginning of the multi- plication process. If the “tamper-proof” device checks whether the given input point is a point in the group of points of the cryptographically strong elliptic curve E, the attack of Sect. 4.1 is no more applicable. Assume however that we can produce one register fault inside the tamper-proof device right after this test is ﬁnished. Then the device computes internally with a pair P which diﬀers in exactly one bit from the input point P . Therefore, the device computes and – if it does not check whether the output is a point on E – outputs d ⊗ P . With Theorem 3 we deduce that d ⊗ P lies on the same elliptic curve E as P . We determine a 6 such that the output pair d ⊗ P satisﬁes the curve equation with coeﬃcients (a 1 , a 2 , a 3 , a 4 , a 6 ). If these coeﬃcients deﬁne an elliptic curve E , we have reduced the original DL problem on E to a DL problem on E : check for all possible candidates P (P is unknown outside the device, but remember that P diﬀers in only one bit from the known point P ) whether this candidate is a point on E and – if so – try to solve the DL problem on E . First, we compute ord(E ) the number of points on E using algorithms for point counting. If ord(E ) has a small divisor r, we solve the DL problem for the points (ord(E )/r) · P E and d · ((ord(E )/r) · P E ). This gives an equation d ≡ c mod r for some value c. Repeating this step with diﬀerent divisors r we can compute d with the Chinese Remainder Theorem. As described in Sect. 2, we can consider El-Gamal decryption as a black box that on input of some point P computes x(d · P ) where d is the secret key stored inside the tamper-proof device. Note however that we cannot apply directly the

<!-- PDF_PAGE: 8 -->

## PDF page 8

Ingrid Biehl, Bernd Meyer, and Volker Müller

138

attack from this section since we do not know the y-coordinate of the output point. Without the y-coordinate we cannot determine the curve E to which the output P belongs. In general there are many possible curves. It is however possible to solve the DL problem with non-negligible probability if there exists a curve E corresponding to a base point P resulting from a one-bit error such that the order of E is smooth. Then we use the algorithm of Pohlig-Hellman (see [12]) to compute d. Similar to the analysis of Lenstra’s Elliptic Curve Factoring Method [9], it follows that we have to consider subexponentially many random elliptic curves until one of them has (subexponentially) smooth order. Thus the expected num- ber of trials of the attack with random points P ∈ E until we ﬁnd such a smooth curve and can determine the secret multiplier d is subexponential again. A similar situation occurs in the elliptic curve DSA signature scheme. In EC DSA, we have two primes p, q which are about the same size, an elliptic curve E over IF q , and a point P on E of order p. The public key is (p, q, E, P, Q) where Q = d · P for some secret value d. To sign a message m with hash value h, the signer randomly chooses an integer 1 &lt; k &lt; p − 1, computes k · P = (x 1 , y 1 ), r ≡ x 1 mod p, and s ≡ k −1 (h + dr) mod p. The signature is (r, s). Please note that we cannot input a point here but a publicly known point P is used as base point for the computation. We again disturb the computation of k · P by a register fault right at the beginning, i.e. P is replaced by some P . The tamper-proof device then computes the signature r ≡ x(k · P ) mod p, and s ≡ k −1 (h + dr ) mod p. Knowing this signature, we can use the following algorithm for all possible candidates P̃ for P :

– compute the curve Ẽ corresponding to P̃ – if it exists –, – derive from r a small set of possible values for the x-coordinate of x(k · P ) (since p, q are of about the same size), – compute two candidates for the corresponding y-coordinate by means of the equation for Ẽ.

In case P̃ was correctly chosen and Ẽ is a weak curve with respect to the discrete logarithm problem and ord( P̃ ) &gt; p − 1, one can ﬁrst ﬁnd k, and then the secret −1 key d as d ≡ r (s k − h) mod p. If we disturb the base point P in such a way that P and P diﬀer only in one bit, we have only 2 log(q) possible choices for the curve E and it is very unlikely that we get a curve with subexponentially smooth order and that the attack succeeds. But if we manage to change o(log(q)) many bits at once such that we get subexponentially many diﬀerent choices for E then there is with high probability at least one curve with smooth order among them and we can compute the one-time key k and so the secret key d, i.e. the signature scheme is completely broken. The expected number of trials to get such a curve E is subexponential again.

<!-- PDF_PAGE: 9 -->

## PDF page 9

Diﬀerential Fault Attacks on Elliptic Curve Cryptosystems 139

Faults at Random Moments of the Multiplication

5

In this section we sketch an attack that works even if we cannot inﬂuence the exact position in the computation process, at which the enforced random register fault happens. In [4], the authors show how to attack RSA smart card implementations by enforcing register faults at random time in the decryption or signing process. The most important operation in RSA is fast exponentiation. For elliptic curves, the situation is similar and we can use some of the ideas of [4]. In the following we assume that the used elliptic curve is cryptographically strong, especially we assume that E(IF q ) contains a subgroup of prime order p with p &gt; q/ log(q). The operation Q = d · P is usually done with either a “right-to-left” or a “left-to-right” multiplication algorithm. Since the ideas for the attacks in both cases are very similar we restrict ourselves here to the “right- to-left” multiplication algorithm and show: if one can enforce a fault randomly in a register at a random state of the computation than one can recover the secret key in expected polynomial time. We start with a result for a fault model where we can introduce register faults during the computation of an a-priory chosen speciﬁc block of multiplier bits, e.g. we assume that we can repeatedly input some point P E on E into the tamper- proof device and enforce a register fault during m successive iterations of the fast multiplication algorithm. Then we will show that we can relax this condition, i.e. even if one cannot inﬂuence at which block the register fault happens one can deduce the secret key after an expected number of polynomially many enforced random register faults. We will present a rather informal description of the attack which abstracts from some less important details. The right-to-left multiplication algorithm works as follows (we denote by (d n−1 d n−2 . . . d 0 ) 2 the binary representation of a positive integer d, where d 0 is the least signiﬁcant bit):

H = P; Q = O; for i = 0 , ... , n-1 do if (d_i == 1) then Q = Q + H; H = 2 * H; output Q;

To simplify the notation assume that we know the binary length n of the un- known multiplier d (note that an attacker can “guess” the length of d). Denote by Q (i) , H (i) the value stored in the variable Q, H in the algorithm description before iteration i. The basic attack operation works as follows: we use the tamper-proof device with some input point P E to get the correct result Q (n) = d · P E and moreover we restart it with input P E but enforce a random register fault to get a faulty result Q̃ (n) . Assume that we enforce the register fault in iteration n−m ≤ j &lt; n, and that this fault ﬂips one bit in a register holding the variable Q (the case that a bit in H is ﬂipped can be handled similarly). Then Q̃ (j) is a disturbed Q-value, i.e. a pair in P 2 that diﬀers in exactly one bit from Q (j) .

<!-- PDF_PAGE: 10 -->

## PDF page 10

Ingrid Biehl, Bernd Meyer, and Volker Müller

140

Next we try to ﬁnd the index of the ﬁrst iteration j with j &gt; j and d j = 1 given Q (n) and Q̃ (n) . For simplicity reasons we assume that there is at least one non-zero bit among the m most signiﬁcant bits of d, i.e. j exists (we omit the technically more diﬃcult case of m zero bits here for reasons of readability). We can ﬁnd a candidate for the disturbed Q-value Q̃ (j ) with the following method: successively, we check each i with n − m ≤ i &lt; n as candidate for j , each x ∈ {0, 1} n−i with least signiﬁcant bit 1 as candidate for the i most signiﬁcant (i) bits of d, and each Q x = Q (n) − x · 2 i · P E as candidate for Q (j) . For each choice (i) of x and i we consider all disturbed Q-values Q̃ x which we can derive from (i) Q x by ﬂipping one bit. Then we check whether this may be the disturbed value which appeared in the device, i.e. we simulate the computation of the device, compute the corresponding result value and check whether it is identical with the found value Q̃ (n) . More precisely: we use pseudo-additions with points x 2 i+ ·P E for = 0, . . . , n − i − 1 where x = (x n−i−1 . . . x 0 ) 2 with x 0 = 1 is the binary (i) (i) representation of x to get for candidates i, x, Q x , and Q̃ x the corresponding faulty result

(i) i i+1 Q̃ (n) · P E ) ⊕ · · · ) ⊕ x n−i−1 2 n−1 · P E . x = (· · · (( Q̃ x ⊕ x 0 2 · P E ) ⊕ x 1 2

(n)

If Q̃ x is equal to the faulty result Q̃ (n) output by the device, then we have found (i) i as a candidate for j , Q̃ x as a candidate for Q̃ (j ) , and the binary representation of x as a candidate for the upper n − j bits of d.

j iterations

n-j iterations

Q (0)

~

Q (j)

Q (j)

~

Q (n)

Q (n)

By trying faults on Q and on H and all m possibilities for i and corresponding integers x we can make sure that this procedure outputs at least one candidate for Q̃ (j ) (or for H̃ (j) , in the case the fault occurs in H). In case there is only one candidate suitable for P E , Q (n) , m, and for Q̃ (n) we have computed the n − j upper bits of the secret key d. One can show that the probability is small that more than one candidate survives (more details can be found in the appendix). To reveal step by step all bits of d we start to compute the most signiﬁcant bits as explained above and work downwards to the least signiﬁcant bits by

<!-- PDF_PAGE: 11 -->

## PDF page 11

Diﬀerential Fault Attacks on Elliptic Curve Cryptosystems 141

iterating the same procedure with new random register faults in blocks of at most m iterations. In each step we use the information that we already know about d to restrict the range of test integers x which have to be considered.

Theorem 4. Let m = o(log log log q) and let n be the binary length of the secret multiplier. Assume that we can generate a register fault in an a-priory chosen block of m iterations of the multiplication algorithm. Using an expected number of O(n) register faults we can determine the secret key d in expected O(nm2 m (log q) 3 ) bit operations.

Finally, we consider the more general situation in which we cannot induce register faults in small blocks, but only at random moments during the multiplication. As in [4] one can show that for a large enough number of disturbed computations we get a reasonable probability that errors happen in each block of m iterations.

Theorem 5. Let E be an elliptic curve deﬁned over a ﬁnite ﬁeld with q ele- ments, let m = o(log log log q), and let n be the binary length of the secret mul- tiplier. Given = O((n/m) log(n)) faults, the secret key can be extracted from a device implementing the “right-to-left” multiplication algorithm in expected O(n 2 m (log q) 3 log(n)) bit operations.

Thus this theorem can be summarized as follows: if we consider the size of the used ﬁnite ﬁeld as a constant then we need O(n log(n)) accesses to the tamper- proof device to compute in O(n log(n)) bit operations the secret key of bit length n. Please notice that the block size m we used as parameter of our algorithm reﬂects the tradeoﬀ between the number of necessary register faults and the running time to analyse the output values inﬂuenced by these faults. It depends on the attackers situation whether more accesses to the tamper-proof device or more time for the analysis can be spent.

Remark 2. We have implemented a software simulation of the algorithm given above and attacked several hundred randomly chosen elliptic curves. Obviously, one can ﬁnd easily non-unique solutions for the indices j and the parts of x of the corresponding discrete logarithms if the order of the base point P E is small in comparison with 2 m where m is the length of the block containing the error. Also, if the size of the ﬁeld is very small (&lt; 1000) the algorithm often ﬁnds contradicting solutions. Both cases are not relevant for a cryptographically strong elliptic curve. In all tested examples with size of the ﬁeld bigger than 2 64 , randomly chosen curve, and random point on the curve we determined the complete secret multiplier d without problems.

If we apply this attack to the device computing the El-Gamal decryption as described in Sect. 2 we cannot determine the y-coordinate of the resulting point uniquely. Since we know the equation of the curve we can compute points Q and −Q such that the correct result Q (n) of the device is one of these points. We start the described attack on both points Q and −Q and compare only the x-coordinate of the disturbed results of the attack with the x-coordinate of the faulty result x( Q̃ (n) ) of the device. Using this procedure we ﬁnd at least one

<!-- PDF_PAGE: 12 -->

## PDF page 12

Ingrid Biehl, Bernd Meyer, and Volker Müller

142

candidate for some point Q̃ (j) (or for some point H̃ (j) , in the case the fault occurs in H) and can determine the upper bits of the secret multiplier d if the candidate is unique.

6 Countermeasures

It became obvious in the preceding sections that DFA techniques for elliptic curves depend mainly on the ability to disturb a point on E to “leave” the group of points and become an ordinary pair in P. Countermeasures against all attacks presented in this paper are therefore obvious. Although it is part of the protocols of most cryptosystems based on elliptic curves to check whether input points indeed belong to a given cryptographically strong elliptic curve it follows from the described attacks that it is even more important for the tamper-proof device to check the output point or any point which serves as basis for the computation of some output values. If any of these points, input points or computed points, do not satisfy this condition, no output is allowed to leave the device. This countermeasure for ECC is similar to the countermeasures proposed against DFA for RSA where the consistency of the output also has to be checked by the device.

Acknowledgements

We would like to thank the unknown referees for several suggestions which im- proved the quality and readability of the paper. Moreover, we would like to thank Susanne Wetzel and Erwin Heß for discussions. Our thank belongs especially to Arjen K. Lenstra who gave us a lot of support to improve the paper and pointed out to us the subexponential time attacks against El-Gamal decryption and EC DSA in Sect. 4.2.

### References

1. R. J. Anderson and M. G. Kuhn: Tamper Resistance – a Cautionary Note, Pro- ceedings of Second USENIX Workshop on Electronic Commerce 1996, pp. 1–11. 2. R. J. Anderson and M. G. Kuhn: Low Cost Attacks on Tamper Resistant Devices, Lecture Notes in Computer Science 1361, Proceedings of International Workshop on Security Protocols 1997, Springer, pp. 125–136. 3. E. Biham and A. Shamir: Diﬀerential Fault Analysis of Secret Key Cryptosystems, Lecture Notes of Computer Science 1294, Proceedings of CRYPTO’97, Springer, pp. 513–525. 4. D. Boneh, R. A. DeMillo, and R. J. Lipton: On the Importance of Checking Crypto- graphic Protocols for Faults, Lecture Notes of Computer Science 1233, Proceedings of EUROCRYPT’97, Springer, pp. 37–51. 5. M. Burmester: A Remark on the Eﬃciency of Identiﬁcation Schemes, Lecture Notes of Computer Science 473, Proceedings of EUROCRYPT’90, Springer, pp. 493–495. 6. I. Connell: Elliptic Curve Handbook, Preprint, 1996.

<!-- PDF_PAGE: 13 -->

## PDF page 13

Diﬀerential Fault Attacks on Elliptic Curve Cryptosystems 143

7. IEEE P1363 Draft Version 12: Standard Speciﬁcations for Public Key Cryptography, available on the Homepage of the IEEE. 8. O. Kömmerling and M. G. Kuhn: Design Principles for Tamper-Resistant Smart- card Processors, Proceedings of USENIX Workshop on Smartcard Technology 1999, pp. 9–20. 9. H. W. Lenstra: Factoring Integers with Elliptic Curves, Annals of Mathematics, 126 (1987), pp. 649–673. 10. C. H. Lim and P. J. Lee: A Key Recovery Attack on Discrete Log-based Schemes Using a Prime Order Subgroup, Lecture Notes of Computer Science 1294, Proceed- ings of CRYPTO’97, Springer, pp. 249–263. 11. A. Menezes: Elliptic Curve Public Key Cryptosystems, Kluwer Academic Publish- ers, 1993. 12. S. Pohlig and M. Hellman: An Improved Algorithm for Computing Logarithms over GF(p) and its Cryptographic Signiﬁcance, IEEE Transactions on Information Theory, vol. 24 (1978), pp. 106–110. 13. J. H. Silverman: The Arithmetic of Elliptic Curves, Graduate Texts in Mathematics 106, Springer 1986.

Appendix: Success Probability of the Attack in Sect. 5

We denote by Q (i) resp. H (i) the value stored in the variable Q resp. H before iteration i of the right-to-left multiplication algorithm described in Sect. 5. We know also the correct result Q (n) = d · P E and a faulty result Q̃ (n) for a given base point P E on E. We deﬁne a disturbed Q-value with respect to P E , Q (n) , m to be a pair in 2 P that diﬀers in exactly one bit from some Q (i) for n − m ≤ i ≤ n. Assume that we enforce a register fault in iteration n − m ≤ j &lt; n, and that this fault ﬂips one bit in a register holding the variable Q. Denote by Q̃ (j) the resulting disturbed Q-value. According to the right-to-left multiplication algorithm we try all possible indices n − m ≤ i &lt; n and all integers x with exactly n − i (i) bits (least signiﬁcant bit 1) to compute candidates Q̃ x for disturbed Q-values that lead to the faulty result Q̃ (n) . The second place where a register fault can happen is the register holding the variable H in the algorithm. The procedure for this case is quite similar. Again, we try all possible indices n − m ≤ i &lt; n and all integers x of exactly n − i bits (least signiﬁcant bit 1). If the fault is now introduced in the variable H (i.e. into one of the points H (i) = 2 i · P E ), this results in some disturbed H-value H̃ (i) and is then propagated by the loop of the algorithm. By trying both Q- and H-case and all m possibilities for i and corresponding integers x we can make sure that this procedure outputs at least one candidate for Q̃ (j) or for H̃ (j) . In case there is only one candidate suitable for P E , Q (n) , m and for Q̃ (n) we call this candidate a uniquely determined disturbed value with respect to P E , Q (n) , m. Otherwise, a candidate is called non-uniquely determined disturbed value. In Lemma 2 we will prove that for m = o(log log log q), all d and almost all points P E there are at most three diﬀerent non-uniquely disturbed values. Thus the expected number of necessary repetitions of attacks (i.e. choosing a point

<!-- PDF_PAGE: 14 -->

## PDF page 14

Ingrid Biehl, Bernd Meyer, and Volker Müller

144

P E and causing a random register fault in the last m iterations), until one ﬁnds a uniquely determined disturbed value, is constant. Next we give an estimate for the probability that an attack allows us to ﬁnd a uniquely determined disturbed value. For background on elliptic curve theory, we recommend [6] or [13].

Lemma 1. Let m = o(log log log q) and assume that we can generate register faults in the last m iterations of the algorithm. The number of points P E for which there exist more than three diﬀerent non-uniquely determined disturbed values with respect to P E , Q (n) , m is bounded by O((log log q)(log q) 5 ).

Proof. We want to bound the number of points P E for which there exists at least four diﬀerent non-uniquely determined disturbed values with respect to P E , Q (n) , m. Thus there are at least two pairs of disturbed values where each pair leads under the secret key d with Q (n) = d · P E to the same faulty multiplication result. Since these disturbed values are either H- or Q-values the following cases must be considered: each such pair either consists of two disturbed Q-values, or two disturbed H-values or is a pair consisting of one disturbed Q- and one disturbed H-value. We show for all nine cases that the number of points P E for which there exists four diﬀerent non-uniquely disturbed values can be bounded by O((log log q)(log q) 5 ). We consider the ﬁrst case that all four non-uniquely disturbed values are Q-values. Then there exist integers x i of binary length at most m, points P i ∈ E(IF q ), and bit locations r i for 1 ≤ i ≤ 4 such that

1. 2. 3. 4.

P 1 + x 1 · R = P 2 + x 2 · R = Q (n) , P 1,(r 1 ) ⊗ x 1 R = P 2,(r 2 ) ⊗ x 2 R, P 3 + x 3 · R = P 4 + x 4 · R = Q (n) , P 3,(r 3 ) ⊗ x 3 R = P 4,(r 4 ) ⊗ x 4 R,

where n is the binary length of the secret multiplier, R = 2 n−m ·P E , P i,(j) denotes a pair which is obtained by switching bit j of point P i (numbering the bits of x- and y-coordinate appropriately), and the notation P ⊗w·R serves as abbreviation for the computation (· · · ((P ⊕ w 0 · R) ⊕ w 1 · 2 · R) ⊕ · · · ) ⊕ w k−1 · 2 k−1 · R for an integer w = (w k−1 . . . w 0 ) 2 . (The values P i,(j) are the non-uniquely determined disturbed values to the faulty results P 1,(r 1 ) ⊗ x 1 R, and P 3,(r 3 ) ⊗ x 3 R.) We translate the four conditions above into polynomial equations using the concept of formal points. Assume that P 1 is given formally as (X 1 , Y 1 ) and R as (X 2 , Y 2 ). Using the theory of division polynomials (see [6]), it follows directly that the X 2 -degree of the numerator, denominator, of points x · R for arbitrary m-bit integers x is O(2 2m ). Combining the ﬁrst and third equation (note that Q (n) occurs in both equations), we see with the addition formulas that the x- coordinates of all the points P i , i ≥ 2, can be written as rational functions of constant degree in X 1 , Y 1 , Y 2 and of degree O(2 cm ) in X 2 for some small con- stant c (both numerator and denominator). The essentially same idea can be used to ﬁnd an equation from the second and the fourth equation: we compute the left hand side as rational functions (using the representation of P 1 , P 3 in X 1 , Y 1 , X 2 , Y 2 , respectively), introducing new variables for the faults r 1 , r 3 . Sim- ilarly, we transform the right hand side of the second and fourth equation into

<!-- PDF_PAGE: 15 -->

## PDF page 15

Diﬀerential Fault Attacks on Elliptic Curve Cryptosystems 145

a rational function, introducing new variables for the faults r 2 , r 4 and using the representation of P 2 , P 4 as function in X 1 , Y 1 , X 2 , Y 2 . Then we can derive a poly- nomial of X 1 , X 2 -degree O(2 c m ) for some small constant c . Using the fact that both P 1 and R are points on E, we can remove the variables Y 1 , Y 2 with the help of the curve equation, increasing the exponent in the degree formula by a constant. Finally, we determine the resultant in the variable X 2 of both these c m ) equations, thereby removing X 2 and getting an equation of X 1 -degree O(2 2 for some constant c (the resultant can be determined by computing the deter- minant of the so called Sylvester matrix). By substituting all possible values for r i , 1 ≤ i ≤ 4, (note that r i are bit faults) and substituting all possible values for x i , 1 ≤ i ≤ 4, (note that 0 ≤ x i ≤ 2 m ), and observing that m = o(log log log q) c m and so O(2 2 ) = O(log q), we get O(2 4m (log q) 4 ) = O((log log q)(log q) 4 ) equa- tions of X 1 -degree O(log q) each. Therefore, the total number of possibilities for X 1 and the number of possible points P E is at most O((log log q)(log q) 5 ). The number of points P E for the other cases can be analyzed analogously.

Lemma 2. Let m = o(log log log q) and q be suﬃciently large. The expected number of attacks, i.e. random choices of a point P E of E(IF q ) and random register faults in the last m iterations of the right-to-left multiplication algorithm, until one ﬁnds a uniquely determined disturbed value, is 2.

Proof. Since E(IF q ) is cryptographically strong, it contains a subgroup of prime order p with p &gt; log q q . Using the Hasse theorem it follows from the previous lemma that we will get a point P E with probability 1 − c(log log q)(log q) 5 /q (for some constant c) of order at least p and for which there exists at most three diﬀerent non-uniquely determined disturbed values with respect to P E , Q (n) , m. Since at least all H (i) for i = n − m, . . . , n are diﬀerent and consist of 2 log q bits, there are O(m log q) bit positions in the computation process which could be disturbed. Since there are less than four non-uniquely determined disturbed values for P E the probability to disturb the computation in a way which will lead to one of these non-uniquely determined disturbed values is bounded by 3/(m log q). It follows that with probability more than 1/2 each attack will lead to a uniquely determined disturbed value.

Lemma 3. Let m = o(log log log q). Assume that we can generate random regis- ter faults in the last m iterations of the algorithm of the attack. Then the expected number of applications of the algorithm with independent random register faults is O(m) until we can compute the m most signiﬁcant bits of the secret key d. Thus the expected number of bit operations is O(m 2 2 m (log q) 3 ).

Proof. For a running time analysis we note that the number of fault positions is at most 4 log q in each iteration (there are at most 2 points that can be disturbed, the x- and y-coordinate of each point have at most log q bits). For each of the 2 m+1 diﬀerent integers x we have at most m pseudo-additions which can be done in O(m(log q) 2 ) bit operations each. In addition we have to compute for

<!-- PDF_PAGE: 16 -->

## PDF page 16

Ingrid Biehl, Bernd Meyer, and Volker Müller

146

all indices n − m ≤ j &lt; n the corresponding values Q (j) and H (j) which can be done in O((log q) 3 ) bit operations. We learn all m most signiﬁcant bits of d if the error changes the value H (n−m) . The probability that a random error during the last m iterations disturbs a bit 1 of H (n−m) is 2m . Therefore, we can lower bound the probability of success if 1 k we have k independent randomly disturbed results by 1 − (1 − 2m ) . Since the register faults are induced at random places, we derive that we expect to need k = O(m) many faulty applications before we have found all the upper m bits of d. Combining all the partial results, we get the expected O(m 2 2 m (log q) 3 ) bit operations.

Lemma 2 is the basis for an algorithm to determine the complete multiplier d. The basic idea is the usage of Lemma 2 successively on blocks of size m. Note the fact that we can “compute backwards” once we know the upper m bits of d to generate a DL problem with a smaller multiplier. Computing backwards from the correct output of the device for a given base point to get a correct intermediate point is trivial. For the disturbed output of the device it follows from Theorem 1 that we can compute backwards the faulty result with high probability too to get a faulty intermediate result. Then we can apply Lemma 2 again on the pair of correct intermediate point and faulty intermediate result. Thus we get:

Theorem 6. Let m = o(log log log q) and let n be the binary length of the secret multiplier. Assume that we can generate a register fault in a block of m iterations of the right-to-left multiplication algorithm. Using an expected number of O(n) register faults we can determine the secret key d in expected O(nm2 m (log q) 3 ) bit operations.
