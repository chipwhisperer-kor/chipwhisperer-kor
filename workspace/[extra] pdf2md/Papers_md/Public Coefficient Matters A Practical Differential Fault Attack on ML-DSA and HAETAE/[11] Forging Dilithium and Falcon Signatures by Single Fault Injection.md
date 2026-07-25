# [11] Forging Dilithium and Falcon Signatures by Single Fault Injection

> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. 그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 source PDF 페이지 표기(PDF_PAGE)를 유지합니다. 표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. 이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.

<!-- PDF_TO_MARKDOWN_METADATA
converter: "kit/tools/pdf_to_markdown.py"
profile: "deterministic-bbox-v1+text-only-v1"
figure_policy: "omit-pixels-keep-caption-and-pdf-page"
pdftotext: "pdftotext version 26.01.0"
pdfinfo_pages: 8
converted_at: "2026-07-26"
source_asset_id: "PCM-DFA-REF-11"
derived_asset_id: "PCM-DFA-REF-11-MD"
source_path: "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[11] Forging Dilithium and Falcon Signatures by Single Fault Injection.pdf"
source_sha256: "f4c4fb6fabaef804feb95aead8717b3c19e75c09d7b29cc28d8ce05880ab564b"
pages: 8
bbox_words: 6609
consumed_bbox_words: 6609
numeric_tokens: 858
consumed_numeric_tokens: 858
source_blocks: 208
consumed_source_blocks: 208
emitted_blocks: 191
embedded_raster_images: 0
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

2023 Workshop on Fault Detection and Tolerance in Cryptography (FDTC)

Forging D ILITHIUM and F ALCON Signatures by Single Fault Injection

Sven Bauer , Fabrizio De Santis

Siemens AG, Technology Munich, Germany {svenbauer, fabrizio.desantis}@siemens.com

2023 Workshop on Fault Detection and Tolerance in Cryptography (FDTC) | 979-8-3503-4252-9/23/$31.00 ©2023 IEEE | DOI: 10.1109/FDTC60478.2023.00017

Abstract—Embedded devices commonly rely on digital signa- tures to ensure both integrity and authentication. For example, digital signatures are typically veriﬁed during the boot process or ﬁrmware updates to verify the integrity of a system. They are also used to ensure authenticity of a communication party in secure protocols. Fault injection can be used to tamper with a device in order to cause malfunctioning during cryptographic computations. For example, fault injections can be used to disturb digital signing operations. With the right type of fault an attacker can compute private keys from faulted signatures. However, fault injections can also be used during veriﬁcation to get maliciously crafted digital signatures accepted during signature veriﬁcation with catastrophic consequences for the security of an embedded device. In this paper, we introduce new non-obvious fault injection attacks on the veriﬁcation routines of D ILITHIUM and F ALCON signature schemes, which allow an attacker to get signatures for arbitrary messages accepted by fault injection. We demonstrate the feasibility of our attacks by simulations using an ARM Cortex-M4 and the pqm4 library as a target of evaluation and pinpoint vulnerable instructions. Finally, we propose and discuss possible countermeasures against these attacks. Index Terms—Fault attack; Post-quantum cryptography; Dig- ital signature schemes; Lattice-based cryptography; Dilithium; Falcon;

### I. I NTRODUCTION

Embedded devices rely heavily on the veriﬁcation of digital signatures to ensure the authenticity and integrity of data. During the boot process, the device veriﬁes the digital sig- nature of the ﬁrmware to ensure that it has not been tampered with or modiﬁed. Similarly, software updates are veriﬁed using digital signatures to ensure that only authorized and unaltered software is installed. Moreover, digital signatures are also used to verify the authenticity of a communication party. When two devices communicate with each other, signatures are often a part of an authentication protocol or digital certiﬁcates. These signatures are then veriﬁed to conﬁrm that both parties are authentic and not being impersonated. Hence, if an attacker manages to bypass or compromise the signature veriﬁcation process, they can inject malicious code into the device or impersonate a legitimate communication party. This can lead to severe consequences, including data breaches, ﬁnancial losses, and reputation damage. Therefore, it is crucial to ensure that signature veriﬁcation is implemented securely and robustly in embedded devices.

2995-0252/23/$31.00 ©2023 IEEE DOI 10.1109/FDTC60478.2023.00017

81

In [1] Muir showed how to trick a device into accepting a maliciously crafted RSA signature in a non-obvious way by fault injection. This attack is particularly noteworthy because it does not focus on the most vulnerable part of RSA signature veriﬁcation, which is the comparison between the computed signature and the provided signature. Typically, an attacker would aim at exploiting this comparison through fault attacks. However, skilled developers are aware of this vulnerability and take measures to mitigate it. Muir’s attack showed that there might be non-obvious ways to bypass existing countermea- sures by fault injection. In July 2022, the U.S. Department of Commerce’s National Institute for Standard and Technology (NIST) selected three algorithms D ILITHIUM [2], F ALCON [3] and S PHINCS + [4] for digital signatures as quantum-computer resistant replace- ments for RSA and elliptic-curve based digital signatures [5]. These three signature schemes are now in the process of being standardized by NIST. In particular, D ILITHIUM and F ALCON are good candidates for general purpose applications because they offer smaller signatures than S PHINCS +. Muir’s attack motivates considering the possibility of fault injection attacks against post-quantum signature schemes. As for RSA veriﬁcation, there are obvious places for a fault injection attack in D ILITHIUM and F ALCON as well, e.g., the ﬁnal decision whether to accept or reject a signature, or the ﬁnal length-check in the F ALCON signature veriﬁcation procedure (see Algorithm 2, Line 6). However, as in the case of RSA, there may be less obvious attacks for D ILITHIUM and F ALCON veriﬁcation routines that developers are more likely to overlook. Consequently, these vulnerabilities may not be adequately protected by appropriate countermeasures in prac- tice. This is especially important for post-quantum signature schemes, as they are relatively new and their implementations may not have been subjected to the same level of scrutiny yet, as more established schemes. By identifying and testing these attack vectors, we can help to improve the security of implementations of these schemes and to prevent potential attacks in the future. In this paper, we describe fault attacks against parts of the D ILITHIUM and F ALCON signature veriﬁcation procedure which are not such obvious targets as the ﬁnal comparison. We show that these attacks are successful on the assumption that a fault injection attack can cause the target hardware to skip instructions.

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:36 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 2 -->

