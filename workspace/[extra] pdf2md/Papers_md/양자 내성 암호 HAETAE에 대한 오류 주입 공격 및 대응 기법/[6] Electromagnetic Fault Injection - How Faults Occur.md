# [6] Electromagnetic Fault Injection - How Faults Occur

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 8
converted_at: "2026-07-26"
source_asset_id: "HAETAE-FIA-REF-06"
derived_asset_id: "HAETAE-FIA-REF-06-MD"
source_path: "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[6] Electromagnetic Fault Injection - How Faults Occur.pdf"
source_sha256: "60cd58cbd32d562d04bb39a40b821c6d322cc387ac6b4c100e061cc5891283e6"
pages: 8
bbox_words: 6352
consumed_bbox_words: 6352
numeric_tokens: 459
consumed_numeric_tokens: 459
source_blocks: 337
consumed_source_blocks: 337
emitted_blocks: 298
embedded_raster_images: 9
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

2019 Workshop on Fault Diagnosis and Tolerance in Cryptography (FDTC)

Electromagnetic Fault Injection : how faults occur ?

### M. Dumont, M.Lisart STMicroelectronics Rousset, France

Abstract—Electromagnetic Fault Injection (EMFI) has re- cently gained popularity as a mean to induce faults because of its inherent advantages. Among them, the most interesting is probably its ability to generate faults in Systems on Chips without removing the package, and this even if only the frontside is exposed to the EM ﬁeld. Despite this popularity, there is only little information on how EMFI generates faults. Within this context, this paper ﬁrst aims at ﬁlling this lack by proposing a complete modeling of EM induction fault mechanism. In a second step, the introduced model is confronted to experimental data in order to demonstrate its soundness.

Keywords-Integrated circuits, fault attacks, EM fault injec- tion, fault model

### I. I NTRODUCTION

Electromagnetic Fault Injection (EMFI) has ﬁrst been sug- gested as a threat against secure circuits in [1], [2]. Despite this early warning, ﬁrst concrete results were published [3] in 2007. In this work, authors demonstrated that a low cost EMFI is efﬁcient to apply a Bellcore attack [4]. After these seminal works, [5], [6] introduced an alterna- tive EMFI setup built around a high voltage pulse generator and a coil with a ferrite core [7]. The interest of such a system over the one used in [3] being its high time resolution rendering induced faults more repeatable and controllable. Following this work, several papers used similar systems [8], [9], [10] to evaluate the effectiveness of EMFI for performing various attacks on different ICs or again to analyse the impact of EMFI on embedded codes. In addition to the proposal of this EMFI system, [6] suggested EM induced faults are timing faults due to the disruption of the power and ground voltages by EM pulses. Following this suggestion, authors of [11], [12], [13] pro- posed EM pulse detectors which operation are based on the monitoring of propagation delays or other timing metrics. However, in 2014, [14] experimentally demonstrated that the timing fault model was not enough to explain how EMFI induces faults. To that end they showed EMFI induces faults in a circuit at rest (clock stopped), i.e. in an IC in which timing faults cannot be induced. They ﬁnally demonstrated in [15] that EM faults are not timing faults before proposing from their numerous experiments a model called the sampling fault model [16]. This model states that EMFI induces faults by directly disrupting the inputs

978-1-7281-2667-8/19/$31.00 ©2019 IEEE DOI 10.1109/FDTC.2019.00010

9

P. Maurine LIRMM, University of Montpellier Monptellier, France

(D, CK , reset/set, V dd and Gnd) of D-type Flip-Flop (DFF) while they are switching. This implies as it has been experimentally observed and as depicted Fig.1 that EMFI susceptibility varies in time and is greater around the rising edges of the clock. More precisely, [16] claims EM susceptibility is higher during time windows centered on the rising clock edges. In addition, it is also stated that the duration of these time windows is independent of the clock frequency at which operate ICs. If experiments have

t s -t setup t s t s +t hold

CK

EMFI susceptibility

Figure 1. The sampling fault model introduced in [16]

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 1]

