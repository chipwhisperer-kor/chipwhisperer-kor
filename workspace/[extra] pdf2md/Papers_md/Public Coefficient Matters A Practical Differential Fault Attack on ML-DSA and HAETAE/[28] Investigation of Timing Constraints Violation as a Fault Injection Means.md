# [28] Investigation of Timing Constraints Violation as a Fault Injection Means

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 6
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-28"
derived_asset_id: "PCM-DFA-REF-28-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[28] Investigation of Timing Constraints Violation as a Fault Injection Means.pdf"
source_sha256: "fe97bfdd3cb9cb4f86a78d0c01e9430a39de73af299617ffdd8cb97341f40b7b"
pages: 6
bbox_words: 4855
consumed_bbox_words: 4855
numeric_tokens: 315
consumed_numeric_tokens: 315
source_blocks: 241
consumed_source_blocks: 241
emitted_blocks: 203
embedded_raster_images: 5
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 6
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

Investigation of timing constraints violation as a fault injection means

Loı̈c Zussa ∗ ,Jean-Max Dutertre ∗ , Jessy Clédière ‡ , Bruno Robisson † and Assia Tria †

∗† Département Systèmes et Architectures Sécurisées ( SAS ) ∗ École Nationale Supérieure des Mines de Saint-Étienne ( ENSMSE ), † CEA - LETI , Gardanne, France

{zussa, dutertre}@emse.fr {bruno.robisson, assia.tria}@cea.fr ‡ CEA - LETI , Minatec Campus, Grenoble, France jessy.clediere@cea.fr

Abstract—Secure circuits are prone to a wide range of physical attacks. Among them, fault attacks are based on modifying the circuit environment in order to change its behaviour or to induce faults into its computations. As a result, the security level of the circuit under attack may be weaken. Many means are of common use to inject such faults: laser shot, electromagnetic pulse, overclocking, chip underpowering, temperature increase, etc. However, the mechanisms involved in the fault injection process have not been yet deeply investigate. Especially, those that have a global effect linked to timing constraints violation. In this paper we provide an experimental proof of the uniqueness of the fault injection process by means of the target’s clock, power supply, or temperature alteration. We also studied further the properties of these fault injection means. These insights are intended to give designers guidelines to strengthen fault countermeasures. It also enable to imagine broad-spectrum countermeasures against most of the fault injection means. Index Terms—Fault injection, timing constraint violation, over- clocking, underpowering, overheating.

### I. I NTRODUCTION

Many of our daily used electronic devices embed crypto- graphic features (e.g. smart cards, cell phones, pay TV, pass- ports, etc.). The use of cryptographic algorithms is intended to provide to the end users confidentiality, authentication and data integrity services. As a consequence, the integrated circuits ( IC s) implementing these security features are often targeted by malicious attackers. They seek to extract confidential in- formation like encoding keys from their targets. To that end, a wide range of physical attacks against secure circuits have been introduced over the past decades. Physical attacks (or hardware attacks) target the IC s which implement cryptographic algorithms. It exists three main kinds of physical attacks. The first one, called invasive attacks, refers to any technique based on the analysis or modification of the target’s design by using invasive methods (e.g. probing the data buses of an IC [1] or using focused ion beams ( FIB ) to cut or change its interconnections). The second kind, called side channel analysis ( SCA ), is a passive attack. It exploits the information leakage related to some physical values of the chip, such as its power consumption, its electromagnetic emissions or the duration of its computations. Indeed, the strong correlation that exists between these quantities and the processed data has made it possible to develop statistical tech- niques to retrieve the secrets concealed in secure devices using

