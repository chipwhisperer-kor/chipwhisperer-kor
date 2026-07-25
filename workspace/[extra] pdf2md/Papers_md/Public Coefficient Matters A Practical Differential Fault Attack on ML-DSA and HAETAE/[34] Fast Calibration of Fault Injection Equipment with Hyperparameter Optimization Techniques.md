# [34] Fast Calibration of Fault Injection Equipment with Hyperparameter Optimization Techniques

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 18
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-34"
derived_asset_id: "PCM-DFA-REF-34-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[34] Fast Calibration of Fault Injection Equipment with Hyperparameter Optimization Techniques.pdf"
source_sha256: "2ef4ebd9a3f1f16da2b33f526d77a6d3390633d7786355294cff50aa7448f34a"
pages: 18
bbox_words: 6932
consumed_bbox_words: 6932
numeric_tokens: 455
consumed_numeric_tokens: 455
source_blocks: 203
consumed_source_blocks: 203
emitted_blocks: 172
embedded_raster_images: 2
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

Fast Calibration of Fault Injection Equipment with Hyperparameter Optimization Techniques

Vincent Werner 1,2( B ) , Laurent Maingault 1 , and Marie-Laure Potet 2

1

Univ. Grenoble Alpes, CEA, LETI, DSYS, CESTI, 38000 Grenoble, France {vincent.werner,laurent.maingault}@cea.fr 2 Univ. Grenoble Alpes, CNRS, VERIMAG, 38000 Grenoble, France {vincent.werner,marie-laure.potet}@univ-grenoble-alpes.fr

Abstract. Although fault injection is a powerful technique to exploit implementation weaknesses, this is not without limitations. An impor- tant preliminary step, based on rigorous calibration of the fault injection equipment, greatly aﬀects the exploitability and repeatability of injected faults. The equipment parameter space is usually explored with ran- dom search, grid search, and more recently with the help of metaheuris- tic algorithms. In this article, we apply, for the ﬁrst time, two recent hyperparameter optimization techniques to fault injection. We evaluate these optimization techniques on three diﬀerent 32-bit microcontrollers, and ﬁnd better glitch waveforms than with metaheuristic algorithms. In addition, we propose a two-stage optimization strategy under black-box conditions to reduce the dimensionality of the parameter space and speed up the equipment calibration. Finally, we apply this approach to bypass the code read protection of a built-in bootloader faster than with genetic algorithms.

Keywords: Fault injection · Voltage glitch · Parameter optimization

1 Introduction

Fault injection is a powerful technique to bypass security features of embedded systems, such as code protection mechanisms [8,15,26]. Using electrical glitches [2], focused light [31], electromagnetic pulses [13] or even nanofocused X-rays [1], one can locally perturb the chip environment to alter its behavior and gain access to critical information. Although fault injection can lead to impressive results, this is not without limitation. One of the biggest challenges is the calibration of fault injection equipment. Each fault injection equipment has multiple speciﬁc parameters that must be adjusted precisely, such as the positions x, y, z of an

This work is supported by the French National Research Agency in the framework of the “Investissements d’avenir” program (ANR-15-IDEX-02 and ANR-10-AIRT-05).

c Springer Nature Switzerland AG 2022 V. Grosso and T. Pöppelmann (Eds.): CARDIS 2021, LNCS 13173, pp. 121–138, 2022. https://doi.org/10.1007/978-3-030-97348-3 _ 7

<!-- PDF_PAGE: 2 -->

## PDF page 2

122 V. Werner et al.

electromagnetic probe tip. This preliminary calibration step is required in order to ﬁnd exploitable and repeatable faults. The parameter space is often too large to be entirely covered manually dur- ing time-constrained security evaluation. The most commonly-used methods to explore the parameter space are Grid Search (GS) and Random Search (RS). GS is a semi-exhaustive search on a predetermined and progressively reﬁned range of values. Although GS is eﬀective with small parameter space, this technique is ineﬃcient to explore a high dimensional parameter space, as the number of eval- uated conﬁgurations increases exponentially with the number of parameters con- sidered. Even though RS is slightly better than GS for exploring large parameter space [6], both GS and RS select next conﬁgurations to evaluate independently of the previous results, thus, many evaluations are wasted on poorly-performing conﬁgurations. Several approaches have been proposed to reduce the time spent on the equip- ment calibration, using more complex optimization techniques, such as meta- heuristic algorithms. However, genetic and memetic algorithms are inherently chaotic and can suﬀer from premature convergence [19]. Accordingly, Bayesian and Bandit Optimization techniques are typically preferred over metaheuris- tic algorithms to optimize hard combinatorial problem solvers [16] or machine learning models [20]. To the best of our knowledge, such techniques have not been considered for fault injection yet. Therefore, in this article, we propose applying two eﬃcient hyperparameter optimization techniques, so as to simplify and speed up the calibration of a fault injection equipment for a given target microcontroller. In addition, we also propose an optimization strategy to reduce the dimensionality of the parameter space in order to speed up even more the equipment calibration. To sum up, our contribution is threefold:

– We apply for the ﬁrst time two hyperparameter optimization techniques, Successive Halving Algorithm (SHA) and Sequential Model-based Algorithm Conﬁguration (SMAC), to ﬁnd the best settings and induce repeatable and exploitable faults with our voltage fault injection (VFI) setup, on three dif- ferent 32-bit microcontrollers. – We propose breaking down the optimization problem into two stages, so as to simplify but also to speed up the equipment calibration; ﬁrst, 1) during the Calibration stage, we focus on fault injection parameters only, using fault characterization tests, which are small programs running on the target device, designed to maximize fault propagation, and then, once the best conﬁgura- tions are identiﬁed, 2) during the Exploitation stage, we ﬁnd the fault injection timing to exploit vulnerabilities on the target application. – Using this strategy and SMAC, we successfully bypass the code protection mechanism of a built-in bootloader. Moreover, SMAC reduces the equipment calibration time by half compared to Genetic Algorithm (GA).