been demonstrated in accordance with this model, up to now and up to the best of our knowledge, this experimental model remains unexplained even if a fully digital EM pulse detector derived from it has been proven experimentally efﬁcient [17]. Within this context, this paper aims at explaining how EM faults occur. This explanation is conducted by successively modeling the interaction between EM probes and ICs, EM pulses on ICs and ﬁnally by analyzing in detail the impact of EM pulse on their operation. We do believe that the proposed model could be of great help to design low cost hardware countermeasures as well as to derive design guidelines to mitigate EM induction effects. This paper is organized as follows. Section II derives from basics about EM induction a modeling of the interaction between EM probes and ICs. This modeling is then used to identify the transient effect of EMFIs on the power and ground voltages of ICs. The transient perturbation induced by EMFIs known, its impact on the operation of ICs is analyzed to identify how EM faults occur in section III. Section IV gives experimental evidences of the proposed model soundness before drawing a conclusion in section V.

### II. I MPACT OF EMFI ON IC S SUPPLY VOLTAGE

The idea on which EMFI relies is the generation of a sudden variation of the magnetic ﬁeld in neighborhood of the target IC surface, such a variation being likely to induce

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:07:43 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 2 -->

## PDF page 2

parasitic currents disrupting its operation. Therefore, EMFI is a direct exploitation of EM induction principle. Next paragraphs recall what is EM induction and derive some consequences when used to disrupt ICs.

A. EM induction basics and consequences

The theory of EM induction was developed by M. Faraday in 1831. The latter ﬁrst experimentally demonstrated an electromotive force, , is induced in any wire loop when the magnetic ﬁeld crossing the surface it encloses changes. Finally he demonstrated is proportional to the derivative of the magnetic ﬂux crossing the aforementioned surface. The direction of is given by Lenz’s law which states that an induced current ﬂows in the wire loop in the direction that opposes the change which produced it. The ﬁrst key lesson of M. Faraday’s observations is that EMFI is expected to induce a parasitic current in all wire loops in ICs, with amplitude proportional to the variation rate of the magnetic ﬁeld. The effectiveness of EMFI in inducing fault being proven, the important question is what are the wire loops one can ﬁnd in an IC.

ON Interconnect wire OFF loop

OFF

ON

loop

C gp

loop

R Interconnect wire

C gn

Figure 2. Interconnect wire (left) and 3D power and ground meshes (right)

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 2]

There are two types of wires in ICs with different roles and characteristics: interconnect wires and power/ground rails. As depicted Fig.2, interconnect wires carries an elec- trical signal from the output of a CMOS gate to the input(s) of one or several CMOS gates. Therefore, at one of its end an interconnect wire is connected to either a power or ground rail through a transistor under conduction being equivalent to a low resistance. At the other end it is con- nected to the input(s) of one or several CMOS gates i.e. at MOS capacitances of extremely high (inﬁnite in theory) resistance. Hence, interconnect wires do not form wire loops or extremely resistive wire loops. They are thus not prone to current variation induced by EM induction. Contrarily to interconnect wires, power and ground rails form two 3D meshes delivering the V dd and Gnd signals to CMOS gates. These two meshes, Fig.2, encompass many vertical and horizontal wire loops and are thus extremely prone to EM induction. From these simple considerations one can assume with a high conﬁdence level that EM disturbances mainly alter the behavior of the power and ground networks. The resulting question is then how to model the interaction between an EM probe and both the power and ground meshes. This question is addressed in the next subsection.

10

B. EM coupling modeling

From the above considerations related to wires, the inter- action between coils used to perform EMFIs and ICs reduces not to one EM coupling but to two : one between the coil and the V dd network and the other between the coil and the Gnd network. This interaction can be modeled [18], [19] as depicted Fig.3a. Fig.3a models the EMFI probe with its inductance L probe , its resistance R probe and its capacitance C probe . This probe is connected to a generator delivering a pulse of amplitude V pulse , of width P W with rising and falling edges of duration T r and T f . The two EM couplings are modeled using two mutual inductances M G and M V sharing L probe . The values of these mutual inductances [20] are given by: M G = k G · L probe · L G (1) M V = k V · L probe · L V

where L G and L V are inductances associated to the part the power and ground networks facing the EM probe. One could expect to have L G ≃ L V because of nearly symmetric routings of the power and ground networks in ICs. However, even if L G ≃ L V the mutual inductances M G and M V are not expected to be equal because of the probe positioning above the target IC surface but also because V dd and Gnd rails can be routed on different metal layers. This asymmetry in the EM couplings is modeled by k G and k V with values in [0, 1]. With such a modeling, an EMFI induces two electro- motrice forces (emf ), one in the V dd mesh and one in the Gnd mesh which effects are modeled by two potential differences between V 1 and V 2 and G 1 and G 2 . At that stage, the next point is to study the effect of these emf .

