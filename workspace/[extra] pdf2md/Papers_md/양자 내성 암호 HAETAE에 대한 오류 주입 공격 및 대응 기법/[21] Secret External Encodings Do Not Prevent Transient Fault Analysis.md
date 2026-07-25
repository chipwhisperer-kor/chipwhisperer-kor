# [21] Secret External Encodings Do Not Prevent Transient Fault Analysis

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 14
converted_at: "2026-07-26"
source_asset_id: "HAETAE-FIA-REF-21"
derived_asset_id: "HAETAE-FIA-REF-21-MD"
source_path: "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[21] Secret External Encodings Do Not Prevent Transient Fault Analysis.pdf"
source_sha256: "7eb9ca34a8882e14dce12eaf29d89238247482983e24b86d7c36a39306bab6c7"
pages: 14
bbox_words: 5892
consumed_bbox_words: 5892
numeric_tokens: 659
consumed_numeric_tokens: 659
source_blocks: 189
consumed_source_blocks: 189
emitted_blocks: 166
embedded_raster_images: 76
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 14
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

Secret External Encodings Do Not Prevent Transient Fault Analysis

Christophe Clavier

Gemalto, Security Labs, La Vigie, Avenue du Jujubier, ZI Athélia IV, F-13705 La Ciotat Cedex, France christophe.clavier@gemalto.com

Abstract. Contrarily to Kerckhoﬀs’ principle, many applications of today’s cryptography still adopt the security by obscurity paradigm. Furthermore, in order to rely on its proven or empirical security, some realizations are based on a given well known and widely used crypto- graphic algorithm. In particular, a possible design would obfuscate a standard block cipher E by surrounding it with two secret external en- codings P 1 and P 2 (one-to-one mappings), leading to the proprietary algorithm E’ = P 2 ◦ E ◦ P 1 . A claimed advantage of this approach is that, since inputs and out- puts of the underlying function E are not known by a potential attacker, such a construction is usually believed to inherently prevent any kind of transient fault analysis that may apply on the core function E. In this paper, we show that this latter argument is not true, by exhibiting a key recovery attack which applies to the whole class of externally encoded DES or Triple-DES. Moreover, our attack remains applicable even in the presence of the classical counter-measure against fault attacks which consists in executing the algorithm twice and returning an output only if both results are identical.

Keywords: Smart Cards, Physical Attacks, Fault Analysis, Secret Algorithm, Cryptographic Design, External Encoding, DES.

1 Introduction

Contrarily to Kerckhoﬀs’ principle, many applications of today’s cryptography still adopt the security by obscurity paradigm. For public and civil applications, this is especially true in GSM and pay-TV domains where the speciﬁcations of the cryptographic function are often kept secret. A usually claimed advantage of concealing the cryptographic function’s details is to protect against known physical attacks such as side-channel analysis (SPA, DPA, CPA,. . . ) [2,10] or fault analysis (DFA, CFA,. . . ) [1,4,5,7], which would otherwise be used to reveal the user’s secret key. The main result of this paper is to partially invalidate this belief. More pre- cisely, we focus on a particular way of designing such a proprietary algorithm

P. Paillier and I. Verbauwhede (Eds.): CHES 2007, LNCS 4727, pp. 181–194, 2007. c Springer-Verlag Berlin Heidelberg 2007

<!-- PDF_PAGE: 2 -->

## PDF page 2

182 C. Clavier

which consists in surrounding a well known and widely used block cipher E with two secret external encodings P 1 and P 2 (one-to-one mappings over the input and output spaces), leading to the new secret obfuscated block cipher E’ = P 2 ◦ E ◦ P 1 . The motivation for such a design strategy is twofold. First, it seems reasonable to base the construction on a well known block cipher E in order to inherit its proven or empirical cryptographic strength. Second, the two secret encodings P 1 and P 2 ensure that inputs to and outputs from E can not be known by an attacker, so that physical attacks requiring this knowledge should not be feasible. In this paper, we present a fault-based key recovery attack which applies to this design when the core block cipher E is the DES or the Triple-DES. Our attack works for any P 1 and P 2 , so that the whole class of externally encoded (Triple-)DES (c.f. Figure 1) is potentially endangered 1 .