The outline of the rest of the article is as follows. After an overview of the related work to overcome the limitations of GS and RS in Sect. 2, we compre- hensively explain our fault injection optimization strategy in Sect. 3. In Sect. 4,

<!-- PDF_PAGE: 3 -->

## PDF page 3

Fast Calibration of Fault Injection Equipment 123

we detail SHA and SMAC optimization techniques, which are used for equip- ment calibration. In Sect. 5, to evaluate the performance of these optimization techniques, we calibrate our VFI setup for three diﬀerent microcontrollers using SHA, SMAC, GA and RS. Finally, in Sect. 6, we apply our fault injection strategy using SMAC to bypass a read protection mechanism on a 32-bit microcontroller faster than with GA.

2 Related Work

Parameter optimization has recently gained in popularity in the fault injection community. Diﬀerent approaches have been proposed to speed up the equipment calibration step. When possible, reducing the parameter space by identifying the regions of interest helps considerably. For example, using a scanning electron microscope, Courbon et al. [12] ﬁnd the most sensitive areas of the die to focus with Laser Fault Injection (LFI). Similarly, Schellenberg et al. [30] measure the optical beam induced current, as imaging technique, in order to localize ﬂip- ﬂops of an hardware AES accelerator. Madau et al. [23] propose to acquire EM emission traces, so as to detect EM hotspots and reduce the parameter space of EM Fault Injection (EMFI) equipment. Finally, to reduce the dimensionality of the problem, Carpi et al. [10] split the optimization problem into two stages, one focusing on voltage parameters and the other one on proper timing. Note that Picek et al. [28] also mention this approach, without further evaluating this idea. Another way to ﬁnd the best settings faster is to use better optimization algorithms than RS or GS. GA is a popular metaheuristic algorithm based on the evolutionary theory, which has been applied to EMFI [24] but also VFI [8,10,28] to ﬁnd the best conﬁgurations. Picek et al. [27] use Memetic algorithm, which is an extension of the traditional GA with a local search technique, also to explore more eﬃciently the VFI parameter space. More recently, Wu et al. [35] have proposed a characterization method for LFI setups based on deep learning to tune the pulse width and the power of the laser.

Table 1. Comparison of the related work according to the optimization technique, the dimension reduction of the parameter space, and the fault injection technique.

Optimization technique Dimension reduction FI technique

Related work

Our contribution Bandit optimization Bayesian optimization

[27]

Memetic algorithm

[24]

Genetic algorithm

[8, 28]

Genetic algorithm

[10]

Genetic algorithm

[35]

Deep learning

[23]

Grid search

[12, 30]

Grid search

✓

VFI

✗

VFI

✗

EMFI

✗

VFI

✓

VFI

✗

LFI

✓

EMFI

✓

LFI

<!-- PDF_PAGE: 4 -->

## PDF page 4

124 V. Werner et al.

Nevertheless, the main limitation of metaheuristic algorithms is the introduc- tion of additional hyperparameters that must be conﬁgured, such as the size of the population, the mutation rate, or the ﬁtness function. Moreover, depending on the optimization problem, metaheuristic algorithms can suﬀer from premature convergence. Similarly, ﬁnding the right number of hidden layers and neurons of the deep neural network is tedious. More eﬃcient optimization techniques have been proposed over the past decade, such as Bayesian optimization or Bandit optimization. Although already used for hyperparameter optimization of machine learning algorithms, these techniques have never been applied to fault injection. Accordingly, we propose for the ﬁrst time to apply SMAC (Bayesian optimization) and SHA (Bandit optimization) to improve the calibration of fault injection equipment. Moreover, we also reduce the dimensionality of the parameter space by splitting the opti- mization in two stages, but unlike [10], we decide to use fault characterization tests to ﬁnd the best conﬁgurations.

Fault Injection Optimization Approach

3

In this section, we detail our general approach for fault injection optimization. This strategy aims to reduce the time spent on searching for the best equipment settings, by reducing the dimensionality of the parameter space. Speeding up the parameter space exploration is particularly important as security evaluations are often time-constrained.

### 3.1 Common Approach

The most common strategy to optimize fault injection consists to calibrate the fault injection equipment directly with the target application. But for large applications, identifying the critical sections, that can potentially lead to vulner- abilities, is tedious, therefore, it is nearly impossible during a black-box, time- constrained, security evaluation to ﬁnd the right equipment settings and the right timing to inject the fault. In addition, the lack of feedback for some application further complicates the equipment calibration [33], and signiﬁcantly increases the amount of work required.

### 3.2 Our Approach

In an eﬀort to tackle these issues, we propose reducing the dimensionality of the parameter space by breaking down the problem of fault injection optimization into two stages, so as to simplify and speed up the parameter space exploration. First, 1) the Calibration stage optimizes the equipment calibration independently of the target application, using fault characterization tests and then, 2) the Exploitation stage ﬁnds the right timing to inject a fault in order to exploit a vulnerability on the target application. Figure 1 presents our fault injection optimization strategy.

<!-- PDF_PAGE: 5 -->

## PDF page 5

Fast Calibration of Fault Injection Equipment 125

Fault Probability. During the calibration stage, only faults resulting in a faulty output are considered as eﬀective, while faults resulting in a crash, a timeout or a normal output are not taken into account. The fault probability is used as a metric to compare performance between conﬁgurations. The fault probability of #{faulty results} a conﬁguration is given by #{fault injected} for this conﬁguration.

