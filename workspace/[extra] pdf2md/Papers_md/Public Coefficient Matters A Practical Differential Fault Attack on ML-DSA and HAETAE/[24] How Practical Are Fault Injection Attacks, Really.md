# [24] How Practical Are Fault Injection Attacks, Really

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 9
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-24"
derived_asset_id: "PCM-DFA-REF-24-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[24] How Practical Are Fault Injection Attacks, Really.pdf"
source_sha256: "031f90079b7ea997a30c82f86d7a5b142451f4755d95fb6d5646c62e1c01e120"
pages: 9
bbox_words: 8344
consumed_bbox_words: 8344
numeric_tokens: 592
consumed_numeric_tokens: 592
source_blocks: 106
consumed_source_blocks: 106
emitted_blocks: 105
embedded_raster_images: 17
images_stored: 0
conversion_issues: 0
glyph_issue_chars: 0
verification: "verified"
curation: "text-only-v1"
linked_visual_assets: 0
images_stripped: 0
curated_pages: 9
glyph_chars_removed: 0
-->

<!-- PDF_PAGE: 1 -->

## PDF page 1

Received 17 September 2022, accepted 23 October 2022, date of publication 26 October 2022, date of current version 2 November 2022.

Digital Object Identifier 10.1109/ACCESS.2022.3217212

How Practical Are Fault Injection Attacks, Really?

1 AND XIAOLU HOU

2

JAKUB BREIER

1 Silicon Austria Labs, 842 16 Graz, Austria

2 Faculty of Informatics and Information Technologies, Slovak University of Technology, 811 07 Bratislava, Slovakia

Corresponding author: Jakub Breier (jbreier@jbreier.com)

ABSTRACT Fault injection attacks (FIA) are a class of active physical attacks, mostly used for malicious purposes such as extraction of cryptographic keys, privilege escalation, attacks on neural network imple- mentations. There are many techniques that can be used to cause the faults in integrated circuits, many of them coming from the area of failure analysis. In this paper we tackle the topic of practicality of FIA. We analyze the most commonly used techniques that can be found in the literature, such as voltage/clock glitching, electromagnetic pulses, lasers, and Rowhammer attacks. To summarize, FIA can be mounted on most commonly used architectures from ARM, Intel, AMD, by utilizing injection devices that are often below the thousand dollar mark. Therefore, we believe these attacks can be considered practical in many scenarios, especially when the attacker can physically access the target device.

INDEX TERMS Hardware security, fault injection attacks, fault analysis, cryptography.

### I. INTRODUCTION

Cryptographic algorithms, both symmetric and public key, are susceptible to fault injection attacks (FIA). In 1997, Boneh, DeMillo and Lipton showed that an implementa- tion of RSA using Chinese remainder theorem (CRT) can be easily broken by using faults [1]. In the same year, Biham and Shamir published an attack titled differential fault analysis (DFA) that can break most of the symmetric cryptosystems [2]. The working principle of FIA is simple – the attacker injects a fault during the algorithm execution, and then, based on the analysis method, they utilize the information from the faulted execution to narrow down the search space of the secret/private key. Nowadays, 25 years after these attacks were published, this area has become one of the major areas in hardware security, alongside the pas- sive side-channel attacks (SCA) [3]. Many analysis methods have been published to date, to mention the most prominent ones apart from the DFA: statistical ineffective fault analysis (SIFA) [4], persistent fault attack (PFA) [5], fault sensitivity analysis (FSA) [6], fault template attacks (FTA) [7], and FIA combined with SCA [8]. Aside from targeting cryp- tography, fault attacks have been used for bypassing check- ing routines [9], [10], and even faulting neural network

The associate editor coordinating the review of this manuscript and

approving it for publication was Derek Abbott .

implementations [11], [12]. Various methods have been used for injecting faults, from clock/voltage glitches [13], to elec- tromagnetic (EM) pulses [14], to lasers [15], to X-rays [16], to Rowhammer attacks [17]. While there have been several surveys [18], [19], [20] and book publications [8], [21], [22] summarizing the state-of- the-art in the area of FIA, there is an important question that often remains unanswered. It is natural that whenever someone from the outside of this area comes across a work that details an attack on some implementations, they wonder whether such an attack vector can be realized in a real world, not just an expensive laboratory setting with a highly skilled personnel. In this paper, we try to address this issue and provide an answer to:

‘‘How practical are fault injection attacks?’’

We tackle this question from multiple points of view – cost of equipment, remote access, device decapsulation, preci- sion of the fault, and device architecture. We note that this article is not a comprehensive survey of all the works in the area – we select works that provide a reasonable description of the experimental setup that can be used for a proper comparison. Similarly, we do not aim at in-depth description of fault injection techniques – while we provide a detailed overview and a high-level working principle of each technique, interested reader is advised to explore other

This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/

113122

VOLUME 10, 2022

<!-- PDF_PAGE: 2 -->

## PDF page 2

J. Breier, X. Hou: How Practical Are Fault Injection Attacks, Really?

resources, such as [23] for EM, and [24] for laser fault injection. The rest of this paper is organized as follows. Section II gives a detailed information on each commonly used fault injection technique. Section III provides an overview of the cost of each achievable fault model published so far. Section IV provides a discussion on countermeasures and future work, and finally, Section V concludes this work.

### II. DETAILED OVERVIEW OF FAULT INJECTION TECHNIQUES

In this section, we will detail the most popular fault injection techniques that are used for testing cryptographic devices nowadays.

A. CLOCK/VOLTAGE GLITCHING

Voltage and clock manipulation based fault injection methods are low-cost, and generally, no sophisticated equipment is necessary. They can be achieved both remotely and with target device in hand. With physical access to the device, voltage glitching is done by manipulating the power supply, causing the faulty behavior on a device. It can be achieved by creating precise high variations in a power supply or by under-powering the device. Precise high variations, or power spikes, modify the state of latches of flip-flops, influencing the control and data path logic of the circuit [25]. For example, if the voltage spike hap- pens during memory reading, wrong data may be retrieved. It was also shown that different shape of the glitch waveform affects the success of the attack [13]. Under-powering of the device can cause erroneous output. Such method affects the algorithm continuously and might cause faults throughout the computation. But single faults are possible when the insufficient power supply causes gentle enough stress so that dysfunctions do not occur immediately after the computation starts and multi-faults do not happen [26]. Figure 1 depicts a real voltage glitch attack based on under-powering on smart cards. When the attacker has access to the target device, voltage glitching is generally easy to implement and it is the cheapest fault injection method as the necessary equipment are wires for connecting to the device and a power source. On the other hand, this method requires that the attacker has access to the power supply line of the device. Voltage glitching attacks were even used to break security enclaves of Intel [27] and AMD [28]. Both attacks used an inexpensive Teensy 4.0 board 1 (≈30 USD), making them highly practical in terms of equipment cost. Naturally, for such attacks it is necessary to have a deep knowledge of the attacked architecture. Another inexpensive fault injection method is a clock glitch. Computation devices use external or internal clocks to synchronize all of their calculations. When the clock