### C. Impact of EMFI on the power and ground bias

To understand EMFIs effect on power and ground net- works, noise free electrical simulations were performed with SPICE. Prior to these simulations, the whole situation has been modeled. The resulting model is depicted Fig.3. It incorporates the pulse generator, the power source (VDC), the EMFI probe, the EM couplings. It also incorporates the power and ground networks with their • the power and ground pads modeled by resistances R pad , inductances L Bond (that of bondings) and ca- pacitors C decap (the decoupling capacitors). • the power and ground grids described using a dis- tributed RC model with C GV the coupling capacitors between the Gnd and V dd rails and R the wire resistance. After this modeling step, simulations were launched. Fig.3c depicts what has been observed in the speciﬁc case of an EMFI with V pulse = 400V , P W = 10ns. This speciﬁc case, reported as an example of what has been observed during many simulations done with various parameters, gives the

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:07:43 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 3 -->

## PDF page 3

(c)

Pulse generator EMFI probe EM Couplings

3

PW

V 1

R probe M V

2

1

V pulse

+ -

V 2

C probe

0

0

G 1

-1

-2

Tr Tf

M G G 2

(a)

-3

(b)

R

Vddi

Vdd

Rpad L

VDC

C decap

C GV

Rpad L

R

Gnd

Gndi

Supply &amp; Pad

= 400V 3 = 10ns V

V Vdd

2

Vdd ∆

S(t)

S(t)

∆

1

ns

ns

0

Gndi 20

Gndj 20

40 60 0 40 60

-1

S overshoot

S undershoot

-2

-3

V 1 V 2

Vddj Vdd

L

Rpad

VDC

C decap

C GV

L Rpad

Gnd

Gndj

G 1 G 2

Power &amp; Ground Grids

Supply &amp; Pad

Figure 3. Complete model for analyzing the impact of EMFIs on the power and ground networks. (a) EM probe and coupling models, (b) model of the power / ground networks (c) effect of EMFIs on V dd and Gnd voltages. (Typical parameters values : R = 12Ω, C GV = 100f F , L BON D = 5nH, R pad = 10mΩ, C Decap = 10nF , L probe = 10nH, L V = L G = 15pH, R probe = 0.2Ω, C probe = 1nF )

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 3]

typical waveforms of V dd(t) and Gnd(t) along the power and ground grids red and blue, respectively. It also gives in black the typical waveform of the voltage swing:

S(t) = V dd(t) − Gnd(t)

(2)

Fig.3c clearly shows that the considered EMFI induces voltage drops on both V dd and Gnd rails on the right side of the power / ground grids (right of V 2 and G2) while voltage bounces are induced on the left of V 1 and G1. The amplitude ΔS of these perturbations increases with V pulse . This is a direct effect of the emf that call electrical charges from the right part of the power / ground grid and push them to the left. Fig.3c also shows that, because of the asymmetrical coupling (k G = 3 · k V ), the drops/bounces on V dd and Gnd have different amplitudes. This results in undershoots and overshoots of voltage swing S that propagate toward the pads while being attenuated along their travel. For symmetrical EM couplings the voltage swing (ΔS = 0) remains stable at its nominal value because drops/bounces on the two rails have exactly the same shape. In this unlikely case no fault can occur.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 3]

III. I MPACT OF EMFI ON IC S OPERATION At that stage, one may wonder about the conditions EM- FIs must met to induce sampling faults and how sampling faults occur. These questions are addressed in the next sections.

A. Simulated Circuit Following the empirical sampling fault model, we simu- lated the effects of these swing undershoots/overshoots on

11

the circuit depicted Fig.4. It represents the end of a logic path arriving at the input of a DFF. It is thus a common structure that can be found thousand of times in ICs. In this ﬁgure, ‘Glue logic’ blocks are chains of 20 inverters while the ‘clock tree’ block is made with 4 clock inverters. C D and C CK are additional loads modeling the inputs of additional gates connected at this point but also interconnect loads.

Vdd

D ref

W r W f

D Q Glue Q ref

DFF

Glue Logic

Logic

C D CK

'S

CK ref

CK

Clock Tree

PW S

C CK

Gnd

D ref stable @ ‘O’ or ‘1’

D=D ref stable @ ‘O’ or ‘1’

CK ref

CK

Q=not(D)

Q=D=D ref

CK ref 2Q ref

Q ref =not(D)

Q ref =D=D ref

CK ref 2E

E