Fig. 1. A DES obfuscated by secret layers P 1 and P 2

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 2]

In Section 2 we present the previous work related to fault analysis of secret cryptographic functions, as well as our threat model and the conditions needed for the attack. Section 3 gives two variants of our attack: ﬁrst, a basic version that illustrates the main principles is explained; then, an improved attack is described and simulation results are presented. Possible counter-measures are discussed in the next section. Finally, Section 5 concludes this work and proposes some possible directions for further research.

2 Preliminaries

Boneh et al. ﬁrst introduced in [5] the use of transient computational errors as a means to extract secret keys of cryptographic algorithms. Their attack applies to RSA in CRT mode and has been shortly followed by similar results applicable to the DES algorithm [4] and other functions. These methods all rely on the fact that the cryptographic algorithm is public. In [3], Biham and Shamir tackled the unknown cryptosystem case and proposed an attack based on the assumption that it is possible to permanently and progressively reset bits of the key stored in a non-volatile memory. This technique has been later improved and extended by Paillier in [12]. Since it requires permanent faults, this model is

1

As a particular case where P 1 and P 2 are XOR-maskings with external keys, our attack notably applies to the DESX construction [9] and allows to recover its internal secret key.

<!-- PDF_PAGE: 3 -->

## PDF page 3

Secret External Encodings Do Not Prevent 183

quite demanding. Moreover, deﬁnitively damaging the device under attack may be undesirable. Nevertheless, as far as we know, no transient fault attack on unknown cryptosystems has ever been published. Our proposed attack precisely attains this goal under the following assumptions: The target is a classical software implementation of the DES on an 8-bit architecture. We assume that the attacker is able to precisely control which instruction is executed when he injects a fault. Concerning the fault model, we assume that a fault injected during the execu- tion of a XOR between two 8-bit operands results in a zero 2 output whatever the input operand values were. Let us mention that this fault model is realistic as we identiﬁed some chips vulnerable to this kind of faults on which we practically performed attacks relying on it. Finally, the attacker is supposed to have control over the input given to the encryption function E’ as well as knowledge of its output 3 . Compared to fault analysis on public cryptosystems, our attack needs a large number (many thousands) of fault injections. We see this drawback as the fair price to pay for the ‘magic’ property of being able to retrieve the key regardless of the two secret external encodings P 1 and P 2 .

3 Ineﬀective Fault Analysis

### 3.1 Fault Injection as a Probing Tool

Our attack, described in Sections 3.2 and 3.3, is based on the main observation that a fault injection capability may be used as a probing tool. More precisely, if an attacker targets a particular XOR instruction in the algorithm, then he is able to detect whether the output of this instruction is equal to zero or not. For some arbitrary input, if the output of the algorithm when a fault is injected during the targeted XOR is the same as that of a normal execution, this indi- cates that the natural value of the XOR result is zero 4 . Some information about an intermediate value is thus obtained by observing two equal outputs of the algorithm. Equivalence between outputs happens when the injected fault has no eﬀect on the targeted instruction and its intermediate result. This event being the most informative one exploited in our attack, we call such kind of attack an Ineﬀective Fault Analysis (IFA). Though it is rather similar to safe-error analy- sis ([8,13,14]), IFA is slightly diﬀerent since the fault targets a true instruction, whose output is possibly not modiﬁed, rather than a fake instruction. In the case of IFA, the event of an unchanged algorithm output results from a data related condition, whereas it is algorithm speciﬁc in safe-error analysis.

2

Note that our attack works equally well if the faulted XOR output is supposed to be any arbitrary known constant instead of zero. 3 These assumptions may be relaxed. It is only required to be able to replay many times diﬀerent arbitrary inputs, and to detect whether two outputs are equal. 4 Or at least that this value is equivalent to zero through the remainder of the algo- rithm. This comment will become clearer in the example given in Section 3.2.

<!-- PDF_PAGE: 4 -->

## PDF page 4

184 C. Clavier

In the context of this paper, for any given plaintext, IFA allows an attacker to detect whether the output of any arbitrary XOR of the embedded DES is zero.

### 3.2 The Basic Attack

