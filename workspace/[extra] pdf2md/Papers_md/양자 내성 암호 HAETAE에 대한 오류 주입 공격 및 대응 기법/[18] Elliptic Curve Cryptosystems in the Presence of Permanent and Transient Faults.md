# [18] Elliptic Curve Cryptosystems in the Presence of Permanent and Transient Faults

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 11
converted_at: "2026-07-26"
source_asset_id: "HAETAE-FIA-REF-18"
derived_asset_id: "HAETAE-FIA-REF-18-MD"
source_path: "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[18] Elliptic Curve Cryptosystems in the Presence of Permanent and Transient Faults.pdf"
source_sha256: "acd20afc928f4914bc73485cc449531e42ea16263fa079622028165a1e7093b4"
pages: 11
bbox_words: 6217
consumed_bbox_words: 6217
numeric_tokens: 643
consumed_numeric_tokens: 643
source_blocks: 166
consumed_source_blocks: 166
emitted_blocks: 155
embedded_raster_images: 0
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 11
glyph_chars_removed: 3
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

Designs, Codes and Cryptography, 36, 33–43, 2005 © 2005 Springer Science+Business Media, Inc. Manufactured in The Netherlands.

Elliptic Curve Cryptosystems in the Presence of Permanent and Transient Faults

MATHIEU CIET ∗ ciet@dice.ucl.ac.be Université Catholique de Louvain, UCL Crypto Group, Place du Levant 3, 1348 Louvain-la-Neuve, Belgium

MARC JOYE marc.joye@gemplus.com Gemplus, Card Security Group, La Vigie, Avenue du Jujubier, ZI Athélia IV, 13705 La Ciotat Cedex, France

Communicated by: P. Wild

Received December 11, 2002; Revised August 26, 2003; Accepted September 11, 2003

Abstract. Elliptic curve cryptosystems in the presence of faults were studied by [Biehl et al., Advances in Cryptology – CRYPTO 2000, Springer Verlag (2000) pp. 131–146]. The ﬁrst fault model they consider requires that the input point P in the computation of dP is chosen by the adversary. Their second and third fault models only require the knowledge of P . But these two latter models are less ‘practical’ in the sense that they assume that only a few bits of error are inserted (typically exactly one bit is supposed to be disturbed) either into P just prior to the point multiplication or during the course of the compu- tation in a chosen location. This paper relaxes these assumptions and shows how random (and thus unknown) errors in either coordinates of point P , in the elliptic curve parameters or in the ﬁeld representation enable the (partial) recovery of multiplier d. Then, from multiple point multiplications, we explain how this can be turned into a total key recovery. Simple precautions to prevent the leakage of secrets are also discussed.

Keywords: elliptic curve cryptography, fault analysis, fault attacks, information leakage

1. Introduction

Elliptic curve cryptography was introduced in the mid 1980s independently by Koblitz [14] and Miller [21] as a promising alternative for cryptographic protocols based on the discrete logarithm problem in the multiplicative group of a ﬁnite ﬁeld (e.g., Difﬁe-Hellman key exchange or ElGamal encryption/signature). The security of elliptic curve cryptosystems relies on the hardness of solving the elliptic curve discrete logarithm problem (ecdlp): given points P and Q = dP on an elliptic curve, one has to recover multiplier d.

∗ The

work described in this paper has been supported [in part] by the Commission of the Euro- pean Communities through the IST Programme under Contract IST-1999-12324, http://www.cryptones- sie.org/. The information in this document is provided as is, and no guarantee or warranty is given or implied that the information is ﬁt for any particular purpose. The user thereof uses the information at his sole risk and liability. The views expressed are those of the authors and do not represent an ofﬁcial view/position of the NESSIE project (as a whole).

<!-- PDF_PAGE: 2 -->

## PDF page 2

34

CIET AND JOYE

1.1. Physical Security

Kocher et al. introduced the notion of side-channel analysis in [15, 16] and showed the importance for an implementation of being resistant against side-channel analysis (e.g., secret leakage from power consumption). Resistance against fault analysis [7, 5] is another threat and should be taken into account, since sensitive informa- tion may leak when the cryptosystem operates under unexpected conditions. The security of point multiplication on elliptic curves in the presence of faults was considered by Biehl et al. [4]. They extended fault attacks initially mounted against the RSA cryptosystem to schemes using elliptic curves. Remarking that elliptic curve parameter a 6 is not used in the classical addition formulæ on elliptic curves, they made the key observation that a random element (x̃, ỹ) (not on the original elliptic curve) may deﬁne a group for which it is computationally feasible = (x̃, ỹ), they were to solve the ecdlp. Therefore, by forcing the input point as P . able to derive information about d from the output value d P Many elliptic curve cryptosystems do not allow to choose (or force) the input point. In the second part of their paper, Biehl et al. suppose that an error of one bit occurs and then try to recover it by successive search.