S(t)=Vdd(t)-Gnd(t) 'S

Figure 4. Top : circuit considered during simulations, Bottom: waveforms of signals during EMFI effect analysis

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 3]

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:07:43 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 4 -->

## PDF page 4

Because this circuit is small, its elements are expected to be placed and routed in a reduced area compared to EM probe size. We therefore assumed that all its elements simultaneously experience the same swing undershoots or overshoots. Still following the sampling fault model stating that EM induced faults are not timing faults we did consider the signals, D ref and D stable at the same value ‘0’ or ‘1’ and we did observe only what occurs before and after a single rising clock edge. Therefore if faults occur in simulation they are not timing faults but sampling faults.

B. IC operation criterion

Because we had planned to explore the effect of many parameters related to either to the EMFI settings or to the circuit itself, a ﬁgure of merit to estimate the effect of EMFIs on the circuits has been set up. In absence of any perturbation, as illustrated Fig.4, the DFF copies at the rising edge of CK the data D onto Q and then Q propagates until Q ref . The times spent by the data to propagate up to Q and Q ref in normal operating conditions are denoted CK2Q| nom and CK2Q ref | nom . Considering that EMFIs alters this operation we did consider the ﬁgures of merit F and F deﬁned as :

CK2Q ref | nom CK2Q| nom F = CK2Q| EM F I CK2Q ref | EM F I

F =

(3)

with CK2Q| EM F I and CK2Q ref | EM F I the propagation delays from CK to Q and Q ref in presence of a perturba- tion. With these deﬁnitions, several effects of EMFIs can be differentiated : • F (F ) &gt; 1: EMFI accelerates the propagation of the data from D to Q (Q ref ), • F (F ) = 1 : EMFI has no effect on IC operation, • 1 &gt; F (F ) &gt; 0: EMFI slows down the propagation of the data from D to Q (Q ref ) and can induce timing faults at the next rising clock edge, • F (F ) = 0: D is not propagated from D to Q (Q ref ). This corresponds to the occurrence of a sampling fault.

### C. Effect of EMFI

To observe the effect of EMFIs on the ICs operation, we launched many simulations with different values of ΔS, P W S , τ r and τ f (see Fig.4) and CK nom 2E; CK nom 2E being the time separating the nominal (without perturbation) arrival time of CK rising edge (denoted CK nom ) from the ending (denoted E) of the swing perturbation as depicted Fig.4. For sake of simplicity this paper gives only results related swing undershoots and D ref = 1 . Similar results can easily be obtained for swing overshoots and D ref stable at the value ‘1’. Fig.5 gives, for ΔS ranging between 0V and 2.2V , the evolution of F wrt CK nom 2E. During these simulations, the

12

1.0

F

'S=0.0V 'S=0.0V 'S=1.2V 'S=1.2V 'S=1.5V 'S=1.5V 'S=1.6V 'S=1.6V 'S=1.8V 'S=1.8V 'S=2.2V 'S=2.2V

0.5

CK nom 2E (ns) CK nom 2E (ns)

0.

-1

0

1

2

3

Figure 5. F vs CK nom 2E for ΔS ∈ [0V, 2.2V ], P W S = 5ns, τ r = τ f = 2.5ns. The continous curves are for D = 1 and a swing undershoot. The dashed green curve is for D = 0 and a swing overshoot.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 4]

pulse width, P W S , was set to 5ns and the transition times, τ r and τ f , of the swing undershoot were set to 2.5ns. For ΔS lower than 1.5, F is strictly positive. No sampling fault occurs. For larger ΔS values F = 0 for a while. Therefore there is a threshold for V pulse (and therefore ΔS) below which no sampling fault is induced. For a powerful EMFI (ΔS = 2.2V ), F has values between ‘0’ and ‘1’ for CK nom 2E ∈ [−1; 0.2] ∪ [0.7; 3]ns. Therefore, for such settings, EMFI induces an increase of the delays CK2Q and CK2Q ref . Regarding CK2Q, the increase consists in roughly a triply of the DFF propaga- tion delay (≃ 150ps). Concerning CK2Q ref , the delay is multiplied by 1.7 (less for lower ΔS) as illustrated Fig.6. According to the operating frequency of the DUT and to the timing slack introduced at the design step to take Process, Voltage and Temperature variations into account, these increases can induce timing faults at the next rising edge of the clock. However this is unlikely to occur when characterizing a chip under its nominal voltage because timing margins (especially those considered for voltage vari- ations) are greater (especially for ICs operating with clock frequency like micro-controllers) than the timing margins [21] for advanced technologies. This could explained why timing faults were not reported in [16] and why we did not observe timing faults during the experiments reported in section IV. However the situation could change if one lower the supply voltage during EMFI characterizations. Fig.5 also indicates that between CK nom 2E = 0.2ns and 0.7ns, F suddenly falls down to 0. There are thus, as observed in former works, time windows during which sampling faults occur. These time windows are denoted by Sampling Fault Window (SFW) afterward. Surprisingly, sampling faults occur during the rising (second) edge of the swing and not during the falling (ﬁrst) edge. This means sampling faults occur during the recovery phase of the supply voltage.

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:07:43 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 5 -->