1 https://www.pjrc.com/store/teensy40.html

VOLUME 10, 2022

FIGURE 1. An example of a voltage glitch on a smart card.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 2]

signal is changed, the resulting computation might have wrong instruction executed or data corrupted. For devices that require an external clock generator, the fault can be introduced by supplying a bad clock signal, e.g. a signal that contains fewer pulses than the normal one [29]. Devices with internal clock generators, however, cannot be attacked by a clock glitching method. Clock glitches are generally considered as the simplest fault injection method as the attack devices are easy to operate with. For example, clock glitches can be achieved by using low-end field-programmable gate array (FPGA) boards [30], [31]. Recently, a multifault evaluation platform named TRAITOR with a price below 130 USD was proposed in [32]. For clock glitches, the adversary needs to have a direct control over the clock generator, which is a common scenario when attacking smart cards. When it comes to remote attacks, clock/voltage glitching can also be achieved. A relatively new class of fault attacks reveals vulnerabilities following the advancement of efficient energy management. The designers of energy management rarely consider the security aspect due to the complexity of devices from hardware point of view as well as software executed, cost and time-to-market constraint [33]. By exploit- ing Dynamic Voltage &amp; Frequency Scaling (DVFS), Tang et al. [34] developed CLKSCREW, where the attacker can manipulate the frequency and voltage of an Nexus 6 phone, forcing the processor to operate beyond recommended limits. They experimentally verified that one-byte random fault is achievable. CLKSCREW can be achieved only by software control of energy management hardware regulators in the target devices. Similar vulnerabilities were also exploited in ARM-based Krait processor from a commodity Android [35] and intel SGX [36]. The features of those attacks are that they are software- based attacks, hence allowing the threat model to shift from a local attacker to a potentially remote attacker. More and more software-based fault attacks by voltage glitching were later developed, e.g. [37], [38]

B. OPTICAL FAULT INJECTION

The phenomenon of ionization effects on transistors has been known for decades. The usage of lasers in the area

113123

<!-- PDF_PAGE: 3 -->

## PDF page 3

FIGURE 2. Optical fault injection attacks: (a) pulsed laser fault injection on ATmega328P mounted on a modified Arduino UNO board as a target; (b) usage of the same setup to get an infrared image of the chip.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 3]

of reliability of microchips is a standard way to test their robustness and dates back to the very beginning of the com- puting era [39]. It is especially important to test chips that will be deployed in adverse conditions. For example, it was shown that the flip-flop circuits in the satellites are affected by cosmic rays [40]. It was just a matter of time until the first optical fault injection technique is used in the area of cryp- tography after it was discovered that faults can compromise the security [41]. Optical fault injection area is perhaps the most diverse from the listed techniques. On one hand, there are works using an inexpensive camera flash to cause random faults [41], on the other, an attacker can use a nanofocused X-ray beam to target a single transistor [16]. Moreover, it was shown that with the usage of lasers it is possible to probe the memory without changing it, which can reveal its content [42]. Therefore, the practicality range varies greatly for this class of attacks. When it comes to security evaluation labs, the method of choice would be a laser fault injection (LFI). There are numer- ous companies selling out-of-the-box setups for performing LFI. A standard setup would consist of the following parts: laser source, objective lens, motorized positioning table, and a controlling device. A digital oscilloscope can be used to pre- cisely align the laser activation with the execution of the target routine on the device. Normally, there would be an optical splitter so that an infrared (IR) camera could be included on the same lens. Such a setup is depicted in Figure 2(a), with a backside chip surface picture taken from the IR camera in Figure 2(b). While the cost of a fully assembled setup would be nor- mally south of 50k USD, recently there has been a proposal showing that it is possible to assemble a working setup under 500 USD [43]. The authors used a solid state laser diode allowing a pulse repetition rate of 200 MHz which is on par with expensive setups from established testing equipment companies. However, as mentioned earlier, lasers are not the only method within the optical fault injection area. The very first

113124

J. Breier, X. Hou: How Practical Are Fault Injection Attacks, Really?

paper in the security realm showed that by using a camera flash coupled with a 1500× magnifying lens (mounted on Wentworth Labs MP-901 manual prober), it was possible to change the value of a single SRAM on a PIC16 chip. While one could argue that the price of such a manual prober could be relatively high, a more recent paper has shown that it is possible to use an inexpensive ball lens to focus the camera flash [44]. Such a setup was used to target registers and skip instructions on ARM Cortex-M0, and to change the values in the RAM and skip instructions on ATmega328P. Optical fault injection is considered as a semi-invasive attack technique, meaning that the chip package needs to be removed to expose the chip to the optical source. This is the main drawback as sometimes it is not possible to de-package the chip without damaging the circuitry or the bonding wires. The injection is normally done on the backside of the chip, as the components are protected from the front side. This creates another challenge as the absorption depth of silicon varies for different wavelenghts, and therefore, the silicon substrate might need to be thinned down to allow an attack. Either a mechanical or a chemical decapsulation techniques can be used to remove the package, each offering different set of advantages and disadvantages [45]. For thinning the sub- strate, a mechanical delayering is necessary, often involving expensive devices (e.g. UltraTec ASAP-I was used in [46]). However, if the chip can be properly prepared, optical fault injection offers a very precise and repeatable way to induce errors [47]. There are several other fault injection techniques which are somewhat related to optical techniques in their modus operandi. There is a long history of using electron and ion beam techniques in the area of failure analysis for reliability testing of integrated circuits [48]. To the best of our knowl- edge, the usage of X-ray nanobeams was the only work within this realm used for security analysis [16]. The advantage of this method is that there is no need to remove the chip package as it is transparent to the beams. These techniques range in millions of USD and are out of the practical bounds for the class of attackers normally considered when attack- ing devices such as credit cards, IoT devices, etc. However, a consideration needs to be in place for very critical systems such as military communication equipment. To summarize, optical fault injection techniques offer a high precision and repeatability at a relatively high cost, apart from few exceptions. The chip preparation is the main draw- back of these techniques (unless the very expensive methods are used), and often makes it impractical to use outside of laboratory environment. As it is often useful to assume highly motivated attackers with high capabilities, laser fault injec- tion is a de-facto standard for security testing labs that certify security critical elements.

### C. ELECTROMAGNETIC FAULT INJECTION

Cryptographic circuits are usually a combination of digital logic, implementing the algorithm, and analog logic which handles the clock sybsystem and random number generators.

VOLUME 10, 2022

<!-- PDF_PAGE: 4 -->

## PDF page 4

J. Breier, X. Hou: How Practical Are Fault Injection Attacks, Really?

FIGURE 3. Pulse EM injection in practice: (a) a high voltage EM pulse generator inducing faults through an off-the-shelf injection probe into ATmega328P (Arduino UNO board); (b) a compact EM pulse generator injecting faults through a custom made injection probe into ARM Cortex-M4 (STM32 Discovery board).

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 4]