## PDF page 2

A good overview of instruction skipping by fault injection can be found in [6], which also shows that this is a very realistic fault model. See also [7] and [8] for recent detailed analyses of the instruction skip fault model.

A. Previous work

Muir’s attack [1] is a generalization of an attack by Seifert described in [9]. It tricks a device into accepting an incorrect RSA-signature with a fault injection attack. Muir’s attack works as follows: the attacker ﬂips a few bits in the public RSA modulus n to obtain a number n that is easy to decompose into prime-factors. Because a randomly chosen integer is likely to have many small prime factors and is hence easy to factor, such an n can typically be found with only a few bit ﬂips. With the factorization of n it is easy to compute φ(n ) and then d = 1/e mod φ(n ) 1 . Now the attacker simply signs an arbitrary message with (d , n ) and sends the signed message and the crafted signature to the device. With a fault injection attack during the signature veriﬁcation procedure, the attacker tries to reproduce the bit ﬂips to turn n into n in the device. If this succeeds, the device accepts the crafted signature as valid. In the ﬁeld of post-quantum cryptography, a number of publications have already addressed fault attacks against post- quantum signature schemes. Prominent examples are [10], [11], [12]. However, these works do not target the signature veriﬁcation procedure. A number of fault attacks against BLISS, ring-TESLA, and the GLP-scheme, including their veriﬁcation procedure, can be found in [13]. Fault attacks against signature veriﬁcation in D ILITHIUM are brieﬂy dis- cussed in [14], [15]. However, these publications describe generic, more obvious, attacks, namely, targeting the ﬁnal comparison. Additionally, [15] presents an attack based on zeroing the twiddle factors during the computation of the Number-Theoretic Transform (NTT).

B. Contributions

This paper shows a number of non-obvious, yet practi- cally simple and realistic fault injection attacks against the veriﬁcation routines of the post-quantum signature schemes D ILITHIUM and F ALCON . The attacks target parts of the code which even an experienced developer would not necessarily consider protecting against fault injections. Consequently, an attacker can trick a device into processing arbitrary unau- thenticated data, hence potentially enabling the attacker to install malicious software on a device. If signature veriﬁcation during the establishment of a secure communication session is attacked, the attacker can force the device to communicate with an unauthenticated party.

### C. Outline

In Section II, a description of the D ILITHIUM signature scheme is provided. In Section III we show an attack against

1 In the unlikely case that gcd(n , e) = 1, the attacker simply tries again with a different n .

82

TABLE I: Parameters of D ILITHIUM signature veriﬁcation

NIST security level 2 3 5

γ 1

2 17 2 19 2 19

γ 2 (q − 1)/88 (q − 1)/32 (q − 1)/32

(k, l) (4, 4) (6, 5) (8, 7)

β

78 196 120

ω

80 55 75

D ILITHIUM signature veriﬁcation. Section IV gives a de- scription of the F ALCON signature scheme. In Section V we show how to attack F ALCON signature veriﬁcation. A practical evaluation of the proposed attacks is provided in Section VI. Possible countermeasures to protect against the proposed fault attacks are described in Section VII. We summarize our conclusions and give an outlook in Section VIII.

### II. D ILITHIUM SIGNATURE VERIFICATION

We give a brief description of the D ILITHIUM signature veriﬁcation procedure. For the full details of the D ILITHIUM signature scheme, we refer the reader to the D ILITHIUM speciﬁcation [2].

D ILITHIUM largely works over a ring R q = Z q [X]/(X 256 + 1) with q = 8380417. The speciﬁcation deﬁnes a representa- tion of elements of R q as byte strings. Hence, we will, for example, apply hash functions to elements of R q , implicitly assuming the encoding deﬁned in the speciﬁcation 2 .

The D ILITHIUM speciﬁcation [2] deﬁnes three variants, targeting NIST security levels 2, 3 and 5 (see [16, Section 4.A.5] for a deﬁnition of these security levels). Therefore, signature veriﬁcation is parameterized. We give the values of the parameters for the three security levels in Table I. The D ILITHIUM speciﬁcation lists more parameters, but we have only listed those which are relevant to signature veriﬁcation.