## PDF page 5

1.0

0.8

PW S =13n

=11ns F’ PW PW =9ns

S

S

0.6

PW S =7ns

0.4

PW S =13ns

0.2

=11ns F PW PW =9ns CK

SFW

S

S

nom 2E (ns)

PW S =7ns

0.0

-1 0 1 2 3

Figure 6. F and F vs CK2E for ΔS = 2.2V , P W S = 7, 9, 11, 13ns and τ r = τ f = 2.5ns

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

(1) (2) (3) (4) (5)

Voltage (V)

S

Vdd-|V T |

Voltage (V)

CK nom

D

( )

Voltage (V)

CK

Voltage (V)

Q

Time (s)

(1) (2) (3) (4) (5)

Figure 7. Waveforms of S, D, CK and Q for several values of CK nom 2E with P W S = 3ns and τ r = τ f = 1.5ns

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

### D. How sampling fault occur

The modeling approach has shown EMFIs can induce sampling faults. This is in accordance with what has been observed in practice in former works and sustains our simulation ﬂow methodology.

13

At that stage, the next key point is to understand how they occur. To that end, Fig.7 reveals the waveforms of signals S, D, CK and Q for several values of CK nom 2E. In this ﬁgure, red (blue) waveforms correspond to a case for which sampling faults occur (resp do not occur). As depicted, the EMFI effect can be divided into 5 regions which positions wrt CK nom (in green) varies with CK nom 2E. Region (1) corresponds to the ﬁrst edge of the voltage pulse delivered to the EM probe and therefore to the ﬁrst EM pulse. In this region the supply voltage is quickly reversed by induction currents. As a result, all signals falls down to zero or even lower because of capacitive couplings between the related nets and V dd and Gnd. At the end of this ﬁrst edge of V pulse , the IC stalls and remains quasi stable all along region (2). Region (3) starts with the rising edge of the voltage pulse (producing a second EM pulse of opposite polarity) and ends when the S(t) reaches V dd − |V T |. This phase corresponds to the beginning of the supply voltage recovery. However, because S(t) is lower than the threshold voltages |V T | of transistors (assumed equal for N an P transistors for sake of simplicity), all signals remain stable. Region (4) starts when S(t) crosses V dd − |V T |. Transis- tors are turned on and the structure carries on its recovery and converges toward a ﬁnal state with the occurrence or not of a sampling fault according to the CK nom 2E value. Finally, when the supply voltage reaches back its nominal value the structure enters region (5) and operates nominally. One key observation is that sampling faults occur during the recovery phase of the supply voltage. This highlights the importance of using voltage pulse generator with fast rising and falling edges so that to induce an EM pulse with two opposite polarities. This ensures EMFI with high time resolution. The role of the ﬁrst pulse is to quickly reverse the supply voltage while that of the second is to quickly restore it. To understand why in some cases a sampling fault occurs, we have to look at the internal operation of the DFF. To that end, Fig.8 gives a zoom on what is going on in the DFF in regions (3) to (5). It reports the nominal waveform of CK (in green), and disrupted waveforms of S, D, Q and those of two DFF internal signals. The ﬁrst internal signal is CK I . It is the internal clock signal of the DFF, the one triggering its master and slave. In practice, it is just a delayed copy of CK by an internal buffer which role is to ensure fast internal clock edges and therefore reduced setup and hold times. The second internal signal is the value stored in the master of the DFF, i.e. the output of the ﬁrst DFF stage which is a tristate gate. In normal operation, the stored value is equal to not(D) (‘0’ in our case) after the rising edge of the CK I . Fig.8 shows that three cases (black, red, blue) must be distinguished according to CK nom 2E. Sampling faults occur only for the red case.

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:07:43 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 6 -->