Electromagnetic (EM) emanation affects both analog and digital blocks, despite their different physical characteristics. However, a different approach needs to be taken in each case. Analog blocks are vulnerable to powerful harmonic EM waves. The attacker generates a stable sinusoidal signal at a given frequency that injects a harmonic wave creating a parasitic signal [49]. Such a signal can bias the clock behavior or inject an additional power directly and locally into the chip. Equipment for this type of EM injection usually consists of a motorized positioning table, signal generation module, and an oscilloscope. Digital blocks are clocked, therefore the preferable way to disrupt their behavior is via EM pulse injection capable of injecting faults in a specific clock cycle in a controllable way [50]. The aim is to inject a sudden and sharp EM pulse into the integrated circuit, introducing intense transient cur- rents altering the behavior of logic cells. Generally, the equip- ment consists of a high voltage pulse generator and a coil with a ferrite core, serving as an injection probe. An example of such an equipment is depicted in Figure 3. As the fault analysis methods mostly work with data perturbation (bit flips, bit sets/resets, random faults, etc.), pulse EM injection is more prevalent in the literature. This injection method provides a good trade-off between the cost and the precision. Pulse injectors can be bought for a rel- atively inexpensive price, for example, NewAE sells their ChipSHOUTER for ≈ 3.3k USD 2 (used for example in [51] to break hardware wallets). For more powerful and precise equipment, one can look into Avtech pulse generators that would generally range between 10k - 20k USD. 3 A near-field injection probe can either be bought (cost here would be a couple of hundred USD) or manufactured from very low-cost components. Several research articles explore the possibility of a custom probe design [52], [53], [54]. Generally, a ferrite core, a copper wire, a connector, and a heat shrinking tube are enough to create a custom probe (depicted in Figure 4).

2 https://www.newae.com/chipshouter

3 https://www.avtechpulse.com/medium/

VOLUME 10, 2022

FIGURE 4. A generic depiction of an EM fault injection probe.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 4]

Recently, there have been published several custom-made low-cost EMFI device prototypes which can be easily repro- duced by using inexpensive off-the-shelf components and a moderate knowledge in electronics. BADFET [10] was shown to be capable of overcoming a secure boot, Silicon- Toaster [55] was used to defeat a firmware security protection of an IoT device, and another low-cost device was shown to be effective in privilege escalation [56]. EM fault injection does not need a device decapsulation for chips enclosed in a standard epoxy package, which is one of the main drawbacks of laser fault injection. The advantage over the clock/voltage glitching is that there is no need to attach any wires on the power supply. To summarize, EM fault injection is a highly practical technique for attackers that have a possession of the target device – it offers good fault reproducibility and precision at a relatively low cost.

### D. ROWHAMMER ATTACKS

The earliest remote fault injection was based on Rowhammer attack [57], which exploits the physical characteristics of DRAM – by aggressively reading/writing to some address in DRAM, the attacker can flip bits in a nearby memory location. Such a vulnerability is mostly due to the advancing of DRAM manufacturing technology, which allowed smaller cells to be placed closer to each other. A smaller cell also means less capacity for charge, hence lower noise margin and making the cell more vulnerable to data loss [58]. High density of cells additionally causes electromagnetic coupling effects between them, resulting in unwanted interactions [59]. Rowhammer attack has been demonstrated on various plat- forms: browsers [60], [61], [62], cloud environment [63], [64], [65], smartphones [66], [67] and flash storage [68], [69]. These attacks do not require the attacker to have a physical access to the device except for the ability to execute code on the target device. Tatar et al. [70] demonstrated that Rowham- mer can also be carried out by sending network packets to a target machine connected to RDMA-enabled networks. In terms of the equipment, to achieve Rowhammer attacks, the attacker just needs an access to Internet and a com- puter. A deeper knowledge of computer architecture might be required for more sophisticated attacks.

### III. CURRENT STATE-OF-THE-ART TECHNIQUES AND THEIR PRACTICALITY

From the attacker’s point of view, a natural question is ‘‘I have a target device and a desired fault model, what are the possible ways of achieving the fault and what is the cost?’’ In this section, we aim at answering this by listing the

113125

<!-- PDF_PAGE: 5 -->

## PDF page 5

J. Breier, X. Hou: How Practical Are Fault Injection Attacks, Really?

TABLE 1. Overview of the techniques currently available in the literature with the lowest cost for a given target device and a fault model. A ‘‘low’’ cost means that only a standard desktop PC (and in some cases, connection wires) are needed for the attack.

available works along with the details that are important for the attacker. Generally, the following categories of fault models are used in the analysis methods in the literature:

Bit flip is the change of the bit value to the opposite value, while this bit can be precisely selected by the attacker. A multiple bit flips also fall within in this category as long as all the target bits are selected by the attacker. For example, most of the fault attacks on neural networks utilize this model [12], [77]. • Bit set/reset is the change of the bit value either to ‘1’ (set) or to ‘0’ (reset). Again, the assumption is that the attacker can select the bit to be set/reset. This fault model is very powerful and can be utilized for example for blind fault attacks [78]. • Random byte is a less precise fault model where a value of a particular byte changes to some random value. This is considered to be the most relaxed fault model to achieve a successful DFA attack [79], [80]. • Instruction skip practically ignores the execution of the currently processed instruction. Powerful attacks can be introduced by using this fault model, such as privilege escalation [81], a simple key extraction [82], or a neural network misclassification [83]. • Execution faults occur in FPGAs where the val- ues being processed are affected by setup violations. For example, physically unclonable functions can be attacked with this fault model [84]. • Stuck-at faults permanently changes the value of the stored data into some other value. SIFA can be used with this fault model [4], and also, true random number

•

113126

generators (TRNGs) can be biased by using stuck-at faults [76].

The high-level overview of current techniques is listed in Table 1. 4 We aimed at finding the techniques with the lowest cost for the given target device and the fault model, along with the information whether this attack can be carried out remotely. We believe that when designing a fault analysis method, it is important to know whether it can be carried out in practice and therefore, the table provides a sufficient answer to that. There are several additional remarks that we would like to mention:

Wherever we use the tilde character (‘∼’), we estimate the cost based on the information on the used setup. Generally a working setup for an electromagnetic fault injection (EMFI) can be assembled for around 30K USD, and for a laser fault injection (LFI) for around 100K USD. If there is no tilde, the number was taken directly from the referenced paper. • In case of ARM, we distinguish between a standalone chip and an embedded one. Generally, the non-remote techniques should be usable for both cases, however, the remote attack assumes a complex operating system (e.g. Linux). • In the first four categories, it is important to know in which component the attack happened. For example, an attack in the register would only have a very short time effect, the change in the SRAM would generally

•

4 The table was populated by crawling through the available works. If you have published a work that should be listed, please contact us and we will update the live version of the paper accessible at https://eprint.iacr.org/2022/301

VOLUME 10, 2022

<!-- PDF_PAGE: 6 -->

## PDF page 6

J. Breier, X. Hou: How Practical Are Fault Injection Attacks, Really?

have a longer effect (and can be used for example for a persistent fault analysis [5]), while the fault in the flash would affect the program itself. Below we provide the details for the affected device categories:

– AVR: [47] and [44] target the SRAM while [71] aims at the flash memory. – ARM (standalone): [14] targets the flash memory and [44] corrupts the registers. – ARM (embedded): [9] targets the registers. – FPGA: [72] and [73] attack the registers, and [74] causes the setup violations corrupting the processed data. The execution faults presented by [75] are also caused by setup violations.

A remote voltage glitch attack, Plundervolt [38], also achieved a certain bit flip fault models. However, the bits flipped could not be chosen by the attacker, only certain bits at specific locations could be flipped. • When the cost is indicated as ‘‘low’’, we mean that only a standard desktop PC (and in some cases, connection wires) are needed for the attack.

•

### IV. DISCUSSION A. COUNTERMEASURES

While the focus of this paper is not on countermeasures, the existence of those confirms that fault attacks constitute a threat against security-critical implementations. The follow- ing techniques have been proposed up to date:

Redundancy. Various usage of redundancy can be implemented to protect against different fault models. The most basic technique would be a duplication where the same circuit is deployed twice and there is an integrity check. In terms of software implementations, this can be achieved by running the same execution twice in series (or in parallel on multiple processors). A triplication with a majority voting can be used against more sophisticated attacks such as SIFA [85]. Intra- instruction redundancy was shown to be capable of pro- tecting against instruction skips [86]. Construction of various codes can be utilized for multiple bit corruptions within the same data [87]. Redundant hardware circuits were proposed to detect faults [88], [89]. • Sensors. Device-level sensors can be used to detect fault injections [90], [91]. Glitch detectors have been used to raise an alert when there is a sudden change in the EM field [92], [93]. Similar sensors have been shown to be efficient against laser fault injection [94]. In that direction, it is also possible to use various sensors to detect de-packaging of the chip – for example, a light sensor, or a simple wire mesh in the epoxy resin that becomes non conductive when the package is tampered with. • Algorithmic techniques. Another direction to thwart FIA is to propose an algorithm design that offers inherent fault detection. This is a relatively new area, started with a lightweight block cipher CRAFT [95], and

•

VOLUME 10, 2022

followed by an authenticated block cipher FRIET [96]. While the two above-mentioned ciphers relied on usage of coding theory, the most recent approach, a lightweight block cipher DEFAULT [97], utilized linear structures introduced in otherwise non-linear substitution compo- nents of the algorithm. Generally, this type of counter- measure seems to be getting traction as it offers a clear advantage of unburdening the implementer from dealing with the fault protection.

There are also other types of countermeasures that do not fall within these categories, such as infective techniques [98] or protocol-level countermeasures [99]. All of the countermeasures naturally introduce an over- head, either in power consumption, time, or space. It is there- fore necessary to conduct a risk assessment to be able to choose the right level of protection depending on the value of assets and potential threat vectors. From the attacker’s perspective, overcoming a particular countermeasure is a matter of resources. For example, a spa- tial duplication where the circuit is deployed twice, was bro- ken by a dual laser [100], where an identical fault was injected into both circuits. Similarly, a triplicated circuit would be vulnerable to three independent laser sources. Sensors can be overcome by using more precise equipment that bypasses the sensing range. Finally, algorithmic techniques can be defeated by using a different fault analysis method. For exam- ple, DEFAULT [97] provides protection against differential fault analysis, but can be broken by statistical ineffective fault attack.

B. FUTURE DIRECTIONS

There are several trends emerging in the recent literature that can be identified as the next directions in the area of fault injection techniques:

Techniques to break security enclaves. Very recent voltage attacks have been shown effective against secu- rity enclaves of both main PC processor manufacturers, Intel [27] and AMD [28]. ARM Trustzone was even broken by a remote attack manipulating the operating frequency [34], [35]. We believe this area will gain a serious traction in the next few years as the security implications of attacking PCs and smartphones are a concern for general public. • Low-cost fault injection techniques. As the fault injection is moving from academic environment and evaluation labs to hardware security enthusiasts and hackers, there is a push towards affordable fault injection techniques. EMFI [56], optical [44], and also voltage glitch [32] custom-made equipment can be built with standard components ranging in a few hundreds of dol- lars. It is expected that researchers will continue building inexpensive devices while tweaking their precision and ease-of-use. • Remote attacks. As shown in Table 1, remote attacks are missing for the majority of fault models and target

•

113127

<!-- PDF_PAGE: 7 -->

## PDF page 7

devices. Recent works, however, are starting to fill this gap. The most popular direction is the development of software-based fault attacks [34], [36], [37], [38]. Due to the attack method nature, among the techniques we describe here, only voltage/clock glitches and Rowham- mer are achievable remotely. Making it possible to remotely target some device with a fault attack creates a very potent threat as these attacks are rarely considered in the security risk assessment. Therefore, there is a strong motivation for researchers to find novel ways to disturb devices by faults remotely.

### V. CONCLUSION

In this paper we aimed at analyzing the practicality of fault injection attacks in a real world setting. For a target device and a desired fault model, we listed the method with the lowest cost from the literature. Additionally, we provided a short sur- vey on different fault injection techniques, listing the current state-of-the-art for each area. The results demonstrate that a reasonable amount of faults can be achieved with affordable cost for individual attackers and hence can be considered very practical.

### REFERENCES

[1] D. Boneh, R. A. DeMillo, and R. J. Lipton, ‘‘On the importance of checking cryptographic protocols for faults,’’ in Proc. Int. Conf. Theory Appl. Cryptograph. Techn. Berlin, Germany: Springer, 1997, pp. 37–51. [2] E. Biham and A. Shamir, ‘‘Differential fault analysis of secret key cryp- tosystems,’’ in Proc. Annu. Int. Cryptol. Conf. Berlin, Germany: Springer, 1997, pp. 513–525. [3] S. Mangard, E. Oswald, and T. Popp, Power Analysis Attacks: Revealing the Secrets of Smart Cards, vol. 31. Berlin, Germany: Springer, 2008. [4] C. Dobraunig, M. Eichlseder, T. Korak, S. Mangard, F. Mendel, and R. Primas, ‘‘SIFA: Exploiting ineffective fault inductions on symmetric cryptography,’’ in IACR Transactions on Cryptographic Hardware and Embedded Systems. Bochum, Germany: Ruhr-Universität Bochum, 2018, pp. 547–572. [5] F. Zhang, X. Lou, X. Zhao, S. Bhasin, W. He, R. Ding, S. Qureshi, and K. Ren, ‘‘Persistent fault analysis on block ciphers,’’ in IACR Trans- actions on Cryptographic Hardware and Embedded Systems. Bochum, Germany: Ruhr-Universität Bochum, 2018, pp. 150–172. [6] Y. Li, K. Sakiyama, S. Gomisawa, T. Fukunaga, J. Takahashi, and K. Ohta, ‘‘Fault sensitivity analysis,’’ in Proc. Int. Workshop Cryptograph. Hardw. Embedded Syst. Berlin, Germany: Springer, 2010, pp. 320–334. [7] S. Saha, A. Bag, D. Basu Roy, S. Patranabis, and D. Mukhopadhyay, ‘‘Fault template attacks on block ciphers exploiting fault propagation,’’ in Proc. Annu. Int. Conf. Theory Appl. Cryptograph. Techn. Berlin, Germany: Springer, 2020, pp. 612–643. [8] S. Patranabis, J. Breier, D. Mukhopadhyay, and S. Bhasin, ‘‘One plus one is more than two: A practical combination of power and fault analysis attacks on PRESENT and PRESENT-like block ciphers,’’ in Proc. Work- shop Fault Diagnosis Tolerance Cryptogr. (FDTC), Sep. 2017, pp. 25–32. [9] A. Vasselle, H. Thiebeauld, Q. Maouhoub, A. Morisset, and S. Ermeneux, ‘‘Laser-induced fault injection on smartphone bypassing the secure boot,’’ in Proc. Workshop Fault Diagnosis Tolerance Cryptogr. (FDTC), Sep. 2017, pp. 41–48. [10] A. Cui and R. Housley, ‘‘BADFET: Defeating modern secure boot using second-order pulsed electromagnetic fault injection,’’ in Proc. 11th USENIX Workshop Offensive Technol. (WOOT), 2017, pp. 1–12. [11] J. Breier, X. Hou, D. Jap, L. Ma, S. Bhasin, and Y. Liu, ‘‘Practical fault attack on deep neural networks,’’ in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., 2018, pp. 2204–2206. [12] J. Breier, D. Jap, X. Hou, S. Bhasin, and Y. Liu, ‘‘SNIFF: Reverse engineering of neural networks with fault attacks,’’ IEEE Trans. Rel., early access, Sep. 6, 2021, doi: 10.1109/TR.2021.3105697.