We refer to [11] for a complete description of the DES algorithm. Nevertheless, and before describing the attack in detail, we remind the reader that the DES key schedule is structured in such a way that the key may be considered as partitioned into two 28-bit half-keys, which we respectively denote K A and K B . During any round, the 24 key bits involved in S-boxes 1 to 4 are a subset of K A , while the 24 key bits involved in S-boxes 5 to 8 belong to K B . Even though our attack does not rely on this property, we will take advantage of it to computa- tionally simplify the faults exploitation by considering the two half-key spaces separately.

We assume a straightforward implementation of the DES on an 8-bit ar- chitecture. In this typical implementation, there are 12 XOR operations per round. As shown in Figure 2, for each round h = 2, . . . , 16, we are concerned with two groups of XOR instructions. The ﬁrst group, made up of four so- called xor left instructions executed at the end of round (h − 1), computes the four bytes (r 1 , . . . , r 4 ) of the 32-bit value R h which enters the round h. Then (r 1 , . . . , r 4 ) is expanded into eight 6-bit values (s 1 , . . . , s 8 ) which are XOR-ed with the round key K h = (k 1 , . . . , k 8 ), through the eight so-called xor key in- structions, to provide the S-box inputs (x 1 , . . . , x 8 ). Each 4-bit S-box output is computed as y j = S j (x j ).

The central idea in this basic attack is to infer information about the key from couples of two ineﬀective faults on two diﬀerent executions with the same input. While information about two intermediate values of some computation is so obtained, we stress that our attack does not require the ability to inject multiple faults on the same execution. First, suppose that for some plaintext M , a fault injected during xor left[i] (for i ∈ {1, . . . , 4}) at round (h − 1) turns out to be ineﬀective. This implies that the corresponding output byte r i is zero. Thus, 8 of the 32 bits of R h are known to be 0. The following permutation expands them to 12 bits which are involved in four adjacent 5 S-boxes at round h. Now, suppose that for another execution with the same plaintext M , a fault on xor key[j] (for j ∈ {2i − 1, 2i}) at round h turns out also to be ineﬀective. In this setting, we show that some valuable information about the 6-bit k j may be inferred. This is the basic principle behind our attack. We now give an example of this reasoning:

Example: For some M , an ineﬀective fault on xor left[3] at round (h − 1) gives r 3 = 0. Figure 3 shows that when r 3 = 0, the 6-bit inputs s 4 to s 7 of xor key[4] to xor key[7] of the next round belong to (∗, ∗, ∗, ∗, ∗, 0), (∗, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, ∗) and (0, ∗, ∗, ∗, ∗, ∗) respectively. Suppose that, for

5

One consider the eight S-boxes form a ring. For example, S-boxes 8, 1, 2 and 3 are adjacent.

<!-- PDF_PAGE: 5 -->

## PDF page 5

Secret External Encodings Do Not Prevent 185

Fig. 2. The 12 XOR instructions per round targeted by the attack

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

Fig. 3. A zero byte through the expansive permutation

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

<!-- PDF_PAGE: 6 -->

## PDF page 6

186 C. Clavier

the same M , a fault on xor key[5] at round h appears also to be ineﬀective. One could ﬁrst conclude that the xor key[5] output x 5 is equal to 0. But actually this rather means that x 5 belongs to the set A 5 = {(0, 0, 0, 0, 0, 0), (0, 0, 0, 1, 0, 1), (1, 0, 0, 0, 1, 0), (1, 0, 1, 1, 0, 1)} of the four pre-images of S 5 (0) by S 5 . This is due to the non-injective property, for each S-box, that any 4-bit output has exactly four pre-images. We can now derive that k 5 = x 5 ⊕ s 5 ∈ A 5 ⊕ (∗, 0, 0, 0, 0, 0), which leads to 8 possible values for k 5 corresponding to 3 bits of information retrieved about the key K. With the same reasoning, an output identity when faulting xor key[6] would imply that k 6 ∈ A 6 ⊕ (0, 0, 0, 0, 0, ∗), revealing 3 other bits of information about the key. Note that for the other two S-boxes (S 4 and S 7 ), it is not possible to determine the value of neither the right-most bit of k 4 nor the left-most bit of k 7 6 .