SCA [2], [3]. The third kind of physical attack, called fault attacks ( FA ), consists in modifying the circuit environment in order to change its behaviour or to induce faults into its computations. Many means are of common use to inject such faults: laser shot, electromagnetic pulse, overclocking, chip underpowering, temperature increase, etc. There are three main subclasses of fault attacks: algorithm modification, safe error and differential fault analysis. Algo- rithm modification consists in replacing instructions executed by a microcontroller [4] to circumvent its security features, or in weakening the strength of an iterative encryption algorithm by changing the number of its rounds [5]. Safe-error attacks are based on distinguishing between the normal and abnormal behaviours of the chip in presence of disturbances intended to induce faults. In order to retrieve the sensitive data processed by the target, they are correlated with the chip’s behaviours [6]. Differential fault analysis ( DFA ) consists in retrieving the keys by comparing correct ciphertext and faulty ciphertexts (i.e. ciphertexts obtained from a faulted encryption). This technique was first introduced for public key encryption algorithms [7], and rapidly extended to secret key algorithms [8]. From that time, many DFA schemes have been proposed to attack various encryption algorithms. All of them are associated with strong timing, range and location requirements regarding the fault injection process. If the faults are not induced at the proper time in the algorithm, or affect the wrong bits, the entire DFA process fails. As a consequence, the ability to control precisely the fault injection process is a key element in carrying out any fault attack. A fine understanding of the various fault injection mechanisms is also mandatory to enable the design of fault resistant IC s. That’s the reason why this paper focuses on an in-depth investigation of the most common fault injection means: those which are related to the violation of the IC s’ timing constraints. These means are based either on modifying the clock signal (i.e. overclocking) or on increasing the data propagation time through the circuit’s logic (i.e. voltage supply deprivation or temperature increase). They have a global effect on the targeted circuit because they affect similarly the whole logic. They are also of great concern because they are usually implemented with none expensive equipments. These fault injection means are known and used since

<!-- PDF_PAGE: 2 -->

## PDF page 2

the beginning of FA [9]. However, there is few papers in the scientific bibliography ([10], [11], [12]), which report a deep investigation and understanding of the underlying fault injection mechanisms. Our contributions to that research field are: • the experimental proof of the uniqueness of the fault in- jection mechanism related to the aforementioned means, • a study of the reproducibility of the obtained results, • a fine analysis of fault injection due to timing constraints violation (with a focus on the fault range and the ability to control faults’ location). To conduct this study we have chosen a programmable circuit ( FPGA ) as a test vehicle. It implements the advanced encryp- tion standard ( AES [13]), which is a secret key encryption algorithm. This article is organized as follows. A remainder on timing constraints and an explanation of how fault may be injected by their violation are given in section II. The experimental setup and results are described in section III. These results are analysed in section IV. Finally, our findings are summarized in the concluding section V with some perspectives.

### II. T IMING CONSTRAINTS

In this section, the basics of timing constraints are firstly reminded. Secondly, the two means of inducing timing con- straints violation for the purpose of fault injection are re- viewed. Then, the experimental proof intended to demonstrate the uniqueness of the fault injection mechanism is introduced.

A. Timing constraints

Almost all digital IC s work according the principle of synchrony: they use a common clock signal to synchronize their internal operations. Figure 1 outlines a representation P of their internal architecture: combinatorial logic (marked ) surrounded upstream and downstream by register banks made of D flip-flops ( DFF ) sharing the same clock signal (clk).

DpMax

n

n

n

n

data D Q

D Q

DFF

DFF

D clk2q

clk

Tclk + T skew − Tsetup

Fig. 1. Internal architecture of digital ICs

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 2]

Data are released from the first register bank on a clock rising edge and then processed through the logic before being latched into the next register bank on the next clock rising edge. Thus, in first approximation the clock period (T clk ) has to be longer than the maximum data propagation time through the logic (D pMax ) to ensure correct operation. Besides, a precise writing of the timing constraint equation requires to take into account three other parameters: D clk2q the delay elapsed between the clock rising edge and the actual

update of a register’s output; T skew the skew or slight phase difference that may exist between the clock signals at the clock inputs of two different registers; T setup the setup time which is the amount of time for which a D flip-flop input must be stable before the clock’s rising edge to ensure reliable operation. It also exists an hold time (T hold ) which expresses the same constraint but after the clock edge. Hence, the timing constraint equation (eq. 1) is obtained:

T clk &gt; D clk2q + D pMax + T setup − T skew (1)

An illustration, at bit level, of the signal flow is given in figure 2-a for which the timing constraint is fulfilled. It exists a time margin (called the slack) between the last signal transition at the input of the downstream register and the setup time.

T setup T hold

clk

D clk2Q

Q upstream

D pMax

slack

D downstream

logic glitches

Q downstream

(a) timing constraint fulfilled

D clk2Q

Q upstream

D pMax

D downstream

Q downstream

metastability

(b) setup time violation

D clk2Q

Q upstream

D pMax

D downstream

Q downstream

fault

(c) early latching

Fig. 2. Timing constraint (a) fulfilled or violated: (b) setup violation, (c) early latching.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 2]

The violation of this timing constraint is a straightforward means to inject faults into a circuit. Two stages of such violations are depicted on fig. 2-b-c. A shaded area around the clock rising edge delineates a time interval which corresponds

<!-- PDF_PAGE: 3 -->

## PDF page 3

to a non-deterministic behaviour of the DFF in case of any transition on its input. It extends before and after the clock edge from an amount of time equal to the setup and hold times respectively. A setup time violation arises if the last signal transition is too close to the clock rising edge (Fig.2- b). Then the DFF ’s output undergoes a metastable behaviour [14]: it may stabilize either on a high or low state. An error may occur or not. Fig.2-c introduces a second kind of faulty behaviour: an early latching. In this instance, an erroneous logic value is latched by the register: a fault is actually injected. The fault injection process is then purely assured and deterministic because there is no signal transition in the shaded area. Hereafter, we will refer to constraint timing violation for both cases. The two next subsections reports the means to achieve such timing violations.

B. Overcloking A straightforward approach to inject faults through timing constraints violation is overclocking. It consists in decreasing the clock’s period until faults appear by setup time violation or early latching (Eq. 2).

T clk overclocking &lt; D clk2q + D pMax + T setup − T skew (2)

An increase in the clock frequency does not provide any timing control: faults may be induced at any clock cycle of the circuit. An enhancement of that technique is the use of clock glitches, which is based on inducing a timing violation by modifying only one clock period [15].

### C. Increasing propagation time

The second means of violating the timing constraint equa- tion (cf. eq. 1) is by increasing its right handside part. It may be achieved by increasing the data propagation time through the logic (D pMax ). As shown by equation 3:

T clk &lt; D clk2q + D pMax increased + T setup − T skew (3)

For the sake of simplicity, the data propagation time through a simple CMOS inverter as a function of the power supply and the temperature is recalled. The physical equations are obvi- ously more elaborated for more complicated logic. However, the observable trends are alike. The inverter’s architecture and waveforms are depicted in figure 3 where t pLH and t pHL are its propagation delays for an output’s transition from low to high and high to low logic levels respectively.

In

vdd

PMOS

In

Out

Time

t pLH t pHL

Out

NMOS

CL

gnd gnd

Time

Fig. 3. Inverter: architecture and typical waveforms

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 3]

t pLH and t pHL may not have the same value. Hence, the data propagation time through the inverter (and through any

logic block) depends on the handled data: the propagation time is data dependent. The propagation time, t pLH (eq. 4), is obtained from a first order analysis [16] of the inverter’s dynamic behaviour: |V th,p | 2|V th,p | + ln 3 − 4 C L V DD − |V th,p | V DD (4) t pLH = W p (V DD − |V th,p |) µ p C ox L p

