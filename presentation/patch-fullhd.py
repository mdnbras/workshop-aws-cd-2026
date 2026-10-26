from pathlib import Path

path = Path(__file__).with_name("index.html")
html = path.read_text(encoding="utf-8")

marker = "/* fullhd-density-v1 */"
if marker in html:
    print("Full HD typography patch already applied.")
    raise SystemExit(0)

css = r'''
    /* fullhd-density-v1 */
    @media (min-width: 1200px) and (max-height: 1100px) {
      .slide{padding:42px 54px 62px}
      .inner{width:min(1280px,100%)}

      h1{font-size:clamp(44px,5.3vw,78px)!important;line-height:.98!important;margin:16px 0 14px!important;max-width:1040px}
      h2{font-size:clamp(32px,3.8vw,52px)!important;line-height:1.04!important;margin:12px 0 16px!important}
      h3{font-size:20px!important;margin-bottom:8px!important}
      p{font-size:17px!important;line-height:1.42!important}
      .lead{font-size:clamp(19px,1.8vw,26px)!important;line-height:1.34!important;max-width:860px}
      .quote{font-size:clamp(28px,3.1vw,44px)!important}

      .eyebrow{font-size:11px!important;padding:6px 10px!important;gap:7px}
      .eyebrow .dot{width:6px;height:6px}
      .pill{font-size:11px!important;padding:7px 10px!important}
      .brand-strip{margin-top:18px!important;gap:8px!important}

      .hero-grid{gap:24px!important}
      .hero-card{padding:20px!important;min-height:220px!important;border-radius:26px!important}
      .hero-card .mini{font-size:12px!important}
      .hero-card .big{font-size:50px!important}

      .grid-2{gap:16px!important;margin-top:20px!important}
      .grid-3{gap:14px!important;margin-top:20px!important}
      .grid-4{gap:12px!important;margin-top:18px!important}
      .card{padding:18px!important;min-height:132px!important;border-radius:22px!important}
      .card strong{font-size:19px!important;margin-bottom:7px!important}
      .card p{font-size:15px!important}

      .timeline{gap:10px!important;margin-top:22px!important}
      .time-card{padding:15px!important;min-height:116px!important;border-radius:18px!important}
      .time-card .time{font-size:12px!important;margin-bottom:8px!important}
      .time-card b{font-size:16px!important}
      .time-card p{font-size:14px!important}

      .diagram{margin-top:22px!important;padding:20px!important;border-radius:22px!important}
      .flow{gap:8px!important}
      .node{padding:13px 16px!important;min-width:112px!important;border-radius:15px!important;font-size:14px!important}
      .arrow{font-size:24px!important}

      .branch{gap:12px!important}
      .branch-code{font-size:15px!important;padding:12px 14px!important;border-radius:14px!important}
      .code{margin-top:18px!important;padding:16px 18px!important;border-radius:18px!important;font-size:14px!important;line-height:1.42!important;max-height:38vh}

      .compare{grid-template-columns:1fr 68px 1fr!important;gap:14px!important;margin-top:22px!important}
      .center-badge{width:54px!important;height:54px!important;font-size:13px!important}

      .list{gap:9px!important;margin-top:18px!important}
      .list-item{gap:10px!important;font-size:16px!important}
      .check{width:23px!important;height:23px!important;font-size:12px!important}
      .num{width:30px!important;height:30px!important;border-radius:10px!important;font-size:13px!important}
      .step{gap:11px!important}

      .callout{margin-top:18px!important;padding:13px 16px!important;border-radius:15px!important;font-size:15px!important}
      .aside{margin-top:16px!important;font-size:13px!important}
      .two-col{gap:18px!important;margin-top:14px!important}
      .status-line{gap:9px!important;margin-top:12px!important;font-size:14px!important}
      .status-dot{width:9px;height:9px}

      .architecture-stack{gap:13px!important;margin-top:20px!important}
      .stack-title{font-size:11px!important}
      .mini-card{padding:12px 14px!important;border-radius:14px!important;font-size:14px!important}
      .big-topic{padding:24px!important;border-radius:22px!important;font-size:21px!important}

      .footer{font-size:10px!important;bottom:12px!important}
      .slide-count{font-size:10px!important}
      .ctrl{height:32px!important;min-width:32px!important;font-size:12px!important;padding:0 9px!important}
      .controls{top:14px!important;right:16px!important}

      /* Inline sizing used by the animated comparison slide */
      .slide[data-title="Síncrono vs Assíncrono — resultado final"] p[style*="font-size"]{font-size:14px!important}
      .slide[data-title="Síncrono vs Assíncrono — resultado final"] strong[style*="font-size"],
      .slide[data-title="Síncrono vs Assíncrono — resultado final"] div[style*="font-size"]{font-size:13px!important}
    }

    @media (min-width: 1200px) and (max-height: 900px) {
      .slide{padding:34px 48px 52px}
      h1{font-size:clamp(40px,4.8vw,68px)!important}
      h2{font-size:clamp(28px,3.4vw,46px)!important}
      p{font-size:15px!important}
      .lead{font-size:22px!important}
      .card{padding:15px!important;min-height:112px!important}
      .diagram{margin-top:16px!important;padding:16px!important}
      .code{font-size:13px!important;max-height:34vh}
      .list{margin-top:14px!important}
      .callout{margin-top:14px!important}
      .grid-2,.grid-3,.grid-4{margin-top:16px!important}
      .timeline{margin-top:16px!important}
    }
'''

needle = "  </style>"
if needle not in html:
    raise RuntimeError("Could not find </style> in presentation/index.html")

html = html.replace(needle, css + "\n" + needle, 1)
path.write_text(html, encoding="utf-8")
print("Full HD typography density patch applied.")