Deﬁnition 1 (Winning event). We call winning event at locus (h, i, j) a pair of observations, for the same plaintext, of two ineﬀective faults: one on xor left[i] at round (h − 1), and another one on xor key[j] at round h, where j ∈ {2i − 1, 2i}.

Winning events such as the one at locus (h, 3, 5) described in the previous ex- ample are the core events exploited in this attack. Obtaining a winning event at some locus obviously depends on the plaintext. Indeed, the values of L h−1 [i] and R h−1 [i] which govern the (in-)eﬀectiveness of a fault on xor left[i], as well as the value of the ‘∗’ bit of s j which inﬂuences the (in-)eﬀectiveness of a fault on xor key[j], all depend on the plaintext. So if a winning event at some locus is not obtained for a given plaintext, it may well be obtained for another one. Nevertheless, for a winning event at some locus to be obtained, the key bits corresponding to the ﬁve ‘0’ bits of s j must be equal to their corresponding values in one representative of A j . Consequently, given a key K, there are some locus at which no winning event may occur whatever the plaintext, and others at which winning events occur for some plaintexts.

Deﬁnition 2 (Winnable locus). Given some key K, we say that (h, i, j) is a winnable locus if the ﬁve bits of k j at ‘0’ positions (those where an ineﬀective fault on xor left[i] at round (h − 1) implies a bit value of s j equal to 0), are equal to their counterpart values in one of the four representatives of A j .

Example: For K = CD3ABC5876AC062B, locus (7, 3, 5) is winnable because the subkey k 5 entering S-box 5 at round 7 is equal to (1, 0, 0, 1, 0, 1) whose ﬁve rightmost bits are equal to those of A 5 ’s element (0, 0, 0, 1, 0, 1). The probability (over all keys) for any given locus to be winnable is 4 · 2 −5 = 0.125. Furthermore, there are 8 ∗ (16 − 1) = 120 interesting loci along the DES (the ﬁrst round is not exploitable), so that, in the simpliﬁed model where all K h

6

This is due to the fact that, by design of any S-box S j , each lateral bit is always represented with both 0 and 1 values amongst A j .

<!-- PDF_PAGE: 7 -->

## PDF page 7

Secret External Encodings Do Not Prevent 187

are viewed as almost independent, 15 winnable loci per key are expected on aver- age. A counting simulation on 27 000 randomly generated keys gives a number of winnable loci distributed as shown in Figure 4, with an average of 14.986. For each winnable locus, and whenever a winning event is obtained, the key space may be reduced according to the previously explained constraint. The optimal residual entropy, obtained after having exploited all winnable loci, is distributed as shown in Figure 5. The percentiles of this distribution for the frequency levels (0.10, 0.50, 0.90) are (14.17, 21.32, 29.98), meaning that for one key out of two, the full exploitation of winnable loci reduces the key space from 2 56 to less than 2 21.32 keys.

2500

2000

Frequency

1500

1000

500

0

10 20 30 40 Number of winnable loci

Fig. 4. Number of winnable loci per key

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 7]

500

Frequency

400

300

200

100

0

10 20 30 40 50 Optimal residual entropy bits

Fig. 5. Optimal residual entropy per key after exploitation of all winnable loci

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 7]

In Appendix A we summarize the procedure of the attack as described in this section. The stopping condition is left to the attacker: it may involve the number of faults injected so far, the current residual entropy of the key space, or other considerations. A simulation of this attack according to this procedure allowed us to quantify the number of fault injections required. Out of 27 000 experiments, the number of faults needed for winning all possible winnable loci is distributed as shown in Figure 6. With 100 000 faults, all winnable loci are won in 54.5 % of cases, and all but at most 1 are won in 87.3 % of cases. As the number of already won loci increases, the probability to win another one strongly decreases. This suggests that there is no point in continuing faulting for a long time. The median residual entropy after 50 000 and 100 000 faults is respectively 26.49 and 22.32 bits.

### 3.3 An Improved Version of the Attack