113128

J. Breier, X. Hou: How Practical Are Fault Injection Attacks, Really?

[13] C. Bozzato, R. Focardi, and F. Palmarini, ‘‘Shaping the glitch: Optimizing voltage fault injection attacks,’’ in IACR Transactions on Cryptographic Hardware and Embedded Systems. Bochum, Germany: Ruhr-Universität Bochum, 2019, pp. 199–224. [14] N. Moro, A. Dehbaoui, K. Heydemann, B. Robisson, and E. Encrenaz, ‘‘Electromagnetic fault injection: Towards a fault model on a 32-bit microcontroller,’’ in Proc. Workshop Fault Diagnosis Tolerance Cryptog- raphy, Aug. 2013, pp. 77–88. [15] J. Breier and D. Jap, ‘‘Testing feasibility of back-side laser fault injection on a microcontroller,’’ in Proc. WESS: Workshop Embedded Syst. Secur., Oct. 2015, pp. 1–6. [16] S. Anceau, P. Bleuet, J. Clédière, L. Maingault, J.-L. Rainard, and R. Tucoulou, ‘‘Nanofocused X-ray beam to reprogram secure circuits,’’ in Proc. Int. Conf. Cryptograph. Hardw. Embedded Syst. Berlin, Germany: Springer, 2017, pp. 175–188. [17] O. Mutlu and J. S. Kim, ‘‘RowHammer: A retrospective,’’ IEEE Trans. Comput.-Aided Design Integr. Circuits Syst., vol. 39, no. 8, pp. 1555–1571, Aug. 2019. [18] C. Giraud and H. Thiebeauld, ‘‘A survey on fault attacks,’’ in Smart Card Research and Advanced Applications VI. Berlin, Germany: Springer, 2004, pp. 159–176. [19] C. H. Kim and J.-J. Quisquater, ‘‘Faults, injection methods, and fault attacks,’’ IEEE Design Test Comput., vol. 24, no. 6, pp. 544–545, Nov. 2007. [20] A. Baksi, S. Bhasin, J. Breier, D. Jap, and D. Saha, ‘‘A survey on fault attacks on symmetric key cryptosystems,’’ ACM Comput. Surv., 2022. [21] M. Joye and M. Tunstall, Fault Analysis in Cryptography, vol. 147. Berlin, Germany: Springer, 2012. [22] J. Breier, X. Hou, and S. Bhasin, Automated Methods in Cryptographic Fault Analysis. Berlin, Germany: Springer, 2019. [23] M. Dumont, M. Lisart, and P. Maurine, ‘‘Electromagnetic fault injection: How faults occur,’’ in Proc. Workshop Fault Diagnosis Tolerance Cryp- togr. (FDTC), Aug. 2019, pp. 9–16. [24] C. Godlewski, V. Pouget, D. Lewis, and M. Lisart, ‘‘Electrical modeling of the effect of beam profile for pulsed laser fault injection,’’ Microelec- tron. Rel., vol. 49, nos. 9–11, pp. 1143–1147, Sep. 2009. [25] R. Kumar, P. Jovanovic, and I. Polian, ‘‘Precise fault-injections using voltage and temperature manipulation for differential cryptanalysis,’’ in Proc. IEEE 20th Int. On-Line Test. Symp. (IOLTS), Jul. 2014, pp. 43–48. [26] N. Selmane, S. Guilley, and J.-L. Danger, ‘‘Practical setup time violation attacks on AES,’’ in Proc. 7th Eur. Dependable Comput. Conf., May 2008, pp. 91–96. [27] Z. Chen, G. Vasilakis, K. Murdock, E. Dean, D. Oswald, and F. D. Garcia, ‘‘VoltPillager: Hardware-based fault injection attacks against Intel SGX Enclaves using the SVID voltage scaling interface,’’ in Proc. 30th USENIX Secur. Symp. (USENIX Secur.), 2021, pp. 699–716. [28] R. Buhren, H.-N. Jacob, T. Krachenfels, and J.-P. Seifert, ‘‘One glitch to rule them all: Fault injection attacks against AMD’s secure encrypted virtualization,’’ in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Nov. 2021, pp. 2875–2889. [29] D. Karaklajić, J.-M. Schmidt, and I. Verbauwhede, ‘‘Hardware designer’s guide to fault attacks,’’ IEEE Trans. Very Large Scale Integr. (VLSI) Syst., vol. 21, no. 12, pp. 2295–2306, Dec. 2013. [30] J. Balasch, B. Gierlichs, and I. Verbauwhede, ‘‘An in-depth and black-box characterization of the effects of clock glitches on 8-bit MCUs,’’ in Proc. Workshop Fault Diagnosis Tolerance Cryptogr., Sep. 2011, pp. 105–114. [31] S. Endo, T. Sugawara, N. Homma, T. Aoki, and A. Satoh, ‘‘An on-chip glitchy-clock generator for testing fault injection attacks,’’ J. Crypto- graph. Eng., vol. 1, no. 4, pp. 265–270, 2011. [32] L. Claudepierre, P.-Y. Péneau, D. Hardy, and E. Rohou, ‘‘TRAITOR: A low-cost evaluation platform for multifault injection,’’ in Proc. Int. Symp. Adv. Secur. Softw. Syst., May 2021, pp. 51–56. [33] S. Pinto and N. Santos, ‘‘Demystifying arm trustzone: A comprehensive survey,’’ ACM Comput. Surv., vol. 51, no. 6, pp. 1–36, 2019. [34] A. Tang, S. Sethumadhavan, and S. Stolfo, ‘‘CLKSCREW: Exposing the perils of security-oblivious energy management,’’ in Proc. 26th USENIX Secur. Symp. (USENIX Secur.), 2017, pp. 1057–1074. [35] P. Qiu, D. Wang, Y. Lyu, and G. Qu, ‘‘VoltJockey: Breaching trustzone by software-controlled voltage manipulation over multi-core frequen- cies,’’ in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., 2019, pp. 195–209.

