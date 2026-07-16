# NixOS/nixpkgs#507531 cache scan — nixpkgs-unstable @ 35d3407a3816 (2026-07-16)

Generated: 2026-07-16 08:07:34 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 1,909,951 |
| Mach-O slices parsed | 1,643,241 |
| Page-hash mismatches (slices) | 270 |
| Page-hash mismatches (distinct packages) | 134 |
|   of which linker-signed (flags=0x20002) | 89 |
|   of which codesign-signed (flags=0x2) | 181 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 7 |
| Type 2 — distinct packages | 5 |
| Type 3 — packages directly declaring a failing build input (default view) | 0 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 728,589 | 170 | 0 | 677,530 | 50,712 | 177 |
| `arm64e` | 229 | 0 | 0 | 89 | 0 | 140 |
| `x86_64` | 602,990 | 100 | 0 | 35,157 | 567,458 | 275 |
| `i386` | 1,455 | 0 | 0 | 490 | 926 | 39 |
| other/legacy (11 arch codes) | 309,978 | 0 | 0 | 14 | 248 | 309,716 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 1,296,674 | 116 | 0 | 683,567 | 612,625 |
| fat | 346,567 | 154 | 0 | 29,713 | 6,719 |

Unique fat binary files: 327,480 in 5,847 packages. 25 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/3f1d7cjknlb5lmf5fjdffcs334chnzkq-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/7mhskg5xn99f3y19qrkc71swg6rm663m-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/a96fj054573w4a5n2xh4rpfvvfrz87lh-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/jqdz7g2x3pr91fv4k1a227vbk2zzwkbc-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/lxabgj4a939bv2s4wdxjrgb3yqfq4yjj-avalonia-ilspy-7.2-rc` |
| ffmpeg-headless-8.0.1-bin | 2 | `/nix/store/lg9r937b4q70s5qqvjhdkf7rnn5x4xvd-ffmpeg-headless-8.0.1-bin` |
| ffmpeg-headless-8.0.1-lib | 7 | `/nix/store/04iq3b9rv98l2grc82mh53w1br70ms1b-ffmpeg-headless-8.0.1-lib` |
| filen-cli-0.0.36 | 1 | `/nix/store/1c8addf04ahbkl17xp49csnm2v6s87f2-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/4iz6w1byhh65qgas9dg2cywvy36lnssn-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/5595x11jf389bj955gngxzpx11lara5n-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/77yybvq3q7dd38srfj93n84w3wjg3y4r-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/dd0g9sxbvs4sc7h6gm92gfqymf9302a1-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/md6winyqwbjwq94fw7zj8jfjz9klxjhf-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/mg7c9jnrr3704l55vjw6y55sgf0imhh1-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/q8r9hlkzlc0q9iip2258syj64y7fcv70-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/yv5dpd687w0qkkk829861cb3g9diq8zs-filen-cli-0.0.36` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/086yhdczlpdmrhw7a0xssgxc84p0bjl8-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/1b47p45agxp3ybc3r5bm5gqrnfmzni37-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/1b96pi504sfxzvq8wrv13pqkrmgflhfc-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/1xakdirg2mk3pk1qpyrk5p1hqs6m7yaq-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/3z6q05ba0mmv3b3y9jq8vgyb618jny30-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/516v4myw7xx03knkf3alcn62j7lcac37-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/5cr4w7yvdi5rnbj2lk2d12rjv10ijl3d-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/6pzd3yz3x8ib4vv4ky9i8v00q8q2nd5w-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/6v6qv6c6ix4pdshb00i4w476b9svaffi-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/73sbgp26iy1v29ygq3yf07x4ckmim21w-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/8acx3f6s0dnwizwbv74f0x5zdvah0dvv-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/aikmh7rgqwnrwawffpbdcvw0akf9nlbw-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/b8czg06qyr00kjmv90vn4k2a0m1ifgsc-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/c8i3ml8rqbrmxpwc1p6cmxpjzllg9gw9-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/dgpz5mrxak4kklvqh3fvr3706bvfvl91-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/i4k8989arfn79a1b7m9fzqcrb15dafh0-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/jq1vw06zzsy83i1x4f13zf60168psbqb-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/lyxx5v9grgp86pnr5m7wxik8md5frgw7-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/n2rfdgl7sdq3gd7s0y84anvs0dkmxm1b-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/q1d8fydpzyg5yarlysjqx1px1bg1v4zr-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/r91sl334r0k4f7f73k0g8r3in62kj212-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/sfw4r997dgdrscywhjyp9lj875vhs8hq-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/vijmlhfcw3n8bil836rwz1k0jnwfqab2-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/vvasv0jkyj78gj2zkgzxf4ayvb686ycj-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/w3jakkvd5dkaycb0b55z4hpgl0cfg8z4-gitlab-duo-8.89.0` |
| httptoolkit-1.24.4 | 1 | `/nix/store/2s8sjmvjwammxn1kmxh65xz96qdhvzhs-httptoolkit-1.24.4` |
| httptoolkit-1.24.4 | 1 | `/nix/store/47wl1p5bsk4c54r8vbkyhn3n2nm0588s-httptoolkit-1.24.4` |
| httptoolkit-1.24.4 | 1 | `/nix/store/rjxrkxzfp47bskl0543cakbx80indwm1-httptoolkit-1.24.4` |
| httptoolkit-1.26.0 | 1 | `/nix/store/nb8nvlirvjhyilzhybcfgxx4qhr8vzhv-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/r85kcr5lmws3kd02xzhz1585apc9mlfk-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/rsz3j3r7d0gl5h9d6hv17mqp9xy9vix0-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/x5l1x55hk5qvgiwshl5bakr7n2sj4ndr-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/xhn6q730vd1y8a9k0wd9lw48qg8sikim-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/zy16z8a20myjnz1v3hk5b36y4i4csh05-httptoolkit-1.26.0` |
| kilo-7.3.40 | 1 | `/nix/store/bwbxzzpgd3x201a6ikwxsv4pyni2gjx2-kilo-7.3.40` |
| libtorch-2.9.0 | 1 | `/nix/store/jd0fnglnhz9pf6vyqsdl22z65cidmz21-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/n4hxxplikjy50p40fzxghi07a6qzzk4v-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/vla1rdlyipmbynck3vq0vr51gij4fryk-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/zvflvy5rsh8wvq5rjm1qz1893n41pi1z-libtorch-2.9.0` |
| mmsyn7ukr-array-0.3.0.0 | 1 | `/nix/store/ffmz0x0yik7jgrw0ljlmg1n6y041fh2x-mmsyn7ukr-array-0.3.0.0` |
| opencode-1.14.35 | 1 | `/nix/store/g1r8yb5n0k1kpy13k16a3vw8w6admpyi-opencode-1.14.35` |
| opencode-1.14.35 | 1 | `/nix/store/npqyfwp0j1172ypv11zmzx0qias179wd-opencode-1.14.35` |
| opencode-1.14.35 | 1 | `/nix/store/q95hrhjnsk49f6h70p0hym0a3pk73v9q-opencode-1.14.35` |
| opencode-1.14.48 | 1 | `/nix/store/js2z13p2d8ym7j3x6dx58vdkk2z36bpa-opencode-1.14.48` |
| opencode-1.15.10 | 1 | `/nix/store/wlwjm1g4qgqpnxkddzrxkz0wbgwjcj5p-opencode-1.15.10` |
| opencode-1.15.11 | 1 | `/nix/store/cpc1xsvv08azx11c8y6zp68xv1czdkfr-opencode-1.15.11` |
| opencode-1.15.13 | 1 | `/nix/store/8ilya8lkzz57a1cpfgfp51qk6h3q5g1f-opencode-1.15.13` |
| opencode-1.15.5 | 1 | `/nix/store/r0xz5ic3z79r3anfssz60j8bbjls6n4d-opencode-1.15.5` |
| opencode-1.15.7 | 1 | `/nix/store/swvx6k42qawwj376byi0fxjiy3yf9yb9-opencode-1.15.7` |
| opencode-1.16.2 | 1 | `/nix/store/380vjma5320nknl45fkvyhaiz6gnxgyv-opencode-1.16.2` |
| opencode-1.17.18 | 1 | `/nix/store/48nsg3qq5rrzj2a54y05miz02hn0jr2p-opencode-1.17.18` |
| opencode-1.17.20 | 1 | `/nix/store/aid0cvplsifb414j8fysm0ynlbxpzi99-opencode-1.17.20` |
| opencode-1.17.4 | 1 | `/nix/store/p23042pa3iqf4gaiihdpbvkp9gs5ky4c-opencode-1.17.4` |
| opencode-1.17.7 | 1 | `/nix/store/yxclajlc2f9b6wiwa0hazn1xqy42py5x-opencode-1.17.7` |
| opencode-1.17.9 | 1 | `/nix/store/4jp729qvs98la97zvnsrwfkm4flzcb5g-opencode-1.17.9` |
| qtcharts-5.15.19-bin | 1 | `/nix/store/dvdsnrnf7mipl6y1ab6psv3wkkj7815x-qtcharts-5.15.19-bin` |
| shogihome-1.27.1 | 1 | `/nix/store/rhagbi0fyfqfnizrdhag5j6cmyqym4jx-shogihome-1.27.1` |
| shogihome-1.27.2 | 1 | `/nix/store/1cwb73vi5aa1nlpbr7ychywlbmkpl19l-shogihome-1.27.2` |
| shogihome-1.27.2 | 1 | `/nix/store/5xvqqb06qb22vz2jfz8mn80w9ma2fzby-shogihome-1.27.2` |
| shogihome-1.27.3 | 1 | `/nix/store/0fs5gp49028zmf208lfrha0hhvsj2bxm-shogihome-1.27.3` |
| shogihome-1.27.3 | 1 | `/nix/store/26lk67lykhcrnlrshv2gigpl8v3jlkkj-shogihome-1.27.3` |
| shogihome-1.27.3 | 1 | `/nix/store/63fx8404ppm6n773sdkcwvwhfwggai5g-shogihome-1.27.3` |
| shogihome-1.27.3 | 1 | `/nix/store/qj3ifm7z75y5j7mjch9sah0jwabqr35x-shogihome-1.27.3` |
| shogihome-1.27.3 | 1 | `/nix/store/srly270piz0pjdd6rsvjx1lr51ijf3wc-shogihome-1.27.3` |
| shogihome-1.28.0 | 1 | `/nix/store/ar1vm01pf61ras376h4lvlii1pzdj39q-shogihome-1.28.0` |
| shogihome-1.28.0 | 1 | `/nix/store/zdl6c1ajlpv6aawc8zg9hfadx84164pz-shogihome-1.28.0` |
| stache-2.3.4 | 1 | `/nix/store/19vf8xbrlh0i4qqvqvvqpc1jxy1klvz8-stache-2.3.4` |
| swift-5.10.1 | 11 | `/nix/store/8dv7sip8h5w8xjkpkh4ynijd00klhqx5-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/f7d3lcdzanmqw5icnxkgcx6kqha1ibif-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/g8ifnf6b7v65bp2hl78i5mrjc8kbblaw-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/p1fpxz9l7rc91fzp0ckwrsxmizqmbvc1-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/qg9vqxfpaqq8cra97dpxk7l2ry1bsrax-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/wr4k2mpjkgkmh39xy4gcrmhcc07wrvbd-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/1vpqmjivp6j62rcpkrr86pirpn12fzaq-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/85sw2bgkpnqnsrj324cz61hxf7r57v5i-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/9hxyg2mlvpmwdk7v027p9kchdysjcwfm-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/h2zz94xy40rnil834vjvikkvrxcsc96n-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/i7j1sls91fmn5vynqryfwhn463mv3jn0-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/ihs1bjs31gl8kcxdwp896jnbawg73jwf-swift-5.10.1-lib` |
| tailwindcss_4-4.2.4 | 1 | `/nix/store/36fkkxav9kvwn0g3571gf3cay92vwyix-tailwindcss_4-4.2.4` |
| tailwindcss_4-4.2.4 | 1 | `/nix/store/fpcmaqm4a8df6c38wzh5lz7s7d12178q-tailwindcss_4-4.2.4` |
| tailwindcss_4-4.3.0 | 1 | `/nix/store/1ir3rnq4a4z963c81sz3mcab35jflm43-tailwindcss_4-4.3.0` |
| tailwindcss_4-4.3.0 | 1 | `/nix/store/8mfvp0gg4igjs62dj457rprvx0lnwxv2-tailwindcss_4-4.3.0` |
| tailwindcss_4-4.3.0 | 1 | `/nix/store/m01q2947z343bhqh59fdc1xzsi9ni8h9-tailwindcss_4-4.3.0` |
| tailwindcss_4-4.3.0 | 1 | `/nix/store/rcdpbw2hfzljsmvrdcjny1brix3xy1fv-tailwindcss_4-4.3.0` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/12pf68d4awjxb9vk6icli7asdqyrcah3-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/4cmsm0k1pyl0pl0ph37gizg3ydgqcpym-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/96qqbp9z1lsq9bwxw2fbxmjnyqclb86q-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/hgw2ymc5nan6xmil94m6akz27r858fr6-tailwindcss_4-4.3.1` |
| teams-for-linux-2.10.0 | 1 | `/nix/store/4qsz50ns5gj04lvfbfjji53lxbqnw3fp-teams-for-linux-2.10.0` |
| teams-for-linux-2.10.0 | 1 | `/nix/store/bw8x9wyvi6vbhjwjpjisq982s02217mb-teams-for-linux-2.10.0` |
| teams-for-linux-2.10.0 | 1 | `/nix/store/q2dbgmblhxcc0dq5a5yv1adyz0i5hfzm-teams-for-linux-2.10.0` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/gbynyrlfxk4yj43brc82vvj7lbsx094k-teams-for-linux-2.11.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/ic4227vk2dfpz3x4w43l52cx6s1cnzl3-teams-for-linux-2.11.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/qa5nqwj53a86i4d743750s3ck83vh8iq-teams-for-linux-2.11.1` |
| teams-for-linux-2.12.0 | 1 | `/nix/store/nwzcinamw9gjq82i85qfzdi3lx0wy7pl-teams-for-linux-2.12.0` |
| teams-for-linux-2.12.0 | 1 | `/nix/store/xmmnpmdm1ddkwmrk6wagha09jb3i84lk-teams-for-linux-2.12.0` |
| teams-for-linux-2.13.0 | 1 | `/nix/store/l7nklpmmz4a8ff3a54scx1siwzwzwnnh-teams-for-linux-2.13.0` |
| teams-for-linux-2.13.0 | 1 | `/nix/store/y529h7db6gfdwgcwnxc6dfvqwhxxy8jh-teams-for-linux-2.13.0` |
| teams-for-linux-2.13.0 | 1 | `/nix/store/zsmpnhbmprfqppvmjlnkqnbdgp50n1rz-teams-for-linux-2.13.0` |
| teams-for-linux-2.8.1 | 1 | `/nix/store/a36aakz4z3ihzamlvkq6384c3vqp8pcb-teams-for-linux-2.8.1` |
| teams-for-linux-2.9.0 | 1 | `/nix/store/f1r0hs7dgi6wfv59ms698gnlv76n09wb-teams-for-linux-2.9.0` |
| teams-for-linux-2.9.0 | 1 | `/nix/store/kdjbkgsi89f7n9ldhfvfficl76593vlg-teams-for-linux-2.9.0` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/5p0fv320r59zjq0g8vdlszqc9m9a5cnc-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/pdf6h2gw3a1m466w03j4ibxrfbd289ms-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/pgpzrqgvw4h1285bhmvsxy7kcl7ivb74-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/rriv3xrcfw1pw899n7x3q34ijfd5wis3-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.3.53 | 1 | `/nix/store/83fagcxfn9xbrc7fc0hvl829kmz1mn9j-vscode-extension-kilocode-Kilo-Code-7.3.53` |
| vscode-extension-kilocode-Kilo-Code-7.3.53 | 1 | `/nix/store/hx2mmww8s5rpqcgbx16n6l687qnxp8v3-vscode-extension-kilocode-Kilo-Code-7.3.53` |
| vscode-extension-kilocode-Kilo-Code-7.3.53 | 1 | `/nix/store/z4w98bdd5cnx11icxgp5mb16lrv9ka28-vscode-extension-kilocode-Kilo-Code-7.3.53` |
| zotero-9.0.4 | 2 | `/nix/store/6iblj6gh65199c25xqjr4fvc88ihb9qq-zotero-9.0.4` |
| zotero-9.0.4 | 2 | `/nix/store/8vrnwr7262535s80p6qaabic6rdj2122-zotero-9.0.4` |
| zotero-9.0.5 | 2 | `/nix/store/0z1h0cmxzvg0r6prghf40n6x75c4rgr1-zotero-9.0.5` |
| zotero-9.0.5 | 2 | `/nix/store/42wp3frqjb4mxr7zi2dgx3sd1q7k7342-zotero-9.0.5` |
| zotero-9.0.5 | 2 | `/nix/store/dhqh6xagy29z5pfzpmx1klfzbrbxpia5-zotero-9.0.5` |
| zotero-9.0.5 | 2 | `/nix/store/lnzd55wxk4c66h29m3p4358ciq1kqjpz-zotero-9.0.5` |
| zotero-9.0.5 | 2 | `/nix/store/xwqvg33kca6i6bk8s3bk4fhd50z0qq4c-zotero-9.0.5` |
| zotero-9.0.5 | 2 | `/nix/store/z65xvsv5cxlbkds7i0byxpap6yfrnf6c-zotero-9.0.5` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 270 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 713,280 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 619,344 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 310,347 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 7 |
| Distinct packages containing such binaries | 5 |
| Failing dylibs that serve as seeds | 136 |
| Total (binary, failing-dylib) pairs | 153 |