1.2. Our Contribution

In this paper, we rather consider a more practical scenario and give several reﬁne- ments of [4]. Typically, in a cryptographic device, the system parameters are stored in non- volatile memory (e.g., eeprom) and are then transferred into working memory (e.g., ram), when needed, for the elliptic curve computations. In our ﬁrst model, we assume that there is a permanent fault, in a unknown position, in any system parameter deﬁning the elliptic curve over which the computations are carried out. In our second model, we analyze the consequences of faults during the trans- fer of the system parameters into working memory. We call such a fault a tran- sient fault. In both models, we explain how this may yield information on (secret) multiplier d. The rest of this paper is organized as follows. In the next section, we review the basics of elliptic curve cryptography. Then, in Section 3, we exhibit how the presence of faults in the public parameters of an elliptic curve cryptosystem may expose the secret key. Finally, we conclude in Section 4.

2. Elliptic Curve Cryptography

An elliptic curve over a ﬁeld K is the set of points (x, y) ∈ K × K satisfying the Weierstraß equation

E /K : y 2 + a 1 xy + a 3 y = x 3 + a 2 x 2 + a 4 x + a 6

(1)

along with the point O at inﬁnity. This set of points form an additive group where O is the neutral element and where the group law is given by the

<!-- PDF_PAGE: 3 -->

## PDF page 3

35

ELLIPTIC CURVE CRYPTOSYSTEMS

‘chord-and-tangent’ rule. The inverse of a point P 1 = (x 1 , y 1 ) is −P 1 = (x 1 , −y 1 − a 1 x 1 − a 3 ). Given two points P 1 = (x 1 , y 1 ) and P 2 = (x 2 , y 2 ) (with P 1 = −P 2 ), the sum P 3 = P 1 + P 2 = (x 3 , y 3 ) is deﬁned as

x 3 = λ 2 + a 1 λ − a 2 − x 1 − x 2 and y 3 = (x 1 − x 3 )λ − y 1 − a 1 x 3 − a 3   3x 1 2 +2a 2 x 1 +a 4 −a 1 y 1 if P 1 = P 2 , with λ = y −y 2y 1 +a 1 x 1 +a 3  1 2 otherwise.

(2)

x 1 −x 2

Remark . When the characteristic of K, Char K, is a ‘large’ prime (namely, ≥ 5), one can take a 1 = a 2 = a 3 = 0 in the Weierstraß parameterization, without loss of generality. Likewise when Char K = 2, one can take a 1 = 1 and a 3 = a 4 = 0, provided that the elliptic curve is non-supersingular. This is the case of interest for crypto- graphic applications since supersingular curves are prone to the mov attack [19].

The scalar multiplication (or point multiplication) is the operation consisting in computing Q = dP = P + P + · · · + P (d times). A related operation is the discrete logarithm, which consists in computing d from P and Q = dP , and is the basis for the security of cryptographic schemes based on elliptic curves over ﬁnite ﬁelds [14, 21]. The discrete logarithm problem on a general elliptic curve (ecdlp) is par- ticularly attractive since there is no known sub-exponential algorithm to solve it. The best method available for attacking the ecdlp is Pollard’s method [22, 23] and variants thereof.

3. Permanent and Transient Faults

Consider the elliptic curve E(a 1 , a 2 , a 3 , a 4 , a 6 ) over K given by equation (1). In [4], Biehl et al. observe that parameter a 6 is not involved in the addition formulae (cf. equation (2)). Consequently, if a cryptographic device (e.g., a smart card) receives = (x̃, ỹ) ∈ K × K but P ∈ on input a ‘point’ P / E then the scalar multiplication d P will take place over the curve E(a 1 , a 2 , a 3 , a 4 , a 6 ) with

6 = ỹ 2 + a 1 x̃ ỹ + a 3 ỹ − x̃ 3 − a 2 x̃ 2 − a 4 x̃ a

