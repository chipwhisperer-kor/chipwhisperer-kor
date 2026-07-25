# [16] Memo on RSA Signature Generation in the Presence of Faults

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 4
converted_at: "2026-07-26"
source_asset_id: "HAETAE-FIA-REF-16"
derived_asset_id: "HAETAE-FIA-REF-16-MD"
source_path: "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[16] Memo on RSA Signature Generation in the Presence of Faults.pdf"
source_sha256: "34dd2283680079f3fc213cd4adbc63a598ce2b093a126bc7e9b36477b3f6d67c"
pages: 4
bbox_words: 2287
consumed_bbox_words: 2287
numeric_tokens: 100
consumed_numeric_tokens: 100
source_blocks: 33
consumed_source_blocks: 33
emitted_blocks: 33
embedded_raster_images: 4
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 4
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

I

Memo on RSA signature generation in the presence of faults

Arjen K. Lenstra, Citibank, NA., September 28 October 28, 1996

-

Introduction. This memo was written after reading newspaper articles about a Beilcore attack on smartcards, because no details about the Beilcore attack were available. In the mean time I have found (cf. [1]) that the first attack described here, on RSA signatures generated using Chinese remaindering, is more efficient and potentially more dangerous than the approach used by the Beilcore researchers: my attack requires a message and only one faulty signature of that message, the Beilcore attack requires one correct and one faulty signature of the same message. The second attack described here, on RSA signatures generated without Chinese remaindering, is probably quite similar to the attack proposed by the Beilcore researchers (cf. [1]), though I have not seen any of the details of their approach in this case. The Beilcore researchers have developed similar attacks against the Fiat-Shamit, Schnorr, and Guillou-Quisquater identification schemes and the ElGamal public key system (cf. [1]).

RSA signatures with Chinese remaindering. Let n=pq be a composite RSA-modulus, with public and secret exponents e and d. The signature S(m) of a message m equals m’ mod n. Thus, S(m)e mod n is again equal to m modulo n. It is well known that S(m) can be computed by computing m’ both modulo p and q, and by combining the two results using the Chinese remainder algorithm. If a fault occurs in the course of the computation of the signature, the resulting value S’(m) will most likely not satisfy the congruence S(m)e m mod n. If however, the fault occurred only during the computation of m’ modulo p, and if the exponentiation modulo q and the application of the Chinese remainder algorithm were carried Out correctly, then the resulting faulty signature S’(m) satisfies S(m)e m mod q, but the same congruence modulo p does not hold. Therefore, q divides S(m)e_m, but p does not divide S(m)e_m, so that a factor of n may be discovered by the recipient of the faulty signature S’(m) by computing the greatest conimon divisor of n and S(m)e_m. This implies that, even if there is the tiniest probability that an error occurs during RSA signature generation, the generator of an RSA-signature must make sure that each signature generated is indeed correct. An inefficient way to do this is by generating the signature twice and checking that the same signature was found twice. This solution assumes that an identical arithmetic error does not occur twice. Since e is usually much smaller than d, a more efficient way to proceed is to check the correctness of the signature in the same way the verifier would do it, namely by checking that S(m)e mod n is equal to m modulo n. Even if an error occurs twice, it is exceedingly unlikely that this test will be satisfied. Note that this possible weakness only occurs if RSA signatures are generated using the method sketched above. But even if m mod n is computed directly modulo n, the secret key might leak if an error is made during the computation; see below. Obviously, faulty decryption of RSA-encrypted messages using the Chinese remainder theorem can lead to decrypted messages m’ for which m’—m and n (where m is

<!-- PDF_PAGE: 2 -->

## PDF page 2

the correctly decrypted message) have a non-trivial factor in common. RSA-decryptions should therefore not be shared before their correcmess is verified. Arithmetic faults of this type may be triggered in devices with relatively low level security specffications if they are subjected to exceptional physical circumstances (abnormal voltage, heat, radiation): according to [2], the specifications of devices with security level 3 or higher require that they shut off and/or self-destroy if they are put in exceptional circumstances.