The attack described in Section 3.2 essentially eliminates keys which are not compatible with any observed winning event. In this section we present a mod- iﬁed version which improves on it in two directions. First, we extend the kind of events which are exploited. For example, when a winning event at locus (h, 3, 5) is observed, and for the same M the attacker knows that r 2 = 0 (this is the case if a fault on xor left[2] at round (h − 1) is

<!-- PDF_PAGE: 8 -->

## PDF page 8

188 C. Clavier

800

600

Frequency

400

200

0

100 200 300 Number of faults x 1000

400

100

% of simulations

80

60

40

20

0

50 100 150 200 Number of faults x 1000

250

Fig. 6. Number of faults needed for winning all winnable loci

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 8]

ineﬀective), then all 6 bits of k 5 are constrained instead of 5. This results in an extra information about the key which was not exploited by the basic attack. As another example, suppose that an ineﬀective fault is observed on xor left[3] at round (h− 1), but not on xor key[5] at round h. Even if this is not a winning event at locus (h, 3, 5), we may infer information about k 5 , namely that k 5 does not belong to A 5 ⊕ (∗, 0, 0, 0, 0, 0). Here also, this informative event was not considered in the basic attack. The second improvement consists in assigning an a posteriori probability to each key, conditioned by the observations. The result of these two improvements is that, not only the space of compatible keys is further reduced, but also its exhaustive search is shortened by trying keys in their decreasing order of probability.

Deﬁnition 3 (Ineﬀectiveness Vector). We call ineﬀectiveness vector at round h, denoted e = (e lef t , e key ), the boolean vector e lef t of the observed inef- fectiveness of faults injected on xor left[1] to xor left[4] at round (h − 1), together with the boolean vector e key of the observed ineﬀectiveness of faults injected on xor key[1] to xor key[8] at round h.

For example, the winning event at locus (h, 3, 5) described in Section 3.2 may have been produced by the ineﬀectiveness vector (e lef t , e key ), where e lef t = (0, 0, 1, 0), and e key = (0, 0, 0, 0, 1, 0, 0, 0).

For each σ ∈ {A, B}, let e σkey denote that part of e key related to the four B σ σ S-boxes involving K σ (so that e key = (e A key , e key )), and e denote (e lef t , e key ).

Any observed ineﬀectiveness vector may be used to assign an a posteriori probability to each half-key K σ by means of Bayes’ formula:

p(K σ |e σ ) = p(e σ |K σ ) ·

p(K σ ) p(e σ )

(1)

From Eq. (1), we derive a recursive form which allows to update the a poste- riori probability of a key, based on a newly observed ineﬀectiveness vector:

p(e σ |K σ ) n σ σ σ · p K p K σ |(e σ 1 , . . . , e σn ) = |(e , . . . , e ) . 1 n−1 p(e σn )

(2)

<!-- PDF_PAGE: 9 -->

## PDF page 9

Secret External Encodings Do Not Prevent 189

Table 1. Percentiles of the residual entropy (in bits) as a function of the number of injected faults

Percentile level 5 % 10 % 25 % 50 % 75 % 90 % 23.59 26.33 30.98 36.10 40.46 43.92 14.35 16.92 21.51 26.62 31.63 35.86 9.17 11.27 15.38 20.23 25.2 29.60 5.13 6.80 9.85 13.95 18.65 22.96 2.81 3.93 6.23 9.57 13.57 17.44 1.40 2.26 4.03 6.68 10.07 13.59

Number of faults 15 000 25 000 35 000 50 000 70 000 100 000

95 % 46.37 38.31 32.31 25.64 19.95 15.87

Note that evaluating the denominator p(e σn ) is not necessary as it is inde- pendent from the key. With the aim of comparing key probabilities together, omitting it will only aﬀect all probabilities by the same multiplicative factor. Thus, while considering a new observation e σ , the process of updating key prob- abilities just comes down to multiplying the (not normalized) probability of each key K σ by p(e σ |K σ ). Assuming a random behavior for R h , evaluating p(e σ |K σ ) is done by counting the number of round inputs compatible with the observation. Indeed, we have:

#{R h : e lef t and e σkey are satisﬁed when K σ is used} 2 32

p(e σ |K σ ) =

(3)

We performed extensive simulations of this attack with diﬀerent numbers of faults ranging from 15 000 to 100 000. In each case, 10 000 simulations were done. The residual entropy with respect to diﬀerent percentile levels and for each considered number of faults is given in Table 1. The median residual entropy for 50 000 and 100 000 faults are 13.95 and 6.68 bits. Compared to corresponding

