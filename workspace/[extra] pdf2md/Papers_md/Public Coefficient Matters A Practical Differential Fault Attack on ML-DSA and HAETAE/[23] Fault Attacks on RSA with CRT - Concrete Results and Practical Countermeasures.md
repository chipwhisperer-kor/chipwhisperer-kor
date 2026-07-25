# [23] Fault Attacks on RSA with CRT - Concrete Results and Practical Countermeasures

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 16
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-23"
derived_asset_id: "PCM-DFA-REF-23-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[23] Fault Attacks on RSA with CRT - Concrete Results and Practical Countermeasures.pdf"
source_sha256: "ff7cc6c8cb925666fd85069d323a54f563d7dc33f219ad407f0a599494b57670"
pages: 16
bbox_words: 5846
consumed_bbox_words: 5846
numeric_tokens: 306
consumed_numeric_tokens: 306
source_blocks: 223
consumed_source_blocks: 223
emitted_blocks: 196
embedded_raster_images: 1
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 16
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

Fault Attacks on RSA with CRT: Concrete Results and Practical Countermeasures

### C. Aumüller, P. Bier, W. Fischer, P. Hofreiter, and J.-P. Seifert

Inﬁneon Technologies Security &amp; ChipCard ICs D-81609 Munich Germany {christian.aumueller, peter.bier, wieland.fischer, peter.hofreiter, jean-pierre.seifert}@infineon.com

Abstract. This article describes concrete results and practically vali- dated countermeasures concerning diﬀerential fault attacks on RSA using the CRT. We investigate smartcards with an RSA coprocessor where any hardware countermeasures to defeat fault attacks have been switched oﬀ. This scenario was chosen in order to analyze the reliability of software countermeasures. We start by describing our laboratory setting for the attacks. Hereafter, we describe the experiments and results of a straightforward implemen- tation of a well-known countermeasure. This implementation turned out to be not suﬃcient. With the data obtained by these experiments we developed a practical error model. This enabled us to specify enhanced software countermeasures for which we were not able to produce any successful attacks on the investigated chips. Nevertheless, we are convinced that only sophisticated hardware countermeasures (sensors, ﬁlters, etc.) in combination with software countermeasures will be able to provide security.

Keywords: Bellcore attack, Chinese Remainder Theorem, Fault attacks, Hardware security, RSA, Spike attacks, Software countermeasures, Tran- sient fault model.

1 Introduction

This paper shows and proves that fault attacks on RSA with the CRT (also known as Bellcore attacks) due to [BDL] are feasible. They are indeed devas- tating if there are neither hardware mechanisms (sensors, ﬁlters, etc.) nor any appropriate software countermeasures implemented in the underlying smartcard ICs. However, this does not imply that modern high-security smartcard ICs are vulnerable to this kind of attacks. Instead, it shows that fault tolerance and especially sophisticated hardware countermeasures are essential for the design of secure hardware. Moreover, we stress that it is very diﬃcult in the ﬁeld to switch oﬀ these sophisticated hardware countermeasures. This has been done

B.S. Kaliski Jr. et al. (Eds.): CHES 2002, LNCS 2523, pp. 260–275, 2003. c Springer-Verlag Berlin Heidelberg 2003

<!-- PDF_PAGE: 2 -->

## PDF page 2

Fault Attacks on RSA with CRT 261

exceptionally for our study concerning software countermeasures against the Bellcore attack. In order to provide better security for data protection under strong encryp- tion more and more implementations on tamper-proof devices (e.g., smartcard ICs) are proposed. The main reason is that smartcard ICs provide high reliability and security with more memory capacity and better performance characteristics than conventional magnetic stripe cards. With special characteristics of compu- tational ability a large variety of cryptographic applications beneﬁt from smart- card ICs. This attracted a huge amount of research on physical attacks against smartcards in 1996 due to [Koch], [BDL] and again 1999 by [KJJ], followed by [GMO,SQ]. However, most research so far focused on Timing or Power Analysis attacks. This is surprising as the frauds with smartcards by inducing faults are reality, cf., [A,AK1,AK2], whereas no frauds via Timing or Power Analysis at- tacks have been reported so far. Moreover, research on fault-based cryptanalysis is not very active compared to the other side-channel attacks. Furthermore, no practical investigation of the Bellcore attack is presently known. Indeed, this topic will be publicly addressed within this paper for the ﬁrst time. It answers a question of Kaliski and Robshaw [KR] of how practical these attacks might be, answered deﬁnitely here by physicists, designers and manufactures of secure hardware. The present paper is organized as follows: Section 2 brieﬂy repeats RSA us- ing the CRT and its fault-based cryptanalysis according to [BDL,JLQ]; it also includes and discusses the advantages and limitations of so far publicly known software countermeasures to defeat fault attacks on RSA in CRT mode. Section 3 ﬁrstly explains so-called spike attacks and their realization on smartcard ICs, their complexity from an attacker’s point of view and reveals an appropriate test equipment to implement fault attacks. Secondly, we will present the result- ing errors on unprotected hardware and software for RSA in CRT mode. This demonstrates the insuﬃciency of a straightforward implementation of a well- known countermeasure due to [Sh]. Within section 4 we basically investigate enhanced software countermeasures derived from our practical observations and our proposed model to counteract fault attacks on RSA. Eventually, section 5 adds some practical conclusions concerning software countermeasures to prevent Bellcore attacks.