A D ILITHIUM public key is a pair (ρ, t 1 ) ∈ {0, 1} 256 × R q l . A D ILITHIUM signature is a triple (c̃, z, h) ∈ {0, 1} 256 × R q l × {0, 1} 256k . The signature veriﬁcation procedure calls a function ExpandA : {0, 1} 256 → R q k×l that is used to expand the bit string ρ to a matrix A ∈ R q k×l . So ρ is a compressed representation of A. Furthermore, the signature veriﬁcation procedure calls a subroutine SampleInBall that produces a pseudo-random 256-bit string with exactly τ bits equal to one from an input seed. Finally, a function UseHint q is needed that takes as input a 256-bit string (the “hint”), a vector in R q k and an integer (the “low-order rounding range”).

2 The exact deﬁnition of this encoding does not matter for the purposes of this paper and can be found in [2]

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:36 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 3 -->

## PDF page 3

Algorithm 1 D ILITHIUM .V ERIFY (m, sig, pk)

Require: A message m a signature sig = (c̃, z, h), a public key pk = (ρ, t 1 ). Ensure: Accept or reject 1: A ← ExpandA(ρ) 2: μ ← SHAKE256(SHAKE256(ρt 1 , 256)m, 512) 3: c ← SampleInBall(c̃) 4: w 1 ← UseHint(h, Az − ct 1 , 2γ 2 ) 5: if z ∞ &lt; γ 1 − β and c̃ = SHAKE256(μw 1 , 256) and the number of 1s in h is ≤ ω then 6: accept 7: else 8: reject

### III. F AULT ATTACKS AGAINST D ILITHIUM SIGNATURE

VERIFICATION

We use the same notation as in Section II and assume the attacker has access to a valid D ILITHIUM public key (ρ, t 1 ) and some message m with a valid D ILITHIUM signature σ = (c̃, z, h) that can be veriﬁed with the public key (ρ, t 1 ). We assume further the attacker has physical access to a device that only accepts messages with signatures that can be veriﬁed under the public key (ρ, t 1 ). The attacker wants to force the device into accepting a message m for which the attacker does not have a valid signature. Our attack consists of two steps: ﬁrst, the attacker constructs an invalid signature σ for m and then, using a fault injection, forces the device to accept this as a valid signature for m . The point is, that σ needs to be speciﬁcally crafted to make this fault injection attack practical. To achieve this, the attacker proceeds as follows: 1) Calculate:

μ := SHAKE256(SHAKE256(ρt 1 , 256)m , 512)) (1) This is the same step as in the veriﬁcation procedure in Line 2 when verifying a signature for m . 2) Compute:

w 1 := UseHint q (h, Az, 2γ 2 )

(2)

This is the same step as in the veriﬁcation procedure algorithm in Algorithm 1 in Line 4, but with c = 0. 3) Compute:

c̃ := SHAKE256(μw 1 , 256)

(3)

4) Let σ := (c̃ , z, h) and send the message m with the purported signature σ to the device for veriﬁcation. Note that the components z and h are taken from the genuine signature σ. 5) During the signature veriﬁcation procedure on the de- vice, the attacker injects a fault to suppress subtracting ct 1 in Algorithm 1, Line 4. If the fault injection is successful, the device will compute the same value w 1 as the attacker in Step 2 of the attack.

83

Hence, the second part of the test in Algorithm 1, Line 4 becomes a test that c̃ = SHAKE256(μw 1 , 256). This is of course correct. The other two parts of this test pass as well, because they are carried out on components z and h of a genuine signature. Therefore, the device will accept σ as a valid signature for m . Of course the critical step is the fault injection in Step 5.

### IV. F ALCON SIGNATURE VERIFICATION

We describe the signature veriﬁcation procedure of F ALCON . For a full description of the F ALCON signature scheme we refer the reader to the speciﬁcation of F ALCON in [3]. There are two variants of F ALCON , namely F ALCON -512 and F ALCON -1024. The two variants target NIST security levels 1 and 5, respectively. Their mathematical descriptions differ only in the choice of some parameters. Most mathematical operations in F ALCON signature veriﬁcation are happening in a truncated polynomial ring Z q [x]/(φ). Here, q = 12289 (a prime number) and φ(x) = x n + 1. We have n = 512 for F ALCON -512 and n = 1024 for F ALCON -1024. Another parameter is a rejection bound, which is β 2 = 34 034 726 for F ALCON -512 and β 2 = 70 265 242 for F ALCON -1024. A message m in F ALCON is simply a string of bytes. A F ALCON signature is a pair (r, s), where r is a random 320-bit string and s is the representation of a polynomial s 2 ∈ Z q [x]/(φ). A F ALCON public key is a polynomial h ∈ Z q [x]/(φ). Furthermore, F ALCON signature veriﬁcation uses a function HashToPoint that maps a byte string to a polynomial in c ∈ Z q [x]/(φ) and a function Decompress that recovers the polynomial s 2 ∈ Z q [x]/(φ) from its representation as a string of bytes.

Algorithm 2 F ALCON .V ERIFY (m, sig, pk)

Require: A message m, a signature sig = (r, s), a public key pk = h ∈ Z q [x]/(φ) Ensure: Accept or reject 1: c ← HashToPoint(rm) 2: s 2 ← Decompress(s) 3: if s 2 =⊥ then 4: reject 5: s 1 ← c − s 2 h mod q 6: if (s 1 , s 2 ) 2 ≤ β 2 then 7: accept 8: else 9: reject

### V. F AULT ATTACKS AGAINST F ALCON SIGNATURE

VERIFICATION

The most obvious target for a fault attack against F ALCON signature veriﬁcation is the comparison (s 1 , s 2 ) &lt; β 2 , cf. Line 6 in Algorithm 2. The goal of the attack is to inject a fault such that the comparison is skipped for an arbitrary (s 1 , s 2 ).

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:36 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 4 -->

