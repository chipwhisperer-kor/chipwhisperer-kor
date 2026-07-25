# [7] On the Importance of Checking Cryptographic Protocols for Faults

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 15
converted_at: "2026-07-26"
source_asset_id: "HAETAE-FIA-REF-07"
derived_asset_id: "HAETAE-FIA-REF-07-MD"
source_path: "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[7] On the Importance of Checking Cryptographic Protocols for Faults.pdf"
source_sha256: "f3fd9d538ed4950aea5bcdeac53b03de02c224c6e76446e99190dcbccb727b93"
pages: 15
bbox_words: 7563
consumed_bbox_words: 7563
numeric_tokens: 347
consumed_numeric_tokens: 347
source_blocks: 194
consumed_source_blocks: 194
emitted_blocks: 188
embedded_raster_images: 15
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

On the Importance of Checking Cryptographic Protocols for Faults

(Extended abstract)

Richard A. DeMillo radQbellcore.com

Dan Boneh daboQbellcore.com

Richard J. Lipton* 1iptonQbellcore.com

Math and Cryptography Research Group, Bellcore, 445 South Street, Morristown N J 07960

Abstract. We present a theoretical model for breaking various cryp- tographic schemes by taking advantage of random hardware faults. We show how to attack certain implementations of RSA and Rabin signa- tures. We also show how various authentication protocols, such as Fiat- Shamir and Schnorr, can be broken using hardware faults.

1 Introduction

Direct attacks on the famous RSA cryptosystem seem to require that one factor the modulus. Therefore, it is interesting to ask whether there are attacks that avoid this. The answer is yes: the first was the recent attack based on timing [4]. It was observed that a few bits could be obtained from the time that operations took. This would allow one t o break the system without factoring. We have a new type of attack that also avoids directly factoring the modulus. We essentially use the fact that from time to time the hardware performing the computations may introduce errors. There are several models that may enable a malicious adversary t o collect and possibly cause faults. We give a high level description:

Transient faults Consider a certification authority (CA) that is constantly

generating certificates and sending them out t o clients. Due t o random tran- sient hardware faults the CA might generate faulty certificates on rare oc- casions. If a faulty certificate is ever sent t o a client, we show that in some cases that client can break the CA's system and generate fake certificates. Note that on many systems, a client is alerted when a faulty certificate is received. L a t e n t faults Latent faults are hardware or software bugs that are difficult t o catch. As an example, consider the Intel floating point division bug. Such bugs may also cause a CA t o generate faulty certificates from time to time. Induced faults When an adversary has physical access t o a device she may try t o purposely induce hardware faults. For instance, one may attempt to attack

* Also at Princeton University. Supported in part by NSF CCR-9304718.

W. Fumy (Ed.): Advances in Cryptology - EUROCRYPT '97, LNCS 1233, pp. 37-51, 1997. 0 Springer-Verlag Berlin Heidelberg 1997

<!-- PDF_PAGE: 2 -->

## PDF page 2

38

a tamper-resistant device by deliberately causing it to malfunction. We show that the erroneous values computed by the device enable the adversary to extract the secret stored on it.

We consider a fault model in which faults are transient. That is, the hard- ware fault only affects the current data, but not subsequent data. For instance, a bit stored in a register might spontaneously flip. Or a certain gate may spon- taneously produce an incorrect value. Note that the change is totally silent: the hardware and the system have no clue that the change has taken place. We as- sume that the probability of such faults is small so that only a small number of them occur during the computation.

Our attack is effective against several cryptographic schemes such as the RSA system and Rabin signatures [lo]. The attack also applies to several au- thentication schemes such as Fiat-Shamir [5] and Schnorr [ll]. As expected, the attack itself depends on the exact implementation of each of these schemes. For an implementation of RSA based on the Chinese remainder theorem we show that given one faulty version of an RSA signature one can efficiently factor the RSA modulus with high probability. The same approach can also be used to break Rabin’s signature scheme. In Section 6 we show that hardware faults can be used to break other implementations of the RSA system though many more faulty values are required.

In Section 4 we show that the Fiat-Shamir identification scheme [5] is vul- nerable t o our hardware faults attack. Given a few faulty values an adversary can completely recover the private key of the party trying to authenticate itself. In Section 5 we obtain the same result for Schnorr’s identification protocol [ll]. Both schemes are suitable for use on smart cards.