50

Residual entropy bits

40

30

20

10

20

90%

50%

10%

100

40 60 80 Number of faults x 1000

Fig. 7. Percentiles of the residual entropy as a function of the number of faults

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 9]

<!-- PDF_PAGE: 10 -->

## PDF page 10

190 C. Clavier

ﬁgures of Section 3.2, this demonstrates a considerable gain for this method over the basic attack. Figure 7 provides a graphical view of the decreasing entropy of the resulting key space. Note that this counting operation may be optimized as e σkey depends on only 18 bits of R h . The procedure given in Appendix B describes a way to implement this im- proved attack. We decided to exploit an ineﬀectiveness vector e σ = (e lef t , e σkey ) only when at least one of its two most inﬂuential xor left instructions shows to be ineﬀective under fault. Four xor key fault injections are thus saved in cases where a negligible amount of information would have been gathered. We performed extensive simulations of this attack with diﬀerent numbers of faults ranging from 15 000 to 100 000. In each case, 10 000 simulations were done. The residual entropy with respect to diﬀerent percentile levels and for each considered number of faults is given in Table 1. The median residual entropy for 50 000 and 100 000 faults are 13.95 and 6.68 bits. Compared to corresponding ﬁgures of Section 3.2, this demonstrates a considerable gain for this method over the basic attack. Figure 7 provides a graphical view of the decreasing entropy of the resulting key space.

4 Countermeasures

Having explained our attack in Sections 3.2 and 3.3, we now analyze the conditions for this attack to be feasible, and the countermeasures which may prevent it. As we already mentioned, the embedded DES we attack must be implemented in software. We think that the proposed attack is not applicable when using a DES co-processor. We also relied on an 8-bit architecture. This condition is not strictly required but it greatly impacts the complexity of the attack. For example, if we have a 16-bit architecture, the expected number of faults needed before obtaining an ineﬀective one when targeting a xor left instruction would be 2 16 instead of 2 8 . The complexity ﬁgures we mentioned for the 8-bit case would thus become prohibitive for a practical realization on architectures with wider data paths. Because the attacker needs to know which instruction is corrupted when a fault is injected, we think that the classical random delays countermeasure (ei- ther software or hardware) should prevent the attack, or at least make its real- ization very diﬃcult. Indeed, an important condition is to be able to interpret an identity of outputs as being the consequence of a natural zero output of the targeted XOR. If random delays exist, this rare particular event may well be lost in many false positive neutral faults. The problem of false-negatives also exists when random delays are implemented. For similar reasons, the random order countermeasure will also perturb the attacker. Nevertheless, and while we have not further investigated this idea, we foresee a way to adapt the attack to this case. When this countermeasure is implemented alone, and by repeatedly injecting faults on the same xor left (resp. xor key) instruction for the same input, the attacker is able to infer the number of xor left[i] (resp. xor key[j]) for which a fault is ineﬀective. The observation obtained by the attacker is not the complete ineﬀectiveness vector

<!-- PDF_PAGE: 11 -->

## PDF page 11

Secret External Encodings Do Not Prevent 191

(e lef t , e key ) anymore, but rather the Hamming weights of e lef t and e key . Prob- ably at the cost of a larger number of needed faults, we think that it should still be possible to assign probabilities to keys based upon this partial information about the ineﬀectiveness vector. A classical counter-measure against side-channel attacks such as SPA, DPA, CPA, . . . is the data masking (also called blinding) [6] which results, when correctly implemented, in a perfect ﬁrst-order unpredictability of intermediate values. A direct consequence of this property is that the attack we described is not possible anymore: any ineﬀective fault, consequence of a physical zero value of the XOR output on the faulted execution, is compatible with any logi- cal masked value and gives no useful information to the attacker. Note that this ﬁrst-order anti side-channel countermeasure is not eﬀective against a variant of our attack if it is possible to inject multiple faults at chosen timings on the same execution. Finally, we consider the classical countermeasure against DFA and CFA which consists in computing the cryptographic function twice and comparing both re- sults: if both results are the same, the value is output by the command; if they diﬀer, a fault is detected and no ciphertext is returned. As already noticed in [13] for general safe-error attacks, we emphasize that this countermeasure does not im- pede our attack. A valid output indicates that the fault was ineﬀective, while no output means that it was not. The attack is even slightly simpliﬁed as the attacker does not need to ask for computations without fault. The counter-measure would remain eﬃcient if a limit is imposed on the number of allowed detected faults.