instead of over the original curve E(a 1 , a 2 , a 3 , a 4 , a 6 ). 1 , a 2 , a 3 , a 4 , is chosen so that E(a Assume that point P a 6 ) is an elliptic curve as an whose order has a small (or smooth) factor r and that the order of P element of E, ord E ( P ), is equal to r. Then, provided that discrete logarithms , the subgroup of order r generated by P , the value of d are computable in P 1 (mod r) can be recovered. Therefore, repeating the process with sufﬁciently many i yields the values of d mod r i (where r i = ord E ( P i )) from different chosen points P i i , and so the whole value of d, by Chinese remaindering. d P

Most elliptic curve cryptosystems take a determined point P on input, mak- ing the previous attack inapplicable (a noteworthy exception is the basic ElGamal

<!-- PDF_PAGE: 4 -->

## PDF page 4

36

CIET AND JOYE

encryption [9]). Indeed, being a system parameter, point P is stored in the non- volatile memory of the cryptographic device and is read from that memory for the computation of dP . In this section, we analyze the implications of permanent faults (intentional or acci- dental) in non-volatile memory, where the system parameters are stored. We alter- nately consider permanent faults in the representation of point P , in the deﬁnition ﬁeld K, and in curve parameters {a 1 , . . . , a 6 }. Our analysis also extends to transient faults originating from a perturbation of the reading in non-volatile memory, and resulting in faulty values for the system parameters actually used in working mem- ory, throughout the computation. The difference between the two models is that a transient fault, as deﬁned, is ﬁxed throughout a single execution (but may vary from one execution to another one) whereas a permanent fault always sticks invariant.

3.1. Faults in the Base Point

Without loss of generality, we assume that the x-coordinate of point P is cor- rupted (the case of a corrupted y-coordinate is similar). The cryptographic device = d P with P = (x̃, y). Contrary to the case considered in [4], the then computes Q is unknown but ﬁxed (in particular, there is no hypothesis on the num- value of P from the output ber of ﬂipped bits). It is however easy to recover the value of P value Q = d(x̃, y) = (x̃ d , ỹ d ). Point Q deﬁnes the curve E on which the computation 1 , a 2 , a 3 , a 4 , was carried out, i.e., E(a a 6 ) with

6 = ỹ d 2 + a 1 x̃ d ỹ d + a 3 ỹ d − x̃ d 3 − a 2 x̃ d 2 − a 4 x̃ d . a

(3)

= (x̃, y) ∈ Therefore, since P E, it follows that x̃ is a root in K of the polynomial (over K[X]) given by

X 3 + a 2 X 2 + (a 4 − a 1 y)X + ( a 6 − y 2 − a 3 y).