It is important to emphasize that the attack described in this paper is cur- rently theoretical. We are not aware of any published results physically experi- menting with this type of attack. The purpose of these results is to demonstrate the danger that hardware faults pose to various cryptographic protocols. The conclusion one may draw from these results is the importance of verifying the correctness of a computation for security reasons. For instance, a smart card using RSA t o generate signatures should check that the correct signature has in- deed been produced. The same applies to a certification authority using RSA to generate certificates. In protocols where the device has to keep some state (such as in identification protocols) our results show the importance of protecting the registers storing the state information by adding error detection bits (e.g. CRC). We discuss these points in more detail at the end of the paper.

We note that FIPS [6] publication 140-1 suggests that hardware faults may compromise the security of a module. Our results explicitly demonstrate the extent of the damage caused by such faults.

<!-- PDF_PAGE: 3 -->

## PDF page 3

39

Chinese remainder based implementations

2

The RSA system

2.1

In this section we consider a system using RSA to generate signatures in a naive way. Let N = p q be a product of two large prime integers. To sign a message 2 using RSA the system computes 2 ' mod N where s is a secret exponent. Here the message 2 is assumed to be an integer in the range 1 to N (usually one first hashes the message to an integer in that range). The security of the system relies on the fact that factoring the modulus N is hard. In fact, if the factors of N are known then one can easily break the system, i.e., sign arbitrary documents without prior knowledge of the secret exponent. The computationally expensive part of signing using RSA is the modular exponentiation of the input z. For efficiency some implementations exponentiate as follows: using repeated squaring they first compute El = x s mod p and E2 = 2 ' mod q. They then use the Chinese remainder theorem (CRT) to compute the signature E = 2' mod N . We explain this last step in more detail. Let a , b be two precomputed integers satisfying:

