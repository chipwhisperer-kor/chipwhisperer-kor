# [3] The Exact Security of Digital Signatures - How to Sign with RSA and Rabin

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 18
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-03"
derived_asset_id: "PCM-DFA-REF-03-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[3] The Exact Security of Digital Signatures - How to Sign with RSA and Rabin.pdf"
source_sha256: "e35ea4e9a3292d6897324664ca220991ca797675afc30c27c964008a27bf9a39"
pages: 18
bbox_words: 9616
consumed_bbox_words: 9616
numeric_tokens: 551
consumed_numeric_tokens: 551
source_blocks: 181
consumed_source_blocks: 181
emitted_blocks: 171
embedded_raster_images: 18
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 18
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

The Exact Security of Digital Signatures- How t o Sign with RSA and Rabin

Mihir Bellare’ and Phillip Rogaway2

Department of Computer Science and Engineering, Mail Code 0114, University of California at San Diego, 9500 Gilrrian Drive, La Jolla, CA 92093, USA. Email: mihir@cs.ucsd.edu ; Web page: http://www-cse.ucsd.edu/users/mihir

a

Department of Computer Science, IJniversity of California at Davis, Davis, CA 95616, IJSA. E-mail: rogawayecs .ucdavis .edu

Abstract. We describe an RSA-based signing scheme which corribines essentially optimal efficiency with attractive security properties. Sign- ing takes one RSA decryption plus sonic hashing, verification takes one RSA encryption plus some hashing, and the size of the signature is the size of the modulus. Assuming the underlying hash functions are ideal, our schemes are not only provably secure, but are so in a tight way- an ability to forge signatures with a certain amount of coniputational resources implies the ability to invert R.SA (on the same size modulus) with about the same computational effort. Furthermore, we provide a second scheme which maintains all of the above features and in addition provides message recovery. These ideas cxt,entl to provide schemes for Rabin signatures with analogous properties; in particular their security can be tightly related to the hardness of factor-ing.

1 Introduction

A widely employed paradigm for signing with RSA is to first “hash” t,lie message into a domain point of RSA and then decrypt. (ie. exponentiate with the RSA decryption exponent,). In particular, this is the basis of several existing standards.

Unfortunately, the security of the standardized schemes cannot be justified under standard assumptions aboiit R S A , wen assuming the underlying hash functions are ideal. We propose new schemes, both for signing and for signing with message recovery. They are as simple and efficient as the standardized ones. (In particular, signing takes one RSA decryption plus some hashing, Verification takes one RSA encryption plus some hashing, and the size of the signature is the size of the modulus.) But, assuming t,he underlying hash function is ideal, oiir rnethods are not, only provably secure, but provably secure in a strong sense: the security of our schemes can be tightly related t o the security of the RSA function. Besides providing concrete new schemes for signing with RSA, this work highlights the import,wnce, for practical applications of provable security, of COIF sideration of the tightness of the security reduction, and also provides a rare ex- m l p k of modifying one provably-good scheme in order t o obtain another which has a better security bound.

U. Maurer (Ed.): Advances in Cryptology - EUROCRYPT ’96, LNCS 1070, pp. 399-416, 1996. 0 Springer-Verlag Berlin Heidelberg 1996

<!-- PDF_PAGE: 2 -->

## PDF page 2

400

Let US now expand on all of the above. We begin by looking at current practice. Then we consider the full domain hash scheme of [3] which is provable, and discuss its exact security. 'Finally we come to our new schemes, PSS and PSS-R, arid their exact security.

### 1.1 Signing with RSA- Current practice

THE R,SA SYS'I'EM. In the RSA public key system [I51 a party has public key ( N , e ) and secret key ( N , d ) , where N is a k-bit modulus, the product of two (k/2)-bit primes, and e,d E Z;") satisfy ed G 1 mod cp(N). (Think of k = 1024, a recomniended modulus size these days.) Recall that the RSA function f: ZT,i -+ Z&amp; is defined by f(x) = 2" mod N and its inverse f-': ZT,i + Z&amp; is defined by f-' (y) = y d mod N (2, y E Zh). The gcnerally-made assumption is that f is trapdoor one-way- roughly, if you don't know d (or the prime factors of N ) then i t is hard to compute 3: = f-'(y) for a y drawn raridorrily from Z h .

HASH-THEN-DECRYPT SCHEMES. A widely employed paradigm to sign a doc- ument M is t o first compute some "hash" y = H u s h ( M ) and then set the signature t o z = f - ' ( y ) = yd mod N . (To verify that z is a signature of M , compute f(x) = xe mod N and check this equals Hash(&amp;').) In particular, this is the basis for several existing standards. A necessary requirement on Hash in such a scheme is that it be collision-intractable and produce a k-bit output in . ; Z Accordingly, Hash is most often implernented via a cryptographic hash function like H = MD5 (which yields a 128 bit output arid is assumed to be collision-intractable) and s011ie padding. A c:oncre,tt' example of such a scheme is [16, 171, wherc the hash is

f f a s h p ~ c s ( M ) = OX 00 01 FF FF ' . FF FF 00 1) ff(?d) .

Here 11 denotes concatenation, and enough OxFF-bytes are used so as to make equal t,o k hits. the length of f f a s h p ~ ~ s ( l M )

SECURITY. We draw attention to the fact that, the security of a hash-then-