2 Preliminaries

### 2.1 The RSA System

Let N = p · q be the product of two large primes of similar length. To sign a message m ∈ Z N using RSA one computes S := m d mod N , where d is the private exponent satisfying e · d ≡ 1 mod (p − 1)(q − 1) for the public exponent e. The computationally expensive part of signing is the modular exponentia- tion. For better eﬃciency most implementations exponentiate as follows: using repeated square and multiply they ﬁrst compute S p := m d mod p and hereafter S q := m d mod q. Then they construct the signature S = m d mod N using the

<!-- PDF_PAGE: 3 -->

## PDF page 3

262 C. Aumüller et al.

CRT. This last step takes negligible time compared to the two exponentiations. It is done eﬃciently by computing S = S q + (S p − S q ) ∗ (q −1 mod p) mod p ∗ q, (1)

using Garner’s algorithm, cf. [Kn]. The exponentiation using the CRT is much faster than the full exponenti- ation. To see this, observe that S p = m d mod p = m dmod(p−1) mod p. Usually, d is of order N , while d mod (p − 1) is of order p. Consequently, computing S p requires half as many multiplications as computing S directly. In addition, in- termediate values during the computation of S p are only half as big — they are in the range [1, . . . , p], rather than [1, . . . , N ]. Clearly, the same arguments are valid for the computation of S q . When quadratic time complexity is used, multi- plying two numbers in Z p takes a quarter of the time as multiplying elements in Z N . Hence, computing S p takes an eighth of the time of computing S directly. Thus, computing S p and S q this way takes a quarter of the time of computing S directly. Thus, CRT exponentiation is four times faster than direct exponen- tiation. This is the reason for using the CRT for RSA signature generation, cf. [CQ,MvOV].

The Fault-Based Cryptanalysis of RSA Using CRT

2.2

We brieﬂy recall the fault-based cryptanalysis of RSA with the CRT due to [BDL,JLQ]. Assume that during the computation of an RSA signature for a message m a random error occurs during the computation of S p . This yields a faulty signature part S p , whereas the computation of S q is done correctly. The combination of S p and S q via (1) will yield an incorrect signature S . For S it holds that S − S = 0 but S − S ≡ 0 mod q. Therefore, one obtains the factorization of N by computing

gcd ((m − (S ) e ) mod N, N ) = q.

Simple Software Countermeasure to Defeat the Fault Attack

2.3

Some simple ad-hoc countermeasures have been already suggested within [BDL, KR]. One approach is to perform calculations twice and the other approach suggests to verify the correctness of the signature by comparing the inverse result with the input. The ﬁrst approach is very time-consuming and it cannot always provide a satisfactory solution because a permanent error may be undetectable by computing the function more than once. The second approach is to verify the correctness by comparing the inverse result with the input m. Generally, this is not a satisfactory solution since the parameter e could be a large integer and this checking procedure becomes time-consuming. Additionally, for a real life software implementation the programmer cannot rely on the fact that e is known and a small number. On the other hand, this countermeasure seems to be the safest.

<!-- PDF_PAGE: 4 -->

## PDF page 4

Fault Attacks on RSA with CRT 263

An interesting countermeasure is the introduction of randomness into the RSA signature process. Here, RSA is applied to F (m, r) where F is some for- matting function and r is a random string which ensures that the user never signs the same message twice and the attacker does not know the signed message, cf. [BDL,BR,KR]. Other countermeasures are mentioned in [Ro].

### 2.4 Shamir’s Software Countermeasure