and { { U E O 1 (modp) (modq)

a r

bEO bEl

(modp) (modq)

Such integers always exist and can be easily found given p and q. It now follows that E = aE1 bEz (mod N )

+

Thus, the signature E is computed by forming a linear combination of El and E2. This exponentiation algorithm is more efficient than using repeated squaring modulo N since the numbers involved are smaller.

RSA's vulnerability to hardware faults

2.2

Our simple attack on RSA signatures using the above implementation enables us to factor the modulus N . Once the modulus is factored the system is consid- ered to be broken. Our attack is based on obtaining two signatures of the same message. One signature is the correct one; the other is a faulty signature. At the end of the section we describe an improvement due t o Arjen Lenstra [9] that factors the modulus using just a single faulty signature of a known message M . Let M be a message and let E = M 8 mod N be the correct signature of the message. Let E be a faulty signature. Recall that E and E are computed as

+ bEz (mod N ) and E = a&amp; + bE2 (mod N )

E = aE1

Suppose that by some miraculous event a hardware fault occurs only during the computation of one of E l , Ez. Without loss of generality, suppose a hard- ware fault occurs during the computation of El but no fault occurs during the computation of E2, i.e. E z = E2. Observe that

E - E = ( a E 1 + bE2) - (a&amp;

+ bkz) = a ( E 1 - E l )

<!-- PDF_PAGE: 4 -->

## PDF page 4

40

NOW, if El - El is not divisible by p then

and so N can be easily factored. Notice that if the factors of N are originally chosen at random then it is extremely unlikely that p divides El - E l . After all, El - El can have at most logN factors. To summarize, using one faulty signature and one correct one the modulus used in the RSA system can be efficiently factored. We note that the above attack works under a very general fault model. It makes no difference what type of fault or how many faults occur in the computation of E l . All we rely on is the fact that faults occur in the computation modulo only one of the primes. Arjen Lenstra [9] observed that, in fact, one faulty signature of a known mes- sage M is sufficient. Let E = M J mod N . Let E be a faulty signature obtained under the same fault as above, that is E E E mod q but E f E mod p . It now follows that gcd(M - ke) N ) = q

where e is the public exponent used to verify the signature, i.e. Ee = M mod N . Thus, using the fact that the message M is known it became possible to factor the modulus given only one faulty signature. This is of interest since most impIementations of RSA signatures avoid signing the same message twice using some padding technique. Lenstra’s improvement shows that as long as the entire signed message is known, even such RSA/CRT systems are vulnerable to the hardware faults attack. The attack on Chinese remainder theorem implementations applies t o other cryptosystems as well. For instance, the same attack applies to Rabin’s signature scheme [lo]. A Rabin signature of a number t mod N is the modular square root o f t . The extraction of square roots modulo a composite makes use of CRT and is therefore vulnerable to the attack described above.

3 Register faults

From here on our attacks are based on a specific fault model which we call register faults. Consider a tamper-resistant device. We view the device as composed of some circuitry and a small amount of memory. The circuitry is responsible for performing the arithmetic operations. The memory (registers plus a small on chip RAM) is used to store temporary values. Our fault model assumes that the circuitry contains no faults. On the other hand, a value stored in a register may be corrupted. With low probability, one (or a few) of the bits of the value stored in some register may flip. We will need this event to occur with sufficiently low probability so that there is some likelihood of the fault occurring exactly once throughout the computation. As before, all errors are transient and the hardware has no clue that the change has taken place.

<!-- PDF_PAGE: 5 -->

## PDF page 5

41

The Fiat-Shamir identification scheme

4

The Fiat-Shamir [5] identification scheme is an efficient method enabling one party, Alice, to authenticate it’s identity to another party, Bob. They first agree on an la-bit modulus N which is a product of two large primes and a security parameter t . Alice’s secret key is a set of invertible elements s1, . . . , st mod N . Her public key is the square of these numbers v1 = s:, . . . , vt = sp (mod N ) . To authenticate herself to Bob they engage in the following protocol:

1. Alice picks a random r E Z$ and sends r2 mod N to Bob. 2. Bob picks a random subset S E (1,. . . , t } and sends the subset to Alice. 3. Alice computes y = r . HiEs s, mod N and sends y to Bob. (mod N ) . 4. Bob verifies Alice’s identity by checking that y2 = r2 . vi

niEs

For the purpose of authentication one may implement Alice’s role in a tamper resistant device. The device contains the secret information and is used by Alice to authenticate herself to various parties. We show that using register faults one can extract the secret s1, . . . , st from the device. We use register faults that occur while the device is waiting for a challenge from the outside world.

Theoreml. Let ilr be an n-bit modulus and t the predetermined security pa- rameter of the Fiat-Shamir protocol. Given t faulty runs of the protocol one can recover the secret s1, . . . , st in the tame it takes t o perform O(nt + t 2 ) modular muitiplieations.

Proof. Suppose that due to a miraculous fault, one of the bits of the register holding the value r is flipped while the device is waiting for Bob to send it the set S. In this case, Bob receives the correct value r2 mod N , however y is computed incorrectly by the device. Due to the fault, the device outputs:

iES

where E is the value added to the register as a result of the fault. Since the fault is a single bit flip we know that E = f2’ for some i = 0, , . . , n - 1. Observe that Bob knows the value v; and he can therefore compute

niEs

Since there are only la possible values for E Bob can guess its value. When E is guessed correctly Bob can recover r since

( r + E)’ - r p 2 = 2 E . r + E2 (mod N )

and this linear equation in T can be easily solved. Bob’s ability t o discover the secret random value r is the main observation which enables him to break the system. Using the value of r and E Bob can compute:

<!-- PDF_PAGE: 6 -->

## PDF page 6

To summarize, Bob can compute the value E and using the formula:

2E.y - r2

ni,,

n,,,

42

n,,, by guessing the fault value

si

+ E 2 (mod N)

n,,,

niEs

ni,,

n,,,

We now argue that Bob can verify that the fault value E was guessed cor- sj obtained from the above for- rectly. Let T be the hypothesized value of mula. To test if T is correct Bob can verify that the relation T 2 = Vi mod N holds. Usually only one of the possible values for E will satisfy the relation. In such a case Bob correctly obtains the value of si. Even in the unlikely event that two values E , E' satisfy the relation, Bob can still break the system. If there are two possible values El E' generating two values T, T', T # T' satisfying the relation then clearly T 2 = (TI)' mod N . If T # -T' mod N then Bob can already factor N . Suppose T = -T' mod N . Then since one of T or T' must equal si (one of E , E' is the correct fault value) it follows that Bob now knows si mod N up to sign. For our purposes this is good enough. The testing method above enables Bob to check whether a certain value of E is the correct one. By testing all n possible values of E until the correct one is found Bob can compute s i . Consequently, to correctly determine the value s i for one set S requires O ( n + t ) modular multiplications. For t sets we of need O(nt t 2 ) modular multiplications. Observe that once Bob has a method for computing si for various sets S of his choice, he can easily find s1, . . . , s t . The simplest approach is for Bob to construct si for singleton sets, i.e. sets S containing a single element. If S = {k} then s; = sk and hence the s;'s are immediately found. How- ever, it is possible that the device might refuse to accept singleton sets S. In this case Bob can still find the si's as follows. We represent a set S (1, . . . , t } by its characteristic vector U E (0, l}t, i.e. U; = 1 if i E S and U; = 0 other- wise. Bob picks sets Sl, . . . , St such that the corresponding set of characteristic vectors U 1 , . . . , Ut form a t x t full rank matrix over 222. Bob then uses the method described above to construct the values Ti == si for each of the sets S1 , . . . , St. To determine s1 Bob constructs elements a l , . . . , at E ( 0 , l ) such that a1U1 . . atUt = ( 1 , 0 , 0 , . , . , O ) (mod 2)

njEs

+

ni,,

niES

+ .+

n,,,

n,,,,

These elements can be efficiently constructed since the vectors U1, . . . , Ut are linearly independent over Zz. When all computations are done over the integers we obtain that

for some known integers bl , . . . , b t . Bob can now compute s1 using the formula

<!-- PDF_PAGE: 7 -->

## PDF page 7

Recall that the values vi = : s

,

43

(mod N ) are publicly available. The values

s2, . . . st can be constructed using the same procedure. This phase of the algo-

rithm requires O(t2) modular multiplications. To summarize, the entire algorithm above made use of t faults and made 0 O(nt t 2 ) modular multiplications.

+

We emphasize that the faults occur while the device is waiting for a challenge from the outside world. Consequently, the adversary knows at exactly what time the register faults must be induced. We described the algorithm above for the case where a register fault causes a single bit flip. More generally, the algorithm can be made to handle a small number of bit flips per register fault. However, finding the correct fault value E becomes harder. If a single register fault causes c bits in the register to flip then the running time of the algorithm becomes O(nct) modular multiplications.

A modification of the Fiat-Shamir scheme

4.1

+

One may suspect that our attack on the Fiat-Shamir scheme is successful due to the fact that the scheme is based on squaring. Recall that Bob was able to compute the random value r chosen by the device since he was given r2 and (T E ) 2 where E is the fault value. One may try to modify the scheme and use higher powers. We show that our techniques can be used to break this modified scheme as well. The modified scheme uses some publicly known exponent e instead of squar- ing. As before, Alice's secret key is a set of invertible elements s1, . . . , st mod N . Her public key the set of numbers w 1 = s:, . . . , wt = s: mod N . To authenticate herself to Bob they engage in the following protocol:

1. Alice picks a random r and sends re mod N to Bob. 2. Bob picks a random subset S E (1,. . . , t } and sends the subset to Alice. 3. Alice computes y = r . s i mod N and sends y to Bob. (mod N ) . 4. Bob verifies Alice's identity by checking that ye = re . 216

n,,,

n,,,

When e = 2 this protocol reduces to the original Fiat-Shamir protocol. Using the methods described in the previous section Bob can obtain the values L1 = re mod N and LZ = (r+E)e mod N . As before we may assume that Bob guessed the value of E correctly. Given these two values Bob can recover T by observing that r is a common root of the two polynomials

x e = L1 ( m o d N ) and

= Lz (mod N )

Furthermore, T is very likely t o be the only common root of the two polyno- mials. Consequently, when the exponent e is polynomial in n Bob can recover r by computing the GCD of the two polynomials. Once Bob has a method for computing T he can recover the secrets sl, . . . , st as discussed in the previous section.

<!-- PDF_PAGE: 8 -->

## PDF page 8

44

Attacking Schnorr's identification scheme

5

The security of Schnorr's identification scheme [ll] is based on the hardness of computing discrete log modulo a prime. Alice and Bob first agree on a prime p and a generator g of Z;. Alice chooses a secret integer s and publishes y = g' mod p as her public key. To authenticate herself to Bob, Alice engages in the following protocol:

1. Alice picks a random integer r E [ O , p ) and sends z = gr m o d p to Bob. 2. Bob picks a random integer t E [0, T ] and sends t to Alice. Here T &lt; p is

some upper bound chosen ahead of time. 3. Alice sends u = T t . s mod p - 1 to Bob. 4. Bob verifies that gu = z ,yt mod p .

+

For the purpose of authentication one may implement Alice's role in a tamper resistant device. The device contains the secret information s and is used by Alice to authenticate herself to various parties. We show that using register faults one can extract the secret s from the device. In this section log z denotes logarithm of z to the base e .

3

Theorem 2 . Let p be an n-bit prime. Given nlog4n faulty runs of the protocol an the time it takes to one can recover the secret s with probability at least perform O(n2 log n) modular multiplications.

-

Proof. Bob wishing to extract the secret information stored in the device first picks a random challenge t E The same challenge will be used in all invocations of the protocol. Since the device cannot possibly store all challenges given to it thus far, it cannot possibly know that Bob is always providing the same challenge t . The attack enables Bob to determine the value t s mod p - 1 from which the secret value s can be easily found. For simplicity we set z = t s mod p - 1 and assume that g" mod p is known to Bob. Suppose that due to a miraculous fault, one of the bits of the register holding the value r is flipped while the device is waiting for Bob to send it the challenge t . More precisely, when the third phase of the protocol is executed the device finds f = T f 2' in the register holding r. Consequently, the device will output i = i z mod p - 1. Suppose 7' = r 2i. Bob can determine the value of i (the fault position) by trying all possible values i = 0, . . . , n - 1 until an i satisfying

+

+

+

is found. Assuming a single bit flip, there is exactly one such i. The above identity proves to Bob that i = r 2' showing that the i'th bit of r flipped from a 0 to a 1. Consequently, Bob now knows that indeed that i'th bit of T must be 0. Similar logic can be used to handle the case where i = r - 2'. In this case Bob can deduce that the i'th bit of r is 1. More abstractly, Bob is given z + r('), . . . , z + dk) mod p - 1 for random values r ( l ) , . . . , r @ ) (recall k = n log4n). Furthermore, Bob knows the value of