Fault Characterization Test. The fault characterization test, is not the tar- get application itself, but rather a series of instructions, arranged in such a way as to maximize the number of eﬀective faults on the target microcontroller, in order to quickly ﬁnd the settings with the highest fault probability. Fault char- acterization tests have been already applied to highlight fault eﬀects on various microcontrollers with diﬀerent fault injection techniques [4,11,14,25,29,32,34]. The main advantage of using a fault characterization test is that we can com- pletely ignore the injection timing during the optimization of our setup for the target microcontroller, which helps the exploration of the parameter space. In addition, a characterization test is often smaller than the target application, reducing the time required in the long run. Furthermore, a fault characteriza- tion test simpliﬁes the equipment calibration by giving instant feedback on the eﬀectiveness of the fault injection parameters, in comparison with an equipment calibration directly with black-box applications [33].

Equipment Parameter Space

Calibration Stage

Best Equipment Setting

Exploitation Stage

Target Microcontroller Fault Characterization Test

Fault Injection Equipment

SMAC / SHA

Target Microcontroller Target Application

RS / GS

Fault Injection Equipment

Successful Attack

Fig. 1. Overview of our fault injection optimization strategy.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 5]

Optimization Techniques. We use diﬀerent optimization techniques for each step of our approach. During the calibration stage, we use hyperparameter opti- mization techniques such as SMAC or SHA, to quickly explore the equipment parameter space, way faster than with GS or RS (due to the curse of dimen- sionality [5]). Then, once the best settings are identiﬁed, the right timing to inject the fault can be found with a simple random/grid search on the target application during the exploitation stage.

<!-- PDF_PAGE: 6 -->

## PDF page 6

126 V. Werner et al.

Hyperparameter Optimization Techniques

4

In this section, we comprehensively explain the two hyperparameter optimization techniques, SHA and SMAC, which are used to improve the convergence speed towards the best fault injection settings during the calibration stage.

Parameter Space and Equipment Configuration

4.1

The parameter space Θ depends on the fault injection technique and the setup used. For example, our VFI setup has 9 free parameters deﬁning the glitch waveform (8 voltage levels and the glitch duration, more detailed information is provided in Sect. 5.2, Fig. 2). Each conﬁguration θ ∈ Θ describes how to adjust each parameter of the given fault injection equipment (e.g. the positions x, y, z of an electromagnetic probe tip). Depending on the number of equipment con- ﬁgurations possible within the parameter space, and the target microcontroller, the complexity of the search will vary. SHA or SMAC can signiﬁcantly help to reduce the time spent identifying conﬁgurations that induce exploitable faults.

### 4.2 Successive Halving Algorithm

SHA has been originally proposed by Karnin et al.[18] to solve multi-armed bandits problems, but it can also be applied for hyperparameter optimization [36]. The main purpose of the algorithm (Algorithm 1) is to identify the best arm correctly (the best conﬁguration) within a ﬁxed budget T , that is a limited amount of time or resources (e.g. the total number of fault injections). The total budget is evenly allocated across log 2 (n) elimination rounds, where n is the number of initial conﬁguration instances Θ 0 . The algorithm evaluates the conﬁgurations in a uniform manner. At the end of each round, the worst ones

Algorithm 1: Successive Halving Algorithm

Input: Total budget T , fault injection parameter space Θ, n initial conﬁguration 0 ⊂ Θ instances Θ Θ log 2 (n) Output: Optimized conﬁguration θ inc ∈

for r = 0 to log 2 (n) − 1 do

T r |log (n) | Θ 2

t r ←

;

Θ r do foreach θ i ∈ Test t r times each conﬁguration θ i ; Compute the empirical mean μ r,i of θ i ;

r |/2; k r ← | Θ /* Keep the k r th best θ i with the largest μ r,i */ Θ r+1 ← BestKthConfigurations( Θ r , k r );

return θ inc ∈ Θ log 2 (n) ;

<!-- PDF_PAGE: 7 -->

## PDF page 7

Fast Calibration of Fault Injection Equipment 127

are eliminated. Then, on each successive round, the remaining conﬁgurations are evaluated twice as much as the previous round, and the process repeats until only one remains. The main concern is, for a ﬁxed budget T , whether to consider many conﬁg- urations (large n) with smaller number of trials for each (t r ); or a small number of conﬁgurations (small n) with larger number of trials for each (t r ). A solution, proposed by Aziz [3], is to take a budget T = n log 2 (n), resulting in an aggressive selection of conﬁgurations after just a single shot (⇒ t r = 1) in the ﬁrst round. Although only a conjecture has been presented to give an upper bound on the simple regret, the particular parameterization T = n log 2 (n) of the Algorithm 1 is better empirically than more complex solutions, also based on SHA, such as HyperBand [20].

Sequential Model-Based Algorithm Configuration

4.3

SMAC, proposed by Hutter et al. [16], is a general framework for Sequen- tial Model-Based Optimization (SMBO), also known as Bayesian Optimiza- tion. SMAC has been successfully applied for hyperparameter optimization of hard combinatorial problem solvers and various machine learning algorithms. Contrary to classical Bayesian-based approaches, SMAC supports all types of parameters, including continuous, discrete, categorical, but can also handle non- deterministic processes which is a key feature to optimize fault injection parame- ters. In Sect. 4, we will see that SMAC outperforms common approaches used to optimize the fault injection equipment. In the following, we explain the SMAC algorithm in detail.