where V DD is the power supply voltage, C L the load ca- pacitance, V th,p the PMOS threshold voltage, µ p the holes mobility, C ox the gate oxyde capacitance and (W p /L p ) the aspect ratio of the PMOS . A similar equation for t pHL may be derived from eq. 4 by substituting the parameters related to the inverter’s NMOS (e.g. µ n , (W n /L n ), V th,n ) for those related to the PMOS . 1) Underpowering: as stated by eq. 4 any decrease of V DD will induce an increase of the propagation delay of the inverter. By extension, the data propagation time through any logic block is increased when an IC is underpowered. Hence, underpowering is a common means to achieve fault injection by violation of the timing constraint. 2) Overheating: the two temperature-dependent parameters of eq. 4 are the charge carriers mobility and the threshold volt- age. However, the temperature dependence of the propagation delay due to V th is a few percent of that due to µ (the mobility for either holes or electrons). Therefore, only the temperature dependence of µ (see eq. 5) is considered at first order [17]. α T µ(T ) = µ(T 0 ) (5) T 0

where T is the temperature, T 0 and α fitting parameters. α varies approximately from −2.2 to −1.5 depending on the doping level [17]. Thus, by extension and from eq. 4 and 5, the data propagation time is increased when an IC is overheated.

### D. Several fault injection means, a common mechanism

Hence, overclocking, underpowering and overheating are three suitable means to inject faults into a circuit by violation of its timing constraints [11], [10]. Intuitively, these three means are usually considered to rely to a same mechanism. The novelty of our approach lies in the proposal of an experimental validation of this assumption. This proof is based on the analysis of the injected faults by means of these three techniques for a test chip handling the same data (the latter condition is due to the data-dependence of the propagation times, and consequently of the induced faults). The uniqueness of the injected faults for every of these three means is the core of that proof as reported in the next section.

### III. E XPERIMENTAL VALIDATION

A. Experiments outline

The following experiments are devoted to the analysis of the faults injected into our test chip by violation of its timing constraints. Three means are investigated: overclocking, un- derpowering and overheating. They all have a global effect on

<!-- PDF_PAGE: 4 -->

## PDF page 4

the target (i.e. they impair similarly every of its part). Hence, injected faults will be located where the timing constraint is violated according the mechanism depicted in figure 2. Any fault may result from a setup time violation, which exhibit a metastable behaviour, or from an early latching, which is purely deterministic. Consequently, it may be a very difficult task to analyse the injected faults if they are too numerous because of the non deterministic behaviour of metastability. Thereby, we have chosen to focus on the first injected fault that may appear when the stress (i.e. overclocking, voltage deprivation or overheating) applied to the test chip is pro- gressively increased. The obtained fault will also reveal the critical path of the design (i.e. the logic path with the longest propagation delay) associated with the current data set. Indeed, the propagation delay through the combinatorial logic is data dependent. As the test chip runs the AES encryption algorithm, the data that have an effect on the propagation delays are both the plaintext and the key. That’s the reason why we used a dataset of 10,000 {Plaintext, Key} pairs choosen randomly. AES is a standard established by the NIST [13] for symmet- ric key cryptography. It is a substitution and permutation net- work based on four transformations (i.e. SubBytes, ShiftRows, MixColumns, AddRoundKey) used iteratively in rounds as depicted on fig.4. The test chip (Xilinx Spartan 3A fpga) embeds an hardware 128-bit version of this algorithm ( AES - 128). It processes data blocks of 128 bits (usually represented as 4x4 bytes matrix, called the AES ’ state) in ten rounds (after round 0). The round keys (K1 to K10) used during every round are calculated on-the-fly by a key expansion module. Hence, a full encryption is completed in eleven clock periods. The test chip nominal clock period is 100 MHz, and its core nominal voltage is 1.2V. In this work, AES is mainly used as

Round 0

Round i i= 1..9

Round 10

AddRoundKey

AddRoundKey

AddRoundKey

MixColumns

Ciphertext C

SubBytes ShiftRows

SubBytes ShiftRows

M

State Mi

(plaintext)

K0 (global key)

K1..K9 (round key 1..9)

K10 (round key 10)

Fig. 4. AES -128 encryption algorithm.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 4]

a test element. Thus, we will not go deeper into its properties. However, because this algorithm is likely to be subject to DFA , the obtained results are yet of interest. As the delays in the encryption module are greater than the delays in the key expander module we can assume that the encryption module will be faulted before every others modules.