Shamir’s idea, cf. [Sh], is to select a random integer t and to do the following computations S pt := m d mod p ∗ t, S qt := m d mod q ∗ t.

In the case of S pt = S qt mod t the computation is deﬁned to be error free and S is computed according to the CRT recombination equation (1). One drawback in Shamir’s method, as pointed out in [JPY], is the following: Within the CRT mode of real RSA applications the value d is not known, only the values d p = d mod (p − 1) and d q = d mod (q − 1) are known. Although d can be eﬃciently computed from d p and d q only, as described in [FS], it will limit the acceptance of Shamir’s method. Moreover, his check will be shown to be insuﬃcient anyway. But, our enhanced software countermeasures will resolve the above critical points of his method.

General Remarks on Methods to Overcome Fault Attacks

2.5

Only very recently the ﬁeld of research on fault attacks countermeasures has been emerged. For instance a series of papers [YJ,YKLM1,YKLM2,JQYY] as- sume that the attacker has a very precise knowledge about the implementation details and especially an absolute accurate control of the timing of his fault induction. Under this strong assumption the private exponent d can be recon- structed by abusing the implemented correctness check as an oracle for the bits of d. However, all the described fault attacks can easily be prevented by various randomization techniques for the RSA algorithm. In a side-channel secure RSA signature implementation such techniques are present. Moreover, [YKLM1] proposed the following very interesting countermeasure: Their key idea is to inﬂuence the computation of S q or the overall computation of S when an error occurred during the computation of S p , or vice versa. The cryptanalysis given in section 2 shows that a successful fault attack is not possible anymore. Unfortunately it was recently shown by [BMS] that their proposal for a so-called infective RSA CRT computation is not secure.

Physical Fault Attacks Realization

3

First of all, we would like to stress again that modern high-end cryptographic de- vices, e.g., smartcards, are usually protected by means of various and numerous

<!-- PDF_PAGE: 5 -->

## PDF page 5

264 C. Aumüller et al.

sophisticated hardware mechanisms to detect any intrusion attempt into their system behavior, cf. [Ma,NR]. This is due to the fact that hardware manufac- turers of cryptographic devices such as smartcard ICs have been aware of the importance of protecting against intrusions by, e.g., external voltage variations, external clock variations, etc. for a long time. However, it should be clear that the design of such mechanisms is a very diﬃcult engineering task. Such mech- anisms should be able to tolerate slight natural deviations from the standard values of the electrical parameter to be safeguarded. This is necessary to ensure a proper functionality of the underlying device within the speciﬁed range, as for example described in [ISO]. On the other hand they also have to detect very fast and unnatural low deviations from the speciﬁed standard range. This condition is necessary to detect any attack attempt by modifying the electrical execution conditions to alter a computation’s result. For example, the standard speciﬁca- tion [ISO] allows for the smartcard IC’s contact V CC under normal operating conditions a voltage supply between 4, 5V and 5, 5V. Although there are lots of possibilities to introduce an error during the cryp- tographic operation of an unprotected smartcard hardware, we will only explain in detail the so-called spike attacks. The reason is that spike attacks are non invasive attacks. Thus, they require no physical opening and no chemical prepa- ration of the smartcard IC. For further information on various methods how to enforce erroneous computations of chips we refer to [A,AK1,AK2,Gu1,Gu2, Koca,Ma].

### 3.1 Spikes

A smartcard of voltage class type A should be able to tolerate on the contact V CC a supply voltage between 4, 5V and 5, 5V, where the standard voltage is speciﬁed at 5V. Within this range the smartcard will be able to work properly. However, a deviation of the external power supply of much more than the speciﬁed 10% tolerance could cause problems with the smartcard IC. Indeed, it could then lead to a wrong computation result, provided that the smartcard IC is still able to ﬁnish its computation completely. But most often this is not possible, as the spike causes too much trouble to the CPU of the smartcard IC. Although a spike with the explanation above seems very simple, a speciﬁc type of a power spike is determined by nine parameters. Using picture 1 we will explain them:

1. Initial value of the power supply V 2 . 2. Starting point t 1 of the spike. 3. Rise time t 2 − t 1 of the spike. 4. Shape of the rising transition. 5. Height V 3 − V 1 of the power spike. 6. Length of the power spike t 3 − t 2 . 7. Falling time t 4 − t 3 of the spike. 8. Shape of the falling transition. 9. Final value V 1 of the power supply.