Sequential Model-Based Optimization. Unlike previous approaches, SMBO keeps track of past results to ﬁt iteratively a probabilistic model, in order to select the next fault injection conﬁgurations which could potentially maximize the number of eﬀective faults on the target microcontroller. SMBO, as detailed in Algorithm 2, is structured around two key components, a probabilistic model and a selection function, also called the surrogate model and the acquisition function respectively. The probabilistic model M is ﬁtted (FitModel) to previous results R = {(θ 1 , o 1 ), ..., (θ n , o n )} where θ i is a possible conﬁguration of the fault injection equipment, and o i is the observed fault prob- ability with conﬁguration θ i . The model aims to predict the fault probability o i+1 of a new conﬁguration θ i+1 to determine if θ i+1 is worth being evaluated. new are selected from the fault injection parameter The new conﬁgurations Θ space Θ by the acquisition function (SelectConfigurations) which keeps bal- ance between exploitation (sampling where the model predicts the highest fault probability) and exploration (sampling where the model has no prior distribu- tion). On top of that, SMBO adds an intensiﬁcation mechanism (Intensify), which determines 1) the budget allocated for each conﬁguration θ i and 2) the best known conﬁguration so far θ inc [16]. SMAC uses Random Forests (RF) as a surrogate model instead of more commonly-used Gaussian process models, which explains how SMAC supports

<!-- PDF_PAGE: 8 -->

## PDF page 8

128 V. Werner et al.

Algorithm 2: Sequential Model-Based Optimization

Input: Total budget T , fault injection parameter space Θ, initial conﬁguration instances Θ init ⊂ Θ Output: Optimized parameter conﬁguration θ inc init ); R, θ inc ← Initialize( Θ repeat /* Fit the model M based on results R */ M ← FitModel(R); new */ /* Select promising configurations Θ Θ new ← SelectConfigurations(M, Θ); /* Find the best configuration θ inc */ Θ new ); R, θ inc ← Intensify(θ inc , until total budget T is exhausted ; return θ inc ;

discrete and categorical parameters. RF [9] is an ensemble method that grows many individual decision trees, which together, can be used to solve both clas- siﬁcation and regression problems. For the latter, decision trees take continuous values (e.g. fault probability) rather than class labels at their leaves (also called regression trees). SMAC estimates the performance (fault probability) mean μ θ and variance σ θ 2 for a new conﬁguration θ by computing the empirical mean and variance of the individual regression trees prediction of the RF. By default, and to maintain a low computational cost, SMAC builds B = 10 regression trees with a maximum depth of 20. Each tree is grown to the largest extent possible, based on a training set of n results sampled at random with replacement from the previous results R (also called bagging). Then, at each node, m features (e.g. fault injection parameters) are randomly selected from the initial features, and the one minimizing the reduced squared sum loss among the training set is chosen to split the node. Finally, the acquisition function of SMAC is based on Expected Improvement (EI), which is used to quantify how much a new conﬁguration θ should improve performance (fault probability) over our current optimum θ inc . Formally, the improvement I(θ) = max(f (θ inc ) − f (θ), 0) compares the performance between the new conﬁguration θ with the best known conﬁguration so far θ inc . As the objective function f is unknown, EI is computed instead using the posterior distribution of θ given the predictive mean μ θ and variance σ θ 2 obtained with RF and the empirical mean performance f θ inc of the best conﬁguration seen so far [16,17]. Next, the new conﬁgurations which yield to the highest expected improvement are selected and evaluated.

Initial Configuration Instances. One main limitation of SMAC is that initial conditions can greatly aﬀect the convergence speed, thus we propose our addi- tional two-step procedure to select the initial conﬁguration instances to better calibrate a given fault injection equipment. Without at least one conﬁguration

<!-- PDF_PAGE: 9 -->

## PDF page 9

Fast Calibration of Fault Injection Equipment 129

in Θ init which induces an eﬀective fault, SMAC struggles to identify the best settings. This procedure ensures that we do not start SMAC without at least one working conﬁguration.

– Pure exploration: conﬁgurations θ ∈ Θ are sampled at random and tested until 1) at least k min conﬁgurations that generate an eﬀective fault have been found, and 2) n min faults have been injected. By default, k min = 1 and n min = 1000. – Mutation: the set Θ init of initial conﬁguration instances includes at least the k min conﬁgurations identiﬁed during the pure exploration step, and addi- tional conﬁgurations generated with a gaussian mutation operator [7] using init | = k init conﬁgurations. the conﬁgurations found so far, so as to reach | Θ By default, k init = 100.

Based on the target microcontroller, k min , n min and k init can be adjusted. For example, SMAC may struggle with some secure microcontrollers. Extending the pure exploration phase (i.e. k min &gt; 1 and n min &gt; 1000) can signiﬁcantly help SMAC in early stages, especially when only a few conﬁgurations induce eﬀective faults.

Equipment Calibration with Diﬀerent Microcontrollers

5

In this section, we optimize our VFI setup for three diﬀerent 32-bit microcon- trollers, using SMAC, SHA, GA and RS. In these experiments, SMAC outper- forms other optimization techniques and consistently identiﬁes the best settings for our VFI setup. First, we present the target microcontrollers and general infor- mation about the experiments. Then, we detail our VFI setup and the parameter space associated. Afterwards, we compare the performance (fault probability and convergence speed) of SMAC and SHA with more commonly-used techniques, such as GA and RS.

### 5.1 Target Microcontrollers

We have selected three diﬀerent 32-bit microcontrollers, based on diﬀerent Cortex-M cores. The die of these microcontrollers are diﬀerent, thus, they will not react the same way to voltage fault injections. Therefore, the best settings for our VFI setup will be diﬀerent for each microcontroller. The selected micro- controllers are:

– µC-M0 is a Cortex M0+ running at 24 Mhz, based on the ARMv6-M archi- tecture with 2 stages pipeline. – µC-M3 is a mainstream microcontroller based on the Cortex M3 running at 24Mhz, which implements the ARMv7-M architecture with 3 stages pipeline. – µC-M4 is ultra-low-power microcontroller based on the Cortex M4, running at 72Mhz. The core is based on the ARMv7E-M architecture with 3 stages pipeline and branch speculation.