B. Overclocking

A first experiment was conducted by using overclocking as a fault injection means. For each {Plaintext, Key} pair

of the dataset the following process was followed: send the plaintext and key to the test chip, launch a first encryption at nominal settings to obtain a correct ciphertext used as a reference, increase successively by an elementary step the stress applied to the target (i.e. the clock frequency) until a first faulty ciphertext is obtained. The elementary frequency step was set to 200 kHz. Then, the faulty ciphertext was processed by reversing the encryption (the key is known) and a comparison was made between the intermediate states of the computations to retrieve the injected fault. The gathered data were added to the dataset: {Plaintext, Key, Ciphertext, Fault}. The obtained faults were single-bit with a rate slightly greater than 90%. Figure 5 gives the spreading of the single- bit faults over the AES ’ rounds. Besides, the value of the

20

18

16

Fault distribution (%)

14

12

10

8

6

4

2

0 1 2 3

4 5 6 Round number

7 8 9 10

Fig. 5. Faults spreading over the AES ’ rounds ( 9,000 single-bit faults).

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 4]

frequency associated with every injected fault gives the corre- sponding critical time (the accuracy of these measures is given apart from T setup , T skew and D clk2q ). These critical times were found between 7,418 ps and 8,741 ps with an average value of 7,968 ps.

### C. Underpowering

A second set of experiments was conducted by using underpowering as a fault injection means according to the process described in III-B: successive decreases of the target’s power supply (its nominal voltage is 1.2V) by elementary steps of 2mV until a first fault is injected. The whole {Plaintext, Key} pairs related to the injection of single-bit faults by overclocking were tested. For every pair, the injected fault was the same: a matching rate of 100% between the faults induced by overclocking and voltage deprivation was obtained. Faults were induced for a power supply ranging from 1.061V to 0.979V, with an average value of 1.02V. Jointly, we used our frequency generator to measure the critical time linked to every setting of the power supply. Figure 6 depicts the critical time as a function of the power supply for three {Plaintext;Key} pairs of the dataset.

### D. Overheating

The third set of experiments was performed by using overheating (a manually controlled thermal air-blower was used) as a fault injection means. Since, heating an IC is done with long time constants only ten {Plaintex, Key} pairs of the dataset were tested according to the process described in

<!-- PDF_PAGE: 5 -->

## PDF page 5

13000

"Dataset_1" Dataset_1_linear(x) "Dataset_2" Dataset_2_linear(x) "Dataset_3" Dataset_3_linear(x)

12000

11000

Critical time (ps)

10000

9000

8000

7000

### 0.9 0.95 1

### 1.05 Power supply (volt)

### 1.1 1.15 1.2

Fig. 6. Critical time versus power supply.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

III-B and III-C. As expected (see eq. 5) an increase in the chip’s temperature (measured outside the package) led to an increase in its critical time until faults are injected when the critical time goes beyond the nominal clock period. For every pair, identical faults with those induced by overcloking and underpowering were obtained. Figure 7 presents the critical time as a function of the temperature for three experiments.

12000

"Dataset_1" Dataset_1_linear(x) "Dataset_2" Dataset_2_linear(x) "Dataset_3" Dataset_3_linear(x)

11000

Critical time (ps)

10000

9000

8000

7000

20 40 60

80 Temperature (degree)

100 120 140

Fig. 7. Critical time versus Temperature

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

E. Underpowering and overheating

Since, underpowering and overheating both lead to an increase of the target’s critical time we used these two injection means in combination to build a 3D curve of the critical time for a given dataset (presented on fig.8).

### IV. R ESULTS ANALYSIS

A. Experimental proof

We drawn in section II the hypothesis that faults injected by overclocking, underpowering or overheating were induced ac- cording to a common mechanism based on timing constraints violation. For the purpose of validating this assumption we have conducted three sets of experiments reported in section

12500 12000 11500 11000 10500 10000 9500 9000 8500