decrypt signature dcpends very much on how exactly one implements Hush. In particular, it is irnportant, t,o recognize that the security of a signature scheme can't ) be justified given (only) that like SignpKcs(M) = f - ' ( H u s h p ~ ( ~ ~ ( M ) RSA is trapdoor one-way, even under the assumption that hash function H is ideal. (The reason is that the set, of points { HashpK(:s(M) : M E {0,1}* } has size at, most 2lZg and hence is a very sparse, and a very structurcd, subset of Z&amp;.) We consider this to be a disadvantage. We stress that we don't know of any attack on this scheme. But we prefer, for such importrant primitives, to h a w some proof of security rathcr than just an absence of known attacks. The same situation holds for other standards, including IS0 9796 [lo]. (There the function Hash involves no cryptographic hashing, and the message M is casily recovered from Hash(M). This doesn't effect the points we've just made.) The above discussion highlights that collision-intractability is not enough. The function I I u s h p ~ ~ is s guaranteed to be collision-intracta~le if we use a collision-intractable H . Rut this won't suffice to get a proof of securit,y.

<!-- PDF_PAGE: 3 -->

## PDF page 3

### 1.2 FDH and its exact security

40 1

TIIE F DH SCHEME. 111 earlier work [3] we suggested to hash M onto the full domain z&amp; of the RSA function before decrypting. T h a t is, HashFnH: {0,1}* + Z;V is understood to hash strings “uniformly” into , ; Z and the signature of M is Sign,,,,(M) = f-’ ( H u s ~ F D H ( M ) ) . (Candidates for suitable functions hush^^" can easily be constructed out of MD5 or similar hash functions, as described in [3].) We call this the Full-DoInain-IIashi-IIas~i scheme ( F D H ) .

PROVABLE SECURITY OF FDII. Assuming Hush is ideal (ie. it behaves like a random function of the specified domain and range) the security of FDH can be proven assuming only that RSA is a trapdoor permutation. (This is a special case of [3, Section 41, which corisiders this construction with an arbitrary t,rapdoor permutation.) This makes the seciirit,y guarantee of the FDH scheme superior to those of the schemes we discussed in Section 1.1. Now we want to go further. We will explain how, within the class of provable schemes, quality depends on the quantifiable notion of exact security. In this paper we compute t,he exact security of the FDH scheme, and then we offer a new scheme which has better exact securit,y.

EXACT SECURITY. We quantify t,he security of RSA as a trapdoor permutation. We say it is (t’, 6‘)-secure if an attacker, given y drawn raridorrily from Z;Y and limited to running in time t ‘ ( k ) , su ds in finding f-’ (y) with proba,bility at most ~ ( k ) . Values of t’, E‘ for which it is safe to assume RSA is (t’, 6’)-secure can be provided based on the perceived cryptanalytic strength of RSA. Next, we quant,ify the security of a signature scheme. A signature scheme is said t o be ( t , qsig, yllasll, €)-secure if an attacker, provided the public key, allowed to run for time t ( k ) , allowed a chosen-message attack in which she can see up to qsig ( k ) legitimate message-signature pairs, and allowed qhas1, invocations of the (ideal) hash function, is successful in forging the sigriatiire of a new message with probability at most, ~ ( k ) .

+

EXACT SECURITY O F F D H . The “exact security” of t,he reduction of [3] used to prove the security of the FDH signature scheme is analyzed in Theorem 1. It says that if RSA is (t’, d-secure and qsig,qt,ast, arc given then the FDH signature scherrie is ( t , qsig, qtlatl, €)-secure for t = t’ - poly(q,i,, qllasll, k) and € = ( q slg . qllaskl) E‘. Here poly is some some small polynomial explicitly speci- fied in Theorem 1. We note that E could thus be considerably larger than 6 ’ . This means that even if RSA is quit,e strong, the guarantee on the signature scheme could be quite weak. To see this, say we would like to allow t,he forger to see at least q s i g ( k ) = 230 example signatures and corripute hashes on, say, qllaStl = 260 strings. Then even if the RSA inversion probability was originally as low as 2--F1, all we can say is that the forging probability is now at most I/2, which is not good enough. To compensate, we will have to be able to assume that d ( k ) is very, very low, like 2-l”. This means that we must have a fairly large value of k , ie. a larger modulus. But this affects the efficiency of the scheme, because the time to do the

<!-- PDF_PAGE: 4 -->

## PDF page 4

402

uriderlyirig modular exponentiation g ~ o w s (and rather quickly) as the modulus size increases. We prefer to avoid this. We reiterate the crucial point: if the reduction provirig security is “loose,” like the one above, the efficiency of the scheme is impacted, because we must move to a larger security parameter. Thus, it would be nice t,o have “tighter” reductions, meaning ones in which E is almost the same as c‘, with the relations amongst the other parameters staying about the same as they are now. One might suggest that it is possible to prove a better security bound for FDH than that outlined above. Perhaps, but we don’t know how. Instead, we will strengthen the scherne so that a better security bound can be proven.

CLARIFICATION. Before going on, let us clarify our assessrrlents of scherne quality. We are not saying the FDH scheme is bad. Indeed, since it is provable, it is ahead of’ schemes discussed in Section 1.1, and a viable alternative to therri. What we are saying is that it is possible to do even better than FDH. That is, it is possible to get a scheme which is not only proven secure, but has strong exact, security. This successor to FDH is the scheme we discuss next.

### 1.3 New schemes: PSS and PSS-R

PSS. We introduce a new scheme which we call the probabilistic signature scheme (PSS). It is fully specified in Section 4. The idea is to strengthen the FDH scheme by making the hashing probabilis- tic. In order to sign message M , the signer first picks a random seed T of length ko, where ko &lt; k is a parameter of the scherne. Then using some hashing, in a specific way we specify, the signer produces from M and r an image point y = Hashpss(M,r) E Z&gt;. As usual, thesignatureis 3: = f-’(y) = y d mod N . (Verifi- cation is a bit morc tricky than usual, since one cannot simple “re-compute” this probabilistic hash, but still takes only one RSA encryption and some hashing. See Section 4.) In particular, our scheme is as efficient as the schemes discussed above. But Theorem 2 shows that the security can be tightly related to that, of RSA. Roughly, it says that if RSA is (t‘, E’)-secure then, given qsig, qllasl1, scheme PSS is (t,qsig, qilasil,c)-secure for t = t’ - p ~ l y ( q ~ i k ~ ) , q and ~ E ~ = ~ E’ ~ ~ - ~ , o(1). Here o( 1) denotes a function exponentially small in ko and kl (another paramet,er of the scheme) and poly denotes a specific polynomial, both of t,hese explicitly specified in the theorern. Continuing the above example, if the KSA inversion probability was originally as low as 2 Y 6 1 , the probability of forgery for the signature scheme is almost equally low, regardless of the number of sign and hash queries the advcrsary makes!

Pss WITH R.ECOVERY. We also have a variant of Pss, called PSS-R, which pro- vides message recovery. The goal is to save on bandwidth. Rather than trarisrnit the message M and its signature 3:, a single “enhanced sigriature”.r, of length less than lMl + 1x1, is transmitted. Thc vc:rificr will ha able to recover M from .r and simultaneously check the authenticity. With security parameter k = 1024, our

<!-- PDF_PAGE: 5 -->

## PDF page 5

403

scheme enables one to authenticate a message of up to n = 767 bits by transmit- ting only a total of k bits. PSS-R accomplishes this by appropriately “folding” the message into the signature iu such a way that the verifier can recover it. The efficiency and security are the same as for PSS. See Section 5.

RABIN SIGNA’I’URES. The same ideas apply for the Rabin function, and, in par- ticular, we have both a basic Rabin scheme and a variant which provides for message recovery, with security tightly related to the hardness of factoring. See Section 6.

### 1.4 Discussion

The above illustrates that to fairly compare the efficiency of two provably-secure schemes one needs to look at more than just Computation time for a k-bit key. Schemes FDH arid PSS have essentially the same computation time when k is fixed. But since PSS has tighter provable security one can safely use a smaller modulus size arid thus, ult,imately, get greater efficiency. A riurnerical example may help to make this clear. Let us again assume that the forger F can compute the hash of a t most 260 strings and that&gt; she can obtain the signatures of at most 230 messages. Assume that it takes time Ce’ 823(10gN)”3(10g10gN)2’3 to invert RSA [12]. Then, our theorems imply that if you use FDH then you must, select a modulus of 3447 bits in order to get the same degree of guaranteed-secuiity as you would have gott,en had you selected a modulus of 1024 bit,s and used PSS.

Related work

1.5

We have already discussed the PKCS standards [16, 171 and the IS0 standard [lo] and seen that their security cannot be justified based on the assumption that RSA is trapdoor one-way. Ot,her standards, such as [l], are similar to [16], and the same statement applies. The schemes we discuss in the reiiiainder of this section do not use the hash-then-decrypt paradigm. Signature schemes whose security can be provably based on the RSA assurnp- tioii include [9, 2, 11, 20, 61. The major plus of these works is that they do not use an ideal hash function (random oracle) model- the provable security is in the standard sense. On the other hand, the security reductions are quite loose for each of those schemes. On the efficiency front, the efficiency of the schemes of [9,2, 11,201 is too poor to seriously consider them for practice. The Dwork-Naor scheme [6], on the other hand, is computationally quite efficient, taking two to six RSA computations, although there is some storage overhead and the signa- tures are longer than a single RSA modulus. This scherrie is the best current choice if one is willing to allow some extra computation and storage, and one wants well-justified security without assuming an ideal hash function. Back among signature schemes which assume an ideal hash, a great many have been proposed, based on RSA, the hardness of factoring, or other assurnp- tions. Most of these schemes are derived from identification schemes, as was

<!-- PDF_PAGE: 6 -->

## PDF page 6

404

first done by [8]. Some of these methods are provable (in the ideal hash model), some not. In some of the proven schemes exact security is analyzed; usually it is not. In no case that we know of is the security tight. The efficiency varies. The computational requirements are often lower than a hash-then-decrypt RSA signature, although key sizes are typically larger. The paradigm of protocol design wit,h ideal hash functions (aka random ora- cles) is developed in [3] and continued in [4]. The current paper is in some ways thc analogue, for digital signatures, of our earlier work on encryption [4]. Further work on signing in the random oracle model includes Pointcheval and Stern [13]. (They do not consider exact security, and it may he helpful to do so in their context .)

2 Definitions

We provide definitions for an exact, securit,y treatment of RSA, basic signature schemes, and signing with recovery.

### 2.1 An exact treatment of RSA

TIIE R.SA FAMILY. RSA is a family of trapdoor permutations. It is specified by the RSA generator, RSA, which, on input l k , picks a pair of random distinct (k/2)-bit primes and multiplies them to produce a modulus N . It also picks, at random, an encryption exponent e E ) , ( Z; and corriputes the corresponding decryption exponent d so that ed = 1 mod p(N). The generator returns N , e , d , these specifying f: Z&amp; + Zh and f-’: Z&amp; + Zh, which are defined by f(x) = Z‘ mod N and f-’ (y) = y d mod N . Recall that both functions arc permutations, and, as the notation indicates, inverses of cach other. The trapdoor permutation generator R S A S is identical to R S A except that, the encryption exponent e is fixed to he 3. More generally, RSA-e provides an encryption exponent of the specified constant. Other variants of RSA use a somewhat different distribution on the rnodulus N . Our results, t,hoiigh stated for RSA, also hold for these other variants.

EXACT SECURITY O F THE K.SA FAMILY. An inverting algorithm for RSA, 1 , gets input N , e,y and tries to find f-’(y). Its success probability is the probability it, outputs f-’(y) when N , c , d are obtained by running R S A ( l k ) and y is set t o f(x) for an x chosen at random from Z;t. The standard asymptotic definition of security asks that the success prohbilit,y of any PPT (probabilistic, polynomial time) algorithm be a negligible function of k . We want to go further. We are interested in exactly how milch time an inverting algorithm uses and what success probability it achieves in this time. Formally an inverting algorithms is said t,o be a t-inverter, where t: N + N, if its running time plus the size of its description is bounded by t(lc), in some fixed standard model of computation. We say that I @,€)-breaks RSA, where 6: N + [0,1], if i is a t-inverter and for each k the success probability of 1 is at least ~ ( k ) . Finally, we say that ‘RSA is (t ! €)-secure if there is no inverter which ( t , c)-breaks R S A .

<!-- PDF_PAGE: 7 -->

## PDF page 7

405

EXAMPLE. The asymptot,ically best factoring algorithm known (NFS) takes time to 3 factor a k-bit modulus. So one might which seems t o be about e 1 . g k ” 3 ( 1 0 g k ) 2 / be willing t o assume that the trapdoor permutation family RSA is ( t , €)-secure for any ( t , c) satisfying t ( k ) / c ( k ) 5 ~ e k ” ~ for , some particular constant, C.

Signature schemes and t h e i r exact security

2.2

SIGNATURE SCIIEMES. A digital signature scheme I7 = (Ge71, Sign, Verify) is specified by a key generation algorithm, Gen, a signing algorithm, Sign, and a verifying algorithm, Verify. The first two arc prohahilistic, and all three should run in expected polynomial time. Given l k , the key generation algorithm outputs a pair of matching public and secret keys, (pk, s k ) . The signing algoritlirn takes the message M to be signed and the secret kcy sk, and it returns a signature x = Signsk ( M ) . The verifying algorithm takes a message M I a carididate signature d, and the public key p k , arid it retiirns a bit I/erifyy,k(M, x’), with 1 signifying "accept" and 0 signifying “reject.” We demand that if x was produced via z t SignSk(M) then Verifypk( M , x) = 1. One or more strong hash functions will usually be available to the algorithms Sz.9n and Verify, their domairi and rarige depending on the scheme. We model t,hem as ideal, meaning that if hash function It is invoked on some input, t,he output is a uniformly distributed point of the range. (But if invoked twice on the same input, the same thing is returned both times.) Formally, h is a random oracle. It is called a hash oracle and it is accessed via oracle queries: an algorithm can write a stxirig z and get back h ( z ) in time 12).

e

SECURITY OF SIGNATURE SCIIEMES. Defiriitions for the security of signatures in the asymptotic setting were provided by Goldwasser, Micali and Rivest [9], and enhanced to take into account the presence of an itleal hash function in [3]. Here we provide an exact version of these definitions. A forger takes as input a public key pk, where ( p k , s k ) Gen(l‘), and tries t o forge signatures with respect to p k . The forger is allowed a chosen mes- sage attack in which it can request, and obtain, signatures of messages of its choice. This is modeled by allowing the forger oracle a s to the signing al- gorithm. The forger is deemed successful if it outputs a lid forgery -namely, a message/signaturc pair ( M , z) such that Verifypk(M, x) = 1 hut M was: not, a message of which a signature was requested earlier of the signer. The forger is said t o be a ( t , qsig, qhas&amp;forger if its running time plus description size is bounded by t ( k ) ; it makes at most qsig(k) queries of its signing oracle; arid it makes a total of at most yllasl1(k) queries of its various hash oracles. As a con- vention, the time t ( k ) includes the time to answer the signing queries. Such a forger F is said t o ( t , psig, pllasll, c)-brcak the signature scheme if, for every k , the Finally we say that probability that F outputs a valid forgery is at least ~ ( k ) . the signature s c h e m (Gen, Sign, Verify) is ( t , psig, qtlasIl, €)-secure if there is no forger who ( t , qsig, qllasll, €)-breaks the scheme. For simplicity we will assume that a forger does any n ssary book-keeping so that, it never repeats a hash query. (It rriight repeat a signing query. If the scheme is probabilistic, this might help it.)

<!-- PDF_PAGE: 8 -->

## PDF page 8

406

### 2.3 Quantifying the quality of reductions

Our theorems will have the form: If RSA is (t’, €‘)-secure, theu some signature scheme ll = (Gen, Szgn, Verzfy) is ( t , psig, qhmh, c)-secure. The proof will take a forger F who (tryslg, ~ ~ = l ~ , ~ ) - b r L e 7 a k and s produce from F an inverter I who (t’,d)-breaks RSA. The quality of the reduction is in how the primed variables depend on the unprimed ones. We will typically view qsig,qllasll as given, these being query bounds we are willing to allow. (For example, qsig = Z 3 O and qllasll = 260 are reasoriable possibilities.) Obviously we want t‘ to be as large as possible and we want E’ to be as small as possible. We are usually satisfied when t’ = t - poly(Q~las~~, qsig, Ic) and C‘ M 6 .

The fill-Domain-Hash Scheme - FDH

3

THE SCHEME. Signature scheme FDH = ( G e n F D H , SignFDH, VerifyFDH) is defined as follows [ 3 ] . T he key generation algorithm, on input lk, runs R S A ( l k ) to obtain ( N , e , d ) . It outputs ( p k , s k ) , where p k = ( N , e ) arid sk = ( N , d ) . The signing and verifying algorithms have oracle access to a hash function H F D H : ( 0 , l}’ + Z;V. (In the security analysis it is assumed to be ideal. In practice it can be implemented on top of a cryptographic hash function such as SHA-1.) Signature generation and verification are as follows:

SignF13HN,, ( M ) Y t HFDH(M) return yd mod N

Verzf?lFDHN,e ( M , x) y t xe mod N ; y’ t H F D H ( M ) if y = 9’ then return I else return 0

SECURITY. The following theorem summarizes the exact security of the FDH scheme as provided by the reduction of [ 3 ] . The proof is straightforward, but it is instructive all the same, so we include it. The disadvantage of the result, froin our point of view, is that 6’ could be rriuch smaller than e.

Proof. Let F be a forger which ( t , qsig, qllasl1, e)-brcaks FDH. We present an in- verter 1 which (t’, el)-breaks RSA.

<!-- PDF_PAGE: 9 -->

## PDF page 9

+

407

Inverting algorithm I is given as input (N, e , y) where N , e, d were obtained by running the generator R S d ( l k ) , and y was chosen at random from Z h . I t is trying to find x = f-'(y), where f is the RSA function described by N , c . It forms the public key N , e of the Full-Domain-Hash signature scheme, and starts running F on input of this key. Forgcr F will make two kinds of oracle queries: hash oraclc queries and signing queries. Inverter I must answer these queries itself. For simplicity we assume that if F makes sign query M then it has already made hash oracle query M . (We will argue later that this is wlog.) Let q = qsig qilaSll. Inverter I picks at random an integer j from (1,. . . , q } . Now we describe how 1 answers oracle queries. Here i is a counter, initially 0. Suppose F makes hash oracle query M . Inverter 1 increments i and sets Mi = M . If i = j then it sets yi = and returns yi. Else it picks ri at random in Zk, sets yi = f ( r i ) , and returns yi. Alternatively, suppose F makes sigriirig query M . By assumption, there was already a hash query of M , so M = Mi for some i. Let I return the corresponding T - ~ as t h e signature. Eventually, F halts, outputting some (attempted forgery) ( M , z). Let invert- ing algorithm I output x. Without loss of generality (see below) we may assume that M = Mi for some i . In that case, if ( M , z ) is a valid forgery, then, with probability at least l / q , we have i = j and z = f-'(yi) = f-'(y) was t,he correct inverse for f . The running time of I is that of F plus the time t,o choose the yi-values. The main thing here is one RSA computation for each yi, which is cubic time (or bett,er). This explains the formula for t . It remains to justify the assumptions. Recall that I is running F . So if the latter makes a sign query without having made the corresponding hash query, I at once goes ahead and makes the hash query itself. Similarly for the output forgery. All this means that the effective number of hash queries is at most 0 qhas11 qsig 1, which is the number we used in the time bound above.

+ +

Is there a different proof which would achieve a trarislation in which t is like the

above but E is [I(€')? We don't believe so. Instead we will modify the scheme to get the security we want. We do this by making the hashing probabilistic.

The Probabilistic Signature Scheme - PSS

4

Here we propose a new scheme a probabilist,ic generalization of FDH. I t pre- serves the efficiency and provable security of FDH but achieves the latter with a much better security bound.

### 4.1 Description of the PSS

+

Signature scheme PSS[ko, k l ] = (GenPSS, SignPSS, VerifyPSS) is pararneter- ized by ICo and IC, , which are numbers between 1 and k satisfying ko kl 5 k - 1. To be concrete, the reader may like to imagine k = 1024, ko = kl = 128.

<!-- PDF_PAGE: 10 -->

## PDF page 10

408

Fig. 1. PSS: Corriponents of image y = 0 11 w I/ T* 11 yl(w) are darkened. The signature of hi’ is yd mod N .

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 10]

The key generation algorithn GenPSS is identical to GenFDH: on input lk,

run RSd(lk) to obtain ( N , e, d ) , and out,put ( p k , sk), where p k = ( N , e) and

sk = ( N , d ) . The signing and verifying algorithms make use of two hash functions. The first, h, called the compressor, maps as 11: ((1,l)’ + (0, l}kl and the second, g , called the generator, maps as g: (0, l } k o 4 (0, l}k-kl-l . (The analysis assumes these to be ideal. In practice they can be implemented in simple ways out of cryptographic hash functions like MD5, as tlisciisscd in Apperidix -4.) Let g1 be the function which on input 7u E (0,1}’0 returns the first ko bits of g(w), and let 9 2 be the function which on input w E (0, l j k 0 returns the remaining k - Ico - kl - 1 bits of g(w). We now describe how to sign arid verify. Refer to Figure 1 for a picture.

VerzfyPSS ( M , x) y c x e mod N Break up y as h 11 7 1 ~ 11 T * 1) y. (That is, let b be the first bit of y, 71) the ncxt kl bits, ?-* t h e next ko bits, and 7 the remairiiiig bits.)

T t 7’*@3,Yl (UJ)

if ( h(M 11 r ) = ’UI and g2(4u) = y and b = 0 ) then return 1 else return 0

The step T &amp; (0, l}ko indicates that t,he signer picks at random a seed T of ko bits. He then concatenates this seed to the message M , effectively “raridornizing”

<!-- PDF_PAGE: 11 -->

## PDF page 11

409

the message, and hashes this down, via the “compressing” function, to a kl bit string w. Then the generator g is applied to w t o yield a ko bit string T * = 91 (w) and a k - ko - kl - 1 bit string 9 2 ( 7 1 1 ) . The first is used to “mask” the seed T , resulting in the masked seed T * . Now w 11 T * is pre-pended with a 0 bit and appended with y ~ ( w ) to create the image point y which is decrypted under the RSA function t o define the signature. (The 0-bit is to guarantee that y is in Zk.) Notice that a new seed is chosen for each mcssage. In particular, a given message has many possible signatures, depending on the value of T chosen by the signer. Given (111, z), the verifier first computes y = x e mod N and recovers T * , w, T . These are used to check that y was correctly constructed, and the verifier only accepts if all the checks succeed. Note the efficiency of t,he scheme is as claimed. Signing takes one application of h, one application of g, and one RSA decryption, while verification t,akes one application of h,, one application of g, arid one RSA encryption.

### 4.2 Security of the PSS

The following theorem proves the security of the PSS based on t,he security of M A , but with a relation betwccn t h e two securities that is much tighter than the one we saw for the FDH scheme. The key difference is that ~ ( k is ) within an additive, rather than multiplicative, factor of d ( k ) , and this additive factor decreases exponentially with ko, k l . Tlie ~elatiori between t and t’ is about the same as in Theorem 1.

the

Theorem 2 . Suppose that R S A is ( t ‘ , c’)-secure. Then for any qsig, qll,l1 signature scheme PSS[ko, k l ] is ( t , qsig, qtllaSt,, E)-secure, where

t ( k : ) = t ’ ( k ) - [ysig(k) + yllasll(k) + 11 k.0 . ~ ( k ’ ) , and

+ [2(qsig(k) + qllash(k))2 + 11 (2+ + 2 - 9 .

F(k) = 4 ( k )

’

The rest of this section is devoted to a sketch of the proof of this theorem.

Proof Sketch. Let F be a forger which (t, q S i g , qlllasl1, €)-breaks the PSS. We present an inverter I which (t’, €‘)-breaks the trapdoor permutation family ’RSA. The input to I is N , e and 7) where q was chosen at random from Zb, and N , e, d were chosen by running the generator RSA( 1”. (But d is not provided to I ! ) We let f : Z&gt; + Zk be f(x) = xe mod N . 1 wants to compute fP1(q) = ‘ q mod N . I t forms the public key N , e , and starts running F on input this key. F will make oracle queries (signing queries, h-oracle queries, and g-oracle queries), which I must answer itself. We assume no hash query ( h or g) is repeated (but, a signing query rriight be repeated). We let 61,. . . , QQs,g+qhnsh denote the sequence of oracle queries that F makes. (This is a sequence of randorn variables.) This list includes all queries, and we implicitly assume that along with each Q i is an indication of whether it is a sigriirig oracle query, an h-oracle query or a g-oracle query. In the process of answering thcsc qiieries, 1 will “build” or “define” t,he fiinctions JL, y.

<!-- PDF_PAGE: 12 -->

## PDF page 12

410

I maintains a counter i, initially 0, which is incrernented for each query. We now indicate how the queries are answered. It depends on the type of query.

Answering signing queries. First, suppose 8% = A4 is a signing query. Let US first try to give some intuition, and then the precise instructions for I to ariswer the query. The problem is that I cannot answer a signing query as the signer would since it doesn't know f-'. So, it fiIst picks a point 2 t Zh, and then arranges that y = f(z) be the image point of a signature of M . (It, does this by viewing y as 0 11 w 11 T* 11 y, and then defining h(A4 11 r ) = w and g(w) = r*$T 11 y, for some raridorn r.) A t this point, x can be returned as a legitimate signature of M . Some technicalities include making sure there are no conflicts (re-defining h or g on points where their values were already assigned) and making sure y has first 0. These are attended to in the following full description of the instructions I t o answer signing query Q i : Increment i and let Mi = Q i . Pick Ti &amp; (0, I}". (Recall this notation means ri is chosen at random from (0, 1 j k o 0 . ) If 3 j : j &lt; i : r j = ri then abort.

Repeat z i &amp; Zh ; yi t f(zi) u n t i l the first bit of yi is 0. Break up yi to write it as 0 11 wi 11 r: 11 yi. (That is, let wi be the ICo bits following the 0, lct T: be the next k l bits, and let yi be tlie last k - ko - kl - 1

bits.) Set h(A4i 11 r i ) = wi. If 3 j : j &lt; i : wj = U I ~ then abort. Set g1 (wi) = r f ~ ; ~ Set ~ y2(wi) i = yi ; Set y(wi) = 91 (wi) 11 yz(wi). (9) Return xi to F as the answer t,o signing query Qi = Mi.

1

Answering h-oracle queries. Next, suppose Qi is an h,-oracle query. We may assume it has length at least k.0 since otherwise it doesn't help the adversary t o make this query. Again, before the precise instructions, here is the intuition. The query looks like M (1 T . We want to arrange that, if F later forges a signature of M using seed r then3 we invert f at rl. To arrange this, we will associate to query M (1 T an image of the form vx:, where xi is random. (Thus if F later comes up with an f-l(qz:) = ziq', then I can divide out zi and recover 7' = f - ' ( q ) . ) This is done by choosing a random xi, viewing qzt as 0 (1 U J 11 r* 11 y, and, as before, defining h ( M (1 T ) = w arid g ( w ) = T * &amp; (1 y. The detailed instxuctions for 1 to answer h-oracle query CJi (taking into account technicalities similar to tlie above) are: (1) Increment i and break up Q i as Mi 11 ri. (That is, let 7-i be the last ko bits of Qi and let Mi be the rest). (2) Say Qi is old if 3-j : j &lt; i : A 4 j (1 rj = M i (1 ~ i , arid new otherwise. (Since h-queries are not repeated, Qi is old iff Mi was signing query M j and in the

F might forge a signature of A4 with a seed T' such that h-query M 11 7.' was never made. But the probability of this is very low.

<!-- PDF_PAGE: 13 -->

## PDF page 13

41 1

process of answering it above we picked rj = T ~ . ) Now if Qi is old then set ( w i , r ; , y i ) = ( 7 ~ j , ~ T , 3 j and ) return w j (which is h ( M j 1) r j ) ) ; Else go on to next step.

(3) Repeat zi Z;V ; zi t f ( z i ) ; yi t qzi mod N u n t i l the first bit of yi is 0. (4) Break up yi to write it as 0 11 wi 11 rt /I yi. (5) Set /&amp;(Mi 11 T i ) = w i . (6) If 3 j : j &lt; i : 111j = wi then abort. (7) Set yl(wi) = r ; @ r i ; Set ga(wi) = ^li ; Set g(74) = gl(wi) (1 yz(wi). (8) Return wi to F as t8he answer to Loracle query Qi = Mi 1) ~ i .

Answering g-oracle queries. Last, suppose &amp;i is a y-oracle query. We may assume it has length Icl since otherwise it doesn't help the adversary to make this query. This time, there is not much to do:

( 1 ) lncrement i and let wi = Q i .

(2) If 3 j : j &lt; i : wj = wi then return g(w,y). Else pick a string (Y &amp; (0, l } k - k o - ' , set g ( w i ) = a , and return a .

Analysis. Let Distinct be the event that we never abort in Steps (3) or (7) in answering signing queries or Step (6) in answering h-oracle queries. The reader can verify that Pr[lDistinct] 5 p where p = 2(ysigSq~,,,~,)'~(2-~o+2-'1). So with probability E - p , Distinct holds and F halts and outputs a valid forgery ( M , x). Assume we are in this situation, and let y = f(z) = ze mod N . If the first bit of y is not 0 then the forgery is invalid, so assume this bit is 0. So we can break y up to view it as 0 11 w 1) T * 1) y. Let T = r*@,91 ( 7 ~ ) . We now claim that with probabilit,y atleastE-p-2-li1, t h e r e i s a n i suchthat: ( M , r , w , r * , y ) = (Mi,ri,wi,r;,yi); h- oracle query Qi = Mi 1) r i was madc; and this query was new when it was made. Assuming this claim we have y = yi = TIZ% rriod N . Now I outputs x / q mod N. Note ( z / ~ i = ) ~ ye/z: = r/ so z / z i is indeed f - l ( q ) as desired. Now let us justify the claim. If M 11 T # M i 1) 7-i for all i then the probability that h ( M 1) T ) = w is at most 2 T k 1 . So now a~suirie there is such an i . Since ( M , z ) is a valid forgery we know that M was never a signing query, so it must be that M 11 T was a h-oracle query. Furthermore, for the same reason, it must have been new. Finally, note that the time for Step (4) in answering signing queries arid Step (3) in answering h-oracle queries can't be bounded. But the expected time is two executions of the loop. So we just stop the loop after 1 + Ic0 steps. This 0 adds at most 2 - l i 0 to the error, completing our proof sketch.

+

We stress how this proof differs from that of Theorem 1. There, we had to "guess" t,he value of i E (1,. . . , qsis qhash} for which F would forge a message, a i d we were only successful if we guessed right. Here we are successful (except, with very small probability) no matter what is the value of i for which the forgery occurs.

<!-- PDF_PAGE: 14 -->

## PDF page 14

41 2

I

I

Fig. 2. PSS-R: Corriponents of image y = 0 ( 1 ‘w 11 r* 11 M ” are darkened.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 14]

Signing with Message Recovery - PSS-R

5

MESSAGE RECOVERY. In a standard signature scheme the signer transmits the message M in the clear, attaching to i t the signature 2. In a scheme which provides rriessagc recovery, only an “enhanced signature” is transmitted. The goal is to save on the bandwidth for a signed message: we want the length of this enhanced signature to be smaller than \MI + 1x1. (In particular, when M is short, we would like the length of T to be k, the signature length.) The verifier recovers the message A4 from the enhanced signaturc and checks authenticity at the same timc. We accomplish this by “folding” part of the message into the signature in such a way t h a t it is “recoverable” by the verifier. When the length n of M is small, we can in fact fold the entire message into the signaturc, so that only a k bit quantity is transmitted. In t,he scheme below, if the security parameter is k = 1024, we can fold up to 767 message bits into the signature.

DEFINITION. Formally, the key gencration arid signing algorithms are as he- fore, but Verify is replaced by Recover, which takes pk and x arid returns Recowerpk(x) E (0, I}* U {REJECT}. The distinguished point REJECT is used to indicate that the recipient rejected the signature; a return value of Ad E (0, l}’ indicates that the verifier accepts the message M as aut,hentic. The formulation of security is the same exccpt for what it means for the forger to be successful: it should provide an 2 such that, Recover,k(z) = M E {0,1}*, where M was not a previous signing query. We demand that if x is produced via 2 t Sign,(M) then Recouer,k(z) = M. A simple variant of PSS achieves message recovery. We now describe that, scheme and its security.

<!-- PDF_PAGE: 15 -->

## PDF page 15

41 3

THE SCHEME. The scheme PSS-R[ko, kl] = (GenPSSR, SagnPSSR, RecPSSR) is parameterized by ko and Icl , as before. The key generation algorithm is GenPSS, the same as before. As with PSS, the signing arid verifying algorithms depend on hash furictions h: (0, I}* -+ (0, l}ki and 9 : (0, l } k o + (0, l}k-kl-l , and we use the same 91 and yz notation. For simplicity of explication, we assume that the messages t,o be signed have length n = k - ko - kl - 1. (Suggested choices of parameters are k = 1024, ko = k l = 128 arid 'rt = 767.) In this case, we produce "enhanced signatures" of only k bits from which the verifier can recover the n-bit message and simultmeously check authenticity. Signature generation and verification proceed as follows. Refer to Figure 2 for a picture.

Rec PSSlz (x) y t ze rriod N Break up y as 6 11 111 11 r* 1) M*. (That is, let h be the first bit of y, w the next kl bits, T * the next, ko bits, and M * the rerriaining bits.)

t 7.*O)Yl(W)

7'

M t M*@~4(711)

if ( h ( M 11 7') = w and b = 0 ) then rctiirn A4 else return REJECT

The difference in SignPSSR with respect, t,o SaynPSS is that the last part of y is not y2(w). Instead, y%(w) is used to "mask" the message, arid the masked message M * is the last part of the image point y. The above is easily adapted to handle messages of arbitrary length. A fully- specified scheme would use about min{k, 7t + k.0 + kl + 16) bits.

SECURITY. The security of PSS-R is the same as for PSS.

Theorem3. Suppose that R S A i s (t', c ' ) - s e c w e . Then f w u n y qsig, qllaYl, the signing-with-recoaery scheme PSS-R[ko, k,] is ( t , qSig, ~ 1 ~ c) ~ ~ -secure, l ~ , tuhere

t ( k ) = t ' ( k ) - [qsig(k)

+ gilail(k) + I] . ko 0 ( k 3 ) , and ~ ( k = ) ~ ' ( k + ) [2(qsig(k) + qlias\l(k))' + 11 ( 2 - k ~ + 2-") .

'

The proof of this theorem is very similar to that of Theorem 2 and hence is omitted.

Rabin signatures - PRab and PRab-R

6

The ideas of this paper extend t o Rabin signatures [18, 191, yielding a signature scheme arid a signing with recovery schcmo whose security can be tightly related to the hardness of factoring.

<!-- PDF_PAGE: 16 -->

## PDF page 16

41 4

+

THE SCHEME. Scheme PRab[ko, k ~ = ] (GenPRab, SzgnPRab, VerifyPRab), the probabilistic Rabin scheme, depends on parameters ko, kl, where Ico k.1 5 k. Algorithm GenPRab, on input l k l picks a pair of random distinct (k/2)-bit primes p , q and multiplies them to produce the k-bit modulus N . It outputs ( p k , s k ) , where pk = N and sk = ( N , p , q ) . The signing and verifying algorithms of PRab use hash functions h, g, where h,: {0,1}* -+ { O , l ) k l and 9: { O , l } k o + { O , l } k - k l . We let g1 be the function and let g~ he the which on input w E {a, l}ko returns the first k~ bits of g(w), function which on input w E (0, l}ko returns the remaining k - ko - kl bits of

g(711).

The signing procedure, SignPRab, is similar to the corresponding SiynPSS, but it returns a random square root of the image y, as opposed to yd mod N . We stress that a random root is chosen; a fixed one won’t, do. The verification procedure checks if the square of the signature has the correct image. Thus verification is particularly fast. IIere, in full, are SzgnPRnb and Verz~yPRab:

SignPRab ( M )

repeat

T

; 711 t h,(M 11 T ) ; 7.* t gl(W)$T (0, Y + 7u II T * I1 92(w)

u n t i l y is a quadratic residue modN. Let { 2 1 , 2 2 , 2 3 , 2 4 } be the four distinct square roots of y in Zk. Let 2 8- { 2 ~ , 2 ~ , 2 3 , L c 4 } . return 2

VerzfyYRab ( M , 2 ) y t x2 mod N Break up y as w 11 T * 11 y. (That is, let w be the first kl bits of y, T * the next ko bits, and y the remaining bits.)

T t T*@)y,(W)

if ( h ( M 11 T ) = w arid g ~ ( w = ) y 1 then return 1 else return 0

EXACT SECURITY OF FACTORING. This scheme is based on the hardness of factoring, so we need an exact security formulation of the hardness of factoring awump tion. A factoring algorithm takes a k-bit number and tries to factor it. It is a t-factoring algorithm if the size of its descriptiori plus it,s running time is at most t ( k ) for every k. We say that A ( t , f)-factors if, given a number which is the product of two random distinct (k/2)-bit primes, A produces the correct factorization with probability at least ~ ( k ) . We say t,hat factoring is (t, €)-hard if there is IIO algorithm which (t, t)-factors. A reasonable assumption would be that factoring is (t, €)-hard for any t , F satisfying t ( k ) / e ( k ) = e k ’ / 4 ( ’ o g k ) 3 / 4 .

SECURITY OF THE PRab. The following theorcm says that the security of PRab is similar to that of PSS.

<!-- PDF_PAGE: 17 -->

## PDF page 17

41 5

Theorem4. Suppose that factoring is (t‘, €‘)-hard. Then for any qsig, qtlasll the signature scheme PRab[ko, k l ] is (t, 48igr ~ l ~ ~ l €)-secure, ~ , where

Thc proof of this theorem is analogous to that of Theorem 2. Given a forger F who ( t , qsig, q ~ , ~ ] , , c)-breaks PRab we construct an algorithm which (t’, €‘)-factors. We begin by picking an element a E Z;C a t random and setting q = u2 rriod N. Then we procccd as in the proof of Theorem 2, with c set t o 2 rather than to the RSA encrypt,ion exponent. We therehy recover a square root of 7 with probability €(k) - 6 ( k ) where b ( k ) = [2(q,ig(k)+4,,,1,(k))~ +1].(2-k0+2-k1 ). Rut with probability e ( k ) / 2 - 6 ( k ) this square root is different from LY arid hence we factor N . Thus we have a factor of two deterioration in the success probability. On the other hand, there is an improvement in the time complexity, since our algorithm has to raise numbers to the power two rather than t o an arbitrary RSA exponent e , thereby bringing the O ( k 3 ) time to O ( k 2 ) . Also, it is a potentially weaker assumption to say that factoring is (t‘, e’) hard.

RECOVERY. As with PSS, we can add message recovcry to the PRab scheme in

the same way, resulting iri the PRab-R signing-with-recovery scheme. Its security is the same as that of PRab.

### References

s.

1. D . BALENSON, “Privacy Enhancement for Internet Electronic Mail: Part 111: Al- gorithms, Modes, and Identifiers,” lETF RFC 1423, February 1993. 2. M. BELLAH.E AND MICALI, “How to sign given any trapdoor permutation,” .JACM Vol. 39, No. 1, 214-233, January 1992. “Random oracles are pract,ical: a paradigm for 3. M. BELLARE A N D P . ROGAWAY, designing efficient protocols,” Proceedings of the First Annual Conference on Com- puter and Communications Security, ACM, 1993. “Optirrial Asymmetric Encryption,” Advances 4. M . BELLARE A N D P. ROGAWAY, in Cryptology - Eurocr,ypt Y4 Proceedings, Lecture Notes in Computer Science Vol. 950, A . De Santis ed., Springer-Verlag, 1994. “New directions in crypt,ography,” I E E E ‘ ~ ~ I L s . 5. W . DIFFII? A N D M. E. HELLMAN, Znfu. Theory IT-22, 644-654, November 1976. 6. C. DWORK A N D M. NAOR.. An efficient existentially unforgeable signature scheme arid its applications. Advances in Cryptology - Crypto 94 Proceedings, Lecture Notes in Computer Science Vol. 839, Y . Desmedt ed., Springer-Verlag, 1994. 7. T. EL GAMAL, “A public key cryptosystem and a signature scheme based on dis- crete logarithms,” IEEE Transactions on Information Theory, Vol. 31, No. 4, July 1985. 8. A . FIAT AND A . SHAMIR, “How to prove yourself: practical solutions to identi- fication and signature problems,” Advances in Cryptology - Crypto 86 Proceed- ings, Lecture Not,es i n Computer Science Vol. 263, A . Odlyzko ed., Springer-Verlag,

1986.

<!-- PDF_PAGE: 18 -->

## PDF page 18

416

9. S. COLDWASSER., S. MICALI A N D R . RIVEST, “A digital signature scheme secure against adaptive chosen-message attacks,” SIAM Journal of Computing, I7(2):281-- 308, April 1988. 10. ISO/lEC 9796, “Information Technology Security Techniques - Digital Signature Scheme Giving Message Recovery,” International Organization for Standards, 1991. 11. M. NAOR A N D M . YUNG, “Universal one-way hash functions and their crypt,o- graphic applications,” Proceedings of the 21st Annual Symposium on Theory of Computing, ACM, 1589. 12. A . LENSTRA ND H . LENSTRA (ctls.), “The development of the number field sieve,” Lecture Notes in Mathematics, vol 1554, Springer-Vcrlag, 1993. AND J . STERN, “Security proofs for signatures,” Advances in 13. D. POINTCHEVAL cryptofogy - Eurocrypt 96 Proceedings, Lecture Notes in Cornpu ter Science, t J . Maurer ed., Springer-Verlag, 1996. 14. R. RIVEST, “The MD5 Message-lligest Algorithm,” IETF RFC 1321, April 1952. 15. R.. RIVEST, A. SHAMIR A N D L. ADLEMAN, “A method for obtaining digital signa- tures and public key cryptosystems,” CACM 21 (1978). 16. RSA Data Security, Inc., “PKCS #1: ItSA Encryption Standard (Version 1.4).” June 1991. 17. RSA Data Security, Inc., “I’KCS #7: Cryptographic Message Syntax Standard (version 1.4).” June 1991. 18. M. R.ABIN, “Digital signatmes,” in Foundations ofsecure computation, R. A. Millo et. al. eds, Academic Press, 1978. 19. M . RARIN., “Digit,al signatures and public key functions nc; intractable as factor- ization,” MIT Laboratory for Computer Science Report TR-212, January 1979. 20. J . ROMPEL, “One-way Functions are Necessary and Sufficient for Secure Signa- t11res,” Proceedings of the 22nd Annual Symposium on Thcory of Computing, ACM, 1990. “A rriodification of the I t S A public key encryption procedure,” IEEE 21. H. WILLIAMS, Transactions on Information Theory, Vol. IT-26, No. 6, November 1980.

How t o implement the hash functions h , g

A

In the PSS we need a concrete hash function h with output length some given number IC, . Typically we will construct / L from some cryptographic hash function H such as H = MD5 o r H = S H A - I . Ways to do this have been discussed before in [3, 41. For completeness we quickly sumrnarize some of these possibilities. T h e simplest is to define h ( z ) as the appropriate-length prcfix of

* .

fZ(const.(O).z) 11 H(const.(l).z) 11 H(const.(2).z) 11

The constant const should bc unique t o h; to make another hash function, g, simply select a different constant.