## PDF page 4

However, because this is the most obvious place to attack, it is also a part of the code that a careful designer most likely implements with appropriate countermeasures against this type of attack. In this section, we are considering attacks which are less obvious and less likely to be prevented by countermeasures in the implementation. We assume the attacker has a valid signature (r, s) for some message m. Every attack starts with the attacker choosing a message m . All attacks aim at constructing a (forged) signature such that it only takes a single fault that can be injected with high probability to force the verifying device into accepting the signature and hence processing m .

A. Fault injection during the inclusion of the message hash

For our ﬁrst attack against F ALCON signature veriﬁcation, the attacker performs the following steps: 1) The attacker chooses r to be an arbitrary string of 320 bits and sets s := Compress(0, n − 328), where n = 512 for F ALCON -512 and n = 1024 for F ALCON - 1024. So s is the compressed representation of the zero- polynomial. 2) The attacker sends the message m and the purported signature (r , s ) to the device for veriﬁcation. 3) During the veriﬁcation procedure, the attacker injects a fault to suppress the inclusion of c in Algorithm 2, Line 5. So the device computes s 1 ← −s 2 h mod q = 0, because s 2 is 0 by construction. If the fault injection is successful, the check in Line 6 becomes a check that β 2 ≥ (s 1 , s 2 ) = 0. This check obviously passes, and the device accepts the signature and starts processing m . We note that this attack does not work when F ALCON is operated in key-recovery mode, see the F ALCON -speciﬁcation, Section 3.12 in [3], because Line 5 in Algorithm 2, the line we attack, does not exist in the signature veriﬁcation procedure in key-recovery mode.

B. Fault injection during the computation of the Euclidean norm

This fault injection attack targets the computation of the Euclidean norm in Algorithm 2, Line 6. Now let i &gt; 0 be the smallest index such that h i = 0 3 . So the public key h has the form:

n−1

h k x k

h(x) = h 0 +

(4)

k=i

We ﬁrst explain how the attacker proceeds and then show why the attack works: 1) The attacker chooses a polynomial s 2 ∈ Z q /(φ) with s 2,i = c 0 h −1 n−i and s 2,j = 0 for j = i. 2) The attacker chooses a random 320-bit string r and sets s := Compress(s 2 , 8 ∗ sbytelen − 328) and sends

3 Note that such an i exists unless the public key h consists only of a constant term.

84

the chosen message m together with the purported signature (r , s ) to the device for processing. 3) The attacker injects a fault such that the computation of the Euclidean norm in Algorithm 2, Line 6 stops after processing the 0 th coefﬁcient. We will show that this is a realistic attack target in Section VI-B. To understand why this attack works (assuming, of course, that the fault injection is successful), we carefully follow the steps of the signature veriﬁcation process. First, the device computes c ← HashToPoint(r m , q, n) and decom- presses s to recover the s 2 the attacker has constructed in the ﬁrst step of the attack. Next, the device computes s 1 ← c − s 2 h. If we look at the th 0 coefﬁcient of the polynomial s 1 , we see that

s 1,0 = c 0 − s 2,i h n−i = c 0 − c 0 h −1 n−i h n−1 = 0,

(5)

because of the way the attacker has constructed s 2 . If the fault injection in the last step of the attack is successful, then the device computes the Euclidean norm of (s 1 , s 2 ) as 2 s 2 (6) 1,0 + s 2,0 = 0 + 0 = 0,

because the fault terminates the loop after the ﬁrst iteration and other coefﬁcients of s 1 and s 2 are ignored. Hence, the norm is short enough for the device to accept the purported signature, and the device will process m like a valid message. Of course s 1,0 does not have to be zero, it is sufﬁcient if 2 s 1,0 ≤ β 2 . This is the case with some probability anyway. So, instead of constructing s 2 as above, an attacker can 2 also choose s 2 = 0 and then try different r until c 2 0 ≤ β , with c = HashToPoint(r m ). We see from Line 5 in 2 2 2 Algorithm 2 that then s 2 1,0 = c 0 ≤ β . Because β is larger for F ALCON -1024 than for F ALCON -512, this simpliﬁed version of the attack is easier for F ALCON -1024. More precisely, we see that for F ALCON -512 we have to have c 2 0 ≤ 34 034 726 and hence 0 ≤ c 0 ≤ 5 833 and for ≤ 70 265 242 and hence F ALCON -1024 we have to have c 2 0 0 ≤ c 0 ≤ 8 382. Note that 0 ≤ c 0 &lt; q = 13329 anyway.

### VI. P RACTICAL EVALUATION

To assess the practical validity of our attacks, we simulated fault injection on a STMF407G-DISC1 board featuring an a 32-bit ARM Cortex-M4 (STMF407VGT6) high-performance microcontroller with FPU core, 1-Mbyte Flash memory, and 192-Kbyte RAM with the aid of a debugger (GNU gdb 13.1). We ran our attacks against the pqm4 library[17] 4 compiled with gcc version 12.2.0 and optimization ﬂags -O3 -mfloat-abi=hard -mfpu=fpv4-sp-d16. Note that such attacks would similarly work on the refer- ence implementations of D ILITHIUM [18] and F ALCON [19] submitted at NIST.

4 commit a525417134995302bb5013dd112dec65cdb28ca9

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:36 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 5 -->