Top failing dylibs by number of downstream binaries:

| Seed package | Downstream binaries |
|---|---:|
| `ffmpeg-headless-8.0.1-lib` | 153 |

Dependent packages (5): `cliairplay-1.1-unstable-2026-03-16`, `cyanrip-0.9.3.1`, `ffmpegthumbnailer-2.3.0`, `gst-libav-1.26.11`, `musikcube-3.0.5`

Full detail: [`load-time-dependents.csv`](load-time-dependents.csv) (one row per `(binary, linked_failing_dylib)` pair).
## Build-time dependents

Packages whose nix expression **directly declares** a direct-failing package as `buildInputs`, `nativeBuildInputs`, `checkInputs`, or `nativeCheckInputs` (1-hop). If the failing binary is invoked during the package's build phase, Hydra fails and the package never reaches the cache. This is a graph-level relationship: whether each listed package actually invokes the failing binary during build is not statically determinable. The canonical confirmed case is direnv — its `nativeCheckInputs = [ fish ]` with a `checkPhase` running `fish ./test/direnv-test.fish`, origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

Default view excludes `propagatedBuildInputs` / `propagatedNativeBuildInputs` edges (propagation threads the input forward; the listed package itself doesn't invoke it). The CSV includes all edge kinds for manual inspection.

| Metric | Count |
|---|---:|
| Packages with failing seeds in declared build/check inputs (default view) | 0 |
| Total direct-edge rows (default view) | 0 |
| Total rows including propagated edges | 0 |
| Distinct failing seeds | 134 |

Full detail: [`build-time-dependents.csv`](build-time-dependents.csv) (one row per `(dependent, edge_kind, seed)` tuple; `in_default_view=true` marks default-filter rows).

## Methodology

- Input: `store-paths.xz` from the channel release URL.
- Per path: `<hash>.narinfo` → stream NAR over HTTP → decompress (xz/zstd/bz2) inline → walk entries, no on-disk NAR persistence.
- Per regular file: peek 4 bytes; buffer and analyze only if Mach-O magic matches.
- Per Mach-O slice (thin or fat): parse `LC_CODE_SIGNATURE`, pick the primary CodeDirectory (SHA-256 preferred over SHA-1 when both are present, matching the kernel's selection order), recompute per-page hash over `data[i*ps : min((i+1)*ps, code_limit)]` with the CD's own algorithm, compare against the stored hash slot.
- `page_hash_mismatch` is defined as: at least one computed per-page hash disagrees with its stored hash slot. This matches the kernel's page-in validator and `codesign -v` rejection criterion for adhoc-signed binaries.
- `other_sig_invalid` is defined as: LC_CODE_SIGNATURE is present but the signature blob is structurally unparseable (e.g. payload OOB, bad SuperBlob magic, unsupported hash type such as SHA-384).
- Scanner source: see the PR repo.