<!-- PDF_PAGE: 10 -->

## PDF page 10

130 V. Werner et al.

### 5.2 Setup

General Information. During the Calibration Stage (Fig. 1), we use the fault characterization test detailed in Table 2. This test has been designed to maxi- mize the propagation of bit-set or bit-reset on the fetched instruction, but also instruction skips (not detailed in this study). For each optimization technique (SMAC, SHA, GA and RS), we inject 50,000 faults (≈ 6 h). For SMAC, we use the Python library SMACv3 [21], and more precisely the class SMAC4HPO. For SHA, GA and RS, we do not use an external library. For SHA, as described in Sect. 3, we use the parameterization T = n log 2 (n), with n = 4096. For GA, each individual of the population represents a valid conﬁguration of the fault injection equipment considered. We train a population of 50 individuals over 200 generations, where each individual is tested ﬁve times. In addition, we use a gaussian mutation operator [7], a roulette-wheel selection via stochastic acceptance [22] and the ﬁtness of an individual is given by its fault probability. For RS, we evaluate 10,000 conﬁgurations, where each conﬁguration is tested ﬁve times. In the following, we detail our VFI setup and its associated parameter space.

Table 2. Instruction Corruption (IC) Test for the ARMv7-M instruction set, as well as the initial values of registers.

Voltage Fault Injection Setup. Our VFI setup is similar to the Bozzato et al. [8] test bench. We use a custom 30 MSps Digital-to-Analog Converter (DAC) to generate arbitrary glitch waveforms instead of an external arbitrary waveform generator. The DAC is a simple R-2R ladder with 8-bit resolution, which converts digital input byte into analog output voltage. The glitch waveform, sent to the DAC, is generated with a function that takes a set of 8 instantaneous voltage levels, that are then interpolated with cubic interpolation on a grid, up to 2048- by-256, that depends on the waveform size requested. This setup is cheap (≈ 100$) and yet oﬀers great versatility to adapt to diﬀerent targets with the ability to generate a large spectrum of glitch waveforms ([8]).

<!-- PDF_PAGE: 11 -->

## PDF page 11

Fast Calibration of Fault Injection Equipment 131

However, the versatility comes at a price, as the parameter space of our VFI setup, presented in Fig. 2, is larger than those of more commonly-used VFI setups. Indeed, most of the time, only two parameters are used (glitch duration and glitch amplitude), while our setup has 9 free parameters (8 voltage levels and the glitch duration). Therefore, our VFI setup is a good candidate to evaluate the relevance of SMAC and SHA optimization techniques.

Fig. 2. VFI parameter space, ≈ 10 18 conﬁgurations. The glitch waveform is deﬁned with 8 voltage levels (x 0 ...x 7 ) and the duration.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 11]

### 5.3 Experimental Protocol

The results of the fault injection optimization with SMAC, SHA, GA and RS are heterogeneous. While SMAC and SHA, by design, return a single conﬁguration (the best found), RS and GA return several conﬁgurations. Indeed, SMAC and SHA progressively increase the number of test to better approximate the fault probability in order to select the best conﬁguration whereas RS and GA always evaluate each conﬁguration the same number of times, thus several conﬁgurations can end up with the same fault probability. Accordingly, to fairly compare the fault probability evolution over time of the conﬁguration(s) found with SMAC, SHA, GA and RS, several considerations have to be taken into account:

– SMAC : by design, with SMAC, the best conﬁguration known so far is updated during runtime execution, thus no post-processing required. – RS : unlike SMAC, post-processing is required for RS. Every 5000 fault injec- tions, we inject 1000 more faults to evaluate the fault probability of the best conﬁguration(s) found so far. – GA: The same post-processing as RS is required. – SHA: We evaluate the average fault probability at each halving of the remain- ing conﬁgurations.

For each microcontroller considered, we optimize our VFI setup using SMAC, SHA, GA and RS and we compare the fault probability evolution over time of the conﬁguration(s) found. The best optimization technique is the one that ﬁnds the conﬁguration with the highest fault probability, within a minimum number of fault injections.

<!-- PDF_PAGE: 12 -->

## PDF page 12

132 V. Werner et al.

### 5.4 Results

The results of the experiments are summarized in Fig. 3 and Table 3. In the Fig. 3, we compare the evolution of fault probability over 50,000 fault injections, to visually determine the convergence speed of each optimization technique (fast or slow). Table 3 presents the fault probability of the best settings found with each technique. For each microcontroller, SMAC is signiﬁcantly faster than other optimiza- tion techniques. In particular, in less than 10,000 fault injections, SMAC sys- tematically identiﬁes conﬁgurations with higher fault probability than GA, RS and SHA. Therefore, SMAC can be used to calibrate an equipment faster than more commonly-used optimization techniques, hence saving valuable time dur- ing security evaluations. On the other hand, SHA slowly converges towards the best conﬁguration. However, at the end, after 50,000 fault injections, SHA ﬁnds the conﬁguration with the best fault probability for µC-M0 and µC-M3. By design, SHA uses all the allocated budget T , and removes iteratively the worst conﬁgurations at each round, which explains the slow convergence speed, in comparison with other optimization techniques. Nevertheless, we ﬁnd that SHA wastes many evaluations on poorly-performing conﬁgurations during the ﬁrst rounds, in particular with µC-M0. Our additional procedure for SMAC, described in Sect. 4.3 could also help SHA to select the initial conﬁguration 0 , so as to reduce the time spent on poorly-performing conﬁgura- instances Θ tions. Although we have not evaluated SMAC or SHA with other fault injection techniques, we believe that these optimization techniques can be easily adapt-