12500 12000 11500 11000 10500 10000 9500 9000 8500

Critical time (ps)

0.95

1

20

1.05

30 40 50 60 Temperature (degree)

1.1

Power supply (volt)

1.15

70

### 1.2 80

Fig. 8. Critical time versus power supply and Temperature

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

III in order to obtain an experimental proof. The same single- bit faults were always obtained by using these three fault injection means. As a consequence, we believe that this is a valid experimental proof of the uniqueness of the fault injection mechanism related to overclocking, underpowering and overheating.

B. Reproducibility and metastability

An analysis of the reproducibility of the fault injection pro- cess was also performed. As exemplified in fig. 2 it exists two kind of faulty behaviour related either to a setup time violation or to an early latching. The latter case is characterized by a 100% reproducibility rate for any experiment carried out with the same experimental settings (dataset, power supply, clock period and temperature): each encryption leads to the same fault. The behaviour is slightly different when a setup time violation occur, because it creates a metastable behaviour of the impacted flip-flop. For a given experimental settings the fault may be induced or not. Figure 9 reports this metastable behaviour induced by overclocking for three different datasets. It gives the fault occurrence rate as a function of the clock period. Consider bit1: for a clock period (T clk ) beyond 8,800ps

100

"Bit_1" "Bit_2" "Bit_3"

80

Fault occurence %

60

40

20

0 7600

7800 8000

8200 8400 Clock periode (ps)

8600 8800 9000

Fig. 9. Metastability: fault occurrence rate versus clock period

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

<!-- PDF_PAGE: 6 -->

## PDF page 6

no fault is injected, for T clk = 8,700ps the fault occurrence rate is 28% (i.e. 28 encryptions out of 100 will lead to a fault), for T clk below 8,500ps a fault is consistently injected (early latching). The injected faults were always the same (100% reproducibility), however there may be no fault. The 100% reproducibility rate mentioned above was ob- tained for single-bits faults. In case of multi-bits faults this rate is lower because of a cumulative effect between bits affected by a metastable behaviour. To be more specific, the reproducibility rate is decreasing as the number of faulted bits is increasing. Because of this phenomenon, it is often considered that the reproducibility of faults injected by timing constraints violation is low. This statement should be mitigate because we have proved that a 100% reproducibility rate may be achieved with a careful choice of the experimental settings.

### C. Fault analysis

1) Fault range: : a careful and progressive increase in the stress applied to the test chip has permit to obtain single-bit faults with a success rate slightly beyond 90%. As regards DFA , this fault model is the most difficult to achieve and the most alarming. Part of the 10% remaining faults were multi- bits faults related to the simultaneous violation of two (or more) critical paths. Yet, most of this 10% faults originates from faults induced in different rounds. This phenomenon is illustrated in figure 10. In fact, the fault injected by violation

Critical Time (ps)

Critical Time (ps)

10 000

8 500

AES rounds 0 to 10

AES rounds 0 to 10

Fig. 10. Path modification after a fault

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 6]

of the critical path of the seventh round (left diagram) induced a modification of the data handled during the subsequent rounds. Consequently, these rounds’ critical times are changed (redrawn on the right diagram). Then, if one of the modified critical time is greater than the clock period (as illustrated) a second fault is injected. This phenomenon also explain the non-equality of the number of faults injected over the AES ’ rounds as depicted in fig. 5. 2) Fault location: : the experimental results also confirm the data dependence of the fault injection process. Any mod- ification of the data has led to a modification of the injected fault. By doing so, faults were injected in every bytes and in half of the 128 bits of the AES state. Changing the data provides a loose control on the faults’ location.

### V. C ONCLUSION

In this paper we have provided an experimental proof of the uniqueness of the fault injection mechanism by means of the target’s clock period, power supply or temperature alteration. The proof lie in the nature of the injected faults: they were exactly the same for a given dataset irrespectively of the injection means used (overclocking, underpowering or overheating). Besides, we have conducted an in-depth study of these faults properties. It has revealed the ability to induce single-bit faults with a success rate beyond 90% and a reproducibility rate of 100%. The data dependence of the injected faults also allowed to control loosely the faults’ location and timing (i.e. the affected round). We hope these results will contribute to a better understand- ing of the threats related to fault injection by means of timing constraints violation. We are already testing a first version of a countermeasure based on these findings.