<!-- PDF_PAGE: 6 -->

## PDF page 6

voltage

V3

V2

V1

t 1 t 2

Fault Attacks on RSA with CRT 265

t 3

t 4 time

Fig. 1. Spike-parameters deﬁning the shape of a speciﬁc spike.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 6]

This indicates the huge range of diﬀerent parameters which must be scanned for penetration attacks against cryptographic devices. On the other hand, it also reveals the strong demands on the corresponding sensor and ﬁlter mechanisms. From the former discussion of spike attacks, one can envision the diﬃculties an attacker is confronted with, when he wants to overcome all the activated hardware countermeasures within modern high-security smartcard ICs.

### 3.2 Laboratory Setting

In order to systematically investigate the eﬀects of spikes and especially our pro- posed countermeasures, we basically used the following spike enforcing hardware set-up, which is shown in ﬁgure 2.

trigger

PC

control/ communication

spike generator

1234

spike

chip card IC

Fig. 2. Diagram of our test equipment.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 6]

With such a test set-up it is indeed possible to enforce a spike with a very high accuracy. This is necessary, if the spike shall just only enforce a tiny ran-

<!-- PDF_PAGE: 7 -->

## PDF page 7

266 C. Aumüller et al.

dom computation fault rather than a complete destruction of the smartcard’s computation, which would make the smartcard’s computation result unusable for a successful attack. Through the coupling of the control and communica- tion of the smartcard with a PC, which is running a dedicated test-software, it is possible to observe and analyze the smartcard’s reaction with respect to the applied spike-form as discussed above, e.g., answering with a correct/wrong answer sequence. Furthermore, the PC is responsible for the stimuli, timing and controlling of the above spike parameters. Coupled with an interface card, the spike generator is triggered by the PC which provides the time and voltage in- formation for the speciﬁc spike to be applied to the card. The spike generator is directly connected to the power supply V CC of the smartcard and provides its IC with the necessary operating voltage including the voltage drop of the spike. By means of the synchronization of the PC, the spike generator and the chipcard itself a very high attack reproducibility of more than 90% can be achieved. Now, one has to ﬁnd parameters for such a spike which enables a tiny random computation fault, but leaves the main computation untouched.

Results on Unprotected Hardware and Software

3.3

We will now discuss our results of successfully applied spike-attacks on unpro- tected smartcards, i.e., ICs where any hardware countermeasures against fault attacks have been switched oﬀ. Moreover, we have also switched oﬀ any (hard- ware and software) countermeasures against other classical side-channel attacks, like Timing Analysis [Koch], Power Analysis [KJJ], Electromagnetic Analysis [SQ,GMO], etc. However, to introduce a spike at the right position of the RSA with the CRT, one should investigate the power proﬁle of the critical computation ﬁrst. Such a power proﬁle of our investigated smartcard equipped with an RSA coprocessor is shown in ﬁgure 3. Let us explain this power proﬁle a little bit more: The upper line represents the proﬁle of the smartcard’s I/O behavior. The ﬁrst I/O activity is the start impulse for the smartcard and the second peak is the answer sequence given by the smartcard. Between these two peaks the smartcard is computing a 2048-bit RSA signature using the CRT. This is shown in the lower line where the main power proﬁle of the smartcard is depicted. The RSA-CRT computation starts at the time block 1.5 and ends at the time block 9.2. In the ﬁgure the blocks are numbered from 0 to 9. This is shown by the fact that the power consumption increases — due to the coprocessors activity. One immediately recognizes the two diﬀerent exponentiations as they are the main power consumers. In our case the ﬁrst exponentiation lies in the time frame 1.6 to 5.1, and the second exponentiation lies in the time frame 5.3 to 8.8. Before the ﬁrst exponen- tiation one recognizes the loading of the data into the crypto coprocessor for the ﬁrst exponentiation, after the ﬁrst exponentiation the corresponding correctness checks and as well the loading of the data into the crypto coprocessor and for the second exponentiation and after the second exponentiation again the correctness checks of the second exponentiation. Finally, one sees the CRT combination of

<!-- PDF_PAGE: 8 -->

## PDF page 8

Fault Attacks on RSA with CRT 267

the two partial exponentiations followed eventually by an additional correctness check for the CRT combination.

Fig. 3. Power proﬁle of RSA with the CRT.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 8]

Results on completely unprotected RSA using the CRT. The ﬁrst al- gorithm we attacked with our spike equipment was the pure RSA signature algorithm using the CRT:

input: m, p, q, d p , d q , q −1 mod p

S p := m d p mod p S q := m d q mod q S := S q + ((S p − S q ) ∗ q −1 mod p) ∗ q return(S)

output: m d mod N

Before discussing the results of our spike attacks on the above algorithm, we note that the inputs p, q, d p , d q , q −1 mod p are usually stored in EEPROM, while the message m is stored in RAM. However, in order to work with the data

<!-- PDF_PAGE: 9 -->

## PDF page 9

268 C. Aumüller et al.

p, q, d p , d q , q −1 mod p they must be moved from EEPROM into RAM or the crypto coprocessor. By varying the time when we applied the appropriate spike to the smartcard IC’s power supply V CC , we were able to induce the following diﬀerent errors:

Observed error Mainly due to modiﬁcation of p, q Moving data from E 2 to coprocessor modiﬁcation of d p , d q Handling data within CPU wrong exponentiation modp, q Error within CPU or coprocessor modiﬁcation of q −1 mod p Moving data from E 2 to coprocessor wrong combination of S p and S q All listed errors faulty signature modp and modq Moving data from coprocessor wrong answer of smartcard Fatal error within CPU

Note that the ﬁrst ﬁve errors may lead to a successful attack, whereas the last two do not. Thus, we can conclude that it is absolutely necessary to have sophisticated hardware and software countermeasures to avoid such kinds of attacks. Within the remaining sections we will analyze already existing software countermeasures and also develop new and more reliable countermeasures.

Results on unprotected hardware with simple software countermea- sures. Motivated by the devastating results obtained within the previous sec- tion, we hereafter tested the reliability of the naively implemented software coun- termeasures due to [Sh] as desribed in section 2. Thus, we applied spikes to the unprotected smartcard while computing the following RSA signature algorithm shown in ﬁgure 4. Again, we ﬁrstly summarize some of the observed errors.

Observed error scenarios A B C 1 modiﬁcation of p , q time dep. time dep. no 2 modiﬁcation of d time dep. time dep. yes 3 modiﬁcation of d p , d q yes yes yes 4 modiﬁcation of r time dep. time dep. yes 5 wrong exponentiation modp, q prob. 1 − 1/r yes yes 6 modiﬁcation of S p or S q time dep. yes no 7 modiﬁcation of q −1 mod p no yes no 8 error during comb. of S p and S q no yes no 9 faulty signature modp and modq no no yes

The above table is organized as follows. The second column denotes the kind of error which might occur. Column A indicates whether the countermeasure rec- ognizes the induced fault, column B indicates whether the corresponding faulty signature S reveals the secret key and column C says whether the countermea- sure is correctly working in the corresponding case. We will brieﬂy comment the observed errors row by row:

<!-- PDF_PAGE: 10 -->

## PDF page 10

input: m, p, q, d, q −1 mod p

Fault Attacks on RSA with CRT 269

randomly choose a short prime r of, e.g., 32 bits p := p ∗ r d p := d mod ((p − 1) ∗ (r − 1)) q := q ∗ r d q := d mod ((q − 1) ∗ (r − 1))

S p := (m mod p ) d p mod p S q := (m mod q ) d q mod q

S p := S p mod p S q := S q mod q S := S q + ((S p − S q ) ∗ q −1 mod p) ∗ q

if ((S p mod r) = (S q mod r)) then return(error) else return(S)

output: S = m d mod (p ∗ q)

Fig. 4. Shamir’s countermeasure.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 10]

1. During the computation of p the value of p may be changed to some value p̃, such that p = p̃r. Then S p is computed correctly modulo r, but not modulo p. If p is destroyed later, then the check reveals the attack. If a destroyed p̃ will be used for the computation of d p then the check will not recognize this relevant fault. 2. If d is changed before the ﬁrst two reductions this will not be detected but is not security relevant. If d is changed between the ﬁrst two reductions, this will be recognized by the check. 3. If d p or d q is destroyed the check will detect this modiﬁcation. 4. Depending on the time r is destroyed, various things can happen: either the errors will be recognized or they are not security relevant. 5. The destruction of one of the two exponentiations is the classical Bellcore attack. This will be recognized. 6. If S p will be changed before the combination to S then the check will fail. 7. If q −1 mod p will be changed then the faulty signature will reveal the key. The check will not recognize the attack. 8. Cf. last row. 9. If the correct signature is destroyed S reveals no information about the key.