Table 3. Performance comparison between optimization techniques.

µC-M0 Max fault probability 0.52 Convergence speed Fast

µC-M3 Max fault probability 0.77 Convergence speed Fast

µC-M4 Max fault probability 0.95 Convergence speed Fast

SMAC SHA GA RS

### 0.53 0.49 0.49 Slow Fast Slow

### 0.81 0.52 0.24 Slow Slow Slow

### 0.79 0.81 0.71 Slow Fast Slow

Fig. 3. Evolution of fault probability over 50,000 fault injections, according to SMAC, GA, SHA and RS, with VFI

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 12]

<!-- PDF_PAGE: 13 -->

## PDF page 13

Fast Calibration of Fault Injection Equipment 133

able to EMFI or LFI. Regarding the results, SMAC is more eﬃcient than GA, RS, and SHA, in particular to quickly calibrate fault injection equipment for a given microcontroller. In the following, we will show that SMAC can also be used to exploit vulnerabilities faster than GA.

SMAC to Bypass a Code Protection Mechanism

6

In this section, we apply our two-stage strategy with SMAC to bypass a code protection mechanism, with VFI, on a 32-bit microcontroller. The presented attack is a known attack [8] which downgrades the security level of the target, so as to extract the ﬁrmware. We will show that SMAC is better than GA at identifying the best settings within a limited number of fault injections, and therefore that SMAC can save valuable time during security evaluations.

### 6.1 STM32F103RB

The microcontroller STM32F103RB is a 32-bit ARM Cortex-M3 core operating at 24 MHz. The preprogrammed bootloader oﬀers code protection mechanisms to prevent any read or write operations from the bootloader on the user ﬂash memory. In practical terms, once the read protection (RDP) is enabled, the bootloader returns a negative response (NACK) when a Read Memory command is issued. To disable RDP, the ﬂash must be completely erased.

Attack. The known attack [8] to bypass the read protection mechanism con- sists in injecting a fault during the Read Memory command. Indeed, when the bootloader receives the Read Memory command, it checks the RDP value and returns the ACK or the NACK byte, depending on whether RDP is disabled or

Fig. 4. Evolution of fault probability over 6000 fault injections, according to SMAC and GA, on the STM32F103RB; and the best glitch waveforms found with SMAC and GA during the calibration stage.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 13]

<!-- PDF_PAGE: 14 -->

## PDF page 14

134 V. Werner et al.

enabled, respectively. By injecting a fault during the RDP checking phase, an attacker can deceive the read protection mechanism and retrieve the content of the selected memory block.

Calibration Stage. In order to ﬁnd the best settings for our VFI equipment to glitch the STM32F103RB, we will use SMAC and GA, and compare the fault probability evolution. For both SMAC and GA, we perform the calibration stage with 6000 fault injections (24 generations for GA) during ≈ 15min, with the fault characterization test in Table 2, and with the default parameters. Figure 4 presents the fault probability evolution over time of the best conﬁguration(s) found with SMAC and GA. We have arbitrarily chosen a small number of fault injections during the calibration stage, so as to show that SMAC is deﬁnitely faster at identifying the best settings than more commonly-used optimization techniques, such as GA. Not only does SMAC converge faster than GA, but SMAC also identiﬁes conﬁgurations twice as eﬃcient as those found with GA (Table 4).

Exploitation Stage. We compare the average of the elapsed time to perform the attack to bypass RDP (exploitation stage) with SMAC and GA, using the best glitch waveforms found during the calibration stage. The attack is easily achieved with the best conﬁguration found with SMAC, on average in less than 5 minutes. On contrary, with the best conﬁgurations found with GA, we have not been able to bypass the read protection mechanism of the STM32F103RB. This shows that with only 6,000 fault injections during the calibration stage, GA clearly underperforms SMAC. Figure 5 presents the oscilloscope traces of the attack to bypass RDP on the STM32F103RB, using the best glitch waveform found with SMAC.

Table 4. Performance comparison between SMAC and GA on the STM32F103RB with VFI.

Number of fault injections 6000 12000

SMAC Max fault probability 0.79 0.79 Calibration time 15 min 30 min Exploitation time &lt;5 min &lt;5 min

GA

Max fault probability 0.37 Calibration time 15 min Exploitation time N/A

### 0.55 30 min &lt;5 min

<!-- PDF_PAGE: 15 -->

## PDF page 15

Fast Calibration of Fault Injection Equipment 135

Fig. 5. Oscilloscope traces of the glitch attack to bypass RDP on the STM32F103RB.

> [FIGURE omitted — image not stored; caption/text above; cite source PDF page 15]

Note that with a larger number of fault injections during the calibration stage, it is also possible to bypass RDP using GA. For example, with twice as many fault injections during the calibration stage (i.e. 12,000 instead of 6,000), GA identiﬁes equipment settings that can successfully glitch the STM32F103RB and bypass the code protection mechanism (Table 4). But even after 12.000 fault injections, the conﬁgurations identiﬁed with GA have a lower fault probability than with SMAC.

7 Conclusion