<!-- PDF_PAGE: 9 -->

## PDF page 9

2,

45

5.

some bit of each of dl), . . . , dk). Obtaining this information requires O(n2 log n ) modular multiplications since for each of the iE. faults one must test all n possible values of i. Each test requires a constant number of modular multiplications. We claim that using this information Bob can recover z in time O ( n 2 ) . We assume the k faults occur at uniformly and independently chosen locations in the register r . The probability that at least one fault occurs in every bit position k = In other words, of the register T is at least 1 - n (1 - $) 2 1 - n . with probability at least for every 0 5 i &lt; n there exists an di) among dl), . . . , dk) such that the i’th bit of di) is known to Bob (we regard the first bit as the LSB). To recover z Bob first guesses the log 8n most significant bits of z. Later we show that Bob can verify whether his guess is correct. Bob tries all possible log 8n, bit strings until the correct one is found. Let X be the integer that matches z on the most significant log8n bits and is zero on all other bits. For now we assume that Bob correctly guessed the value of X. Bob recovers the rest of 1: starting with the LSB. Inductively su pose Bob already knows bits x i - 1 . . . zlzo of 1: (Initially i = 0). Let Y = Cizo 23 zj. To determine bit zi Bob uses di), of which he knows the i’th bit and the value of 2 + di). Let b be the i’th bit of di). Then