## PDF page 6

S

CK nom

not(D)

D

CK I

Q

t (ns)

Figure 8. Waveforms of S, D, Q, CK I and not(D) for several values of CK nom 2E with P W S = 3ns and τ r = τ f = 1.5ns

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 6]

In the ﬁrst case (in black), the recovery of S(t) ends before the nominal arrival time of CK in green. In that case, D has time to settle back to a value higher than 0.5 · V dd before the arrival of the internal clock edge CK I . As result, not(D) is lower than 0.5 · V dd and the DFF samples the right value. In the second case (in red), the recovery of the S(t) is well started but not achieved when the normal clock edge should have occur. In that case, D has little time to recover its expected value. As result, D &lt; 0.5 · V dd and not(D) &gt; 0.5 · V dd when CK I rises as shown Fig.8. Consequently the DFF samples the wrong value. The third case (in blue) is quite surprising. It corresponds to a recovery phase starting just before or after the nominal arrival time of CK. In that case, D and not(D) starts rising all together following S(t). However, because CK I recovery is faster than that of D and not(D), the DFF stores a ‘0’ in the master i.e. stores the right value. However, the way this correct value has been sampled by the DFF is completely abnormal. It is the result of the simultaneous wake up of all signals and not of a correct operation of the DFF. These three cases explain why and how EMFI induces sampling faults only during short time windows and sustains the experimental observations reported in [16]. They also explain why timing settings of EMFI are so important in practice. The concordance between simulations and experimental results given in [16] sustains the soundness of the EM fault

14

model described in this paper. However, to further demon- strate it, comparisons between experimental and simulation results are given in the next section.

IV. E XPERIMENTAL VALIDATION Getting direct experimental evidences demonstrating the validity of the proposed model is extremely difﬁcult because EMFIs pollute all measurements at several meters. One alternative is to integrate embedded sensors in DUT. How- ever, even this complex approach is insufﬁcient because the supply voltage of these embedded sensors will be disrupted by EMFIs. We therefore searched for indirect evidences of the sound- ness of the EMFI model and simulation ﬂow methodology introduced in this paper. The idea has been to compare trends observed in practice when changing EMFI settings with trends reported by simulations when varying the same parameters. Among the parameters that can be easily varied in practice one can ﬁnd : • the clock frequency, F CK , of the device under test, • the amplitude, V pulse , of the voltage pulse • the width, P W , of the voltage pulse. Next sections give experimental and simulation data related to variations of those parameters but also provide detail about the DUT and the EMFI platform we used.

A. EMFI platform Our EMFI platform features a voltage pulse generator delivering pulse of amplitude ranging between ±50V and ±400. The pulse width of the generated pulse can be as low as 6ns and as high as 100ns. The timing accuracy of the platform is equal to ±100ps + 0.03% of the pulse generator latency. The latter, measured between the external trigger and the shot, can be tuned by step of 10ps between 370ns and 1s. Used EM probes are coils with spaced turns around a ferrite core with a diameter ranging 300μm and 1500μm. Fig.9 shows an EM probe above our testchip.

Figure 9. EM probe above the frontside of our testchip

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 6]

B. Device Under Test and EMFI EMFIs were applied to our DUT, designed with a low power 40nm CMOS technology. The core of this testchip occupies an area equal to 2150μm × 2150mm and is supplied with 1.2V . The clock frequency of this testchip can be externally controlled.

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:07:43 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 7 -->

## PDF page 7

This testchip embeds among various crypto-primitives an hardware AES which was the target of our EMFI campaigns. These EMFIs were performed with various settings so that to verify if sampling fault windows exist and behave as predicted by the modeling with respect to F CK , V pulse and PW .

### C. Effect of F CK variations

To verify the existence of SFW, EMFIs were performed at different EM probe positions and different values of F CK . These EMFIs were done so that EM shots sweep at least two clock periods with a time step equal to 100ps. For each considered shot time, t shot , 100 EMFIs were performed so that to estimate the probability P f to induce a fault. Fig.10 gives the evolution of P f vs t shot for three values of F CK . As expected SF W appear on the probability (P f ) traces. These windows repeat, accordingly to the model, with a period equal to that of the DUT (30M Hz, 50M Hz and 70M Hz). Their width measured at P f = 0.5 are as expected independent of the clock frequency. However their value ranges between 6.3ns and 7.1ns. This uncertitude in the measure of the SFW width is mainly due to the pulse generator jitter (±100ps+0.03% of the tuned latency) which has a value close to 0.9ns for the set latencies allowing to shoot in the AES at the considered clock frequencies. Therefore, there is a quite good agreement between the model prediction and experiments.