Fault injection requires a preliminary step of equipment calibration in order to ﬁnd exploitable and repeatable faults. In this article, we have proposed applying state-of-the-art optimization techniques, already used for machine learning and other hard combinatorial problems, to fault injection. Bayesian Optimization (SMAC) and Bandit Optimization (SHA) are used to identify the best equip- ment conﬁgurations which maximize exploitable faults on a target microcon- troller. While SHA is a simple algorithm, easily adaptable to fault injection and yet oﬀers decent performance, SMAC is arguably the most interesting optimiza- tion technique, ﬁnding better equipment conﬁgurations faster than metaheuristic algorithms. In addition, to simplify and speed up the equipment calibration, we have proposed splitting fault injection optimization into two stages, the calibration stage and the exploitation stage. We optimize fault injection parameters inde- pendently of the target application with a fault characterization test and then, once the best conﬁgurations are identiﬁed, we ﬁnd fault injection timings to exploit vulnerabilities on the target application. With SMAC and this strategy, we successfully bypass a code protection mechanism of the STM32F103RB boot- loader. In particular, the calibration stage with SMAC is twice as fast as with

<!-- PDF_PAGE: 16 -->

## PDF page 16

136 V. Werner et al.

GA. Furthermore, SMAC and SHA have systematically identiﬁed better conﬁg- urations than metaheuristic algorithms, and although it has not been studied in this article, ﬁnding conﬁgurations with high fault probability is even more important when multi-fault injections are necessary, as inducing more repeat- able faults greatly help in carrying out complex multi-fault attacks. As future work, it will be interesting to apply other promising optimization techniques such as HyperBand (Bandit Optimization) or Tree-structured Parzen Estimator (Bayesian Optimization). Moreover, we will investigate the applica- tions of hyperparameter optimization techniques to ﬁnd exploitable faults with other fault injection techniques, such as LFI or EMFI. Finally, our ongoing research is focused on direct applications of fault injection optimization with SMAC or SHA on secure microcontrollers. For example, we believe that we can ﬁnd exotic waveforms with SMAC that can bypass voltage glitch attack detec- tors.

### References

1. Anceau, S., Bleuet, P., Clédière, J., Maingault, L., Rainard, J., Tucoulou, R.: Nanofocused X-ray beam to reprogram secure circuits. In: Fischer, W., Homma, N. (eds.) CHES 2017. LNCS, vol. 10529, pp. 175–188. Springer, Cham (2017). https:// doi.org/10.1007/978-3-319-66787-4 9 2. Aumüller, C., Bier, P., Fischer, W., Hofreiter, P., Seifert, J.-P.: Fault attacks on RSA with CRT: concrete results and practical countermeasures. In: Kaliski, B.S., Koç, K., Paar, C. (eds.) CHES 2002. LNCS, vol. 2523, pp. 260–275. Springer, Heidelberg (2003). https://doi.org/10.1007/3-540-36400-5 20 3. Aziz, M.: On Multi-Armed Bandits Theory and Applications. PhD thesis, Ph. D. Thesis, Northeastern University, Boston, MA, USA (2019) 4. Balasch, J., Gierlichs, B., Verbauwhede, I.: An in-depth and black-box character- ization of the eﬀects of clock glitches on 8-bit mcus. In: 2011 Workshop on Fault Diagnosis and Tolerance in Cryptography, pp. 105–114. IEEE (2011) 5. Bellman, R.E.: Adaptive Control Processes. Princeton University Press, Princeton (1861) 6. Bergstra, J., Bengio, Y.: Random search for hyper-parameter optimization. J. Mach. Learn. Res. 13(2), 281–305 (2012) 7. Beyer, H.-G., Schwefel, H.-P.: Evolution strategies-a comprehensive introduction. Natural Comput. 1(1), 3–52 (2002) 8. Bozzato, C., Focardi, R., Palmarini, F.: Shaping the glitch: optimizing voltage fault injection attacks. IACR Trans. Cryptogr. Hard. Embed. Syst. 199–224, 2019 (2019) 9. Breiman, L.: Random forests. Mach. Learn. 45(1), 5–32 (2001) 10. Carpi, R.B., Picek, S., Batina, L., Menarini, F., Jakobovic, D., Golub, M.: Glitch it if you can: parameter search strategies for successful fault injection. In: Francillon, A., Rohatgi, P. (eds.) CARDIS 2013. LNCS, vol. 8419, pp. 236–252. Springer, Cham (2014). https://doi.org/10.1007/978-3-319-08302-5 16 11. Colombier, B., Menu, A., Dutertre, J.-M., Moëllic, P.-A., Rigaud, J.-B., Danger, J.-L.: Laser-induced single-bit faults in ﬂash memory: instructions corruption on a 32-bit microcontroller. IACR Cryptol. ePrint Arch. 2018, 1042 (2018)

<!-- PDF_PAGE: 17 -->

## PDF page 17

Fast Calibration of Fault Injection Equipment 137