Remark. Note that the attack works if a fault is made in the data operated upon, or in the order or type of instructions that are carried out, or both, as long as the code works again properly for the Chinese remainder operation. The time-window of one of the modular exponentiations is sufficiently large that they may indeed be successfully targeted; it is unclear, however, if the circuitry will again function faultlessly afterwards, and correctly perform the remainder of the computation. If the result of the first exponentiation is stored at some particular location that is not used for any other purposes, then this attack can also be carried Out by permanently damaging the wiring of that location so that its value will never be retrieved correctly.

...,

RSA signatures without Chinese remaindering. Assume that we compute RSA signatures without the use of the Chinese remainder theorem and that a small error is made during the computation of the signature S(m) of message m. Can the secret exponent d be recovered? If only one faulty signature of some message is available, there does not seem to be much one can do. Let us assume that we may request faulty signatures S’(m) of as many different and known messages m as we would like to have, and that all S’(m)’s have some particular type of fault that is randomly selected from some collection of faults. Can we find d, and if so, how many faulty signatures do we need to find d? Let e again be the corresponding public exponent. Let the collection of (faulty signature, message) pairs received be (S’(mi), ) 1 m , (S’(m 2 ) ,m , If each S’(m ) 1 would be the (correct) signature of + (S’(mk), mk)). m , 1 E i.e., the original message plus some random and presumably small error pattern E, then we would be able to break RSA in general if we could find d from the collection of corrupted signatures. Since we consider that to be unlikely, we assume that the collection of faulty signatures received looks different, in particular we assume that they are not all dth powers (of a known value). So, let us assume that the error does not occur right away at the beginning, corrupting only the message (but leaving the computation intact), but that some type of error occurs in the course of the computation. We analyze what the effect of a single error may be, where we restrict ourselves to an error that affects a single register value once; we do not consider the possible effects of corruption of values that may be hardwired or that are stored in non-volatile memory, such as d and n. We also assume that the proper instructions are carried out in the right order. Thus, we assume that the correct code operates on values d and n that remain correct, but that one of the other values during the computation gets corrupted, presumably by a value of small Hamming weight. For an attack based on single bit distortions of d, see [3].

2

<!-- PDF_PAGE: 3 -->

## PDF page 3

9

To study this effect, we first have to consider how the exponentiation is carried out. There are essentially two methods to do this, the first using the bits of d from right to left (least to most significant), the second one using them from left to right:

1. s=m; r=1; for i=1 to #d { if (bit I of d is on) r *s; s *s;} output r

and

2. r=1; for i=#d downto 1 { r ‘= r; if (bit i of d is on) r ‘= m;} output r