## PDF page 5

Listing 1: Excerpt from the D ILITHIUM -2 signature veriﬁcation function crypto_sign_verify in ﬁle crypto_sign/dilithium2/m4f/sign.c

274 275

... /* Matrix-vector multiplication; compute Az - c2ˆdt1 */ poly_challenge(&amp;cp, c); polyvec_matrix_expand(mat, rho);

276 277 278 279 280

polyvecl_ntt(&amp;z); polyvec_matrix_pointwise_montgomery(&amp;w1, mat, &amp;z);

281 282 283 284 285

poly_ntt(&amp;cp); polyveck_shiftl(&amp;t1); polyveck_ntt(&amp;t1); polyveck_pointwise_poly_montgomery(&amp;t1, &amp; cp, &amp;t1);

286 287 288 289 290

polyveck_sub(&amp;w1, &amp;w1, &amp;t1); polyveck_reduce(&amp;w1); polyveck_invntt_tomont(&amp;w1); ...

Listing 2: Assembly code corresponding to the D ILITHIUM - 2 signature veriﬁcation function crypto_sign_verify in ﬁle crypto_sign/dilithium2/m4f/sign.c

1 2 3

... 0x80030c4 &lt;crypto_sign_verify+252&gt; adds r2, #16 0x80030c6 &lt;crypto_sign_verify+254&gt; bl 0x80028f8 &lt;polyveck_sub&gt; 0x80030ca &lt;crypto_sign_verify+258&gt; add.w r0, sp , #10304 ...

4

5

A. Experiments with D ILITHIUM

For the sake of evaluation, the implementation of D ILITHIUM -2 was considered. The fault attack described in Section III targets polyveck_sub operation is the function call in line 287 in ﬁle crypto_sign/dilithium2/m4f/sign.c. Skipping this function call has exactly the effect required in Step 5 of the attack (see Listing 1). This can be achieved on a ARM Cortex-M4 by skip- ping the branch with link (bl) instruction at address 0x80030c6, which corresponds to the machine code lo- cation +254 in the crypto_sign_verify function lo- cated in the crypto_sign/dilithium2/m4f/sign.c, and jumps to the address 0x80028f8 corresponding to the polyveck_sub operation. If the memory for cp is pre-initialized with zero, then skipping the call to poly_challenge() in Line 276 in Listing 1 has a similar effect. We did not pursue this variant of the attack experimentally. Note that a seminal idea of removing the term ct 1 from the computation in Algorithm 1, Line 4 can also be found in

85

Listing 3: Excerpt from the F ALCON -512 signa- ture veriﬁcation function verify_raw in ﬁle crypto_sign/falcon-512/m4-ct/vrfy.c

664 665 666

... /* * Compute -s1 = s2*h - c0 mod phi mod q (in tt[]). */ mq_NTT(tt, logn); mq_poly_montymul_ntt(tt, h, logn); mq_iNTT(tt, logn); mq_poly_sub(tt, c0, logn);

667 668 669 670 671 672 673 674

/* * Normalize -s1 elements into the [-q /2..q/2] range. */ for (u = 0; u &lt; n; u ++) { int32_t w;

675 676 677 678 679 680

w = (int32_t)tt[u]; w -= (int32_t)(Q &amp; -(((Q &gt;&gt; 1) - (uint32_t)w) &gt;&gt; 31)); ((int16_t *)tt)[u] = (int16_t)w;

681 682 683 684 685

}

/* * Signature is valid if and only if the aggregate (-s1,s2) vector * is short enough. */ return Zf(is_short)((int16_t *)tt, s2, logn); ...

686 687 688

689

[15]. However, in [15] the target of the attack is the number- theoretic transform, which requires a slightly more involved construction of the forged signature and a fault that zeroes data or changes a pointer to point into an array ﬁlled with zeroes. As skipping instructions is a well-documented effect of fault injections, we believe our attack to be easier in practice. Also, a similar idea, this time in the context of the signature scheme ring-TESLA, can be found in [13]. Again, the fault model used in [13] is zeroing of data.

B. Experiments with F ALCON

For the sake of evaluation, the implementation of F ALCON - 512 was considered. The ﬁrst attack described in Section V-A requires skipping the inclusion of the message hash c. Listing 3 shows an excerpt of the pqm4 implementation of the Falcon signature veriﬁcation procedure. The excerpt corresponds to Line 5 in Algorithm 2. The buffer tt contains the polynomial s 2 . The targeted operation is the function call in line 671 in ﬁle crypto_sign/falcon-512/m4-ct/vrfy.c. If the attacker manages to skip the function call in this line, the attack is successful for the reasons explained in Section V-A.

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:36 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 6 -->

## PDF page 6

TABLE II: F ALCON -512: Success rate of instruction skip on bne.n instruction over number of coefﬁcients of c. The numbers are the result of 50 experiments per column with the pqm4 library.

# of coefﬁcients Success rate

1 1

2 0.81

3 0.61

4 0.32

5 0.19

6 0.08

This could be achieved on an ARM Cortex-M4 by skip- ping the branch with link (bl) instruction to the function mq_poly_sub. However, the ARM Cortex-M4 machine code translation does not generate a function call to mq_poly_sub when compiled with the option -O3, because the function gets in- lined by the compiler, being deﬁned and used only once in the same ﬁle crypto_sign/falcon-512/m4-ct/vrfy.c. Listing 4 shows the corresponding assembly code. Note that the instructions on lines 4-8 correspond to the function mq_sub, which also gets inlined by the compiler, cf. line 629 in Listing 5.