Suppose ﬁrst that this polynomial has a unique root, which must be x̃. Provided that is small (or smooth) enough so that the ) (i.e., the order of P = (x̃, y) in E) r = ord E ( P discrete logarithm of Q w.r.t. P is computable, the value of d mod r can be recovered. If now the above polynomial has 2 or 3 roots, then there are 2 or 3 possible candidates for x̃. In the permanent-fault model, the ambiguity can however be removed by assuming that only a portion of x is corrupted (remember that param- eter P = (x, y) is public). Hence, the candidate having the most bits matching those of x is likely to be x̃. In the transient-fault model, the whole value of x is likely to be corrupted; the actual value of x̃ is then known with probability 1, 2 1 or 13 , = (x̃, y) is known (or more according to the number of candidates. Next, once P exactly, guessed), the value of d mod r can be recovered.

= (x, ỹ)) then ỹ is Remark . If it is the y-coordinate of P that is corrupted (i.e., P a root of a polynomial of degree 2 and the above methodology applies to recover

<!-- PDF_PAGE: 5 -->

## PDF page 5

37

ELLIPTIC CURVE CRYPTOSYSTEMS

the value of d mod r. (Note that an error in the y-coordinate only makes sense when there is no point compression 2 —with point compression, an error merely changes P into −P .) A more intricate case appears when both the x- and the y-coordinates of P are = (x̃, ỹ) the corresponding point. As before, the output corrupted. We write P = (x̃ , ỹ ) yields the value of a value d P 6 from equation (3). But it seems that there d d ; we only know that it lies on the curve is no way to recover the whole value of P . For E(a 1 , a 2 , a 3 , a 4 , a 6 ). Further assumptions are needed to completely recover P example, in case of permanent fault, if it is possible to ﬂip one bit of d, say bit can be obtained as then the value of ±2 i P d i , during the computation of d P − d P where d P

d = d + (¬d i − d i ) 2 i .

1 , a 2 , a 3 , a 4 , on E(a a 6 ) eventually yields the value of Successively halving ±2 i P ± P . Then, once ± P is retrieved, the value of ±d mod r can be recovered. This extends the attacks of [3, 13] in the sense that more information on secret d (i.e., ±d mod r) can be recovered.

3.2. Faults in the Deﬁnition Field

We now suppose that the representation of ﬁeld K in non-volatile memory is faulty (permanent fault) or that an error occurred in the transfer from non-volatile mem- ory to working memory (transient fault). We have to handle the cases K = F p and K = F 2 q separately since their internal representations are different.

3.2.1. Large Prime Field Let p be a large prime number. The ﬁeld F p is simply represented by the value of p, stored as a binary string in non-volatile memory. An error on K means in this case an error in the representation of p. We let p̃ denote the faulty value. The computations are then carried out modulo p̃ instead of modulo p. As mentioned in Section 2, elliptic curves over a large prime ﬁeld are given by the simpliﬁed equation

E /F p : y 2 = x 3 + a 4 x + a 6 .

= (x̃, ỹ) where x̃ ≡ x (mod p̃) and ỹ ≡ y Over F p̃ , point P = (x, y) becomes P deﬁned on the curve E (mod p̃). The computation of dP on E is replaced by d P by 3

/Z : y 2 = x 3 + E a 4 x + a 6 p̃

= d P = (x̃, ỹ) and Q = (x̃ d , ỹ d ) are points on where a 4 ≡ a 4 (mod p̃). Since both P E, we deduce that

a 4 x̃ ≡ y 2 − x 3 − a 4 x ≡ ỹ d 2 − x̃ d 3 − a 4 x̃ d 6 ≡ ỹ 2 − x̃ 3 − a

(4)

(mod p̃).

<!-- PDF_PAGE: 6 -->

## PDF page 6

38

CIET AND JOYE

d = ỹ 2 − x̃ 3 − a 4 x̃ (R and R d are evaluated over Letting R = y 2 − x 3 − a 4 x and R d d d d . Consequently, the fac- Z), the previous relation implies that p̃ divides = R − R torization of will reveal the value of p̃ as the combination of the factors of whose product has the most bits matching those of p. If no such p̃ is found (e.g., a transient fault gave rise to a random value for p̃), we have to assume that the original prime, p, satisﬁes additional properties. A concrete example is discussed in § 3.2.3.

Remark . Although being a 3k-bit integer (where k is the bit-length of prime p), is within the range of modern factorization algorithms since k is typically a 160- bit integer. Furthermore, when the fault is permanent, the length of the number to . be factored can be lowered from an additional scalar multiplication with point P Let Q = d P = (x̃ d , ỹ d ) with d = d. Then (x̃ d , ỹ d ) satisﬁes equation (4) and, letting d , it follows that p̃ must divide gcd(, ). If d = ỹ 2 − x̃ 3 − a 4 x̃ and = R − R R d d d further (distinct) scalar multiplications are available, p̃ can be obtained easilier as a factor of gcd(, , , . . . ).

We now assume that the value of p̃ is known. Let p̃ = li=1 q̃ i e i denote the prime factorization of p̃. Consider the direct product of groups

1 (Z/q̃ 1 Z) × · · · × E l (Z/q̃ e l Z). G = E l 1

e

= k P corresponds was supposed successful, point Q Since the computation of Q 1 , . . . , i = Q mod q̃ e i [18, § 2.5]. to a unique element of G, namely ( Q Q ) with Q i l ) denotes the order of P viewed as an element of the ellip- Hence, if r i = ord E i ( P i (i.e., P i i = P mod q̃ e i ), then solving the discrete logarithm in P i ⊆ E tic curve E i yields the value of d mod r i so that by Chinese remaindering the value of

d mod lcm(r 1 , . . . , r l )

can be calculated.

3.2.2. Binary Field The ﬁeld F 2 q is usually regarded as a quotient F 2 [X]/(P) where P is an irreducible polynomial of degree q over F 2 . Each element α ∈ F 2 q is represented as a binary q−1 string (α 0 . . . α q−1 ) corresponding to polynomial i=0 α i X i (mod P(X)) in F 2 [X]. With this polynomial representation, the ﬁeld F 2 q is determined by polynomial P, which is stored in non-volatile memory as a binary string (b 0 . . . b q−1 b q ) corre- q sponding to P(X) = i=0 b i X i with b q = 1. Over F 2 q , a (non-supersingular) elliptic curve is given by the simpliﬁed Weierstraß equation

E /F 2 q : y 2 + xy = x 3 + a 2 x 2 + a 6 .

Remark . There exist other representations for elements of F 2 q . A common choice is the normal basis representation. We shall not consider this representation here,

<!-- PDF_PAGE: 7 -->

## PDF page 7

39

ELLIPTIC CURVE CRYPTOSYSTEMS

as optimized implementations of elliptic curve doubling with normal bases make use of parameter a 6 [1, §. A.10.2]. Our analysis, however, implies that parameter a 6 is not used. Moreover, we assume that afﬁne coordinates are used, as a projective doubling needs the value of a 6 [1, §. A.10.6]. Furthermore, note that afﬁne coordi- nates lead to faster arithmetic than projective coordinates [8] in binary ﬁelds with polynomial representation.

Suppose that K = F 2 q is faulty, namely that there is an error in the represen- q tation of P. As a result, computations are performed modulo P(X) = i=0 b̃ i X i instead of modulo P(X). Viewing elements as polynomials over K[X], similarly to can be recovered by observing that prime case, polynomial P

6 ≡ y 2 + xy + x 3 + a 2 x 2 ≡ ỹ d 2 + x̃ d ỹ d + x̃ d 3 + a 2 x̃ d 2 (mod P(X)) a

and P ≡ P (mod P(X)). Hence, letting where (x̃ d , ỹ d ) = d P

(X) = y 2 + xy + x 3 + a 2 x 2 + ỹ d 2 + x̃ d ỹ d + x̃ d 3 + a 2 x̃ d 2

(over F 2 [X]),

(5)

it follows that P(X) divides (X). So, given the factorization of , trying all pos- as the polynomial whose representation best matches sible combinations yields P the representation of P. Further, in case of permanent fault, an additional scalar as a factor of = d P with d = d, eases the recovery of P multiplication, Q gcd(, ) where is deﬁned from Q . In § 3.2.3, we When the fault is transient, it is always possible to distinguish P. present a technique that can successfully recover P in most practical implementa- tions. q If polynomial P(X) = i=0 b i X i representing the ﬁeld F 2 q is modiﬁed into poly- q is no longer irreducible over nomial P(X) = i=0 b̃ i X i , it is very probable that P F 2 . Hence, we can write P as the product

e e P = P 1 1 . . . P l l

i are distinct irreducible polynomials in F 2 [X] and e i are positive integers. where P P), we can collect informa- From the structure of the class residue ring F 2 [X]/( i . Let P i ) be the representative of i (resp. Q tion modulo the irreducible factors P viewed as an element in the ﬁeld F q̃ i ∼ (resp. Q) P 2 = F 2 [X]/( P i ) where q̃ i = deg( P i ), i ). Therefore, the discrete logarithm of Q i = Q mod P i i = P mod i.e., P P i (resp. Q i (F q̃ i ) is d mod r i , where r i = ord E ( P i = i in the group P i ⊆ E i ) and E w.r.t. P 2 i i ( E a 2,i , a 6,i ) with

i (X)) and a (mod P 6,i ≡ y 2 + xy + x 3 + a 2 x 2

i (X)). (mod P

2,i ≡ a 2 a

i yields the value of Hence, Chinese remaindering on each subgroup E

d mod lcm(r 1 , . . . , r l ).

Remark that, when q̃ i is composite, the computation of discrete logarithms in i (F q̃ i ) can be speeded up by Weil descent [11] (see also [17, 20, 24] for a thor- E 2 ough analysis and [10, 12] for recent developments).

<!-- PDF_PAGE: 8 -->

## PDF page 8

40

CIET AND JOYE

3.2.3. Unknown Error is known. The above analysis implies that the error on the representation of K When only a portion of the representation of K is damaged, we choose for the candidate best matching K. In some cases, the error on (the representa- K tion of) K is completely random so that it is no longer possible to determine as a set obtained by combining the resulting K. We can merely restrict K several known prime factors (case K = F p ) or irreducible polynomials (case K = F 2 q ). In this paragraph, we take advantage of some particularities of elliptic curves recommended for practical implementations to recover the right combination lead- ing to K when the ‘best-matching’ strategy does not apply. Over prime ﬁelds, the security of elliptic curve cryptography does not depend on the form of the primes. For example, in order to optimize the efﬁciency of ﬁeld arithmetic, the elliptic curves recommended by the NIST [2] 4 are deﬁned over F p where p is a (generalized) Mersenne prime, that is, a prime of the form

B

p = 2 ω 0 − ±2 ω i

i=1

where B is chosen small [25]. Hence, if p is a Mersenne prime with B ≤ 4 (this includes all NIST curves), it can be stored much more economically as {ω 0 , σ 1 ω 1 , σ 2 ω 2 , σ 3 ω 3 , σ 4 } and reconstructed in working memory as

3

p = 2 ω 0 + σ i 2 ω i + σ 4

(6)

i=1

with σ 1 , σ 2 , σ 3 ∈ {−1, 0, 1} and σ 4 ∈ {−1, 1}. In this case, an error on p means an error on ω 0 , σ 4 and/or σ i ω i for some 1 ≤ i ≤ 3. Then, instead of testing the com- binations of factors of having the most bits matching those of p (cf. § 3.2.1), we can conclude that the faulty p̃ is a number obtained as a combination of the fac- tors of , whose product can be written as a Mersenne number (non necessarily prime) satisfying equation (6). This additional assumption drastically reduces the number of candidates for p̃ and may allow to recover the value of p̃ even if the error is random (i.e., unknown). A similar assumption holds for binary ﬁelds. For every q up to 1000, there exists an irreducible pentanomial P(X) = X q + X q 1 + X q 2 + X q 3 + 1 to represent the ele- ments of F 2 q as polynomials in F 2 [X]/(P) [1, § A.8]. Since the reduction of poly- nomials modulo a pentanomial is efﬁcient, we may assume that only pentanomials are accepted for representing F 2 q (again, this includes all NIST curves 5 ) and that they are stored in a compact way as {q, q 1 , q 2 , q 3 }. An error on P translates in an error on q, q 1 , q 2 and/or q 3 , which can be easilier recovered by testing the fac- tors of (cf. § 3.2.2) that combine into a pentanomial P(X) = X q̃ + X q 1 + X q 2 + q 3 X + 1.

<!-- PDF_PAGE: 9 -->

## PDF page 9

41

ELLIPTIC CURVE CRYPTOSYSTEMS

3.3. Faults in the Curve Parameters

As parameter a 6 is not needed in the addition formulæ, a modiﬁcation of its value does not affect the computation of dP . So we only consider the situation of an error occurring in curve parameters a 1 , a 2 , a 3 or a 4 . To ﬁx the ideas, we assume that parameter a 4 is faulty (the other cases are similar). We let a 4 denote the corrupted value. As previously, since a 6 is not employed in the addition formulae, computations are performed on the curve = dP = (x̃ d , ỹ d ) lie E(a 1 , a 2 , a 3 , a 4 , a 6 ). Furthermore, since both P = (x, y) and Q on the curve E, we have the system of equations

4 x + a a 6 = y 2 + a 1 xy + a 3 y − x 3 − a 2 x 2 4 x̃ d + a a 6 = ỹ d 2 + a 1 x̃ d ỹ d + a 3 ỹ d − x̃ d 3 − a 2 x̃ d 2

whose resolution (over K) gives the values of a 4 and a 6 .

Remark . In the (very) unlikely event where the two equations are linearly depen- dent, the process can be re-iterated with another scalar multiplication.

After resolving the system of equations for ã 4 and ã 6 , we compute the logarithm of Q w.r.t. P in P ⊆ E(a 1 , a 2 , a 3 , a 4 , a 6 ) and get the value of d mod r, where r = ord E (P ).

4. Concluding Remarks

We have shown that a (permanent) fault in the system parameters may enable one to recover the value of d (mod r). However, it is fairly easy to avoid the leakage of d (mod r) by checking the parameters for faults prior to the computation of Q = dP . This can be done by adding a crc to each system parameter. Then, after reading a system parameter in non-volatile memory, its crc is computed and compared with the crc stored in non-volatile memory. Another possibility is to use curve parameter a 6 as an integrity check (i.e., a 6 is used to verify whether the coordinates of point P = (x, y) satisfy, over K, the relation y 2 + a 1 xy + a 3 y − x 3 − a 2 x 2 − a 4 x = a 6 ). To prevent the leakage of d (mod r) in the presence of a transient fault, we have shown that the system parameters actually used (i.e., in working memory) must also be checked during the computation of Q = dP . In addition, we recommend to perform a check on point Q just before outputting it. More importantly, our analysis teaches that not only the secret parameters (e.g., a secret key) but also the public parameters must be checked for faults.

Acknowledgments

Part of this work was done while the ﬁrst author was visiting Gemplus. Thanks go to David Naccache, Philippe Proust and Jean-Jacques Quisquater for making this arrangement possible.

<!-- PDF_PAGE: 10 -->

## PDF page 10

42

CIET AND JOYE

Notes

1.

Note that r needs not be prime —when r is a smooth composite number, discrete logarithms can be attacked with the Pohlig–Hellman algorithm. If the x-coordinate of point P is ﬁxed, its y-coordinate satisﬁes a quadratic in y. Since a single bit is sufﬁcient to distinguish between the two possible solutions of a quadratic, a point can be com- pressed into its x-coordinate and this additional bit. When p̃ is not prime, Z p̃ = Z/p̃ Z is no longer a ﬁeld but a ring. As a result, the computation of is not guaranteed to succeed. This occurs when the computation involves a point that is on E d P the point at inﬁnity modulo a factor p̃ 1 of p̃ but not modulo p̃ 2 = p̃/p̃ 1 . The 5 NIST elliptic curves over large prime ﬁelds are deﬁned with the Mersenne primes 2 192 − 2 64 − 1 (curve P-192), 2 224 − 2 96 + 1 (curve P-224), 2 256 − 2 224 + 2 192 + 2 96 − 1 (curve P-256), 2 384 − 2 128 − 2 96 + 2 32 − 1 (curve P-384) and 2 521 − 1 (curve P-521) [2]. The 10 NIST elliptic curves over binary ﬁelds are deﬁned with the irreducible polynomials X 163 + X 7 + X 6 + X 3 + 1 (curves K- and B-163), X 233 + X 74 + 1 (curves K- and B-233), X 283 + X 12 + X 7 + X 5 + 1 (curves K- and B-283), X 409 + X 87 + 1 (curves K- and B-409) and X 571 + X 10 + X 5 + X 2 + 1 (curves K- and B-571) [2].

2.

3.

4.

5.

### References

1.

IEEE Std 1363-2000. IEEE Standard Speciﬁcations for Public-Key Cryptography. IEEE Computer Society, August 29, 2000. Federal Information Processing Standards Publication FIPS 186-2. Digital Signature Standard (DSS), appendix 6: “Recommended elliptic curves for federal government use”. National Insti- tute of Standards and Technology, January 27, 2000. Available at URL http://csrc.nist.gov/publi- cations/ﬁps/ﬁps186-2/ﬁps186-2.pdf. F. Bao, R. H. Deng, Y. Han, A. B. Jeng, A. D. Narasimbalu and T.-H. Ngair, Breaking public key cryptosystems on tamper resistant devices in the presence of transient faults. In B. Christian- son, B. Crispo, M. Lomas and M. Roe (eds), Security Protocols, Volume 1361 of Lecture Notes in Computer Science, Springer-Verlag (1997) pp. 115–124. I. Biehl, B. Meyer and V. Müller. Differential fault attacks on elliptic curve cryptosystems. In M. Bellare (ed.), Advances in Cryptology – CRYPTO 2000, Volume 1880 of Lecture Notes in Com- puter Science, Springer-Verlag (2000) pp. 131–146. E. Biham and A. Shamir, Differential fault analysis of secret key cryptosystems. In B. S. Kaliski Jr. (ed.), Advances in Cryptology – CRYPTO ’97, Volume 1294 of Lecture Notes in Computer Sci- ence, Springer-Verlag (1997) pp. 513–525. D. Boneh, R. A. DeMillo and R. J. Lipton, On the importance of checking cryptographic pro- tocols for faults. In W. Fumy (ed.), Advances in Cryptology – EUROCRYPT ’97, Volume 1233 of Lecture Notes in Computer Science, Springer-Verlag (1997) pp. 37–51. D. Boneh, R. A. DeMillo and R. J. Lipton, On the importance of eliminating errors in crypto- graphic computations. Journal of Cryptology, Vol. 14, No. 2 (2001) pp. 101–119. An earlier ver- sion appears in [6]. E. De Win, S. Mister, B. Preneel and M. Wiener, On the performance of signature schemes based on elliptic curves. In J.-P. Buhler (ed.), Algorithmic Number Theory Symposium, Volume 1423 of Lecture Notes in Computer Science, Springer-Verlag (1998) pp. 252–266. T. ElGamal, A public key cryptosystem and a signature scheme based on discrete logarithms. IEEE Transactions on Information Theory, Vol. IT-31, No. (4) (1985) pp. 469–472. S. D. Galbraith, F. Hess and N. P. Smart, Extending the GHS Weil descent attack. In L. Knudsen (ed.), Advances in Cryptology – EUROCRYPT 2002, Volume 2332 of Lecture Notes in Computer Science, Springer-Verlag (2002) pp. 29–44. P. Gaudry, F. Hess and N. P. Smart, Constructive and destructive facets of Weil descent on elliptic curves. Journal of Cryptology, Vol. 15, No. 1 (2002) pp. 19–46.

2.

3.

4.

5.

6.

7.

8.

9.

10.

11.

<!-- PDF_PAGE: 11 -->

## PDF page 11

43

ELLIPTIC CURVE CRYPTOSYSTEMS

12.

F. Hess, The GHS attack revisited. In E. Biham (ed.), Advances in Cryptology – EURO- CRYPT 2003, Volume 2656 of Lecture Notes in Computer Science, Springer-Verlag (2003) 374–387. M. Joye, J.-J. Quisquater, F. Bao and R. H. Deng, RSA-type signatures in the presence of tran- sient faults. In M. Darnell, (ed.), Cryptography and Coding, Volume 1355 of Lecture Notes in Computer Science, Springer-Verlag (1997) pp. 155–160. N. Koblitz, Elliptic curve cryptosystems. Mathematics of Computation, Vol. 48, No. 177 (1987) pp. 203–209. P. Kocher, Timing attacks on implementations of Difﬁe-Hellman, RSA, DSS, and other systems. In N. Koblitz (ed.), Advances in Cryptology – CRYPTO ’96, Volume 1109 of Lecture Notes in Computer Science, Springer-Verlag (1996) pp. 104–113. P. Kocher, J. Jaffe and B. Jun, Differential power analysis. In M. Wiener (ed.), Advances in Cryp- tology – CRYPTO ’99, Volume 1666 of Lecture Notes in Computer Science, Springer-Verlag (1999) pp. 388–397. M. Maurer, A. J. Menezes and E. Teske, Analysis of the GHS Weil descent attack on the ECDLP over characteristic two ﬁnite ﬁelds of composite degree. In C. Pandu Rangan and C. Ding (ed.), Progress in Cryptology – INDOCRYPT 2001, Volume 2247 of Lecture Notes in Computer Science, Springer-Verlag (2001) pp. 195–213. A. J. Menezes, Elliptic Curve Public Key Cryptosystems. Kluwer Academic Publishers (1993). A. Menezes, T. Okamoto and S. Vanstone, Reducing elliptic curve logarithms to logarithms in a ﬁnite ﬁeld. IEEE Transactions on Information Theory, Vol. 39 (1993) pp. 1639–1646. A. J. Menezes and M. Qu, Analysis of the Weil descent attack of Gaudry, Hess and Smart. In D. Naccache (ed.), Topics in Cryptology – CT-RSA 2001, Volume 2020 of Lecture Notes in Com- puter Science, Springer (2001) pp. 308–318. V. S. Miller, Use of elliptic curves in cryptography. In H. C. Williams (ed.), Advances in Cryptol- ogy – CRYPTO ’85, Volume 218 of Lecture Notes in Computer Science, Springer (1986) pp. 417– 426. J. M. Pollard, Monte Carlo methods for index computation (mod p). Mathematics of Computa- tion, Vol. 32 (1978) pp. 918–924. J. M. Pollard, Kangaroos, monopoly and discrete logarithms. Journal of Cryptology, Vol. 13, No. 4 (2000) pp. 437–447. N. P. Smart, How secure are elliptic curves over composite extension ﬁelds? In B. Pﬁtzmann (ed.), Advances in Cryptology – EUROCRYPT 2001, Volume 2045 of Lecture Notes in Computer Sci- ence, Springer-Verlag (2001) pp. 30–39. J. A. Solinas, Generalized Mersenne numbers. Technical Report CORR-99-39, Dept of C&amp;O, University of Waterloo, Canada (1999).

13.

14.

15.

16.

17.

18. 19.

20.

21.

22.

23.

24.

25.