In (1) we consider a single corruption of either r or s in the course of the computation, in (2) we consider a single corruption of either m or r in the course of the computation. We refer to the four different possibilities as (ir), (is), (2m), and (2r). We assume that d=(d , 1 2 * 2)+d that the corresponding public exponent is e, and that the single corruption takes place during iteration j.. We also assume that the computation from that point on is based on the corrupted value, i.e., once s gets corrupted (in (is)), all subsequent powers of s are also corrupted, and are powers of the corrupted s. (For an attack where only a single s gets corrupted by a single bit, and where all subsequent powers are again correct, see [3].) The attack is based on the observation that (again assuming (is)) if the leading j bits of d are known and k is large enough, then there should be an 1 m for which the (d 2 2J) is equal to the corrupted signature divided by its correct signature divided by ml” * ‘corrupted part’ 2 (m”(2)+E)”d for some small error E. Thus the eth powers of these values are also equal, so that the eth power of the correct signature can be replaced by m. This equality can be used to confirm a guess for the jth bit of d, once the first j—1 bits of d are known, by trying sufficiently many small error patterns E. We now describe this approach in somewhat more detail. Let #d denote the number of bits of d. As a result of the corruption and based on our assumption, the S(m)’s look as follows, where in each case 1 E is an error pattern, most likely of small Hamming weight (and everything is done modulo n):

) (m 2 1 A 2J))(m di+E (d (ir): * (is): ” ((m 2 1 ) (2)+E ”d d (m1(d 2 2J))(m ) (2m): * +E 1 ”d (2r): + ) ((m 2 1 ” E)”(2))(m’d d

Given a sufficiently large k (with either all S(m ) of type (ir) or (is), or all of type (2m) or 1 (2r)) we may be able to retrieve d. Omitting all details, and with a lot of handwaving, this goes as follows (assuming (ir) or (is); (2m) or (2r) goes similarly). Assume that the first f and the last I bits of d are already known (namely d and ) 1 d . We guess the next bit of df and append it to df resulting in dr’ of length f÷1. For all E’s of low Hamming weight and all available (and unused) ) S’(m 1 ’s (some of them of type (is), and some of which might even have the correct j=#d—f—1), compute

(m ” /((m ’ (2 4 ))+E) ‘d’)’ (s ) 1

‘

and compare the result to

3

<!-- PDF_PAGE: 4 -->

## PDF page 4

(S(m 1 ) /(m A (df’ *2# d.4_1)))e = 1 mjl(m A (e*dr *2# d—f_1))•

If a match is found, it is likely that we were using the correct guess dr’, the correct E, and that we were comparing with a type (is) fault. The ‘correct’ S’(m) can now be marked as used. If no match is found, guess the other df’, and try again. Similarly, we may try to find new bits of d , hoping that we have values of type (ir). If none of the S’(m)’s had the 1 right j=#d—f—1 or j=I+1, we may simply progress with a guess for either d’ or ’ 1 d , until we find a match at f+u or 1+u for a small value of u (trying all guesses for all small u’s). If no match is found, the ‘j-gap’ in the collection of ) S’(m 1 ’s is too large, or the error pattern was too large, and more ) S’(m 1 ’s need to be collected. How large does k need to be? If we do not allow gaps between the j’s and insist on a match at each step we need k on the order of (#d)log(#d). If we allow rather large gaps (i.e., large u’s) and make sure that we try all possible error patterns, then a k of the same order of magnitude as #d suffices. For instance, for #d= 1024, the maximal gap for k=i024 can be expected to be about 7 (for 512 it is only 4, however). As mentioned above, many details would have to be filled in in order to obtain a complete description of this ‘attack’. Given how ‘realistic’ our attack scenario is, however, providing these details is probably not worth the trouble. In circumstances where this attack is considered to be realistic, signatures should be checked for correctness before they are transmitted. Note that our attack scenario is about just as realistic as the scenarios from [4] and [5].

Run time. For each fixed u the run time of the above approach is polynomial in the number of error patterns allowed, and in all other relevant variables. Note that a similar approach can be used to retrieve d if more than a single corruption takes place during the computation; the run time remains polynomial as long as the number of corruptions is bounded by a fixed constant.

References.

1. Dan Boneh’, personal communication, October 1996. 2. Security Requirements for Cryptographic Modules, FIPS PUB 140-1. 3. Feng Bao, Robert Deng, Yongfei Han, Albert Jeng, Teow Hin Nagir, Desai Narasinihalu, A new attack to RSA on tamperproof devices, manuscript, October 23, 1996. Available from the first author (baofeng@iss nus. sg). 4. Eli Biham, Adi Shamir, A new cryptanalytic attack on DES, draft, October 18, 1996. 5. Jean-Jacques Quisquater, Short cut for exhaustive search using fault analysis: applications to DES, MAC, keyed hash function, identification protocols, draft, October 23, 1996.

.

...,

Dan Boneh is one of the authors of the original Beilcore paper Cryptanalysis in the presence of hardware faults by Boneh, DeMillo, and Lipton; a draft of this paper exists, but is not for distribution. Addition, October 30, 1996: an extended abstract of a Beilcore paper titled On the importance of checking computations by the same authors may now be obtained from the first author (dabo@bellcore corn).

.

4