<!-- PDF_PAGE: 11 -->

## PDF page 11

270 C. Aumüller et al.

4

Practical Fault Attacks Countermeasures for Unprotected Hardware

Within this section we will use the formerly discussed errors to propose a simple practical error model. Hereafter, we propose enhanced countermeasures.

d (p)

p

check

RSA d, p

m

RSA d, q

q

d (q)

d p

p

RSA dp, pt

cross

m

check

RSA dq, qt

q

d q

q p -1

p

s p

p * p -1 = 1 (q) ?

Combine

s

s q

s p

S' p mod p

Combine s

check

s q

S' q

mod q

s

Fig. 5. Information ﬂow during checking.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 11]

Model to Understand Resulting/Possible Faults

4.1

From the observed error scenario, we have learned by an extensive data analysis the following facts:

<!-- PDF_PAGE: 12 -->

## PDF page 12

Fault Attacks on RSA with CRT 271

– During the computation, every input value to the RSA signature algorithm can be altered to a value diﬀerent from the original value. – During the computation, every variable can be changed. – The instruction sent to the CPU or a peripheral can be changed. – The only values to trust, are the values which are stored in ROM or EEP- ROM.

Armed with this knowledge, we formulated the following checking philosophy:

Check (at least in a probabilistic sense) every computed intermediate result with respect to its correctness by relying on trusted values only.

In a rough sense, this is reﬂected by ﬁgure 5. In this context we adapt the transient fault model due to [BDL] which assumes that our power spikes intro- duce arbitrary errors. Additionally, we assume that the attacker can induce only one spike but at a speciﬁc time chosen by himself.

Software Countermeasures Derived According to the Model

4.2

Inspired by the previous section, we developed the following countermeasures (shown in ﬁgure 6) to counteract fault attacks. It takes into account that in a practical application only d p and d q are given. Also, it avoids the use of the public exponent e, which in real applications is most often not known to the signature software. We will brieﬂy comment on this algorithm. The check after the CRT com- bination ensures that S is correctly computed from the data S p and S q . There- fore, it remains to guarantee that the latter ones are correct. The central check d d (S pt qt ≡ S qt pt mod t) proves that the two big exponentiations itself where pro- cessed in a correct way — assuming that the inputs are not compromised. Note that an erroneous pass of this check can only be due to some very subtle mod- iﬁcations of these input values. Such errors will be intercepted by the ﬁrst two checking blocks. Finally, we would like to point out the following important advice for a careful implementation: for the two checking blocks the secret pa- rameters d p and d q have to be reloaded from a secure area (EEPROM).

Measurement Results for Enhanced Software Countermeasures

4.3

By extensive penetration tests via spikes on the algorithm shown in ﬁgure 6 we obtained the following table. It proves empirically the reliability of our software countermeasures.

<!-- PDF_PAGE: 13 -->

## PDF page 13

272 C. Aumüller et al.

input: m, p, q, d p , d q , q −1 mod p

let t be a short prime number, e.g., 32 bits

p := p ∗ t d p := d p + random 1 ∗ (p − 1) S p := m d p mod p if ¬(p mod p ≡ 0 ∧ d p mod (p − 1) ≡ d p ) then return(error)

q := q ∗ t d q := d q + random 2 ∗ (q − 1) S q := m d q mod q if ¬(q mod q ≡ 0 ∧ d q mod (q − 1) ≡ d q ) then return(error)

S p := S p mod p S q := S q mod q S := S q + ((S p − S q ) ∗ q −1 mod p) ∗ q if ¬((S − S p mod p ≡ 0) ∧ (S − S q mod q ≡ 0)) then return(error)

S pt := S p mod t d pt := d p mod (t − 1) S qt := S q mod t d qt := d q mod (t − 1) d d if (S pt qt ≡ S qt pt mod t) then return(S) else return(error)

output: m d mod (p ∗ q)

Fig. 6. Practically secured RSA with CRT.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 13]

Observed error scenarios A B C modiﬁcation of p, p , q, q yes yes yes modiﬁcation of d p , d q yes yes yes modiﬁcation of t yes yes yes wrong exp. modp, q prob. 1 − 1/t yes yes modiﬁcation of S p or S q yes yes yes modiﬁcation of q −1 mod p yes yes yes error during comb. of S p and S q yes yes yes faulty signature modp and modq prob. 1 − 1/t no yes

Clearly, the probability that an error is undetected is equal to 1/t. For t a 32-bit integer, this probability is small enough; t can thus be seen as a security parameter.