‘ P .

+

zi = b @ i’th bit(z

s.

- Y - X mod p - 1)

T(’)

assuming no wrap around, i.e., 0 5 z + d i ) - Y - X &lt; p - 1. By construction we know that 0 5 1: - X - Y &lt; p / 8 n . Hence, wrap around will occur only if d i ) &gt; (1 - &amp; ) p . Since the T ’ S are independently and uniformly chosen in the range [ O , p ) the probability that this doesn’t happen in all n iterations of the algorithm is ( 1 - &amp;)” &gt; To summarize, we see that for the algorithm to run correctly two events must simultaneously occur. First, all bits of T must be “covered” by faults. Second, all the P , must be less than (1 - &amp; ) p . Since each event occurs with probability at least both events happen simultaneously with probability at least f . Consequently, with probability at least f , once X is guessed correctly the algorithm runs in linear time and outputs the correct value of x. Of course, once a candidate x is found it can be easily verified using the public data. There are O ( n ) possible values for X and hence the running time of this step is O ( n 2 ) . Since the first part of the algorithm requires O(n2 log n) modular multiplications it dominates in the overall running time. 0

2,

We note that the attack also works when a register fault induces multiple bit flips in the register T (i.e. i = P + 2,j). As long as the number of bit flips c is constant, their exact location can be found in polynomial time. We also note that the faults we use occur while the device is waiting for a challenge from the outside world. Consequently, the adversary knows at exactly what time the faults should be induced.

<!-- PDF_PAGE: 10 -->

## PDF page 10

46

6 Breaking other implementations of RSA

In Section 2.1 we observed that CRT based implementations of RSA can be easily broken in the presence of hardware faults. In this section we show that using register faults it is possible t o break other implementations of RSA as well. Let N be an n-bit RSA composite and s a secret exponent. The exponentiation zs mod N can be computed using either one of the following two function t algorithms (we let s = sn-1sn-2 . . . slso be the binary representation of s):