Listing 4: Assembly code corresponding to the F ALCON - 512 signature veriﬁcation function verify_raw in ﬁle crypto_sign/falcon-512/m4-ct/vrfy.c

1 2

... 0x800d834 &lt;verify_raw+136&gt; bl 0x800d62c &lt; mq_iNTT&gt; 0x800d83a &lt;verify_raw+142&gt; movw r1, #12289 0x800d83e &lt;verify_raw+146&gt; ldrh.w r3, [r4, #2]! 0x800d842 &lt;verify_raw+150&gt; ldrh.w r2, [r6, #2]! 0x800d846 &lt;verify_raw+154&gt; subs r3, r3, r2 0x800d848 &lt;verify_raw+156&gt; and.w r2, r1, r3, asr #31 0x800d84c &lt;verify_raw+160&gt; add r3, r2 0x800d84e &lt;verify_raw+162&gt; cmp r9, r4 0x800d850 &lt;verify_raw+164&gt; strh r3, [r4, #0] 0x800d852 &lt;verify_raw+166&gt; bne.n 0x800d83e &lt; verify_raw+146&gt; ...

3 4 5 6 7

8 9 10 11

12

In this case, one option is to choose r such that the ﬁrst coefﬁcient of c is small enough, e.g., choose r such that the ﬁrst coefﬁcient of c is zero, and perform an instruction skip of bne.n to early-abort the loop in the mq_poly_sub function call (cf. Listing 5) and pass the ﬁnal comparison. Note that the attack works even if multiple instructions around the bne.n are skipped, e.g., all instructions from verify_raw+146 to verify_raw+166 can be safely skipped and the attack would still be successful. Furthermore, the attack works even if multiple coefﬁcients are considered, i.e., the bne.n instruc- tion is skipped after a certain number of iterations. The success probability for randomly chosen r and m over the number of coefﬁcients considered is shown in Table II. It can be observed that the success probability decreases as multiple coefﬁcients of c are included in the norm computations. This shows that there are multiple ways of attacking the mq_poly_sub and the attack is still effective in the considered attack scenario. A second option is to set logn to zero in order to early- abort the for loop, cf. line 627 in Listing 5.

86

Listing 5: Excerpt from the F ALCON -512 signature veriﬁcation function my_poly_sub in ﬁle crypto_sign/falcon-512/m4-ct/vrfy.c

618 619 620

... /* * Subtract polynomial g from polynomial f. */ static void mq_poly_sub(uint16_t *f, const uint16_t * g, unsigned logn) { size_t u, n;

621 622 623

624 625 626 627 628 629

n = (size_t)1 &lt;&lt; logn; for (u = 0; u &lt; n; u ++) { f[u] = (uint16_t)mq_sub(f [u], g[u]); }

630 631 632

} ...

The second fault attack, described in Section V-B, targets the computation of the Euclidean norm in Algorithm 2, Line 6. There are a number of ways to attack this. This is best shown by looking at the pqm4 source code. It seems plausible that other implementations are similar because there is an obvious way to compute the Euclidean norm of a vector. The veriﬁcation function verify_raw() in [19] calls a function is_short() in line 688 5 . This function veriﬁes that the signature (s 1 , s 2 ) is short. The function is_short() is implemented in common.c and shown in Listing 6. One possible target for a fault injection is the passing of the parameter logn when is_short() is called. An attacker may be able to force logn to zero. In this case, the loop in lines 252–261 that computes the Euclidean norm stops after the ﬁrst iteration. Alternatively, the attacker could inject a fault to skip the jump-instruction at the end of the loop body in line 261 back to the beginning of the loop. Again, this would lead to the loop terminating after the ﬁrst iteration. This can be observed by looking at the assembly code of Listing 7. In this case is sufﬁcient to skip the shift instruction lsls or by zeroing the content of register r2 or r5 before executing it.

Listing 7: Assembly code corresponding to the F ALCON - 512 signature veriﬁcation function is_short in ﬁle crypto_sign/falcon-512/m4-ct/common.c

1 2 3 4

... 0x8000d7a &lt;is_short+2&gt; 0x8000d7c &lt;is_short+4&gt; 0x8000d7e &lt;is_short+6&gt;

movs subs lsls

r5, #2 r0, #2 r5, r2

5 Note that Zf is a macro that just puts a pre-ﬁx in front of the function name; we can safely ignore this for our purposes here.

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:36 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 7 -->

## PDF page 7

Listing 6: Excerpt from the F ALCON -512 auxiliary func- tion that computes the Euclidean length of a vector in ﬁle crypto_sign/falcon-512/m4-ct/common.c.

237 238 239

int Zf(is_short)( const int16_t *s1, const int16_t *s2, unsigned logn) { /* * We use the l2-norm. Code below uses only 32-bit operations to * compute the square of the norm with saturation to 2ˆ32-1 if * the value exceeds 2ˆ31-1. */ size_t n, u; uint32_t s, ng;

240 241 242

243

244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267

n = (size_t)1 &lt;&lt; logn; s = 0; ng = 0; for (u = 0; u &lt; n; u ++) { int32_t z;

z = s1[u]; s += (uint32_t)(z * z); ng |= s; z = s2[u]; s += (uint32_t)(z * z); ng |= s;

} s |= -(ng &gt;&gt; 31);

/* * Acceptance bound on the l2-norm is: 1.2*1.55*sqrt(q)*sqrt(2*N) * * Value 7085 is floor((1.2ˆ2) *(1.55ˆ2)*2*1024). */ return s &lt; (((uint32_t)7085 * ( uint32_t)12289) &gt;&gt; (10 - logn));

268 269

270 }