VOLUME 10, 2022

<!-- PDF_PAGE: 8 -->

## PDF page 8

J. Breier, X. Hou: How Practical Are Fault Injection Attacks, Really?

[36] P. Qiu, D. Wang, Y. Lyu, R. Tian, C. Wang, and G. Qu, ‘‘VoltJockey: A new dynamic voltage scaling-based fault injection attack on Intel SGX,’’ IEEE Trans. Comput.-Aided Design Integr. Circuits Syst., vol. 40, no. 6, pp. 1130–1143, Jun. 2021. [37] Z. Kenjar, T. Frassetto, D. Gens, M. Franz, and A.-R. Sadeghi, ‘‘V0LTpwn: Attacking x86 processor integrity from software,’’ in Proc. 29th USENIX Secur. Symp. (USENIX Secur.), 2020, pp. 1445–1461. [38] K. Murdock, D. Oswald, F. D. Garcia, J. Van Bulck, D. Gruss, and F. Piessens, ‘‘Plundervolt: Software-based fault injection attacks against Intel SGX,’’ in Proc. IEEE Symp. Secur. Privacy (SP), May 2020, pp. 1466–1482. [39] D. H. Habing, ‘‘The use of lasers to simulate radiation-induced tran- sients in semiconductor devices and circuits,’’ IEEE Trans. Nucl. Sci., vol. NS-12, no. 5, pp. 91–100, Oct. 1965. [40] D. Binder, E. C. Smith, and A. B. Holman, ‘‘Satellite anomalies from galactic cosmic rays,’’ IEEE Trans. Nucl. Sci., vol. NS-22, no. 6, pp. 2675–2680, Dec. 1975. [41] S. P. Skorobogatov and R. J. Anderson, ‘‘Optical fault induction attacks,’’ in Proc. Int. Workshop Cryptograph. Hardw. Embedded Syst. Berlin, Germany: Springer, 2002, pp. 2–12. [42] S. Chef, C. T. Chua, J. Y. Tay, Y. W. Siah, S. Bhasin, J. Breier, and C. L. Gan, ‘‘Descrambling of embedded SRAM using a laser probe,’’ in Proc. IEEE Int. Symp. Phys. Failure Anal. Integr. Circuits (IPFA), Jul. 2018, pp. 1–6. [43] M. S. Kelly and K. Mayes, ‘‘High precision laser fault injection using low-cost components,’’ in Proc. IEEE Int. Symp. Hardw. Oriented Secur. Trust (HOST), Dec. 2020, pp. 219–228. [44] O. M. Guillen, M. Gruber, and F. D. Santis, ‘‘Low-cost setup for localized semi-invasive optical fault injection attacks,’’ in Proc. Int. Workshop Con- structive Side-Channel Anal. Secure Design. Berlin, Germany: Springer, 2017, pp. 207–222. [45] J. Breier and C.-N. Chen, ‘‘On determining optimal parameters for testing devices against laser fault attacks,’’ in Proc. Int. Symp. Integr. Circuits (ISIC), Dec. 2016, pp. 1–4. [46] J. Breier, W. He, S. Bhasin, D. Jap, S. Chef, H. G. Ong, and C. L. Gan, ‘‘Extensive laser fault injection profiling of 65 nm FPGA,’’ J. Hardw. Syst. Secur., vol. 1, no. 3, pp. 237–251, Sep. 2017. [47] M. Agoyan, J.-M. Dutertre, A.-P. Mirbaha, D. Naccache, A.-L. Ribotta, and A. Tria, ‘‘How to flip a bit?’’ in Proc. IEEE 16th Int. On-Line Test. Symp., Jul. 2010, pp. 235–239. [48] J. M. Soden and R. E. Anderson, ‘‘IC failure analysis: Techniques and tools for quality reliability improvement,’’ Proc. IEEE, vol. 81, no. 5, pp. 703–715, May 1993. [49] Y.-I. Hayashi, N. Homma, T. Sugawara, T. Mizuki, T. Aoki, and H. Sone, ‘‘Non-invasive EMI-based fault injection attack against cryptographic modules,’’ in Proc. IEEE Int. Symp. Electromagn. Compat., Aug. 2011, pp. 763–767. [50] J.-M. Schmidt and M. Hutter, ‘‘Optical and EM fault-attacks on CRT- based RSA: Concrete results,’’ in Proc. Austrochip, 15th Austrian Workhop Microelectron., Graz, Austria, Oct. 2007. [51] C. O’Flynn, ‘‘MINimum failure: EMFI attacks against USB stacks,’’ in Proc. 13th USENIX Workshop Offensive Technol. (WOOT), 2019, pp. 1–10. [52] R. Omarouayache, J. Raoult, S. Jarrix, L. Chusseau, and P. Maurine, ‘‘Magnetic microprobe design for EM fault attack,’’ in Proc. Int. Symp. Electromagn. Compat., Sep. 2013, pp. 949–954. [53] L. Sauvage, ‘‘Electric probes for fault injection attack,’’ in Proc. Asia–Pacific Symp. Electromagn. Compat. (APEMC), May 2013, pp. 1–4. [54] A. Beckers, M. Kinugawa, Y. Hayashi, D. Fujimoto, J. Balasch, B. Gierlichs, and I. Verbauwhede, ‘‘Design considerations for em pulse fault injection,’’ in Proc. Int. Conf. Smart Card Res. Adv. Appl. Berlin, Germany: Springer, 2019, pp. 176–192. [55] K. M. Abdellatif and O. Heriveaux, ‘‘SiliconToaster: A cheap and pro- grammable EM injector for extracting secrets,’’ in Proc. Workshop Fault Detection Tolerance Cryptogr. (FDTC), Sep. 2020, pp. 35–40. [56] S. Delarea and Y. Oren, ‘‘Practical, low-cost fault injection attacks on personal smart devices,’’ Appl. Sci., vol. 12, no. 1, p. 417, Jan. 2022. [57] Y. Kim, R. Daly, J. Kim, C. Fallin, J. H. Lee, D. Lee, C. Wilkerson, K. Lai, and O. Mutlu, ‘‘Flipping bits in memory without accessing them: An experimental study of DRAM disturbance errors,’’ ACM SIGARCH Comput. Archit. News, vol. 42, no. 3, pp. 361–372, 2014.

VOLUME 10, 2022