-

- Algorithm I

init yltz; z t l . main For k = 0 , . . . , n - 1. If sk = 1 then z + z . y (mod N ) . y+y2 (modN). output 2. - Algorithm I1 init z t 1. main For k = n - 1 down to 0. If Sk = 1 then z + z2 . t (mod N ) . Otherwise, z t z2 (mod N ) . output 2 .

For both algorithms given several faulty values one can recover the secret exponent in polynomial time. Here by faulty values we mean values obtained in the presence of register faults. The attack only uses erroneous signatures of randomly chosen messages; the attacker need not obtain the correct signature of any of the messages. Furthermore, an attacker need not obtain multiple sig- natures of the same message. The following result was the starting point of our research on fault based cryptanalysis:

Theorem3. Let N be an n-bit RSA modulus. For a n y 1 5 m 5 n, given (n/m)Iog2n faults, the secret exponent s can be extracted from a device imple- menting the first exponentiation algorithm with probability at least in the tame it takes t o perform O ( ( P n 3 log2 n)/m2) RSA encryptions.

4

Proof. We use the following type of faults: let M E ZN be a message to be signed. Suppose that at a single random point during the computation of M S mod N a register fault occurs. More precisely, at a random point in the computation one of the bits of the register z is flipped. We denote the resulting erroneous signature by E . We intend to show that an ensemble of such erroneous signatures enables one to recover the secret exponent s. Even if other types of faulty signatures are added to the ensemble, they do not confuse our algorithm. Let 1 = (n/m)log2n and let M I , . . . , Ml E ZN be a set of random messages. Set Ei = Mi” mod N to be the correct signature of Mi. Let E; be an erroneous signature of Mi. We are given E i but do not know the value of Ei. A register fault occurs at exactly one point during the computation of E i , Let ki be the

<!-- PDF_PAGE: 11 -->

## PDF page 11

47

(y)'

&amp; 4.

value of k (recall k is the counter in algorithm I) at the point at which the fault occurs. Thus, for each faulty signature, I?,, there is a corresponding Ici indicating the time at which the fault occurs. We may sort the messages so that 0 5 kl 5 kz 5 . . . 5 k , &lt; n. The time at which the faults occur is chosen uniformly (among the n iterations) and independently at random. It follows that given 1 such faults, with probability at least half, k i + l - k i &lt; rn for all i = 1, . . . , I - 1. To see this observe that the probability that no fault occurs in a specific interval of width rn is &lt; 1/2n. Since there are at most n such intervals the probability that all of them contain a fault is at least 1 - n . = Note that since we do not know where the faults occur, the values ki are unknown to us. Let s = ~ ~ - 1 . s . 1 . s o be the bits of the secret exponent s. We recover a block of these bits at a time starting with the MSBs. Suppose we already know bits s n - l . . . s k , for some i. Initially i = 1 + 1 indicating that no bits are known. I've show how to recover bits s k , - l S k , - z . . . s k , - l . w e intend to try all possible bit vectors until the correct one is found. Since even the length of the block we are looking for is unknown, we have to try all possible lengths. The algorithm works as follows:

c,",-:,

1. For all lengths r = 1 , 2,3 . . . do: 2. For all candidate r-bit vectors U k 1 - 1 u k , - 2 . . . u k , - , . do: 3 . Set w = sj2J + E;L.:-r u j 2 3 . In other words, w matches the bits of s and u at all known bit positions and is zero everywhere else. 4. Test if the current candidate bit vector is correct by checking if one of the erroneous signatures E3 , j = 1, . . . , I satisfies

3b E (0,. . . , n} s.t.

(kj &amp; 2 b M y ) e = Mj

(mod N )

Recall that e is the public signature verification exponent. The f means that the condition is satisfied if it holds with either a plus or minus. 5 . If a signature satisfying the above condition is found output U k , - l U k , - 2 . . . U k , - r and stop . At this point we know that k i - 1 = k i -r and S k , - l S k , - 2 . . . s k , - l - -

Ukt-1Uk,-2 * * .Uk,-r*

Uk,-1?&amp;,-2

We show that the condition at step (4) is satisfied by the correct candidate . . . u k , - l . To see this recall that E i - 1 is obtained from a fault at the Rd-l'st iteration. That is, at the ICi-I'st iteration the value of z was changed to 2 + z f 2b for some b. Notice that at this point E d - 1 = zMiw_,. From that point on no fault occurred and therefore the signature E i - 1 satisfies

= ; M E l = Ei-1 f 2bMiW_i (mod N )