1.0

T CK =33ns

P f

6.3ns

### 0.0 1.0

7.1ns

P f

T CK = 20ns

### 0.0 1.0

6.7ns

P f

T CK =14.2ns

0.0

0

1T CK

2T CK

Probability of inducing a fault vs normalized time ( T t )

Figure 10.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 7]

CK

### D. Effect of V pulse variations

Other similar experiments and simulations were done to estimate the evolution of SF W width wrt V pulse . Simula-

15

1.0

0.8

Normalized SFW width

0.6

0.4

0.2

V pulse (V)

0

Figure 11. Simulated and measured normalized SFW width wrt V pulse

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 7]

1.0

Normalized SFW width

0.8

0.6

0.4

0.2

PW (ns)

0

9 11 13 15 17 19 21

Figure 12. Simulated and measured normalized SFW width wrt the voltage pulse width P W

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 7]

tions predict the width of sample fault windows increases with V pulse . This trend can also be observed experimentally as reported Fig.11. This ﬁgure gives the normalized sim- ulated and measured trends of SF W width with V pulse . Normalization has been done with respect to the SF W width measured and simulated for V pulse = 380V . The agreement between simulations and experiments demon- strates the soundness of the proposed EM fault modeling.

E. Effect of P W variations

Finally, similar experiments than those described in pre- vious section were done to analyze the effect of P W on the SF W width. From simulations (see Fig.6) it was expected that P W does not affect much the SF W width. Experiments have conﬁrmed this observation. To further sustain this result, Fig.12 gives the normalized simulated and measured trends of SF W width wrt P W . Normalization has been done wrt the value obtained for P W = 13ns Again, the agreement between simulations and experiments is good. This demonstrates the soundness of the proposed EM fault modeling.

### V. C ONCLUSION

An explanation of how EMFI could induce faults has been given in this paper. The associated simulation approach has been used to forecast how EMFI settings changes the probability to induce faults. The simulated trends have been

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:07:43 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 8 -->

## PDF page 8

successfully confronted to experiments. This model states that EM faults are induced because voltage pulse applied to EM probe generates an EM pulses with two opposite polarities. The ﬁrst one induces a reversal of the supply voltage while the second one restores it. During the supply voltage recovery, the DFF can sample wrong values because they operates under abnormal conditions. The accordance between the simulation and experiments shows that the model is headed in the right direction. However, the model covers only cases in which the EMFI are shorter than the clock period (case of microcontrolers) and applied to glue logic. Furthermore, EMFI effects can vary signiﬁcantly between devices or EM conﬁguration, so this explanation given in this paper may not be the only or ﬁnal one. There is thus room for reﬁnements. Further works will focus on reﬁning the proposed model (taking the effect of the substrate into account, considering EMFI effect on analogue blocks, etc) but also on extending it to cases for which the EM induced perturbation lasts for more than a clock cycle.

R EFERENCES

[1] J. Quisquater and D. Samyde, “Eddy current for magnetic analysis with active sensor,” in Proceedings of ESmart 2002, p. pp 185194, Eurosmart, 2002.

[2] D. Samyde, S. P. Skorobogatov, R. J. Anderson, and J. Quisquater, “On a new way to read data from memory,” in Proceedings of the First International IEEE Security in Storage Workshop, SISW 2002, Greenbelt, Maryland, USA, December 11, 2002, pp. 65–69, 2002.

[3] J.-M. Schmidt and M. Hutter, “Optical and em fault-attacks on crt-based rsa: Concrete results,” in Austrochip 2007, 15th Austrian Workhop on Microelectronics, 11 October 2007, Graz, Austria, Proceedings (J. W. Karl C. Posch, ed.), pp. 61 – 67, Verlag der Technischen Universität Graz, 2007.

[4] D. Boneh, R. A. DeMillo, and R. J. Lipton, “On the impor- tance of eliminating errors in cryptographic computations,” J. Cryptology, vol. 14, no. 2, pp. 101–119, 2001.

[5] A. Dehbaoui, J.-M. Dutertre, B. Robisson, P. Orsatelli, P. Maurine, and A. Tria, “Injection of transient faults using electromagnetic pulses -practical results on a cryptographic system-,” IACR Cryptology ePrint Archive, vol. 2012, p. 123, 2012.