12. Courbon, F., Loubet-Moundi, P., Fournier, J.J.A., Tria, A.: Increasing the eﬃ- ciency of laser fault injections using fast gate level reverse engineering. In: 2014 IEEE International Symposium on Hardware-Oriented Security and Trust (HOST), pp. 60–63. IEEE (2014) 13. Dehbaoui, A., Dutertre, J.M., Robisson, B., Tria, A.: Electromagnetic transient faults injection on a hardware and a software implementations of AES. In: 2012 Workshop on Fault Diagnosis and Tolerance in Cryptography, pp. 7–15. IEEE (2012) 14. Dureuil, L., Potet, M.-L., de Choudens, P., Dumas, C., Clédière, J.: From code review to fault injection attacks: ﬁlling the gap using fault model inference. In: Homma, N., Medwed, M. (eds.) CARDIS 2015. LNCS, vol. 9514, pp. 107–124. Springer, Cham (2016). https://doi.org/10.1007/978-3-319-31271-2 7 15. Gerlinsky, C.: Breaking code read protection on the nxp lpc-family microcontrollers (2017) 16. Hutter, F., Hoos, H.H., Leyton-Brown, K.: Sequential model-based optimization for general algorithm conﬁguration. In: Coello, C.A.C. (ed.) LION 2011. LNCS, vol. 6683, pp. 507–523. Springer, Heidelberg (2011). https://doi.org/10.1007/978- 3-642-25566-3 40 17. Hutter, F., Hoos, H.H., Leyton-Brown, K., Murphy, K.P.: An experimental investi- gation of model-based parameter optimisation: spo and beyond. In: Proceedings of the 11th Annual conference on Genetic and evolutionary computation, pp. 271–278 (2009) 18. Karnin, Z., Koren, T., Somekh, O.: Almost optimal exploration in multi-armed bandits. In: International Conference on Machine Learning, pp. 1238–1246. PMLR (2013) 19. Katoch, S., Chauhan, S.S., Kumar, V.: A review on genetic algorithm: past, present, and future. Multimedia Tools Appl. 80, 1–36 (2020) 20. Li, L., Jamieson, K., DeSalvo, G., Rostamizadeh, A., Talwalkar, A.: Hyperband: a novel bandit-based approach to hyperparameter optimization. J. Mach. Learn. Res. 18(1), 6765–6816 (2017) 21. Lindauer, M., Eggensperger, K., Feurer, M., Falkner, S., Biedenkapp, A., Hut- ter, F.: Smac v3: algorithm conﬁguration in python (2017). https://github.com/ automl/SMAC3 22. Lipowski, A., Lipowska, D.: Roulette-wheel selection via stochastic acceptance. Physica A Stat. Mech. Appl. 391(6), 2193–2196 (2012) 23. Madau, M., Agoyan, M., Maurine, P.: An EM fault injection susceptibility crite- rion and its application to the localization of hotspots. In: Eisenbarth, T., Teglia, Y. (eds.) CARDIS 2017. LNCS, vol. 10728, pp. 180–195. Springer, Cham (2018). https://doi.org/10.1007/978-3-319-75208-2 11 24. Maldini, A., Samwel, N., Picek, S., Batina, L.: Optimizing electromagnetic fault injection with genetic algorithms. In: Breier, J., Hou, X., Bhasin, S. (eds.) Auto- mated Methods in Cryptographic Fault Analysis, pp. 281–300. Springer, Cham (2019). https://doi.org/10.1007/978-3-030-11333-9 13 25. Moro, N., Dehbaoui, A., Heydemann, K., Robisson, B., Encrenaz, E.: Electromag- netic fault injection: towards a fault model on a 32-bit microcontroller. In: 2013 Workshop on Fault Diagnosis and Tolerance in Cryptography, pp. 77–88. IEEE (2013) 26. Obermaier, J., Tatschner, S.: Shedding too much light on a microcontroller’s ﬁrmware protection. In: 11th {USENIX} Workshop on Oﬀensive Technologies ({WOOT} 2017) (2017)

<!-- PDF_PAGE: 18 -->

## PDF page 18

138 V. Werner et al.

27. Picek, S., Batina, L., Buzing, P., Jakobovic, D.: Fault injection with a new ﬂavor: memetic algorithms make a diﬀerence. In: Mangard, S., Poschmann, A.Y. (eds.) COSADE 2014. LNCS, vol. 9064, pp. 159–173. Springer, Cham (2015). https:// doi.org/10.1007/978-3-319-21476-4 11 28. Picek, S., Batina, L., Jakobović, D., Carpi, R.B.: Evolving genetic algorithms for fault injection attacks. In: 2014 37th International Convention on Information and Communication Technology, Electronics and Microelectronics (MIPRO), pp. 1106– 1111. IEEE (2014) 29. Riviere, L., Najm, Z., Rauzy, P., Danger, J. L., Bringer, J., Sauvage, L.: High precision fault injections on the instruction cache of armv7-m architectures. In: 2015 IEEE International Symposium on Hardware Oriented Security and Trust (HOST), pp. 62–67. IEEE (2015) 30. Schellenberg, Markus F., et al.: On the complexity reduction of laser fault injection campaigns using obic measurements. In: 2015 Workshop on Fault Diagnosis and Tolerance in Cryptography (FDTC), pp. 14–27. IEEE (2015) 31. Skorobogatov, S.P., Anderson, R.J.: Optical fault induction attacks. In: Kaliski, B.S., Koç, K., Paar, C. (eds.) CHES 2002. LNCS, vol. 2523, pp. 2–12. Springer, Heidelberg (2003). https://doi.org/10.1007/3-540-36400-5 2 32. Trouchkine, T., Bouﬀard, G., Clédière, J.: Fault injection characterization on mod- ern CPUs. In: Laurent, M., Giannetsos, T. (eds.) WISTP 2019. LNCS, vol. 12024, pp. 123–138. Springer, Cham (2020). https://doi.org/10.1007/978-3-030-41702-4 8 33. Van den Herrewegen, J., Oswald, D., Garcia, F.D., Temeiza, Q.: Fill your boots: Enhanced embedded bootloader exploits via fault injection and binary analysis. IACR Trans. Cryptogr. Hardw. Embed. Syst. 56–81, 2021 (2021) 34. Werner, V., Maingault, L., Potet, M.-L.: An end-to-end approach for multi-fault attack vulnerability assessment. In: 2020 Workshop on Fault Detection and Toler- ance in Cryptography (FDTC), pp. 10–17. IEEE (2020) 35. Wu, L., Ribera, G., Beringuier-Boher, N., Picek, S.: A fast characterization method for semi-invasive fault injection attacks. In: Jarecki, S. (ed.) CT-RSA 2020. LNCS, vol. 12006, pp. 146–170. Springer, Cham (2020). https://doi.org/10.1007/978-3- 030-40186-3 8 36. Yang, L., Shami, A.: On hyperparameter optimization of machine learning algo- rithms: theory and practice. Neurocomputing 415, 295–316 (2020)