<!-- PDF_PAGE: 14 -->

## PDF page 14

5 Conclusion

Fault Attacks on RSA with CRT 273

We have shown that the classical Bellcore fault attack is in principal feasible when using completely unprotected microcontrollers. Moreover, it also shows that unskilled implementations of countermeasures are not always reliable. It again answers a question of Kaliski and Robshaw [KR], and shows that these attacks are indeed practical. Our investigation also reveals that one should test any conceivable countermeasures in reality against all possible attack scenarios before trusting them. This was especially done with our newly developed software countermeasures. Although our software countermeasure seems to be very promising, we are strongly convinced that cryptographic hardware should never be used without appropriate hardware countermeasures in combination with software counter- measures. As a result, we ﬁnish with an advice given by Kaliski and Robshaw [KR] from the RSA Laboratories stating that good engineering practices in the design of secure hardware are essential.

### References

[A] [AK1]

[AK2]

[BDL]

[BDHJ + ]

[BR]

R. Anderson, Security Engineering, John Wiley &amp; Sons, New York, 2001. R. Anderson, M. Kuhn, “Tamper Resistance – a cautionary note”, Proc. of 2nd USENIX Workshop on Electronic Commerce, pp. 1–11, 1996. R. Anderson, M. Kuhn, “Low cost attacks attacks on tamper resistant devices”, Proc. of 1997 Security Protocols Workshop, Springer LNCS vol. 1361, pp. 125–136, 1997. D. Boneh, R. A. DeMillo, R. Lipton, “On the Importance of Eliminating Errors in Cryptographic Computations” Journal of Cryptology 14(2):101– 120, 2001. F. Bao, R. H. Deng, Y. Han, A. Jeng, A. D. Narasimbalu, T. Ngair, “Break- ing public key cryptosystems on tamper resistant dives in the presence of transient faults”, Proc. of 1997 Security Protocols Workshop, Springer LNCS vol. 1361, pp. 115–124, 1997. M. Bellare, P. Rogaway, “The exact security of digital signatures — how to sign with RSA and Rabin”, Proc. of EUROCRYPTO ’96, Springer LNCS vol. 1070, pp. 399–416, 1996. E. Biham, A. Shamir, “Diﬀerential fault analysis of secret key cryptosys- tems”, Proc. of CRYPTO ’97, Springer LNCS vol. 1294, pp. 513–525, 1997. I. Biehl, B. Meyer, V. Müller, “Diﬀerential fault attacks on elliptic curve cryptosystems”, Proc. of CRYPTO ’00, Springer LNCS vol. 1880, pp. 131– 146, 2000. J. Blömer, A. May, J.-P. Seifert, personal communication, April 2002. C. Couvreur, J.-J. Quisquater, “Fast decipherment algorithm for RSA public-key cryptosystem”, Electronics Letters 18(21):905–907, 1982. W. Fischer, J.-P. Seifert, “Note on fast computation of secret RSA expo- nents”, Proc. of ACISP ’02, Springer LNCS vol. 2384, pp. 136–143, 2002. K. Gandolﬁ, C. Mourtel, F. Olivier, “Electromagnetic analysis: Concrete results”, Proc. of CHES ’01, Springer LNCS vol. 2162, pp. 255–265, 2001.

[BS]

[BMM]

[BMS] [CQ]

[FS]

[GMO]

<!-- PDF_PAGE: 15 -->

## PDF page 15

274 C. Aumüller et al.

[Gu1]

[Gu2]

[HP1]

[HP2]

[ISO]

[JLQ]

[JPY]

[JQBD]

[JQYY]

[KR]