[58] J. A. Mandelman, R. H. Dennard, G. B. Bronner, J. K. DeBrosse, R. Divakaruni, Y. Li, and C. J. Radens, ‘‘Challenges and future direc- tions for the scaling of dynamic random-access memory (DRAM),’’ IBM J. Res. Develop., vol. 46, nos. 2–3, pp. 187–212, Mar. 2002. [59] Y. Konishi, M. Kumanoya, H. Yamasaki, K. Dosaka, and T. Yoshihara, ‘‘Analysis of coupling noise between adjacent bit lines in megabit DRAMs,’’ IEEE J. Solid-State Circuits, vol. 24, no. 1, pp. 35–42, Feb. 1989. [60] E. Bosman, K. Razavi, H. Bos, and C. Giuffrida, ‘‘Dedup est machina: Memory deduplication as an advanced exploitation vector,’’ in Proc. IEEE Symp. Secur. Privacy (SP), May 2016, pp. 987–1004. [61] D. Gruss, C. Maurice, and S. Mangard, ‘‘Rowhammer.js: A remote software-induced fault attack in Javascript,’’ in Proc. Int. Conf. Detec- tion Intrusions Malware, Vulnerability Assessment. Berlin, Germany: Springer, 2016, pp. 300–321. [62] M. Seaborn and T. Dullien, ‘‘Exploiting the DRAM rowhammer bug to gain kernel privileges,’’ Black Hat, vol. 15, p. 71, Mar. 2015. [63] M. Oliverio, K. Razavi, H. Bos, and C. Giuffrida, ‘‘Secure page fusion with VUsion: Https://www.vusec. net/projects/VUsion,’’ in Proc. 26th Symp. Operating Syst. Princ., 2017, pp. 531–545. [64] K. Razavi, B. Gras, E. Bosman, B. Preneel, C. Giuffrida, and H. Bos, ‘‘Flip Feng Shui: Hammering a needle in the software stack,’’ in Proc. 25th USENIX Secur. Symp. (USENIX Secur.), 2016, pp. 1–18. [65] Y. Xiao, X. Zhang, Y. Zhang, and R. Teodorescu, ‘‘One bit flips, one cloud flops: Cross-VM row Hammer attacks and privilege escalation,’’ in Proc. 25th USENIX Secur. Symp. (USENIX Secur.), 2016, pp. 19–35. [66] V. Van Der Veen, Y. Fratantonio, M. Lindorfer, D. Gruss, C. Maurice, G. Vigna, H. Bos, K. Razavi, and C. Giuffrida, ‘‘Drammer: Deterministic rowhammer attacks on mobile platforms,’’ in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., 2016, pp. 1675–1689. [67] P. Frigo, C. Giuffrida, H. Bos, and K. Razavi, ‘‘Grand pwning unit: Accelerating microarchitectural attacks with the GPU,’’ in Proc. IEEE Symp. Secur. Privacy (SP), May 2018, pp. 195–210. [68] Y. Cai, S. Ghose, Y. Luo, K. Mai, O. Mutlu, and E. F. Haratsch, ‘‘Vulnerabilities in MLC NAND flash memory programming: Experi- mental analysis, exploits, and mitigation techniques,’’ in Proc. IEEE Int. Symp. High Perform. Comput. Archit. (HPCA), Feb. 2017, pp. 49–60. [69] A. Kurmus, N. Ioannou, M. Neugschwandtner, N. Papandreou, and T. Parnell, ‘‘From random block corruption to privilege escalation: A filesystem attack vector for rowhammer-like attacks,’’ in Proc. 11th USENIX Workshop Offensive Technol. (WOOT), 2017, pp. 1–9. [70] A. Tatar, R. K. Konoth, E. Athanasopoulos, C. Giuffrida, H. Bos, and K. Razavi, ‘‘Throwhammer: Rowhammer attacks over the network and defenses,’’ in Proc. USENIX Annu. Tech. Conf. (USENIX ATC), 2018, pp. 213–226. [71] A. Beckers, J. Balasch, B. Gierlichs, I. Verbauwhede, S. Osuka, M. Kinugawa, D. Fujimoto, and Y. Hayashi, ‘‘Characterization of EM faults on ATmega328p,’’ in Proc. Joint Int. Symp. Electromagn. Compat., Sapporo Asia–Pacific Int. Symp. Electromagn. Compat. (EMC Sap- poro/APEMC), Jun. 2019, pp. 1–4. [72] W. He, J. Breier, S. Bhasin, D. Jap, H. G. Ong, and C. L. Gan, ‘‘Com- prehensive laser sensitivity profiling and data register bit-flips for crypto- graphic fault attacks in 65 nm FPGA,’’ in Proc. Int. Conf. Secur., Privacy, Appl. Cryptogr. Eng. Berlin, Germany: Springer, 2016, pp. 47–65. [73] S. Ordas, L. Guillaume-Sage, and P. Maurine, ‘‘Electromagnetic fault injection: The curse of flip-flops,’’ J. Cryptograph. Eng., vol. 7, no. 3, pp. 183–197, Sep. 2017. [74] F. Khelil, M. Hamdi, S. Guilley, J. L. Danger, and N. Selmane, ‘‘Fault analysis attack on an FPGA AES implementation,’’ in Proc. New Tech- nol., Mobility Secur., Nov. 2008, pp. 1–5. [75] M. M. Alam, S. Tajik, F. Ganji, M. Tehranipoor, and D. Forte, ‘‘RAM-jam: Remote temperature and voltage fault attack on FPGAs using memory collisions,’’ in Proc. Workshop Fault Diagnosis Tolerance Cryptography (FDTC), Aug. 2019, pp. 48–55. [76] M. Madau, M. Agoyan, J. Balasch, M. Grujic, P. Haddad, P. Maurine, V. Rozic, D. Singelee, B. Yang, and I. Verbauwhede, ‘‘The impact of pulsed electromagnetic fault injection on true random number genera- tors,’’ in Proc. Workshop Fault Diagnosis Tolerance Cryptogr. (FDTC), Sep. 2018, pp. 43–48. [77] A. S. Rakin, Z. He, J. Li, F. Yao, C. Chakrabarti, and D. Fan, ‘‘T-BFA: Targeted bit-flip adversarial weight attack,’’ IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 11, pp. 7928–7939, Nov. 2022.

113129

<!-- PDF_PAGE: 9 -->

## PDF page 9