5 Conclusion

We have presented a fault-based key recovery attack on a software implemented DES. This attack relies on the following fault model: when a fault is injected during a XOR instruction, the output of this XOR is forced to zero whatever the input operand values were. A large amount of information about the secret key K is retrieved without knowing the DES input, nor its output. Only the ability to detect that two DES outputs are equal is required. An important consequence is that our attack applies to the whole class of externally encoded DES or Triple- DES 7 , deﬁned as secret block ciphers built by embedding a DES or a Triple-DES between two arbitrary secret permutations. This is particularly meaningful as it potentially endangers proprietary cryptographic algorithms based on this obfus- cating design and invalidates the supposed immunity of these secret functions against fault analysis. As far as we know, our attack is the ﬁrst published exam- ple of transient fault analysis against a class of secret cryptographic functions. Finally, we suggest some possible directions to extend our result. Further investigations could aim at designing a variant of this attack that would rely on other realistic fault models, or that would apply to other externally encoded block ciphers. For example, a similar result applicable to an externally encoded

7

The Triple-DES case is treated by applying the attack on K 1 and K 2 separately.

<!-- PDF_PAGE: 12 -->

## PDF page 12

192 C. Clavier

AES would threaten the most common usage of the MILENAGE [15] scheme for authentiﬁcation and key generation functions.

Acknowledgements

The author would like to thank Eric Brier and Benoı̂t Chevallier-Mames for fruitful discussions related to the ideas presented in this paper. The work described in this document has been ﬁnancially supported by the European Commission through the IST Program under Contract IST-2002- 507932 ECRYPT.

### References

1. Amiel, F., Clavier, C., Tunstall, M.: Fault Analysis of DPA-Resistant Algorithms. In: Breveglieri, L., Koren, I., Naccache, D., Seifert, J.-P. (eds.) FDTC 2006. LNCS, vol. 4236, pp. 223–236. Springer, Heidelberg (2006) 2. Brier, E., Clavier, C., Olivier, F.: Correlation Power Analysis with a Leakage Model. In: Joye, M., Quisquater, J.-J. (eds.) CHES 2004. LNCS, vol. 3156, pp. 16–29. Springer, Heidelberg (2004) 3. Biham, E., Shamir, A.: The Next Stage of Diﬀerential Fault Analysis: How to break completely unknown cryptosystems (October 30, 1996) (draft) Available at www.fit.vutbr.cz/ ∼ cvrcek/cards/nextstage.ps 4. Biham, E., Shamir, A.: Diﬀerential Fault Analysis of Secret Key Cryptosystems. In: Kaliski Jr., B.S. (ed.) CRYPTO 1997. LNCS, vol. 1294, pp. 513–525. Springer, Heidelberg (1997) 5. Boneh, D., DeMillo, R.A., Lipton, R.J.: On the Importance of Checking Cryp- tographic Protocols for Faults. In: Fumy, W. (ed.) EUROCRYPT 1997. LNCS, vol. 1233, pp. 37–51. Springer, Heidelberg (1997) 6. Goubin, L., Patarin, J.: DES and Diﬀerential Power Analysis (The ‘Duplication’ Method). In: Koç, Ç.K., Paar, C. (eds.) CHES 1999. LNCS, vol. 1717, pp. 158–172. Springer, Heidelberg (1999) 7. Hemme, L.: A Diﬀerential Fault Attack Against Early Rounds of (Triple-)DES. In: Joye, M., Quisquater, J.-J. (eds.) CHES 2004. LNCS, vol. 3156, pp. 254–267. Springer, Heidelberg (2004) 8. Joye, M., Quisquater, J.-J., Yen, S.-M., Yung, M.: Observability Analysis: Detect- ing When Improved Cryptosystems Fail. In: Preneel, B. (ed.) CT-RSA 2002. LNCS, vol. 2271, pp. 263–276. Springer, Heidelberg (2002) 9. Kilian, J., Rogaway, P.: How to protect DES against exhaustive key search. In: Koblitz, N. (ed.) CRYPTO 1996. LNCS, vol. 1109, pp. 252–267. Springer, Heidel- berg (1996) 10. Kocher, P., Jaﬀe, J., Jun, B.: Diﬀerential Power Analysis. In: Wiener, M.J. (ed.) CRYPTO 1999. LNCS, vol. 1666, pp. 388–397. Springer, Heidelberg (1999) 11. National Bureau of Standards. Data Encryption Standard. Federal Information Processing Standard, vol. 46 (1977) 12. Paillier, P.: Evaluating Diﬀerential Fault Analysis of Unknown Cryptosystems. In: Imai, H., Zheng, Y. (eds.) PKC 1999. LNCS, vol. 1560, pp. 235–244. Springer, Heidelberg (1999) 13. Yen, S.-M., Joye, M.: Checking Before Output May Not Be Enough Against Fault- Based Cryptanalysis. IEEE Trans. Computers 49(9), 967–970 (2000)