5 6 7

... 0x8000d9c &lt;is_short+36&gt; cmp 0x8000da2 &lt;is_short+42&gt; bne.n _is_short+16&gt; ...

r5, r0 0x8000d88 &lt;

8

Note that the comparison in line 269 in Listing 6 will pass, even if the attacker forces logn to zero, because all values are unsigned integers. This can be observed by looking at the assembly code of Listing 8.

### VII. C OUNTERMEASURES

Obviously, generic countermeasures against manipulation of the control ﬂow, e.g., hardware instruction skip, make most of the attacks presented in this paper more difﬁcult to realize in practice.

87

Listing 8: Assembly code corresponding to the F ALCON - 512 signature veriﬁcation function is_short in ﬁle crypto_sign/falcon-512/m4-ct/common.c

1 2 3 4 5

... 0x8000da4 &lt;is_short+44&gt; ldr 0x8000da6 &lt;is_short+46&gt; rsb 0x8000daa &lt;is_short+50&gt; lsrs 0x8000dac &lt;is_short+52&gt; orr.w asr #31 0x8000db0 &lt;is_short+56&gt; cmp 0x8000db2 &lt;is_short+58&gt; ite 0x8000db4 &lt;is_short+60&gt; movls 0x8000db6 &lt;is_short+62&gt; movhi ...