[78] R. Korkikian, S. Pelissier, and D. Naccache, ‘‘Blind fault attack against SPN ciphers,’’ in Proc. Workshop Fault Diagnosis Tolerance Cryptogr., Sep. 2014, pp. 94–103. [79] C. Giraud, ‘‘DFA on AES,’’ in Proc. Int. Conf. Adv. Encryption Standard. Berlin, Germany: Springer, 2004, pp. 27–41. [80] P. Luo, Y. Fei, L. Zhang, and A. A. Ding, ‘‘Differential fault analysis of SHA3-224 and SHA3-256,’’ in Proc. Workshop Fault Diagnosis Toler- ance Cryptogr. (FDTC), Aug. 2016, pp. 4–15. [81] N. Timmers and C. Mune, ‘‘Escalating privileges in Linux using voltage fault injection,’’ in Proc. Workshop Fault Diagnosis Tolerance Cryptogr. (FDTC), Sep. 2017, pp. 1–8. [82] J. Breier, D. Jap, and C.-N. Chen, ‘‘Laser profiling for the back-side fault attacks: With a practical laser skip instruction attack on AES,’’ in Proc. 1st ACM Workshop Cyber-Phys. Syst. Secur., 2015, pp. 99–103. [83] X. Hou, J. Breier, D. Jap, L. Ma, S. Bhasin, and Y. Liu, ‘‘Physical security of deep learning on edge devices: Comprehensive evaluation of fault injection attack vectors,’’ Microelectron. Rel., vol. 120, May 2021, Art. no. 114116. [84] S. Tajik, H. Lohrke, F. Ganji, J.-P. Seifert, and C. Boit, ‘‘Laser fault attack on physically unclonable functions,’’ in Proc. Workshop Fault Diagnosis Tolerance Cryptogr. (FDTC), Sep. 2015, pp. 85–96. [85] J. Breier, M. Khairallah, X. Hou, and Y. Liu, ‘‘A countermeasure against statistical ineffective fault analysis,’’ IEEE Trans. Circuits Syst. II, Exp. Briefs, vol. 67, no. 12, pp. 3322–3326, Dec. 2020. [86] C. Patrick, B. Yuce, N. F. Ghalaty, and P. Schaumont, ‘‘Lightweight fault attack resistance in software using intra-instruction redundancy,’’ in Proc. Int. Conf. Sel. Areas Cryptogr. Berlin, Germany: Springer, 2016, pp. 231–244. [87] J. Breier, X. Hou, and Y. Liu, ‘‘On evaluating fault resilient encoding schemes in software,’’ IEEE Trans. Dependable Secure Comput., vol. 18, no. 3, pp. 1065–1079, May 2021. [88] T. Schneider, A. Moradi, and T. Güneysu, ‘‘ParTI—Towards com- bined hardware countermeasures against side-channel and fault-injection attacks,’’ in Proc. Annu. Int. Cryptol. Conf. Berlin, Germany: Springer, 2016, pp. 302–332. [89] A. Aghaie, A. Moradi, S. Rasoolzadeh, A. R. Shahmirzadi, F. Schellenberg, and T. Schneider, ‘‘Impeccable circuits,’’ IEEE Trans. Comput., vol. 69, no. 3, pp. 361–376, Mar. 2020. [90] R. P. Bastos, F. S. Torres, J.-M. Dutertre, M.-L. Flottes, G. Di Natale, and B. Rouzeyre, ‘‘A bulk built-in sensor for detection of fault attacks,’’ in Proc. IEEE Int. Symp. Hardw.-Oriented Secur. Trust (HOST), Jun. 2013, pp. 51–54. [91] M. T. H. Anik, J. Danger, S. Guilley, and N. Karimi, ‘‘Detecting failures and attacks via digital sensors,’’ IEEE Trans. Comput.-Aided Design Integr. Circuits Syst., vol. 40, no. 7, pp. 1315–1326, Jul. 2021. [92] L. Zussa, A. Dehbaoui, K. Tobich, J.-M. Dutertre, P. Maurine, L. Guillaume-Sage, J. Clediere, and A. Tria, ‘‘Efficiency of a glitch detector against electromagnetic fault injection,’’ in Proc. Design, Autom. Test Eur. Conf. Exhib. (DATE), 2014, pp. 1–6. [93] J. Breier, S. Bhasin, and W. He, ‘‘An electromagnetic fault injection sensor using hogge phase-detector,’’ in Proc. 18th Int. Symp. Quality Electron. Design (ISQED), Mar. 2017, pp. 307–312. [94] W. He, J. Breier, and S. Bhasin, ‘‘Cheap and cheerful: A low-cost digital sensor for detecting laser fault injection attacks,’’ in Proc. Int. Conf. Secur., Privacy, Appl. Cryptogr. Eng. Berlin, Germany: Springer, 2016, pp. 27–46.

113130

J. Breier, X. Hou: How Practical Are Fault Injection Attacks, Really?

[95] B. Christof, ‘‘CRAFT: Lightweight tweakable block cipher with effi- cient protection against DFA Attacks,’’ IACR Trans. Symmetric Cryptol., vol. 2019, no. 1, pp. 5–45, 2019. [96] T. Simon, L. Batina, J. Daemen, V. Grosso, P. M. C. Massolino, K. Papagiannopoulos, F. Regazzoni, and N. Samwel, ‘‘FRIET: An authen- ticated encryption scheme with built-in fault detection,’’ in Proc. Annu. Int. Conf. Theory Appl. Cryptograph. Techn. Berlin, Germany: Springer, 2020, pp. 581–611. [97] A. Baksi, S. Bhasin, J. Breier, M. Khairallah, T. Peyrin, S. Sarkar, and S. M. Sim, ‘‘DEFAULT: Cipher-level resistance against differential fault attack,’’ in Proc. Int. Conf. Theory Appl. Cryptol. Inf. Secur. Berlin, Germany: Springer, 2021, pp. 124–156. [98] S. Patranabis, A. Chakraborty, and D. Mukhopadhyay, ‘‘Fault tolerant infective countermeasure for AES,’’ in Proc. Int. Conf. Secur., Privacy, Appl. Cryptogr. Eng. Berlin, Germany: Springer, 2015, pp. 190–209. [99] A. Baksi, S. Bhasin, J. Breier, M. Khairallah, and T. Peyrin, ‘‘Protecting block ciphers against differential fault attacks without re-keying,’’ in Proc. IEEE Int. Symp. Hardw. Oriented Secur. Trust (HOST), Apr. 2018, pp. 191–194. [100] B. Selmke, J. Heyszl, and G. Sigl, ‘‘Attack on a DFA protected AES by simultaneous laser fault injections,’’ in Proc. Workshop Fault Diagnosis Tolerance Cryptogr. (FDTC), Aug. 2016, pp. 36–46.

JAKUB BREIER received the bachelor’s degree in informatics from the Slovak University of Tech- nology (STU), Slovakia, in 2008, the master’s degree in information technology security from Masaryk University, Czech Republic, in 2010, and the Ph.D. degree in applied informatics from (STU), in 2013. He is currently a Senior Researcher in embedded security with the Silicon Austria Laboratories, Graz, Austria. His research interests include fault and side-channel analysis methods and countermeasures, advanced fault injection techniques, and deep-learning security.

XIAOLU HOU received the Ph.D. degree in math- ematics from Nanyang Technological University (NTU), Singapore, in 2017. She is currently an Assistant Professor with the Faculty of Informat- ics and Information Technologies, Slovak Uni- versity of Technology, Slovakia. Her work has been published at top venues within various fields, ranging from mathematics to computer security. Her research interests include hardware security of cryptographic implementations and neural net- works. She designs and develops novel attacks and protection techniques on protocol, hardware, and software levels.

VOLUME 10, 2022