[6] A. Dehbaoui, J.-M. Dutertre, B. Robisson, and A. Tria, “Electromagnetic transient faults injection on a hardware and a software implementations of aes,” in FDTC, pp. 7–15, 2012.

[7] P. Maurine, “Techniques for em fault injection: Equipments and experimental results,” in FDTC, pp. 3–4, 2012.

[8] F. Majeric, E. Bourbao, and L. Bossuet, “Electromagnetic security for SoC,” in 23rd IEEE International Conference on Electronics Circuits and Systems (ICECS) (IEEE, ed.), (Monté Carlo, Monaco), IEEE, 2016.

16

[9] J. Proy, K. Heydemann, F. Majéric, A. Cohen, and A. Berzati, “Studying EM pulse effects on superscalar microarchitectures at ISA Level, journal = CoRR, volume = abs/1903.02623, year = 2019,,”

[10] N. Moro, A. Dehbaoui, K. Heydemann, B. Robisson, and E. Encrenaz, “Electromagnetic fault injection: to- wards a fault model on a 32-bit microcontroller,” CoRR, vol. abs/1402.6421, 2014.

[11] L. Zussa, A. Dehbaoui, K. Tobich, J.-M. Dutertre, P. Maurine, L. G.-Sage, J. Cledire, and A. Tria, “Efﬁciency of a glitch detector against electromagnetic fault injection,” in DATE, pp. 1–6, 2014.

[12] J. Breier, S. Bhasin, and W. He, “An electromagnetic fault injection sensor using hogge phase-detector,” in 18th Inter- national Symposium on Quality Electronic Design, ISQED 2017, Santa Clara, CA, USA, March 14-15, 2017, pages = 307–312, year = 2017,.

[13] L. Rivire, Z. Najm, P. Rauzy, J. Danger, J. Bringer, and L. Sauvage, “High precision fault injections on the instruction cache of armv7-m architectures,” in 2015 IEEE Interna- tional Symposium on Hardware Oriented Security and Trust (HOST), pp. 62–67, May 2015.

[14] S. Ordas, L. G.-Sage, K. Tobich, J. Dutertre, and P. Maurine, “Evidence of a larger em-induced fault model,” in Smart Card Research and Advanced Applications - 13th International Conference, CARDIS 2014, November 5-7, 2014., pp. 245– 259, 2014.

[15] S. Ordas, L. Guillaume-Sage, and P. Maurine, “EM injection: Fault model and locality,” in 2015 Workshop on Fault Di- agnosis and Tolerance in Cryptography, FDTC 2015, Saint Malo, France, September 13, 2015, pp. 3–13, 2015.

[16] S. Ordas, L.-G.Sage, and P. Maurine, “Electromagnetic fault injection: the curse of ﬂip-ﬂops,” J. Cryptographic Engineer- ing, vol. 7, no. 3, pp. 183–197, 2017.

[17] D. El-Baze, J. Rigaud, and P. Maurine, “An embedded digital sensor against EM and BB fault injection,” in 2016 Work- shop on Fault Diagnosis and Tolerance in Cryptography, FDTC2016, Santa Barbara, CA, USA, August 16, 2016, pp. 78–86, 2016.

[18] S. Ben Dhia, M. Ramdani, and E. Sicard, Electromagnetic Compatibility of Integrated Circuits: Techniques for low emis- sion and susceptibility. 2006.

[19] J. Raoult, P. Payet, R. Omarouayache, and L. Chusseau, “Electromagnetic coupling circuit model of a magnetic near- ﬁeld probe to a microstrip line,” in 2015 10th International Workshop on the Electromagnetic Compatibility of Integrated Circuits (EMC Compo), pp. 29–33, 2015.

[20] S. R. and Hui and X. Liu, “Mutual inductance calculation of movable planar coils on parallel surfaces,” IEEE Transactions on Power Electronics, vol. 24, no. 4, pp. 1115–1123, 2009.

[21] D. K. Arora, D. A. Patel, Shahabuddin, S. Kumar, N. K. Dayani, B. Singh, S. Naudet, A. Virazel, and A. Bosio, “Anal- ysis of setup and hold margins inside silicon for advanced technology nodes,” in 2016 17th International Symposium on Quality Electronic Design (ISQED), pp. 295–300, 2016.

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:07:43 UTC from IEEE Xplore. Restrictions apply.