<!-- PDF_PAGE: 13 -->

## PDF page 13

Secret External Encodings Do Not Prevent 193

14. Yen, S.-M., Kim, S.-J., Lim, S.-G., Moon, S.-J.: A Countermeasure Against One Physical Cryptanalysis May Beneﬁt Another Attack. In: Kim, K.-c. (ed.) ICISC 2001. LNCS, vol. 2288, pp. 414–427. Springer, Heidelberg (2002) 15. 3GPP TS 35.206. Speciﬁcation of the MILENAGE algorithm set: An example algorithm Set for the 3GPP Authentication and Key Generation functions f1, f1*, f2, f3, f4, f5 and f5*; Document 2: Algorithm speciﬁcation. Available at http://www.3gpp.org/ftp/Specs/html-info/35206.htm

A Basic Algorithm

Algorithm 1. The Basic Attack

1: while stopping condition is not satisﬁed do

Pick a plaintext M at random C ← E(M, K) for h from 2 to 16 do

2: 3:

4:

for i from 1 to 4 do C ∗ ← E(M, K) with fault on xor left[i] at round h − 1

5: 6:

if C ∗ = C then for j from 2i − 1 to 2i do C ∗ ← E(M, K) with fault on xor key[j] at round h

7: 8: 9:

10: 11:

if C ∗ = C then Reduce the relevant half-key space (K A or K B ) according to the winning event (h, i, j) 12: end if 13: end for 14: end if 15: end for 16: end for 17: end while

<!-- PDF_PAGE: 14 -->

## PDF page 14

194 C. Clavier

B Improved Algorithm

Algorithm 2. The Improved Attack

1: For each 2 28 possible K A , set proba(K A ) ← 1 2: For each 2 28 possible K B , set proba(K B ) ← 1

3: while stopping condition is not satisﬁed do 4: Pick a plaintext M at random 5: C ← E(M, K) 6: for h from 2 to 16 do 7: for i from 1 to 4 do 8: C ∗ ← E(M, K) with fault on xor left[i] at round h − 1

?

e lef t [i] ← (C ∗ = C) end for

9: 10:

11: 12: 13:

if (e lef t [1] = True) or (e lef t [2] = True) then for j from 1 to 4 do C ∗ ← E(M, K) with fault on xor key[j] at round h

?

∗ e A key [j] ← (C = C) end for for all K A such that proba(K A ) &gt; 0 do A proba(K A ) ← proba(K A ) · p((e lef t , e A key )|K ) end for end if

14: 15: 16: 17: 18: 19:

20: 21: 22:

if (e lef t [3] = True) or (e lef t [4] = True) then for j from 1 to 4 do C ∗ ← E(M, K) with fault on xor key[j + 4] at round h

?

∗ 23: e B key [j] ← (C = C) 24: end for 25: for all K B such that proba(K B ) &gt; 0 do B 26: proba(K B ) ← proba(K B ) · p((e lef t , e B key )|K ) 27: end for 28: end if 29: end for 30: end while