ii-1

When in step (4) the signature hi-1 is corrected it properly verifies when raised to the public exponent e . Consequently, when the correct candidate is tested, the faulty signature E i - 1 guarantees that it is accepted. To bound the running time of the algorithm we bound the number of times the condition of step (4) is executed. One must try all possible candidate bit

<!-- PDF_PAGE: 12 -->

## PDF page 12

vectors u against all possible error locations b and erroneous signatures Ej. Consequently, the number of times the condition is tested is at most

Hence, the algorithm runs in the time it takes to perform O((2"n310g2 n ) / r n 2 ) RSA encryptions. We still need to show that a wrong candidate will not pass the test of step (4) with high probability. Suppose some signature E,, incorrectly causes the wrong candidate u' to be accepted at some point in the algorithm. That is, E,, f2'MM,w = E,, mod N even though E,, was generated by a different fault (here w is defined as in step (3) using the bits of u'). We know that &amp; = Ev k 2 " M ~ ' for some b l , wl with w1 # w. Therefore,

E,, f 2'lMt1 f 2°F

= E, (mod N )

n:='=,

In other words, Mu is a root of a polynomialof the form u l x w l +a2zW = 0 mod N for some u l , u2, w1, w. To bound the number of roots write p(N) = qr' and gcd(w1 - w , cp(N)) = $ where the qi are distinct primes. The number of

nf=,

n,=,

roots is upper bounded by a def = e q,". (this is the maximum number of roots of a polynomial of the form d " l - w = u3 mod N ) . Observe that a is a function of w and w1. Since the message Mv is chosen independently of the fault location (i e. independently of b l , 201) it follows that Mu is a root with probability at most a / N . Consequently, the probability that a specific E,, causes a specific wrong candidate u' to be accepted is bounded by a / N . Define 6 to be the maximum value of a over all possible values of w, wl (note that there are I possible values for w1 and 0(2"1) possible values for w). Let B be the number of times the equality test at step (4) is invoked, i.e. B = O ( d 2 2 " ) . Then the probability that throughout the algorithm a wrong candidate is ever accepted is bounded by B Q I N . We argue that with high probability (over the fault locations) 6 &lt; N / n B . This will prove that a wrong candidate is never accepted with probability at least 1 - (over the random messages I&amp;). This will complete the proof of the theorem. Suppose that over the random choice of the secret exponent s, and the ran- dom choice of the fault location k, we have that Pr[&amp; &gt; N / n B ] &gt; l / n c for some fixed c 2 1. We show that in this case there is an efficient algorithm for factoring N . This will prove that we may indeed assume that &amp; &lt; N / n B with probability bigger than 1 - for all c 2 1 (since otherwise N can already be factored). 'The factoring algorithm works as follows. It picks a random exponent s and random messages M I , . . . , Mi E Z N . It then computes erroneous signatures E, of the Mi by using the first exponentiation algorithm to compute Mp mod N and deliberately simulating a random register fault at a random iteration. By assumption, with probability at least l/nc we have (Y &gt; N / n B . Here the values w, wi, a and (Y are defined as above using the simulated faults. Since i5 &gt; N / n B

5

<!-- PDF_PAGE: 13 -->

## PDF page 13

49

there exist some w , w 1 for which a &gt; N / n B . By definition of a it follows that p(N) divides t ( q - w)" for some integer 0 &lt; t 5 nB. To see this observe that a divides (w1 - w ) ~ and a = p(N)/t for some 0 &lt; t 5 nB. These values 20, w1, t can be found using exhaustive search since there are only O(I. 2*l$ n B ) = ( n 2 " ) O ( l ) possibilities. Once a multiple of y ( N ) is constructed, namely t ( q - w)", the modulus N can be efficiently factored. By repeating this process ne times we factor N with constant probability. The total running time of the algorithm is polynomial in n and 2".

0

If one allows the algorithm to obtain both the erroneous and correct signature of each message Mi then the running time of the algorithm can be improved. The test at step (4) can be simplified to

3b E ( 0 , . . . , n } s.t. Ej k 2*M? = Ej

(mod N )

thus saving the need for an RSA encryption on every invocation of the test.

7

Defending against an attack based on hardware faults

One can envision several methods of protection against the type of attack dis- cussed in the paper. The simplest method is for the device to check the output of the computation before releasing it. Though this extra verification step may reduce system performance, our attack suggests that it is crucial for security reasons. In some systems verifying a computation can be done efficiently (e.g. verifying an RSA signature when the public exponent is 3). In other systems verification appears to be costly (e.g. DSS). Our attack on authentication protocols such as the Fiat-Shamir scheme uses a register fault which occurs while the device is waiting for a response from the outside world. One can not protect against this type of a fault by simply verifying the computation. As far as the device is concerned, it computed the correct output given the input stored in its memory. Therefore, to protect multi- round authentication schemes one must ensure that the internal state of the device can not be affected. Consequently, our attack suggests that for security reasons devices must protect internal memory by adding some error detection bits (e.g. CRC). Another way to prevent our attack on RSA signatures is the use of random padding. See for instance the system suggested by Bellare and Rogaway [l]. In such schemes the signer appends random bits to the message to be signed. To verify the RSA signature the verifier raises the signature to the power of the public exponent and verifies that the message is indeed a part of the resulting value. The random padding ensures that the signer never signs the same message twice. Furthermore, given an erroneous signature the verifier does not know the full plain-text which was signed. Consequently, our attack cannot be applied to such a system.

<!-- PDF_PAGE: 14 -->

## PDF page 14

8 Summary and open problems

50

We described a general attack which makes use of hardware faults. The attack applies to several cryptosystems. We showed that encryption schemes using Chi- nese remainder, e.g. RSA and Rabin signatures, are especially vulnerable t o this kind of attack. Other implementations of RSA are also vulnerable though many more faults are necessary. The idea of using hardware faults to attack crypto- graphic protocols applies to authentication schemes as well. For instance, we ex- plained how the Fiat-Shamir and Schnorr identification protocols may be broken using hardware faults. The same applies to the Guillou-Quisquater identification scheme [8] though we do not give the details here. Recently several symmetric ciphers such as DES have also been analyzed for their ability to withstand a faults based attack [2]. Verifying the computation and protecting internal storage using error de- tection bits defeats attacks based on hardware faults. We hope that this paper demonstrates that these measures are necessary for security reasons. Methods of program checking [3] may come in useful when verifying computations in crypto- graphic protocols. Specifically, a recent result of Frankel, Gemmel and Yung [7] could prove useful in this context. An obvious open problem is whether the attacks described in this paper can be improved. That is, can one mount a successful attack using fewer faults? TO make the problem crisp we pose the following concrete question: can a general implementation of RSA be broken using significantly fewer faults than n, say fi? (here n is the size of the modulus). Such a result would significantly improve our Theorem 3. Ideally we would like to break a general implementation of RSA using only a constant number of erroneous encryptions.

Acknowledgements

We are grateful to Arjen Lenstra for his many helpful comments. We also thank R. Venkatesan for his help in working out some preliminary details of Differential Fault Analysis of DES in parallel to Biham and Shamir.

### References

1. M. Bellare, P. Rogaway, “The exact security of digital signatures - Bow to sign with RSA and Rabin”, in Proc. Eurocrypt 96, pp. 399416. 2. E. Biham, A. Shamir, ‘‘A New Cryptanalytic Attack on DES: Differential Fault Analysis”, Manuscript. 3. M. Blum, H. Wasserman, “Program result checking”, proc. FOCS 94, pp. 382- 392. 4. P. Kocher, “Timing attacks on implementations of Diffie-Hellman, RSA, DSS, and other systems”, Proc. of Cyrpto 96, pp. 104-113. 5. U. Feige, A. Fiat, A. Shamir, “Zero knowledge proofs of identity”, Proc. of

STOC 87.

<!-- PDF_PAGE: 15 -->

## PDF page 15

51

6. Federal Information Processing Standards, “Security requirements for cryp- FIPS publication 140-1, tographic modules”, http://vaw.nist.gov/itl/csl/fips/fipl40-1.txt. 7. Y. Frankel, P. Gemmell, M. Yung, “Witness based cryptographic program checking and robust function sharing”, proc. STOC 96, pp. 499-508. 8. L. Guillou, J. Quisquater, “A practical zero knowledge protocol fitted to se- curity microprocessor minimizing both transmission and memory”, in P ~ o c . Eurocrypt 88, pp. 123-128 9. A.K. Lenstra, Memo on RSA signature generation in the presence of faults, manuscript, Sept. 28, 1996. Available from the author. 10. M. Rabin, “Digital signatures and public key functions as intractable as factorization”, MIT Laboratory for computer science, Technical report MIT/LCS/TR-212, Jan. 1979. 11. C. Schnorr, “Efficient signature generation by smart cards”, J. Cryptology, V O ~ . 4, (1991), pp. 161-174.