P. Gutmann, “Secure deletion of data from magnetic and solid-state mem- ory”, Proc. of 6th USENIX Security Symposium, pp. 77–89, 1997. P. Gutmann, “Data Remanence in Semiconductor Devices”, Proc. of 7th USENIX Security Symposium, 1998. H. Handschuh, P. Pailler, “Smart Card Crypto-Coprocessors for Public- Key Cryptography”, CryptoBytes 4(1):6–11, 1998. H. Handschuh, P. Pailler, “Smart Card Crypto-Coprocessors for Public- Key Cryptography”, Proc. of CARDIS ’98, Springer LNCS vol. 1820, pp. 372–379, 1998. International Organization for Standardization, “ISO/IEC 7816-3: Elec- tronic signals and transmission protocols”, http://www.iso.ch, 2002. M. Joye, A. K. Lenstra, J.-J. Quisquater, “Chinese remaindering based cryptosystem in the presence of faults”, Journal of Cryptology 12(4):241– 245, 1999. M. Joye, P. Pailler, S.-M. Yen, “Secure Evaluation of Modular Functions”, Proc. of 2001 International Workshop on Cryptology and Network Secu- rity, pp. 227–229, 2001. M. Joye, J.-J. Quisquater, F. Bao, R. H. Deng, “RSA-type signatures in the presence of transient faults”, Cryptography and Coding, Springer LNCS vol. 1335, pp. 155–160, 1997. M. Joye, J.-J. Quisquater, S. M. Yen, M. Yung, “Observability analysis — detecting when improved cryptosystems fail”, Proc. of CT-RSA Confer- ence 2002, Springer LNCS vol. 2271, pp. 17–29, 2002. B. Kaliski, M. J. B. Robshaw, “Comments on some new attacks on cryp- tographic devices”, RSA Laboratories Bulletin 5, July 1997. D. E. Knuth, The Art of Computer Programming, Vol.2: Seminumerical Algorithms, 3rd ed., Addison-Wesley, Reading MA, 1999. O. Kocar, “Hardwaresicherheit von Mikrochips in Chipkarten”, Daten- schutz und Datensicherheit 20(7):421–424, 1996. P. Kocher, “Timing attacks on implementations of Diﬃe-Hellmann, RSA, DSS and other systems”, Proc. of CYRPTO ’97, Springer LNCS vol. 1109, pp. 104–113, 1997. P. Kocher, J. Jaﬀe, J. Jun, “Diﬀerential Power Analysis”, Proc. of CYRPTO ’99, Springer LNCS vol. 1666, pp. 388–397, 1999. D. P. Maher, “Fault induction attacks, tamper resistance, and hostile reverse engineering in perspective”, Proc. of Financial Cryptography, Springer LNCS vol. 1318, pp. 109–121, 1997. A. J. Menezes, P. van Oorschot, S. Vanstone, Handbook of Applied Cryp- tography, CRC Press, New York, 1997. D. Naccache, D. M’Raihi, “Cryptographic smart cards”, IEEE Micro, pp. 14–24, 1996. I. Petersen, “Chinks in digital armor — Exploiting faults to break smart- card cryptosystems”, Science News 151(5):78–79, 1997. T. Rosa, “Future Cryptography: Standards are not enough”, Proc. of Se- curity and Protection of Information 2001, pp. 237–245, 2001. R. Rivest, A. Shamir, L. Adleman, “A method for obtaining digital sig- natures and public-key cryptosystems”, Comm. of the ACM 21:120–126, 1978. D. Samyde, J.-J. Quisquater, “ElectroMagnetic Analysis (EMA): Measures and Countermeasures for Smart Cards”, Proc. of Int. Conf. on Research in Smart Cards, E-Smart 2001, Springer LNCS vol. 2140, pp. 200–210, 2001.

[Kn]

[Koca]

[Koch]

[KJJ]

[Ma]

[MvOV]

[NR]

[Pe]

[Ro]

[RSA]

[SQ]

<!-- PDF_PAGE: 16 -->

## PDF page 16

[Sh]

[YJ]

[YKLM1]

Fault Attacks on RSA with CRT 275

A. Shamir, “Method and Apparatus for protecting public key schemes from timing and fault attacks”, U.S. Patent Number 5,991,415, November 1999; also presented at the rump session of EUROCRYPT’97. S.-M. Yen, M. Joye, “Checking before output may not be enough against fault-based cryptanalysis”, IEEE Trans. on Computers 49:967–970, 2000. S.-M. Yen, S.-J. Kim, S.-G. Lim, S.-J. Moon, “RSA Speedup with Residue Number System immune from Hardware fault cryptanalysis”, Proc. of the ICISC 2001, Springer LNCS vol. 2288, pp. 397–413, 2001. S.-M. Yen, S.-J. Kim, S.-G. Lim, S.-J. Moon, “A countermeasure against one physical cryptanalysis may beneﬁt another attack”, Proc. of the ICISC 2001, Springer LNCS vol. 2288, pp. 414–427, 2001. Y. Zheng, T. Matsumoto, “Breaking real-world implementations of cryp- tosystems by manipulating their random number generation”, Proc. of the 1997 Symposium on Cryptography and Information Security, 1997.

[YKLM2]

[ZM]