R EFERENCES

[1] O. Kömmerling and M. G. Kuhn, “Design principles for tamper-resistant smartcard processors,” in Proceedings of the USENIX Workshop on Smartcard Technology, 1999, pp. 9–20. [2] P. C. Kocher, J. Jaffe, and B. Jun, “Differential power analysis,” in CRYPTO, 1999, pp. 388–397. [3] E. Brier, C. Clavier, and F. Olivier, “Correlation power analysis with a leakage model,” in CHES, 2004, pp. 16–29. [4] J. Balasch, B. Gierlichs, and I. Verbauwhede, “An in-depth and black- box characterization of the effects of clock glitches on 8-bit mcus,” in Fault Diagnosis and Tolerance in Cryptography (FDTC), 2011 Workshop on, 2011. [5] J.-M. Dutertre, A.-P. Mirbaha, D. Naccache, A.-L. Ribotta, A. Tria, and T. Vaschalde, “Fault round modification analysis of the advanced encryption standard,” in IEEE Int. Symposium on Hardware-Oriented Security and Trust, 2012. [6] S.-M. Yen and M. Joye, “Checking before output may not be enough against fault-based cryptanalysis,” IEEE Transactions on Computers, vol. 49, no. 9, pp. 967–970, 2000. [7] D. Boneh, R. DeMillo, and R. Lipton, “On the importance of checking cryptographic protocols for faults,” in EUROCRYPT ’97, ser. Lecture Notes in Computer Science, vol. 1233, 1997, pp. 37–51. [8] E. Biham and A. Shamir, “Differential fault analysis of secret key cryptosystems,” in Advances in Cryptology - CRYPTO ’97, ser. Lecture Notes in Computer Science, vol. 1294, 1997, pp. 513–525. [9] H. BarEl, H. Choukri, D. Naccache, M. Tunstall, and C. Whelan, “The sorcerer’s apprentice guide to fault attacks,” in Special Issue on Cryptography and Security, 2006, pp. 370–382. [10] N. Selmane, S. Bhasin, S. Guilley, and J. Danger, “Security evaluation of asics and field programmable gate arrays against setup time violation attacks,” Information Security, IET, vol. 5, no. 4, pp. 181–190, 2011. [11] A. Barenghi, G. Bertoni, L. Breveglieri, M. Pellicioli, and G. Pelosi, “Low voltage fault attacks to aes,” in HOST, 2010, pp. 7–12. [12] Y. Li, K. Ohta, and K. Sakiyama, “New fault-based side-channel attack using fault sensitivity,” IEEE Transactions on Information Forensics and Security, vol. 7, no. 1, pp. 88–97, 2012. [13] NIST, “Announcing the advanced encryption standard (aes),” Federal Information Processing Standards Publication 197, 2001. [14] J. Horstmann, H. Eichel, and R. Coates, “Metastability behavior of cmos asic flip-flops in theory and test,” Solid-State Circuits, IEEE Journal of, vol. 24, no. 1, pp. 146 –157, feb 1989. [15] M. Agoyan, J. Dutertre, D. Naccache, B. Robisson, and A. Tria, “When clocks fail: On critical paths and clock faults,” Smart Card Research and Advanced Application, pp. 182–193, 2010. [16] B. Razavi, Fundamentals of Microelectronics. Wiley, 2008. [17] D. Ha, K. Woo, S. Meninger, T. Xanthopoulos, E. Crain, and D. Ham, “Time-domain cmos temperature sensors with dual delay-locked loops for microprocessor thermal monitoring,” Very Large Scale Integration (VLSI) Systems, IEEE Transactions on, vol. 99, pp. 1–12, 2011.