r0, [pc, #20] r2, r2, #10 r0, r2 r12, r12, r4,

6 7 8 9 10

r0, r12 ls r0, # r0, #1

However, there are also more speciﬁc countermeasures that can be implemented to thwart our attacks. For instance, against the attack described in Section III, one can proceed as follows: the implementation generates a random u ∈ R q k and then computes Az + u and ct 1 + u. The attacked step in Algorithm 1, Line 4 then becomes

(Az + u) − (ct 1 + u).

(7)

If the attacker skips this subtraction, then, with overwhelming probability, the value w 1 computed in Algorithm 1, Line 4 is not the value w 1 calculated by the attacker. Hence, signature veriﬁcation will most likely fail. A similar countermeasure can be used against the attack in Section V-A. We modify the implementation of Algorithm 2 to generate a random u ∈ Z q [x]/(φ). Then u is added to c and to s 2 h. Consequently, Line 5 in Algorithm 2 becomes

s 1 ← (c + u) − (s 2 h + u) mod q.

(8)

If the attacker skips the inclusion of c + u in this operation, then the test in Line 6 will fail with very high probability. Finally, by checking the integrity of function parameters and introducing redundant loop counters seem to be efﬁcient countermeasures against the attack in Section V-B.

### VIII. C ONCLUSION AND FUTURE WORK

We have shown several fault injection attacks against non- obvious targets in the veriﬁcation routines of D ILITHIUM and F ALCON which allow to get forged signatures accepted for arbitrary messages. The attacks aim to demonstrate potential vulnerabilities in implementations of the veriﬁcation routines of D ILITHIUM and F ALCON which are non-obvious targets for fault attacks and which can hence be expected to have been left unprotected even by experienced designers. Following up from this work, it would be interesting to transfer our attacks to other lattice-based signature schemes. Applying our attacks against F ALCON to the signature veriﬁ- cation procedure of Mitaka [20], for example, seems straight- forward. Generalizing the attack techniques in this paper to target also ModFalcon [21] would similarly be of interest.

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:36 UTC from IEEE Xplore. Restrictions apply.

<!-- PDF_PAGE: 8 -->

## PDF page 8

Another line of research would be to consider further implementations of D ILITHIUM and F ALCON . At the moment, however, most implementations of the signature veriﬁcation procedure seem to be based on the reference code that was part of the respective submission to the NIST standardization project.

R EFERENCES

[1] J. A. Muir, “Seifert’s RSA fault attack: Simpliﬁed analysis and gener- alizations,” in ICICS 06, ser. LNCS, P. Ning, S. Qing, and N. Li, Eds., vol. 4307. Springer, Heidelberg, Dec. 2006, pp. 420–434. [2] V. Lyubashevsky, L. Ducas, E. Kiltz, T. Lepoint, P. Schwabe, G. Seiler, D. Stehlé, and S. Bai, “CRYSTALS-DILITHIUM,” Na- tional Institute of Standards and Technology, Tech. Rep., 2022, available at https://csrc.nist.gov/Projects/post-quantum-cryptography/ selected-algorithms-2022. [3] T. Prest, P.-A. Fouque, J. Hoffstein, P. Kirchner, V. Lyubashevsky, T. Pornin, T. Ricosset, G. Seiler, W. Whyte, and Z. Zhang, “FALCON,” National Institute of Standards and Technology, Tech. Rep., 2022, available at https://csrc.nist.gov/Projects/post-quantum-cryptography/ selected-algorithms-2022. [4] A. Hülsing, D. J. Bernstein, C. Dobraunig, M. Eichlseder, S. Fluhrer, S.-L. Gazdag, P. Kampanakis, S. Kölbl, T. Lange, M. M. Lau- ridsen, F. Mendel, R. Niederhagen, C. Rechberger, J. Rijneveld, P. Schwabe, J.-P. Aumasson, B. Westerbaan, and W. Beullens, “SPHINCS + ,” National Institute of Standards and Technology, Tech. Rep., 2022, available at https://csrc.nist.gov/Projects/post-quantum- cryptography/selected-algorithms-2022. [5] NIST, “NIST announces ﬁrst four quantum-resistant cryptographic algorithms,” https://www.nist.gov/news-events/news/2022/07/nist- announces-ﬁrst-four-quantum-resistant-cryptographic-algorithms, 2022, accessed 2022-12-21. [6] N. Moro, K. Heydemann, E. Encrenaz, and B. Robisson, “Formal veriﬁcation of a software countermeasure against instruction skip at- tacks,” Cryptology ePrint Archive, Report 2013/679, 2013, https:// eprint.iacr.org/2013/679. [7] J.-M. Dutertre, T. Riom, O. Potin, and J.-B. Rigaud, “Experimental anal- ysis of the laser-induced instruction skip fault model,” accessed 2023- 05-03. [Online]. Available: https://hal.science/hal-02379754/document [8] A. Menu, J.-M. Dutertre, O. Potin, J.-B. Rigaud, and J.-L. Danger, “Experimental analysis of the electromagnetic instruction skip fault model,” accessed 2023-05-03. [Online]. Available: https: //hal.science/hal-02572398/document [9] J.-P. Seifert, “On authenticated computing and rsa-based authentication,” in Proceedings of the 12th ACM Conference on Computer and Communications Security, ser. CCS ’05. New York, NY, USA: Association for Computing Machinery, 2005, p. 122–127. [Online]. Available: https://doi.org/10.1145/1102120.1102138 [10] L. G. Bruinderink and P. Pessl, “Differential fault attacks on determinis- tic lattice signatures,” IACR TCHES, vol. 2018, no. 3, pp. 21–43, 2018, https://tches.iacr.org/index.php/TCHES/article/view/7267. [11] S. McCarthy, J. Howe, N. Smyth, S. Brannigan, and M. O’Neill, “BEARZ attack FALCON: Implementation attacks with countermea- sures on the FALCON signature scheme,” Cryptology ePrint Archive, Report 2019/478, 2019, https://eprint.iacr.org/2019/478. [12] S. Bauer and F. D. Santis, “A differential fault attack against deterministic falcon signatures,” Cryptology ePrint Archive, Paper 2023/422, 2023, https://eprint.iacr.org/2023/422. [Online]. Available: https://eprint.iacr.org/2023/422 [13] N. Bindel, J. Buchmann, and J. Krämer, “Lattice-based signature schemes and their sensitivity to fault attacks,” Cryptology ePrint Archive, Report 2016/415, 2016, https://eprint.iacr.org/2016/415. [14] P. Ravi, A. Chattopadhyay, and A. Baksi, “Side-channel and fault- injection attacks over lattice-based post-quantum schemes (kyber, dilithium): Survey and new results,” Cryptology ePrint Archive, Report 2022/737, 2022, https://eprint.iacr.org/2022/737. [15] P. Ravi, B. Yang, S. Bhasin, F. Zhang, and A. Chattopadhyay, “Fiddling the twiddle constants - fault injection analysis of the number theoretic transform,” IACR TCHES, vol. 2023, no. 2, pp. 447–481, 2023.

88

[16] NIST, “Submission Requirements and Evaluation Cri- teria for the Post-Quantum Cryptography Standardiza- tion Process,” 2016, accessed 2023-05-09. [Online]. Available: https://csrc.nist.gov/CSRC/media/Projects/Post-Quantum- Cryptography/documents/call-for-proposals-ﬁnal-dec-2016.pdf [17] M. J. Kannwischer, J. Rijneveld, P. Schwabe, and K. Stoffelen, “pqm4: Testing and benchmarking NIST PQC on ARM cortex-M4,” Cryptology ePrint Archive, Report 2019/844, 2019, https://eprint.iacr.org/2019/844. [18] G. Seiler, T. Lepoint, B. Hess, M. Baentsch, P. Schwabe, B. Westerbaan, V. Hanquez, M. J. Kannwischer, oittaa, J. Schanck, and zanxu-blackhorse, “Dilithium reference implementation v3.1 on github,” accessed 2023-04-28. [Online]. Available: https://github.com/pq-crystals/dilithium/tree/v3.1 [19] T. Pornin, “Falcon source ﬁles (reference implementation) vrfy.c,” accessed 2023-05-03. [Online]. Available: https://falcon-sign.info/impl/ vrfy.c.html [20] T. Espitau, P.-A. Fouque, F. Gérard, M. Rossi, A. Takahashi, M. Ti- bouchi, A. Wallet, and Y. Yu, “Mitaka: a simpler, parallelizable, mask- able variant of falcon,” Cryptology ePrint Archive, Report 2021/1486, 2021, https://eprint.iacr.org/2021/1486. [21] C. Chuengsatiansup, T. Prest, D. Stehlé, A. Wallet, and K. Xagawa, “ModFalcon: Compact signatures based on module-NTRU lattices,” in ASIACCS 20, H.-M. Sun, S.-P. Shieh, G. Gu, and G. Ateniese, Eds. ACM Press, Oct. 2020, pp. 853–866.

Authorized licensed use limited to: Attached Institute of ETRI. Downloaded on July 23,2026 at 05:01:36 UTC from IEEE Xplore. Restrictions apply.
