HTML=r"""<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>StokLedger Pro Ultima by ACIS</title><link rel="icon" href="/assets/stokledger-icon.png">
<style>body{font-family:Segoe UI,Arial;background:#edf5f6;margin:0;color:#17343a}.wrap{max-width:1250px;margin:24px auto;padding:16px}.card{background:#fff;border-radius:15px;padding:20px;box-shadow:0 7px 25px #17343a18;margin-bottom:16px}h1,h2{color:#087f8c}h1{margin:0}.muted{color:#647a7f}.row{display:flex;gap:9px;flex-wrap:wrap}.row>*{flex:1;min-width:125px}input,select,textarea,button{box-sizing:border-box;padding:9px 11px;border:1px solid #bacacc;border-radius:8px;font:inherit}button{background:#087f8c;color:white;border:0;cursor:pointer;flex:0 0 auto}.secondary{background:#60777c}.danger{background:#b42318}.hidden{display:none}.nav{display:flex;gap:7px;flex-wrap:wrap;margin:15px 0}.nav button{background:#d9eff1;color:#075e67}.nav button.active{background:#087f8c;color:#fff}.page{display:none}.page.active{display:block}table{width:100%;border-collapse:collapse;font-size:14px}.accounting-manual{overflow-x:auto}.accounting-manual table{min-width:1120px}.accounting-manual th,.accounting-manual td{white-space:nowrap}.accounting-manual input,.accounting-manual select{min-width:115px}th,td{padding:8px;border-bottom:1px solid #e1eaec;text-align:left}.stat{padding:15px;background:#f1f8f9;border-radius:12px;min-width:150px}.stat b{display:block;font-size:23px;color:#087f8c}.ok{color:#067647}.error{color:#b42318}.sale-line{display:grid;grid-template-columns:2.4fr 2fr .8fr 1.2fr 1.1fr 1.2fr auto;gap:7px;margin:7px 0}.right{text-align:right}
.form-section{border:1px solid #dbe7e9;background:#f8fbfb;border-radius:12px;padding:16px;margin:14px 0}.form-section h3{margin:0 0 4px;color:#087f8c}.section-help{margin:0 0 13px;color:#647a7f;font-size:13px}.field-grid{display:grid;grid-template-columns:repeat(4,minmax(160px,1fr));gap:12px}.field-grid.three{grid-template-columns:repeat(3,minmax(180px,1fr))}.field-grid.two{grid-template-columns:repeat(2,minmax(220px,1fr))}.field{display:flex;flex-direction:column;gap:6px;min-width:0}.field>span{font-weight:600;color:#24484e;font-size:13px}.field small{font-weight:400;color:#71868a;line-height:1.25}.field input,.field select,.field textarea{width:100%;background:#fff}.required{color:#b42318}.action-bar{display:flex;align-items:center;justify-content:flex-end;gap:10px;margin-top:14px}.summary-box{margin-left:auto;min-width:260px;background:#eaf6f7;border:1px solid #b9dfe3;border-radius:12px;padding:14px}.summary-row{display:flex;justify-content:space-between;gap:20px;padding:3px 0}.summary-row.total{font-size:18px;font-weight:700;color:#087f8c;border-top:1px solid #b9dfe3;margin-top:6px;padding-top:8px}.line-header{display:grid;grid-template-columns:3fr 1fr 1.4fr 1.3fr 1.3fr auto;gap:7px;font-weight:700;font-size:13px;color:#24484e;padding:5px 0}.purchase-line-editor{display:grid;grid-template-columns:2.3fr .8fr 1.2fr 1.1fr 1.2fr auto;gap:10px;align-items:end}.hint{background:#fff8e6;border:1px solid #f6d78b;color:#745000;padding:10px 12px;border-radius:9px;font-size:13px}.table-toolbar{display:flex;gap:9px;flex-wrap:wrap;align-items:center}.table-toolbar h2{margin-right:auto}.wide-note{grid-column:1/-1}.transaction-title{display:flex;align-items:flex-start;justify-content:space-between;gap:15px}.transaction-title h2{margin-bottom:4px}.field input:focus,.field select:focus,.field textarea:focus{outline:2px solid #73c5cc;border-color:#087f8c}@media(max-width:950px){.field-grid,.field-grid.three{grid-template-columns:repeat(2,minmax(180px,1fr))}.purchase-line-editor{grid-template-columns:repeat(2,minmax(160px,1fr))}.line-header{display:none}}@media(max-width:600px){.field-grid,.field-grid.three,.field-grid.two{grid-template-columns:1fr}.summary-box{width:100%;min-width:0}.action-bar{flex-wrap:wrap}.purchase-line-editor{grid-template-columns:1fr}}
@media(max-width:800px){.sale-line{grid-template-columns:1fr 1fr}.sale-line select{grid-column:1/-1}}
/* Modern desktop-style sidebar layout v1.3.0 */
:root{--navy:#102a43;--navy2:#173f5f;--teal:#0e8793;--teal-soft:#dff4f5;--surface:#ffffff;--bg:#eef3f7;--line:#d9e2ec;--text:#243b53;--muted:#6b7c93;--shadow:0 8px 28px rgba(16,42,67,.09)}
body{background:var(--bg);color:var(--text);overflow-x:hidden}
.wrap{max-width:none;margin:0;padding:0;min-height:100vh}
.wrap> .card:first-child{display:none}
#login{max-width:520px;margin:9vh auto;background:#fff;border-top:5px solid var(--teal);box-shadow:var(--shadow);padding:30px}
#app:not(.hidden){display:grid;grid-template-columns:270px minmax(0,1fr);min-height:100vh;align-items:start}
.sidebar{position:sticky;top:0;height:100vh;box-sizing:border-box;margin:0;border-radius:0;padding:18px 14px;background:linear-gradient(180deg,var(--navy),#0b2033);color:#fff;box-shadow:8px 0 28px rgba(16,42,67,.13);overflow-y:auto;z-index:20}
.brand-block{display:flex;align-items:center;gap:11px;padding:4px 7px 17px;border-bottom:1px solid rgba(255,255,255,.13);margin-bottom:13px}.brand-block strong{display:block;font-size:17px}.brand-block small{display:block;color:#b9d1df;font-size:11px;margin-top:2px}.brand-mark{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#14b8a6,#22d3ee);display:flex;align-items:center;justify-content:center;font-weight:800;color:#073b4c;box-shadow:0 6px 15px rgba(34,211,238,.25)}
.server-user{padding:8px 8px 12px}.server-user b{font-size:13px;color:#fff}.server-user .muted{color:#9fb8c7;font-size:11px;margin-top:3px}
.nav{display:flex;flex-direction:column;gap:3px;margin:0}.nav-group{font-size:10px;letter-spacing:.12em;color:#7897aa;padding:15px 10px 5px;font-weight:700}.nav button{display:flex;align-items:center;gap:10px;width:100%;padding:9px 11px;border-radius:8px;background:transparent;color:#d8e7ef;text-align:left;font-size:13px;transition:.15s ease;box-shadow:none}.nav button:hover{background:rgba(255,255,255,.09);color:#fff;transform:translateX(2px)}.nav button.active{background:linear-gradient(90deg,var(--teal),#10a5af);color:#fff;box-shadow:0 5px 13px rgba(14,135,147,.28)}.nav-icon{width:18px;text-align:center;font-size:15px;opacity:.95}
.logout-btn{width:100%;margin-top:18px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);color:#fff}.logout-btn:hover{background:#a83b3b}
.page{grid-column:2;padding:22px 26px 34px;min-width:0}.page.active{display:block}.page>.card:first-child,.page.card{border-top:3px solid var(--teal)}
.card{border-radius:12px;box-shadow:var(--shadow);border:1px solid rgba(217,226,236,.8);margin-bottom:17px;padding:19px;background:var(--surface)}
h1,h2,h3{color:var(--navy2)}h2{font-size:19px;margin-top:0}.transaction-title h2,.table-toolbar h2{color:var(--navy2)}
button{background:var(--teal);border-radius:7px;font-weight:600;font-size:13px;transition:.15s ease}button:hover{filter:brightness(.95);transform:translateY(-1px)}button.secondary{background:#526d82}
input,select,textarea{border-color:#cbd7e1;background:#fff;border-radius:7px}input:hover,select:hover,textarea:hover{border-color:#91a7b8}.field>span,label{color:#334e68}
.form-section{background:#f8fafc;border-color:#dce6ed;border-radius:10px}.form-section h3{color:var(--navy2)}
table{background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden}thead th{background:#e8f1f5;color:#243b53;font-size:12px;text-transform:uppercase;letter-spacing:.025em;position:sticky;top:0;z-index:2}tbody tr:nth-child(even){background:#f9fbfc}tbody tr:hover{background:#eaf7f8}th,td{border-bottom:1px solid #e4ebf0;padding:9px 10px}
.stat{background:linear-gradient(135deg,#fff,#eef8f8);border:1px solid #d7e9eb;box-shadow:0 4px 14px rgba(16,42,67,.05)}.stat b{color:var(--teal);margin-top:5px}
.summary-box{background:#edf8f8;border-color:#b8e0e3}.summary-row.total{color:var(--teal)}
.table-toolbar{background:#f8fafc;border-radius:9px;padding:9px 10px;margin-bottom:10px;border:1px solid #e1e9ef}.table-toolbar h2{margin:0}
.muted,.help,.section-help{color:var(--muted)}
@media(max-width:900px){#app:not(.hidden){grid-template-columns:220px minmax(0,1fr)}.sidebar{padding:14px 9px}.page{padding:16px}.nav button{font-size:12px}.brand-block small{display:none}}
@media(max-width:680px){#app:not(.hidden){display:block}.sidebar{position:relative;height:auto}.nav{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.nav-group{grid-column:1/-1}.page{padding:12px}.logout-btn{margin-bottom:4px}}
.analytics-grid{display:grid;grid-template-columns:minmax(360px,1.35fr) repeat(2,minmax(280px,1fr));gap:16px;align-items:start}.reminder-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.reminder-grid>div{max-height:360px;overflow-y:auto;overscroll-behavior:contain}.reminder-grid>div h3{position:sticky;top:0;background:var(--card,#fff);z-index:2;padding:6px 0;margin-top:0}.bar-row{display:grid;grid-template-columns:120px 1fr 80px;gap:8px;align-items:center}.bar-row i{height:12px;background:#0e8793;display:block}.cash-section,.inventory-section,.accounting-section{display:block}@media(max-width:900px){.analytics-grid,.reminder-grid{grid-template-columns:1fr}}
.module-nav{gap:10px}.module-nav button{min-height:54px;font-size:14px}.module-shell{min-height:calc(100vh - 70px)}.module-header{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;margin-bottom:20px}.eyebrow{font-size:11px;letter-spacing:.16em;color:#0e8793;font-weight:800;margin:0 0 4px}.module-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px}.module-card{border:1px solid #d6e3e8;background:linear-gradient(145deg,#fff,#f6fbfc);border-radius:16px;padding:20px;min-height:150px;cursor:pointer;transition:.18s ease;box-shadow:0 7px 18px rgba(22,55,73,.06);display:flex;flex-direction:column;justify-content:space-between}.module-card:hover{transform:translateY(-3px);border-color:#19a7b4;box-shadow:0 14px 28px rgba(14,135,147,.15)}.module-card-icon{width:48px;height:48px;border-radius:14px;background:#dff5f7;color:#087f8c;display:grid;place-items:center;font-size:25px;font-weight:700}.module-card h3{margin:14px 0 6px;color:#123b5a}.module-card p{margin:0;color:#6d8794;font-size:13px;line-height:1.45}.module-card small{display:block;margin-top:12px;color:#0e8793;font-weight:700}@media(max-width:700px){.module-header{display:block}.module-header button{margin-top:10px}.module-grid{grid-template-columns:1fr}}

/* StokLedger branding v1.4.4a */
:root{
  --brand-green:#138a36;
  --brand-blue:#084fbd;
  --brand-orange:#ff8a00;
  --teal:#0d8f99;
}
#app:not(.hidden){grid-template-columns:310px minmax(0,1fr)}
.sidebar{padding:18px 16px;background:linear-gradient(180deg,#092b50 0%,#0b3158 55%,#08243f 100%)}
.brand-logo-block{display:block;padding:8px 8px 18px;text-align:center}
.sidebar-logo{width:100%;max-width:250px;height:auto;display:block;margin:0 auto 8px;filter:drop-shadow(0 5px 10px rgba(0,0,0,.17));border-radius:7px;background:#fff;padding:5px}
.brand-copy strong{font-size:20px;line-height:1.2;color:#fff}
.brand-copy small{font-size:12px;line-height:1.35;color:#c8dceb}
.server-user{padding:12px 10px 14px}.server-user b{font-size:15px}.server-user .muted{font-size:13px}
.module-nav{gap:8px}
.nav button{min-height:58px;padding:13px 14px;font-size:17px;font-weight:650;border-radius:12px;line-height:1.2}
.nav-icon{width:27px;font-size:22px}
.nav button.active{background:linear-gradient(90deg,var(--brand-green),#17a553);box-shadow:0 7px 18px rgba(19,138,54,.32)}
.nav button:hover{background:rgba(255,255,255,.12)}
.logout-btn{min-height:48px;font-size:16px}
.module-grid{grid-template-columns:repeat(auto-fill,minmax(245px,1fr));gap:20px}
.module-card{min-height:180px;padding:24px;border-radius:18px;border-top:4px solid var(--brand-blue)}
.module-card:nth-child(3n+2){border-top-color:var(--brand-green)}
.module-card:nth-child(3n+3){border-top-color:var(--brand-orange)}
.module-card-icon{width:58px;height:58px;font-size:30px}
.module-card h3{font-size:20px;margin:17px 0 8px}
.module-card p{font-size:15px;line-height:1.55}
.module-card small{font-size:14px}
.module-header h2{font-size:27px}.module-header .muted{font-size:15px}
.login-logo{display:block;width:min(100%,390px);height:auto;margin:0 auto 22px}
#login h2{text-align:center;font-size:25px}
#login input,#login button{font-size:16px;min-height:48px}
@media(max-width:1050px){
  #app:not(.hidden){grid-template-columns:270px minmax(0,1fr)}
  .sidebar-logo{max-width:220px}
  .nav button{font-size:15px;min-height:52px}
}
@media(max-width:680px){
  .sidebar-logo{max-width:280px}
  .nav button{font-size:16px}
}

.income-report{max-width:820px;margin:18px auto}.income-row,.income-total,.income-grand{display:flex;justify-content:space-between;padding:9px 12px;border-bottom:1px solid var(--line)}.income-total{font-weight:700;background:#f3f7f8}.income-grand{font-size:18px;font-weight:800;margin-top:10px;border-radius:8px}.income-grand.gross{background:#fff3cd}.income-grand.net{background:#dff7e6;color:#12612c}.table-scroll{max-height:560px;overflow:auto}.table-scroll thead th{position:sticky;top:0;background:#e7f0f4}.import-desc{min-width:340px;white-space:normal}.import-coa{min-width:250px}.import-partner{min-width:220px}.page#smartImport .accounting-section{display:none!important}.page#smartImport .income-report{display:none!important}.field-grid.four{grid-template-columns:repeat(4,minmax(180px,1fr))}.report-filter{display:none}.table-scroll{max-height:620px;overflow:auto}.table-scroll thead th{position:sticky;top:0;background:#e7f0f4;z-index:2}@media(max-width:1100px){.field-grid.four{grid-template-columns:repeat(2,1fr)}}@media(max-width:700px){.field-grid.four{grid-template-columns:1fr}}.button-like{display:inline-flex;align-items:center;background:#087f8c;color:#fff;padding:9px 14px;border-radius:7px;cursor:pointer;font-weight:600}.doc-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 18px}.doc-tabs button.active{background:#0d8f99;color:white}.doc-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.doc-tabs button.active{background:#087f8c;color:#fff}.designer-checks{display:grid;grid-template-columns:repeat(2,minmax(180px,1fr));gap:10px;margin:14px 0}.designer-widths{margin:16px 0;padding:12px;border:1px solid #d5e2e6;border-radius:9px;background:#f8fbfc}.designer-widths h4{margin:0 0 5px}.designer-widths>p{margin:0 0 10px}.designer-width-grid{display:grid;grid-template-columns:repeat(4,minmax(120px,1fr));gap:9px}.designer-width-grid label{display:flex;flex-direction:column;gap:4px;font-size:12px}.designer-width-grid input{width:100%}@media(max-width:800px){.designer-width-grid{grid-template-columns:repeat(2,1fr)}}.designer-checks label{display:flex;gap:8px;align-items:center}@media(max-width:650px){.designer-checks{grid-template-columns:1fr}}.designer-layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(340px,.9fr);gap:18px;align-items:start}.designer-preview-wrap{position:sticky;top:12px}.preview-toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}.document-preview{background:#eef3f4;padding:12px;border:1px solid #cbd8dc;border-radius:10px;overflow:auto}.preview-sheet{background:#fff;margin:auto;padding:18px;color:#1d2b32;box-shadow:0 2px 10px #607d8b44}.preview-a5{max-width:520px;min-height:735px}.preview-a4{max-width:650px;min-height:920px}.preview-letter{max-width:665px;min-height:860px}.preview-header{display:grid;grid-template-columns:70px 1fr auto;gap:10px;align-items:start;border-bottom:2px solid #087f8c;padding-bottom:8px}.preview-logo{height:48px;border:1px dashed #8ca5ab;display:grid;place-items:center;font-size:11px}.preview-company{display:flex;flex-direction:column;font-size:11px}.preview-company strong{font-size:14px;color:#075f68}.preview-title{text-align:right}.preview-title h2{font-size:15px;margin:0}.preview-title b{font-size:10px}.preview-note{margin-top:8px;padding:7px;background:#f1f8f8;border-left:3px solid #087f8c;font-size:10px}.preview-meta{display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;margin:10px 0;font-size:10px}.preview-meta div{display:flex;justify-content:space-between;gap:8px}.preview-meta span{color:#60737a}.preview-table{width:100%;border-collapse:collapse;font-size:9px;table-layout:fixed}.preview-table th,.preview-table td{overflow-wrap:anywhere;word-break:break-word;white-space:normal}.preview-table th{background:#087f8c;color:#fff;padding:5px 3px}.preview-table td{border-bottom:1px solid #ccd8dc;padding:5px 3px}.preview-table .num{text-align:right}.preview-totals{width:58%;margin-left:auto;margin-top:8px;font-size:10px}.preview-totals div{display:flex;justify-content:space-between;padding:3px}.preview-totals .grand{border-top:2px solid #087f8c;background:#eaf6f7;font-weight:bold}.preview-transaction-note{margin-top:8px;padding:6px;border:1px solid #d4dee1;font-size:9px}.preview-signatures{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:38px;text-align:center;font-size:9px}.preview-signatures div{padding-top:35px;border-bottom:1px solid #6f8085}.preview-footer{margin-top:10px;padding-top:6px;border-top:1px solid #c7d2d5;text-align:center;font-size:9px;color:#64777e}@media(max-width:1100px){.designer-layout{grid-template-columns:1fr}.designer-preview-wrap{position:static}}.access-tabs{display:flex;gap:8px;margin-top:14px}.access-tabs button.active{background:#087f8c;color:#fff}.access-role-layout{display:grid;grid-template-columns:320px minmax(0,1fr);gap:16px}.role-list{display:flex;flex-direction:column;gap:8px}.role-list-item{display:flex;flex-direction:column;align-items:flex-start;text-align:left;background:#f1f6f8;color:#173f5f;border:1px solid #d7e4e8}.role-list-item.active{background:#dff4f5;border-color:#0e8793}.role-list-item small{margin-top:3px;color:#6b7c93}.permission-toolbar{display:flex;gap:8px;margin:14px 0}.permission-matrix{display:grid;grid-template-columns:repeat(2,minmax(260px,1fr));gap:12px}.permission-group{border:1px solid #d9e4e8;border-radius:10px;padding:12px;background:#f9fbfc}.permission-group-title{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e1eaec;margin-bottom:8px}.permission-group-title h3{margin:0 0 8px}.permission-item{display:flex;gap:9px;align-items:flex-start;padding:7px 3px}.permission-item span{display:flex;flex-direction:column}.permission-item small{color:#71868a;font-weight:400;margin-top:2px}.actions-cell{display:flex;gap:6px;flex-wrap:wrap}.status-toggle{display:flex;gap:7px;align-items:center}.access-tab-panel.hidden{display:none!important}@media(max-width:1000px){.access-role-layout{grid-template-columns:1fr}.permission-matrix{grid-template-columns:1fr}}.financial-report-view{margin-top:12px}.psak-paper{max-width:900px;margin:0 auto;background:#fff;color:#17212b;border:1px solid #d6dee5;border-radius:10px;padding:28px;box-shadow:0 8px 24px #0f172a12}.psak-report-header{text-align:center;border-bottom:2px solid #263b50;padding-bottom:12px;margin-bottom:18px}.psak-report-header h2{margin:0;font-size:22px;letter-spacing:1px}.psak-report-header p{margin:5px 0 0;color:#607080}.psak-section{margin:15px 0}.psak-section h3,.psak-balance-column>h3{font-size:13px;margin:0;padding:7px 9px;background:#eef3f7;border-left:4px solid #1f5b8f;letter-spacing:.4px}.psak-line{display:flex;justify-content:space-between;gap:16px;padding:6px 10px 6px 22px;border-bottom:1px dotted #ccd5dd}.psak-line span{display:flex;gap:9px}.psak-line small{min-width:48px;color:#6c7b88}.psak-line b{font-variant-numeric:tabular-nums;white-space:nowrap}.psak-subtotal{display:flex;justify-content:space-between;padding:8px 10px;font-weight:700;border-top:1px solid #8393a0}.psak-grand{display:flex;justify-content:space-between;padding:10px 12px;margin:10px 0;background:#e7f0f8;border-top:2px solid #284e72;border-bottom:2px solid #284e72;font-size:15px;font-weight:800}.psak-grand.final{background:#e2f4e9;border-color:#28794b;font-size:16px}.psak-empty{padding:9px 22px;color:#7c8993;font-style:italic}.psak-skonto{display:grid;grid-template-columns:1fr 1fr;gap:18px}.psak-balance-column{border:1px solid #cfd8e0;border-radius:8px;overflow:hidden;display:flex;flex-direction:column}.psak-balance-column>h3{background:#284e72;color:#fff;border:0;text-align:center;font-size:14px}.psak-balance-group h4{margin:0;padding:8px 10px;background:#f3f6f8;font-size:12px}.psak-column-total{margin-top:auto;display:flex;justify-content:space-between;padding:11px;background:#dce8f2;border-top:2px solid #284e72;font-weight:800}.psak-balance-status{display:flex;justify-content:space-between;padding:10px 12px;margin-top:15px;border-radius:7px;font-weight:800}.psak-balance-status.balanced{background:#def4e5;color:#17633a}.psak-balance-status.unbalanced{background:#ffe2e2;color:#9d2424}@media(max-width:800px){.psak-skonto{grid-template-columns:1fr}.psak-paper{padding:16px}}@media print{.psak-paper{box-shadow:none;border:0;max-width:none;padding:0}.psak-report-header h2{font-size:18pt}.psak-balance-status{break-inside:avoid}.psak-section,.psak-balance-group{break-inside:avoid}}.ledger-account-head{display:grid;grid-template-columns:repeat(2,minmax(180px,1fr));gap:8px;margin:12px 0}.ledger-account-head div{display:flex;justify-content:space-between;gap:12px;padding:8px 10px;background:#f4f8fa;border:1px solid #dce6e9;border-radius:7px}.ledger-account-head span{color:#60777e}.ledger-opening{display:flex;justify-content:space-between;padding:9px 11px;margin:8px 0;background:#eaf5f6;border-left:4px solid #087f8c;font-weight:700}.ledger-table-wrap{overflow:auto;border:1px solid #d6e1e4;border-radius:8px}.ledger-report-table{width:100%;border-collapse:collapse;font-size:10px}.ledger-report-table th{background:#123f78;color:#fff;padding:7px;white-space:nowrap}.ledger-report-table td{padding:7px;border-bottom:1px solid #e1e8ea}.ledger-report-table tbody tr:nth-child(even){background:#f8fafb}.ledger-report-table .num{text-align:right;white-space:nowrap}.ledger-totals{width:min(360px,100%);margin:12px 0 0 auto}.ledger-totals div{display:flex;justify-content:space-between;padding:7px 9px;border-bottom:1px solid #dbe4e7}.ledger-totals .final{background:#dff2e7;border-top:2px solid #16845b;font-size:12px}.cashflow-section{margin:13px 0;border:1px solid #d8e3e6;border-radius:9px;overflow:hidden}.cashflow-section h3{margin:0;padding:9px 11px;background:#123f78;color:#fff;font-size:12px}.cashflow-line{display:flex;justify-content:space-between;gap:18px;padding:8px 11px;border-bottom:1px solid #e4eaec}.cashflow-line span{display:flex;flex-direction:column}.cashflow-line small{margin-top:2px;color:#71858b}.cashflow-line strong{white-space:nowrap}.cashflow-total{display:flex;justify-content:space-between;padding:9px 11px;background:#eef5f8;font-weight:800}.cashflow-reconciliation{margin-top:16px;border:2px solid #123f78;border-radius:9px;overflow:hidden}.cashflow-reconciliation div{display:flex;justify-content:space-between;padding:9px 11px;border-bottom:1px solid #dce4ea}.cashflow-reconciliation .final{background:#dff2e7;font-size:13px;border-bottom:0}.negative{color:#b42318}@media(max-width:700px){.ledger-account-head{grid-template-columns:1fr}.cashflow-line{flex-direction:column;gap:4px}}.project-budget-summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:12px;margin-bottom:16px}.project-budget-stat{background:#fff;border:1px solid #dce6ea;border-radius:13px;padding:14px;box-shadow:0 7px 18px rgba(22,55,73,.05)}.project-budget-stat span{display:block;color:#6d7f88;font-size:12px}.project-budget-stat b{display:block;margin-top:5px;color:#123b5a;font-size:18px}.project-budget-stat.primary{background:linear-gradient(135deg,#123f78,#0e8793);color:#fff}.project-budget-stat.primary span,.project-budget-stat.primary b{color:#fff}.project-budget-layout{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(300px,.75fr);gap:16px}.project-budget-control-body{display:flex;flex-direction:column;gap:8px}.project-budget-control-title{display:flex;flex-direction:column;padding-bottom:9px;border-bottom:1px solid #dce6ea}.project-budget-control-title span{color:#6d7f88;font-size:12px;margin-top:3px}.budget-control-line{display:flex;justify-content:space-between;gap:12px;padding:7px 0;border-bottom:1px solid #edf1f3}.budget-control-line.total{font-size:15px;font-weight:800;color:#123f78}.budget-control-line.remaining{background:#eaf7ef;border:0;border-radius:8px;padding:9px}.budget-progress-head{display:flex;justify-content:space-between;margin-top:8px}.budget-progress{height:12px;border-radius:999px;background:#e7edef;overflow:hidden}.budget-progress i{display:block;height:100%;border-radius:999px}.budget-progress i.safe,.budget-badge.safe{background:#239b65}.budget-progress i.warning,.budget-badge.warning{background:#d59a16}.budget-progress i.over,.budget-badge.over{background:#c83b35}.budget-badge{display:inline-block;padding:4px 8px;border-radius:999px;color:#fff;font-weight:800;font-size:11px}.number-cell{text-align:right;white-space:nowrap}@media(max-width:900px){.project-budget-layout{grid-template-columns:1fr}}.budget-control-section{margin:8px 0 12px;padding:10px;border:1px solid #dce6ea;border-radius:10px;background:#fbfdfe}.budget-control-section h4{margin:0 0 6px;color:#123f78}.service-master-layout{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(300px,.75fr);gap:16px}@media(max-width:960px){.service-master-layout{grid-template-columns:1fr}}.profit-chart-panel{min-width:0}.dashboard-chart-card{min-width:0}.dashboard-chart-canvas{display:block;width:100%;max-width:560px;height:auto;margin:0 auto}.mini-pie-summary{display:grid;gap:6px;margin-top:8px}.mini-pie-item{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;align-items:center;padding:7px 9px;border:1px solid #dbe4ee;border-radius:8px;background:#f8fafc;font-size:12px}.mini-pie-item span{display:flex;align-items:center;gap:7px;min-width:0}.mini-pie-item span em{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-style:normal}.mini-pie-item i{display:inline-block;width:10px;height:10px;border-radius:50%;flex:0 0 auto}.mini-pie-item b{white-space:nowrap}@media(max-width:1180px){.analytics-grid{grid-template-columns:1fr 1fr}.profit-chart-panel{grid-column:1/-1}}@media(max-width:760px){.analytics-grid{grid-template-columns:1fr}.profit-chart-panel{grid-column:auto}}.pl-summary{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:8px}.pl-item{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 10px;border:1px solid #dbe4ee;border-radius:8px;background:#f8fafc;font-size:12px}.pl-item span{display:flex;align-items:center;gap:6px}.pl-item i{display:inline-block;width:10px;height:10px;border-radius:50%}.pl-item b{white-space:nowrap}@media(max-width:760px){.pl-summary{grid-template-columns:1fr}}.project-income-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(430px,1fr));gap:20px;align-items:start}.project-income-card{border:1px solid #d6dee5;border-radius:12px;padding:22px;background:#fff;box-shadow:0 8px 24px #0f172a12}.project-income-card header{text-align:center;border-bottom:2px solid #263b50;margin-bottom:18px;padding-bottom:12px}.project-income-card h3{margin:0;font-size:19px;letter-spacing:.4px;color:#173f5f}.project-income-card small{display:block;margin-top:5px;color:#607080}.project-income-card .financial-section{margin:14px 0}.project-income-card .financial-section h3{font-size:13px;text-align:left;margin:0;padding:7px 9px;background:#eef3f7;border-left:4px solid #1f5b8f;letter-spacing:.4px}.project-income-card .financial-line{display:flex;justify-content:space-between;gap:18px;padding:7px 10px 7px 20px;border-bottom:1px dotted #ccd5dd}.project-income-card .financial-total{display:flex;justify-content:space-between;padding:8px 10px;font-weight:700;border-top:1px solid #8393a0}.project-income-card .financial-highlight{display:flex;justify-content:space-between;padding:10px 12px;margin:10px 0;background:#e7f0f8;border-top:2px solid #284e72;border-bottom:2px solid #284e72;font-weight:800}.project-income-card .financial-highlight.secondary{background:#e2f4e9;border-color:#28794b;font-size:16px}.project-income-total{grid-column:1/-1;max-width:900px;width:100%;margin:0 auto 2px}.project-income-total .project-budget-summary{margin:0}@media(max-width:600px){.project-income-grid{grid-template-columns:1fr}.project-income-card{padding:14px}}.od-line-block{margin:10px 0;padding:10px;border:1px solid #dbe7ea;border-radius:10px}.od-line-labels,.od-line{display:grid;grid-template-columns:2.2fr 2fr .7fr 1fr .9fr auto;gap:7px;align-items:center}.od-line-labels{font-size:12px;font-weight:700;color:#526b72;margin-bottom:5px}.od-line{margin:0}.od-line select,.od-line input{width:100%;min-width:0}@media(max-width:900px){.od-line-labels{display:none}.od-line{grid-template-columns:1fr 1fr}.od-line .od-product,.od-line .od-desc{grid-column:1/-1}}


.sl-select-search-popover{background:#fff;border:1px solid #b9cbd1;border-radius:9px;box-shadow:0 10px 28px rgba(15,45,55,.22);padding:8px}.sl-select-search-input{width:100%;box-sizing:border-box;margin:0 0 6px;padding:9px 10px;border:1px solid #9fb7bf;border-radius:7px}.sl-select-search-list{max-height:220px;overflow:auto;display:grid;gap:3px}.sl-select-search-option{display:block;width:100%;text-align:left;background:#fff;color:#173f5f;border:0;border-radius:5px;padding:8px 9px;font-weight:500}.sl-select-search-option:hover,.sl-select-search-option:focus{background:#e6f4f5;color:#075f68}.sl-select-search-empty{padding:10px;color:#71868a;text-align:center}
.product-master-grid{display:grid;grid-template-columns:repeat(4,minmax(180px,1fr));gap:14px;align-items:end;margin-top:12px}.product-master-grid label{display:flex;flex-direction:column;gap:6px;min-width:0}.product-master-grid input,.product-master-grid select{width:100%;box-sizing:border-box}.product-master-grid .wide{grid-column:span 2}@media(max-width:1050px){.product-master-grid{grid-template-columns:repeat(2,minmax(180px,1fr))}}@media(max-width:620px){.product-master-grid{grid-template-columns:1fr}}
.service-master-layout>.card{min-width:0}.service-master-layout .field-grid{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}.service-master-layout input,.service-master-layout select,.service-master-layout textarea{width:100%;min-width:0}.accounting-manual{width:100%;max-width:100%;overflow-x:auto}.accounting-manual table{min-width:980px}.accounting-manual td input,.accounting-manual td select{width:100%;min-width:105px}.accounting-manual td:nth-child(1) select{min-width:220px}.accounting-manual td:nth-child(5) input,.accounting-manual td:nth-child(6) input{min-width:125px}.sale-line input[type=number]{min-width:90px}@media(max-width:1200px){.sale-line{grid-template-columns:minmax(210px,2fr) minmax(180px,1.5fr) 95px 120px 120px 120px auto;overflow-x:auto}.line-header{min-width:980px}.sale-line{min-width:980px}.service-master-layout{grid-template-columns:1fr}}.page{position:relative}.page-close-btn{position:sticky;top:8px;z-index:50;float:right;margin:4px 4px 8px 10px;width:38px;height:38px;padding:0;border-radius:50%;background:#b42318;color:#fff;font-size:22px;font-weight:800;line-height:38px;box-shadow:0 5px 14px rgba(180,35,24,.25)}.page-close-btn:hover{background:#8f1b13}.product-unit-editor{display:grid;gap:9px}.product-unit-row{display:grid;grid-template-columns:minmax(170px,1.2fr) minmax(140px,.8fr) minmax(150px,1fr) minmax(150px,1fr) auto;gap:9px;align-items:end}.product-unit-row label{display:flex;flex-direction:column;gap:5px;font-size:12px;font-weight:600;color:#24484e}.product-unit-row input,.product-unit-row select{width:100%}@media(max-width:900px){.product-unit-row{grid-template-columns:repeat(2,minmax(170px,1fr))}}@media(max-width:560px){.product-unit-row{grid-template-columns:1fr}}
<style id="transaction-grid-v1206">

.product-recommendation-box{margin:14px 0 18px;padding:14px;border:1px solid #cfe0e4;border-radius:12px;background:#f8fbfc}.product-recommendation-toolbar{display:grid;grid-template-columns:minmax(220px,1fr) auto auto;gap:10px;align-items:end}.product-recommendation-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:8px;margin-top:12px}.product-recommendation-item{display:flex;align-items:flex-start;gap:8px;padding:9px 10px;border:1px solid #dbe7e9;border-radius:9px;background:#fff}.product-recommendation-item input{width:auto;margin-top:3px}.product-recommendation-item b{display:block}.product-recommendation-item small{display:block;color:#6b7f84;margin-top:2px}.product-recommendation-actions{display:flex;gap:6px;margin-left:auto}.product-recommendation-actions button{padding:6px 8px;font-size:12px}@media(max-width:720px){.product-recommendation-toolbar{grid-template-columns:1fr}.product-recommendation-toolbar button{width:100%}}
.transaction-lines-section{overflow:hidden}.transaction-lines-title{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:12px}.transaction-lines-title h3{margin:0 0 4px}.transaction-grid-scroll{width:100%;overflow-x:auto;border:1px solid #dbe7e9;border-radius:10px;background:#fff}.sale-grid,.sale-line{display:grid;grid-template-columns:46px minmax(260px,2.5fr) minmax(105px,.7fr) minmax(210px,1.5fr) 88px 130px minmax(190px,1.2fr) 135px 64px;gap:8px;align-items:center;min-width:1260px}.line-header.sale-grid{padding:10px 12px;background:#e8f2f4;border-bottom:1px solid #d3e2e5;font-size:12px;text-transform:uppercase;letter-spacing:.02em}.sale-line{padding:8px 12px;margin:0;border-bottom:1px solid #edf2f3}.sale-line:last-child{border-bottom:0}.sale-line input,.sale-line select{width:100%;min-width:0;height:40px}.sale-line .slQty,.sale-line .slPrice,.sale-line .slDiscount{text-align:right;font-variant-numeric:tabular-nums}.line-no{text-align:center;font-weight:700;color:#60777c}.discount-combo{display:grid;grid-template-columns:minmax(95px,.9fr) minmax(88px,.8fr);gap:6px}.line-subtotal{text-align:right;font-weight:700;color:#075e67;font-variant-numeric:tabular-nums;white-space:nowrap}.icon-delete{width:40px;height:40px;padding:0;border-radius:8px;font-size:18px;line-height:40px}.keyboard-hint{margin:9px 0 0;color:#71868a;font-size:12px}.purchase-line-editor{display:grid;grid-template-columns:minmax(280px,2.4fr) minmax(105px,.7fr) 90px 135px minmax(190px,1.25fr) auto;gap:10px;align-items:end}.purchase-product-field{min-width:0}.purchase-line-editor input,.purchase-line-editor select{height:42px}.numeric-field input{text-align:right;font-variant-numeric:tabular-nums}.purchase-add-btn{height:42px;white-space:nowrap}.purchase-lines-table{min-width:930px}.purchase-lines-table th{background:#e8f2f4;color:#24484e;font-size:12px;text-transform:uppercase}.purchase-lines-table .num,.purchase-lines-table td.num{text-align:right;font-variant-numeric:tabular-nums}.purchase-lines-table .action-col{width:70px;text-align:center}.purchase-lines-table td.action-col{text-align:center}.purchase-lines-table .item-name{font-weight:600}.purchase-lines-table .item-type{display:block;color:#71868a;font-size:11px;margin-top:2px}
@media(max-width:1000px){.purchase-line-editor{grid-template-columns:repeat(2,minmax(180px,1fr))}.purchase-add-btn{grid-column:1/-1;justify-self:end}.transaction-lines-title{align-items:center}}
@media(max-width:600px){.transaction-lines-title{flex-direction:column}.transaction-lines-title button{width:100%}.purchase-line-editor{grid-template-columns:1fr}.purchase-add-btn{width:100%;justify-self:stretch}}
.hide-cost .cost-sensitive{display:none!important}.report-field-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:7px}.report-field-grid label{display:flex;gap:7px;align-items:center;padding:6px 8px;border:1px solid var(--line);border-radius:7px;background:#fff}.report-field-grid input{width:auto}

.flex-invoice-layout{display:grid;grid-template-columns:minmax(420px,1fr) minmax(380px,1fr);gap:18px}.flex-block-list{display:grid;gap:6px;margin:8px 0 14px}.flex-block-row{display:grid;grid-template-columns:28px 1fr 42px 42px;align-items:center;gap:6px;border:1px solid #d5e0e3;border-radius:7px;padding:7px;background:#f9fbfb}.flex-block-row button{padding:4px 7px}.flex-preview{background:#e8edef;padding:12px;min-height:500px;position:sticky;top:10px}.flex-preview-paper{background:white;max-width:620px;margin:auto;padding:24px;box-shadow:0 2px 10px #7895}.flex-preview-paper .pv-block{border:1px dashed #b8c8ce;margin:7px 0;padding:7px}.flex-preview-paper table{width:100%;border-collapse:collapse;font-size:10px}.flex-preview-paper th{background:#087f8c;color:white}.flex-preview-paper th,.flex-preview-paper td{padding:4px;border-bottom:1px solid #ddd}@media(max-width:1050px){.flex-invoice-layout{grid-template-columns:1fr}.flex-preview{position:static}}
.invoice-material-box{border:1px solid #d6e1e4;border-radius:8px;padding:10px;overflow:auto}.invoice-material-row{display:grid;grid-template-columns:34px 105px 115px 1fr 85px 65px 110px;gap:7px;align-items:center;padding:6px 0;border-bottom:1px solid #e5ecee}.invoice-material-row.head{font-weight:700;background:#eef6f7;padding:7px}.invoice-material-row input[type=number]{width:100%}@media(max-width:900px){.invoice-material-row{min-width:760px}}.od-line-labels-unit,.od-line-unit{grid-template-columns:minmax(220px,2fr) minmax(90px,.7fr) minmax(180px,1.5fr) 90px 120px 100px 75px!important}.od-search{width:100%;margin:5px 0}@media(max-width:1100px){.od-line-labels-unit,.od-line-unit{min-width:980px}}.sale-product-picker{display:grid;gap:4px;min-width:220px}.sale-product-picker .slProduct{width:100%;min-width:0}.fa-dep-controls{display:flex;align-items:flex-end;gap:10px;flex-wrap:wrap}.fa-dep-controls>label{display:flex;flex-direction:column;gap:6px;margin:0}.fa-dep-controls>label input{height:40px}.fa-dep-controls>button{height:40px;margin:0}
/* Web v1.2.1: mobile-first shell, compact bottom nav + drawer */
.web-status-chip{display:inline-flex;align-items:center;gap:6px;margin:5px 8px 8px;padding:5px 9px;border-radius:999px;background:rgba(255,255,255,.1);color:#d9f7f5;font-size:11px}.subscription-kpis{display:grid;grid-template-columns:repeat(4,minmax(150px,1fr));gap:12px;margin:12px 0}.subscription-kpis .stat{min-width:0}.plan-grid{display:grid;grid-template-columns:repeat(2,minmax(240px,1fr));gap:12px}.plan-card{border:1px solid #d8e6e9;border-radius:14px;padding:16px;background:linear-gradient(145deg,#fff,#f3fbfb)}
@media(max-width:760px){body{background:#f4f7f9}#login{margin:3vh 12px;padding:22px}.wrap{padding-bottom:76px}#app:not(.hidden){display:block}.sidebar{position:sticky;top:0;height:auto;min-height:0;padding:8px 10px;border-radius:0;overflow:visible;display:grid;grid-template-columns:1fr auto;align-items:center;z-index:100}.brand-block{border:0;margin:0;padding:3px 6px}.sidebar-logo{max-height:42px;width:auto}.brand-copy small{display:none}.server-user{padding:3px 8px}.server-user .muted{display:none}.web-status-chip{grid-column:1/-1;margin:2px 6px 4px}.logout-btn{margin:0;padding:8px 10px;width:auto;font-size:0}.logout-btn:after{content:'Keluar';font-size:12px}.nav.module-nav{position:fixed;left:0;right:0;bottom:0;z-index:9999;display:flex;flex-wrap:nowrap;gap:2px;overflow-x:auto;background:#0b2033;padding:6px 6px calc(6px + env(safe-area-inset-bottom));box-shadow:0 -5px 20px rgba(16,42,67,.2);scrollbar-width:none}.nav.module-nav::-webkit-scrollbar{display:none}.nav.module-nav button{flex:0 0 82px;min-height:54px;padding:5px 4px;justify-content:center;flex-direction:column;gap:2px;text-align:center;font-size:10px;white-space:nowrap}.nav-icon{font-size:18px;width:auto}.page{padding:10px}.card{padding:14px;border-radius:14px}.module-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.module-card{min-height:120px;padding:14px}.field-grid,.field-grid.two,.field-grid.three,.field-grid.four{grid-template-columns:1fr}.sale-line,.purchase-line-editor{grid-template-columns:1fr}.action-bar{position:sticky;bottom:70px;z-index:8;background:rgba(255,255,255,.94);padding:8px;border-radius:10px;box-shadow:0 5px 18px rgba(16,42,67,.12)}.action-bar button{min-height:42px}table{display:block;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch}.analytics-grid,.reminder-grid,.plan-grid,.subscription-kpis{grid-template-columns:1fr}.summary-box{width:auto}.transaction-title{flex-direction:column}.table-toolbar{align-items:stretch}.table-toolbar input,.table-toolbar select{min-height:42px}}

/* Web v1.2.1 mobile UI fix: compact header + bottom tabbar + drawer menu */
.mobile-tabbar,.mobile-drawer,.mobile-drawer-backdrop{display:none}
body.mobile-drawer-open{overflow:hidden}
@media(max-width:760px){
  .sidebar .nav.module-nav,.sidebar .logout-btn{display:none!important}
  .sidebar{position:sticky!important;top:0!important;height:auto!important;min-height:0!important;padding:10px 12px!important;display:grid!important;grid-template-columns:minmax(0,1fr) auto!important;align-items:center!important;gap:8px;background:linear-gradient(180deg,#0a2a4a 0%,#0b3158 100%)!important;overflow:visible!important;box-shadow:0 4px 18px rgba(16,42,67,.14)!important;z-index:80!important}
  .brand-block{margin:0!important;padding:0!important;border:0!important;gap:10px!important;min-width:0}
  .brand-logo-block{display:flex!important;align-items:center!important}
  .sidebar-logo{max-height:40px!important;width:auto!important;max-width:none!important;padding:3px!important;margin:0!important}
  .brand-copy{min-width:0}
  .brand-copy strong{display:block;font-size:15px;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .brand-copy small{display:block!important;font-size:11px;color:#d8edf2;line-height:1.25}
  .server-user{padding:6px 9px!important;margin:0!important;white-space:nowrap;font-size:12px;justify-self:end}
  .server-user .muted{display:none!important}
  .web-status-chip{grid-column:1/-1;margin:0!important;font-size:12px;padding:8px 10px!important;border-radius:999px;background:rgba(255,255,255,.12)!important;color:#eaf7fa!important;border:1px solid rgba(255,255,255,.18)!important}
  .wrap{padding-bottom:86px!important}
  .page{padding:12px!important}
  .mobile-tabbar{display:grid!important;grid-template-columns:repeat(5,minmax(0,1fr));position:fixed;left:0;right:0;bottom:0;z-index:9999;background:rgba(10,32,51,.98);padding:8px 8px calc(8px + env(safe-area-inset-bottom));gap:6px;box-shadow:0 -7px 22px rgba(16,42,67,.22)}
  .mobile-tabbar button{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;min-height:56px;padding:6px 4px;border-radius:14px;background:transparent;color:#d6e8ef;font-size:10px;font-weight:700;line-height:1.2;border:1px solid transparent}
  .mobile-tabbar button.active{background:#123b5a;color:#fff;border-color:#1d6e92}
  .mobile-tabbar .nav-icon{font-size:19px;line-height:1;width:auto}
  .mobile-drawer-backdrop:not(.hidden){display:block}
  .mobile-drawer:not(.hidden){display:block}
  .mobile-drawer-backdrop{position:fixed;inset:0;background:rgba(7,22,35,.45);z-index:10000}
  .mobile-drawer{position:fixed;left:0;right:0;bottom:0;max-height:78vh;z-index:10001;background:#f8fbfc;border-radius:20px 20px 0 0;box-shadow:0 -10px 30px rgba(16,42,67,.22);padding:16px 14px calc(18px + env(safe-area-inset-bottom));overflow:auto}
  .mobile-drawer-header{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px}
  .mobile-drawer-header strong{font-size:18px;color:#123b5a}
  .mobile-drawer-close{width:38px;height:38px;padding:0;border-radius:50%;font-size:22px;line-height:38px;background:#dbe9ef;color:#123b5a}
  .mobile-drawer-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  .mobile-drawer-card{display:flex;gap:10px;align-items:flex-start;padding:14px;border-radius:16px;border:1px solid #d6e3e8;background:#fff;box-shadow:0 6px 18px rgba(16,42,67,.06);cursor:pointer}
  .mobile-drawer-card h4{margin:0 0 4px;font-size:14px;color:#123b5a}
  .mobile-drawer-card p{margin:0;font-size:12px;line-height:1.35;color:#6c818d}
  .mobile-drawer-icon{flex:0 0 42px;width:42px;height:42px;border-radius:12px;background:#dff5f7;color:#087f8c;display:grid;place-items:center;font-size:22px;font-weight:800}
  .mobile-drawer-logout{width:100%;margin-top:14px;min-height:42px}
  .module-header button.secondary{width:100%}
  .module-grid{grid-template-columns:1fr!important}
  .module-card{min-height:unset!important;padding:16px!important}
  .module-card h3{font-size:17px!important;margin:10px 0 6px!important}
  .module-card p{font-size:13px!important}
}
@media(max-width:430px){
  .mobile-drawer-grid{grid-template-columns:1fr}
  .brand-copy strong{font-size:14px}
}


/* Web v1.3.0 public auth landing */
.auth-shell{min-height:100vh;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(420px,.75fr);background:linear-gradient(135deg,#eef8f7 0%,#f6f9fc 48%,#eaf3fb 100%)}
.auth-hero{padding:54px clamp(28px,6vw,92px);display:flex;flex-direction:column;justify-content:center;position:relative;overflow:hidden}.auth-hero:before{content:'';position:absolute;width:430px;height:430px;border-radius:50%;background:#75d4bf33;right:-130px;top:-120px}.auth-hero:after{content:'';position:absolute;width:360px;height:360px;border-radius:50%;background:#4ba3d522;left:-160px;bottom:-170px}.auth-brand{display:flex;align-items:center;gap:14px;position:relative;z-index:1}.auth-brand img{height:66px;width:66px;object-fit:contain}.auth-brand h1{margin:0;color:#123b5a;font-size:clamp(27px,3.2vw,44px)}.auth-brand p{margin:5px 0 0;color:#607986}.auth-copy{position:relative;z-index:1;margin-top:52px;max-width:720px}.auth-copy h2{font-size:clamp(32px,4.5vw,58px);line-height:1.05;margin:0 0 18px;color:#0b2942}.auth-copy h2 span{color:#0e8793}.auth-copy>p{font-size:18px;line-height:1.6;color:#526d7a;max-width:620px}.auth-features{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:30px}.auth-feature{background:#ffffffaa;border:1px solid #d9e8ed;padding:14px;border-radius:16px;backdrop-filter:blur(8px)}.auth-feature b{display:block;color:#123b5a;margin-bottom:5px}.auth-feature small{color:#6b818c;line-height:1.4}.auth-panel{display:flex;align-items:center;justify-content:center;padding:26px;background:#ffffffaa;backdrop-filter:blur(14px)}
#login.auth-card{margin:0!important;max-width:540px!important;width:100%;padding:28px!important;border-radius:24px!important;border-top:0!important;box-shadow:0 25px 70px #17324a20!important}.auth-tabs{display:grid;grid-template-columns:1fr 1fr;background:#edf3f5;border-radius:12px;padding:4px;margin:16px 0}.auth-tabs button{background:transparent;color:#58717d;border-radius:9px;padding:10px}.auth-tabs button.active{background:#fff;color:#087f8c;box-shadow:0 3px 10px #17324a12}.auth-pane{display:none}.auth-pane.active{display:block}.auth-field{display:flex;flex-direction:column;gap:5px;margin-bottom:11px}.auth-field span{font-size:12px;font-weight:700;color:#365663}.auth-field input{width:100%;min-height:44px;background:#fff}.auth-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.auth-action{width:100%;min-height:46px;margin-top:6px}.trial-pill{display:inline-flex;align-items:center;gap:7px;background:#e3f8ed;color:#17623f;padding:7px 11px;border-radius:999px;font-size:12px;font-weight:700}.auth-note{background:#f2f8fa;border:1px solid #d8e8ed;border-radius:12px;padding:10px 12px;color:#5f7782;font-size:12px;line-height:1.5;margin-top:12px}
@media(max-width:900px){.auth-shell{grid-template-columns:1fr}.auth-hero{padding:28px 22px 18px}.auth-copy{margin-top:26px}.auth-copy h2{font-size:34px}.auth-copy>p{font-size:15px}.auth-features{grid-template-columns:1fr 1fr 1fr}.auth-panel{padding:14px 14px 30px}.auth-brand img{height:50px;width:50px}}
@media(max-width:560px){.auth-hero{padding:22px 16px 8px}.auth-copy h2{font-size:29px}.auth-features{display:none}.auth-panel{align-items:flex-start}.auth-grid{grid-template-columns:1fr}#login.auth-card{padding:20px!important;border-radius:18px!important}.auth-brand h1{font-size:22px}.auth-brand p{font-size:12px}}
/* v1.3.2: authentication and application are mutually exclusive screens */
.auth-shell.hidden{display:none!important}
#app.hidden{display:none!important}
#app:not(.hidden){min-height:100vh}



/* Web v1.3.3 UI polish and mobile transaction ergonomics */
:root{--web-primary:#078a96;--web-primary-2:#0aa7b4;--web-navy:#0a2a4a;--web-surface:#ffffff;--web-soft:#f4f9fb;--web-border:#d8e6eb;--web-radius:16px}
.card{border:1px solid rgba(214,227,232,.8);box-shadow:0 10px 28px rgba(16,42,67,.07)}
button{transition:transform .12s ease,box-shadow .12s ease,background .12s ease}button:hover{box-shadow:0 6px 14px rgba(7,127,140,.14)}button:active{transform:translateY(1px)}
input,select,textarea{border-color:#cbdbe1;background:#fff;transition:border-color .15s ease,box-shadow .15s ease}input:focus,select:focus,textarea:focus{outline:none!important;border-color:#16a2af!important;box-shadow:0 0 0 3px rgba(22,162,175,.13)}
.plan-card{position:relative;overflow:hidden;background:linear-gradient(145deg,#fff,#f7fbfc);border:1px solid var(--web-border);border-radius:18px;padding:20px}.plan-card.featured{border-color:#8dd2d9;background:linear-gradient(145deg,#fff,#eefafb)}.plan-badge{display:inline-flex;padding:4px 8px;border-radius:999px;background:#e1f6f7;color:#087f8c;font-size:11px;font-weight:800;letter-spacing:.04em}.subscription-price-box{margin-top:14px;padding:16px;border-radius:14px;background:linear-gradient(135deg,#eaf7f8,#f8fcfd);border:1px solid #cfe6e9;color:#24484e}.subscription-estimator h3{margin-top:0}
.sale-mobile-label{display:none}.sale-mobile-field{min-width:0}.sale-mobile-field>input,.sale-mobile-field>select{width:100%;min-width:0}
@media(max-width:760px){
 body{font-size:15px}.page{padding:10px!important}.card{padding:14px!important;margin-bottom:12px!important;border-radius:16px!important}.form-section{padding:13px!important;border-radius:14px!important}.transaction-title h2{font-size:21px;margin-top:4px}.section-help,.muted{line-height:1.45}.field>span{font-size:12px}.field input,.field select,.field textarea{min-height:46px;font-size:16px}
 .subscription-kpis{grid-template-columns:repeat(2,minmax(0,1fr))!important}.subscription-kpis .stat{min-width:0;padding:12px}.subscription-kpis .stat b{font-size:18px}.plan-grid{grid-template-columns:1fr!important}.plan-card{padding:16px}.subscription-estimator .field-grid{grid-template-columns:1fr!important}
 .transaction-lines-section{overflow:visible!important}.transaction-grid-scroll{overflow:visible!important;border:0!important;background:transparent!important}.line-header.sale-grid{display:none!important}
 .sale-line{min-width:0!important;width:100%!important;display:grid!important;grid-template-columns:1fr 1fr!important;grid-template-areas:'no delete' 'product product' 'unit qty' 'price subtotal' 'discount discount' 'desc desc'!important;gap:10px!important;padding:14px!important;margin:0 0 12px!important;border:1px solid #d5e5e9!important;border-radius:16px!important;background:#fff!important;box-shadow:0 7px 18px rgba(16,42,67,.07)!important;align-items:end!important}
 .sale-line .line-no{grid-area:no;justify-self:start;align-self:center;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:#e4f6f7;color:#087f8c;font-size:13px}.sale-line .line-no:before{content:'Item ';font-size:0}
 .sale-line .product-field{grid-area:product}.sale-line .unit-field{grid-area:unit}.sale-line .qty-field{grid-area:qty}.sale-line .price-field{grid-area:price}.sale-line .subtotal-field{grid-area:subtotal}.sale-line .discount-field{grid-area:discount}.sale-line .desc-field{grid-area:desc}.sale-line .icon-delete{grid-area:delete;justify-self:end;width:38px;height:38px;border-radius:12px}
 .sale-mobile-field{display:flex!important;flex-direction:column!important;gap:5px!important}.sale-mobile-label{display:block!important;font-size:11px!important;font-weight:800!important;color:#5d737d!important;text-transform:uppercase;letter-spacing:.03em}.sale-mobile-field input,.sale-mobile-field select{height:46px!important;font-size:16px!important;border-radius:10px!important}.sale-line .slQty,.sale-line .slPrice{font-weight:700}.sale-line .discount-combo{display:grid!important;grid-template-columns:1fr 1fr!important;gap:7px!important}.sale-line .discount-combo .sale-mobile-label{grid-column:1/-1}.sale-line .subtotal-field{min-height:46px;padding:7px 10px;border:1px solid #dbe7e9;border-radius:10px;background:#f4fbfb;justify-content:center}.sale-line .line-subtotal{font-size:16px;text-align:left!important}.sale-line .sale-product-picker{min-width:0!important}.sale-line .slProduct{min-width:0!important}
 .action-bar{display:grid!important;grid-template-columns:1fr!important;position:sticky!important;bottom:76px!important;padding:9px!important;background:rgba(255,255,255,.96)!important;backdrop-filter:blur(8px);border:1px solid #dbe7e9}.action-bar button{width:100%!important;min-height:46px!important}
 .summary-box{margin-left:0!important}.table-toolbar{gap:8px}.table-toolbar button,.table-toolbar input,.table-toolbar select{min-height:44px!important}
}
@media(max-width:400px){.sale-line{grid-template-columns:1fr!important;grid-template-areas:'no' 'delete' 'product' 'unit' 'qty' 'price' 'subtotal' 'discount' 'desc'!important}.sale-line .icon-delete{margin-top:-42px}.subscription-kpis{grid-template-columns:1fr!important}}

</style></head><body><div class="wrap">
<div class="card"><h1>StokLedger Pro</h1><div class="muted">Server API multi-user LAN · UI Branding v1.4.4a</div></div>
<section id="authShell" class="auth-shell"><div class="auth-hero"><div class="auth-brand"><img src="/assets/stokledger-icon.png" alt="StokLedger"><div><h1>StokLedger Pro Ultima Web</h1><p>Kelola stok, penjualan, keuangan, dan proyek dari mana saja.</p></div></div><div class="auth-copy"><span class="trial-pill">✓ Trial gratis 7 hari · 2 user</span><h2>Operasional lebih rapi.<br><span>Keputusan lebih cepat.</span></h2><p>Versi web yang dirancang untuk kerja kolaboratif: akses aman dari laptop maupun ponsel, data tersimpan di PostgreSQL, dan semua modul bisnis tetap terintegrasi.</p><div class="auth-features"><div class="auth-feature"><b>📦 Stok & Gudang</b><small>Multi gudang, valuasi, assembly, dan adjustment.</small></div><div class="auth-feature"><b>💳 Keuangan</b><small>Kas, piutang, hutang, jurnal, dan laporan terhubung.</small></div><div class="auth-feature"><b>📱 Mobile Friendly</b><small>Input transaksi dan pantau dashboard dari HP.</small></div></div></div></div><div class="auth-panel"><div id="login" class="card auth-card"><div class="auth-brand" style="display:none"><img src="/assets/stokledger-icon.png"><div><h1>StokLedger</h1></div></div><h2 style="margin:0">Selamat datang</h2><p class="muted" style="margin-top:6px">Login atau buat akun baru untuk memulai trial 7 hari.</p><div class="auth-tabs"><button id="authLoginTab" class="active" onclick="showAuthPane('login')">Masuk</button><button id="authSignupTab" onclick="showAuthPane('signup')">Buat Akun Trial</button></div><div id="authLoginPane" class="auth-pane active"><label class="auth-field"><span>Email</span><input id="username" placeholder="nama@perusahaan.com" autocomplete="username"></label><label class="auth-field"><span>Password</span><input id="password" type="password" placeholder="Password" autocomplete="current-password"></label><button class="auth-action" onclick="doLogin()">Masuk ke StokLedger</button><p id="loginMsg"></p></div><div id="authSignupPane" class="auth-pane"><div class="auth-grid"><label class="auth-field"><span>Nama Perusahaan</span><input id="signupCompany" placeholder="PT / CV / Usaha"></label><label class="auth-field"><span>Nama Admin</span><input id="signupName" placeholder="Nama lengkap"></label></div><label class="auth-field"><span>Email Login</span><input id="signupEmail" type="email" placeholder="admin@perusahaan.com"></label><div class="auth-grid"><label class="auth-field"><span>No. HP / WhatsApp</span><input id="signupPhone" placeholder="08..."></label><label class="auth-field"><span>Password</span><input id="signupPassword" type="password" minlength="8" placeholder="Minimal 8 karakter"></label></div><button class="auth-action" onclick="createTrialAccount()">Mulai Trial Gratis 7 Hari</button><p id="signupMsg"></p><div class="auth-note">Dengan membuat akun, Anda mendapat trial 7 hari untuk maksimal 2 user. Setelah trial berakhir, data tetap tersimpan dan dapat dilanjutkan setelah aktivasi langganan.</div></div></div></div></section>
<div id="app" class="hidden">
<aside class="sidebar card">
  <div class="brand-block brand-logo-block"><img class="sidebar-logo" src="/assets/stokledger-logo.png" alt="StokLedger by ACIS"><div class="brand-copy"><strong>StokLedger Pro Ultima</strong><small>Kelola Stok, Penjualan & Keuangan</small></div></div>
  <div class="server-user"><b id="who"></b><div id="health" class="muted"></div></div><div id="webSubscriptionChip" class="web-status-chip">Memuat status langganan...</div>
  <nav class="nav module-nav">
    <button onclick="page('dashboard',this)" class="active"><span class="nav-icon">⌂</span>Dashboard</button>
    <button onclick="showModule('master',this)"><span class="nav-icon">▦</span>Master Data</button>
    <button onclick="showModule('sales',this)"><span class="nav-icon">⇧</span>Penjualan</button>
    <button onclick="showModule('purchases',this)"><span class="nav-icon">⇩</span>Pembelian</button>
    <button onclick="showModule('cash',this)"><span class="nav-icon">▣</span>Kas & Bank</button>
    <button onclick="showModule('inventory',this)"><span class="nav-icon">▤</span>Persediaan</button>
    <button onclick="showModule('assembly',this)"><span class="nav-icon">⚒</span>Assembly</button>
    <button onclick="showModule('fixedassets',this)"><span class="nav-icon">▦</span>Aktiva Tetap</button>
    <button onclick="showModule('project',this)"><span class="nav-icon">◆</span>Proyek</button>
    <button onclick="showModule('accounting',this)"><span class="nav-icon">∑</span>Akuntansi</button><button onclick="showModule('reports',this)"><span class="nav-icon">▥</span>Laporan</button>
    <button onclick="showModule('system',this)"><span class="nav-icon">⚙</span>Sistem</button>
  </nav>
  <button class="logout-btn" onclick="logout()">Keluar / Logout</button>
</aside>

<div id="mobileDrawerBackdrop" class="mobile-drawer-backdrop hidden" onclick="closeMobileDrawer()"></div>
<section id="mobileDrawer" class="mobile-drawer hidden" aria-hidden="true">
  <div class="mobile-drawer-header"><strong>Menu Cepat</strong><button type="button" class="mobile-drawer-close" onclick="closeMobileDrawer()">×</button></div>
  <div id="mobileDrawerGrid" class="mobile-drawer-grid"></div>
  <button type="button" class="secondary mobile-drawer-logout" onclick="logout()">Keluar / Logout</button>
</section>
<nav id="mobileTabbar" class="mobile-tabbar hidden" aria-label="Navigasi mobile">
  <button type="button" data-mobile-tab="dashboard" onclick="openMobileDashboard(this)"><span class="nav-icon">⌂</span><span>Home</span></button>
  <button type="button" data-mobile-tab="sales" onclick="openMobileModule('sales',this)"><span class="nav-icon">⇧</span><span>Jual</span></button>
  <button type="button" data-mobile-tab="purchases" onclick="openMobileModule('purchases',this)"><span class="nav-icon">⇩</span><span>Beli</span></button>
  <button type="button" data-mobile-tab="cash" onclick="openMobileModule('cash',this)"><span class="nav-icon">▣</span><span>Kas</span></button>
  <button type="button" data-mobile-tab="more" onclick="openMobileDrawer(this)"><span class="nav-icon">☰</span><span>Menu</span></button>
</nav>

<div id="dashboard" class="page active"><div class="card"><h2>Ringkasan Persediaan</h2><div class="row"><div class="stat">Total Barang<b id="sTotal">0</b></div><div class="stat">Barang Aktif<b id="sActive">0</b></div><div class="stat">Stok Minimum<b id="sLow">0</b></div><div class="stat">Nilai Stok<b id="sValue">0</b></div></div></div><div class="card"><h2>Ringkasan Penjualan</h2><div class="row"><div class="stat">Transaksi<b id="ssCount">0</b></div><div class="stat">Total Penjualan<b id="ssTotal">0</b></div><div class="stat">Piutang<b id="ssDue">0</b></div></div></div><div class="card"><div class="table-toolbar"><h2>Analitik Bulan Ini</h2><button onclick="loadDash()">↻ Refresh</button></div><div class="analytics-grid"><div class="profit-chart-panel dashboard-chart-card"><h3>Profit &amp; Loss</h3><canvas id="pie" class="dashboard-chart-canvas" width="560" height="330"></canvas><div id="pieInfo" class="pl-summary"></div></div><div class="dashboard-chart-card"><h3>5 Barang Paling Laku</h3><canvas id="topItemsPie" class="dashboard-chart-canvas" width="420" height="270"></canvas><div id="topItems" class="mini-pie-summary"></div></div><div class="dashboard-chart-card"><h3>5 Top Sales</h3><canvas id="topSalesPie" class="dashboard-chart-canvas" width="420" height="270"></canvas><div id="topSales" class="mini-pie-summary"></div></div></div><div class="reminder-grid"><div><h3>Piutang Jatuh Tempo</h3><table><tbody id="dueAr"></tbody></table></div><div><h3>Hutang Jatuh Tempo</h3><table><tbody id="dueAp"></tbody></table></div><div><h3>Reminder Stok</h3><table><tbody id="lowSt"></tbody></table></div><div><h3>Dead Stock</h3><table><tbody id="deadSt"></tbody></table></div></div></div></div>
<div id="moduleHome" class="page"><div class="card module-shell"><div class="module-header"><div><p class="eyebrow">MODUL</p><h2 id="moduleTitle">Master Data</h2><p id="moduleDescription" class="muted">Pilih menu yang ingin dibuka.</p></div><button class="secondary" onclick="page('dashboard',document.querySelector('.module-nav button'))">Kembali ke Dashboard</button></div><div id="moduleGrid" class="module-grid"></div></div></div>


<div id="assembly" class="page">
 <div class="card"><div class="transaction-title"><div><h2>Assembly · Produksi Sederhana</h2><p class="muted">Tahap 1 mengambil bahan baku dan biaya ke Persediaan Dalam Proses (WIP). Tahap 2 membagi total cost ke satu atau beberapa barang jadi.</p></div></div>
 <div class="field-grid four"><label class="field"><span>Tanggal</span><input id="asmDate" type="date"></label><label class="field"><span>Gudang</span><select id="asmWarehouse"></select></label><label class="field"><span>Akun Persediaan Dalam Proses</span><select id="asmWip"></select></label><label class="field"><span>Catatan</span><input id="asmNotes"></label></div>
 <h3>Bahan Baku</h3><div class="action-bar"><button type="button" onclick="addAsmMaterial()">Tambah Bahan</button></div><table><thead><tr><th>Barang</th><th>Qty</th><th>Aksi</th></tr></thead><tbody id="asmMaterials"></tbody></table>
 <h3>Biaya Tambahan</h3><div class="action-bar"><button type="button" onclick="addAsmCost()">Tambah Biaya</button></div><table><thead><tr><th>Akun sumber biaya</th><th>Keterangan</th><th>Nilai</th><th>Aksi</th></tr></thead><tbody id="asmCosts"></tbody></table>
 <div class="action-bar"><button onclick="saveAssembly()">Posting Tahap 1</button></div><p id="asmMsg"></p></div>
 <div class="card"><div class="table-toolbar"><h2>Daftar Assembly</h2><button class="secondary" onclick="loadAssemblies()">↻ Refresh</button></div><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>Gudang</th><th>Material</th><th>Biaya</th><th>Total Cost</th><th>Status</th><th>Aksi</th></tr></thead><tbody id="asmList"></tbody></table></div><div class="card"><div class="table-toolbar"><h2>Daftar Penyelesaian Assembly</h2><button class="secondary" onclick="loadAssemblies()">↻ Refresh</button></div><table><thead><tr><th>Tanggal Finishing</th><th>Nomor</th><th>Gudang</th><th>Total Cost</th><th>Barang Jadi</th><th>Aksi</th></tr></thead><tbody id="asmFinishList"></tbody></table></div>
</div>
<div id="assemblyFinish" class="page"><div class="card"><h2>Finishing Assembly <span id="asmFinishNo"></span></h2><p class="muted">Kosongkan persentase untuk alokasi otomatis proporsional berdasarkan Qty × Harga Jual. Isi semua persentase untuk alokasi manual dengan total 100%.</p><label class="field"><span>Tanggal Finishing</span><input id="asmFinishDate" type="date"></label><div class="action-bar"><button onclick="addAsmOutput()">Tambah Barang Jadi</button></div><table><thead><tr><th>Barang Jadi</th><th>Qty</th><th>% Cost (opsional)</th><th>Aksi</th></tr></thead><tbody id="asmOutputs"></tbody></table><div class="action-bar"><button onclick="finishAssembly()">Posting Finishing</button><button class="secondary" onclick="page('assembly')">Kembali</button></div><p id="asmFinishMsg"></p></div></div>


<div id="subscriptionAdmin" class="page"><div class="card subscription-customer-card"><div class="transaction-title"><div><p class="eyebrow">LANGGANAN</p><h2>Trial & Langganan</h2><p class="muted">Pantau status akun dan hitung pilihan paket. Aktivasi langganan dikelola melalui StokLedger Owner Admin.</p></div><button class="secondary" onclick="loadSubscriptionAdmin()">↻ Refresh</button></div><div class="subscription-kpis"><div class="stat">Status<b id="subStatus">-</b></div><div class="stat">Sisa Hari<b id="subDays">-</b></div><div class="stat">Batas User<b id="subUsers">-</b></div><div class="stat">Berlaku Sampai<b id="subExpiry">-</b></div></div><div class="plan-grid"><div class="plan-card"><span class="plan-badge">6 BULAN</span><h3>Paket 6 Bulan</h3><b>Rp1.200.000 / 2 user</b><p class="muted">Add-on user Rp100.000/user per 6 bulan.</p></div><div class="plan-card featured"><span class="plan-badge">1 TAHUN</span><h3>Paket 1 Tahun</h3><b>Rp2.000.000 / 2 user</b><p class="muted">Add-on user Rp200.000/user per tahun.</p></div></div><div class="form-section subscription-estimator"><h3>Simulasi Paket</h3><p class="section-help">Pilih paket dan jumlah add-on user untuk melihat estimasi biaya. Hubungi admin StokLedger untuk aktivasi.</p><div class="field-grid two"><label class="field"><span>Paket</span><select id="subPlan"><option value="HALF">6 Bulan · Rp1.200.000 / 2 user</option><option value="YEAR">1 Tahun · Rp2.000.000 / 2 user</option></select></label><label class="field"><span>Add-on User</span><input id="subAddon" type="number" min="0" value="0"></label></div><div id="subPriceInfo" class="subscription-price-box"></div><p id="subMsg" class="muted"></p></div></div></div>
<div id="reportsPage" class="page">
<div class="card">
  <div class="transaction-title"><div><h2 id="reportTitle">Laporan</h2><p id="reportHelp" class="muted">Pilih laporan dari modul Laporan.</p></div>
  <div><button onclick="exportCurrentReport('xlsx')">Ekspor Excel</button> <button class="secondary" onclick="exportCurrentReport('pdf')">Ekspor PDF</button></div></div>
  <div class="field-grid four">
    <label class="field"><span>Tanggal Mulai</span><input id="reportFrom" type="date"></label>
    <label class="field"><span>Tanggal Akhir</span><input id="reportTo" type="date"></label>
    <label class="field report-filter" data-filter="customer"><span>Pelanggan</span><select id="reportCustomer"></select></label>
    <label class="field report-filter" data-filter="supplier"><span>Pemasok</span><select id="reportSupplier"></select></label>
    <label class="field report-filter" data-filter="salesperson"><span>Salesman</span><select id="reportSalesperson"></select></label>
    <label class="field report-filter" data-filter="product"><span>Barang</span><select id="reportProduct"></select></label>
    <label class="field report-filter" data-filter="category"><span>Kategori</span><select id="reportCategory"></select></label>
    <label class="field report-filter" data-filter="brand"><span>Merk</span><select id="reportBrand"></select></label>
    <label class="field report-filter" data-filter="warehouse"><span>Gudang</span><select id="reportWarehouse"></select></label>
    <label class="field report-filter" data-filter="inventory_account"><span>Akun Persediaan</span><select id="reportInventoryAccount"></select></label>
    <label class="field report-filter" data-filter="account"><span>Akun Buku Besar</span><select id="reportAccount" onchange="refreshReportLedgerPartner()"></select></label>
<label class="field report-filter" data-filter="ledger_partner"><span>Pelanggan / Pemasok</span><select id="reportLedgerPartner"><option value="">Semua</option></select><small id="reportLedgerPartnerHelp">Aktif untuk akun Piutang atau Hutang.</small></label>
<label class="field report-filter" data-filter="cash_account"><span>Akun Kas/Bank</span><select id="reportCashAccount"></select></label>
  </div>
  <div id="reportFieldSelector" class="form-section" style="display:none"><div class="row"><div><strong>Pilih Kolom yang Ditampilkan</strong><p class="help">Centang field yang ingin muncul pada laporan rincian dan hasil ekspor.</p></div><div><button type="button" class="secondary" onclick="toggleAllReportFields(true)">Pilih Semua</button> <button type="button" class="secondary" onclick="toggleAllReportFields(false)">Kosongkan</button></div></div><div id="reportFieldChecks" class="report-field-grid"></div></div>
  <div class="action-bar"><button onclick="loadCurrentReport()">Tampilkan Laporan</button><button class="secondary" onclick="resetReportFilters()">Reset Filter</button></div>
  <p id="reportMessage"></p>
</div>
<div class="card">
  <div id="reportSummary" class="summary-box"></div>
  <div id="financialReportView" class="financial-report-view" style="display:none"></div>
  <div id="reportTableContainer" class="table-scroll"><table><thead id="reportHead"></thead><tbody id="reportBody"></tbody></table></div>
</div>
</div>


<div id="fixedAssetNewPage" class="page"><div class="card"><div class="table-toolbar"><h2>Aktiva Tetap Baru</h2><button class="secondary" onclick="showModule('fixedassets')">Kembali</button></div><p class="help">Metode penyusutan garis lurus. Saat disimpan sistem membuat jurnal perolehan: Debit akun aktiva tetap dan Kredit akun lawan yang dipilih.</p><div class="field-grid three"><label class="field"><span>Kode Aktiva *</span><input id="faCode"></label><label class="field"><span>Nama Aktiva *</span><input id="faName"></label><label class="field"><span>Tanggal Perolehan *</span><input id="faDate" type="date"></label><label class="field"><span>Harga Perolehan *</span><input id="faCost" type="number" min="0" value="0"></label><label class="field"><span>Nilai Residu</span><input id="faResidual" type="number" min="0" value="0"></label><label class="field"><span>Masa Manfaat (bulan) *</span><input id="faLife" type="number" min="0" value="48"><small>Isi 0 untuk tanah/aset yang tidak disusutkan.</small></label><label class="field"><span>Akun Aktiva Tetap *</span><select id="faAssetAccount"></select></label><label class="field"><span>Akun Akumulasi Penyusutan *</span><select id="faAccumAccount"></select></label><label class="field"><span>Akun Beban Penyusutan *</span><select id="faExpenseAccount"></select></label><label class="field"><span>Akun Lawan Perolehan *</span><select id="faContraAccount"></select></label><label class="field wide-note"><span>Catatan</span><input id="faNotes"></label></div><div class="action-bar"><button onclick="saveFixedAsset()">Simpan Aktiva Tetap</button></div><p id="faMsg"></p></div></div>
<div id="fixedAssetListPage" class="page"><div class="card"><div class="table-toolbar"><div><h2>Daftar & Laporan Aktiva Tetap</h2><p class="help">Menampilkan harga perolehan, penyusutan per bulan, akumulasi penyusutan, dan nilai buku terkini.</p></div><div><button class="secondary" onclick="loadFixedAssets()">↻ Refresh</button><button class="secondary" onclick="window.print()">Cetak Laporan</button></div></div><div class="table-scroll"><table><thead><tr><th>Kode</th><th>Nama</th><th>Tgl Perolehan</th><th>Harga Perolehan</th><th>Nilai Residu</th><th>Masa Manfaat</th><th>Penyusutan/Bulan</th><th>Akumulasi Penyusutan</th><th>Nilai Buku</th><th>Status</th><th>Aksi</th></tr></thead><tbody id="faBody"></tbody><tfoot id="faFoot"></tfoot></table></div></div></div>
<div id="fixedAssetDepPage" class="page"><div class="card"><div class="table-toolbar"><h2>Penyusutan Otomatis Bulanan</h2><button class="secondary" onclick="showModule('fixedassets')">Kembali</button></div><p class="help">Penyusutan metode garis lurus dimulai sejak bulan perolehan. Setiap aktiva hanya dapat diproses satu kali untuk periode yang sama. Riwayat dapat dilihat dan dihapus untuk dihitung ulang.</p><div class="row fa-dep-controls" style="align-items:flex-end"><label>Periode<input id="faPeriod" type="month"></label><button onclick="runFixedAssetDepreciation()">Proses Penyusutan</button></div><p id="faDepMsg"></p></div><div class="card"><h3>Pratinjau Nilai Buku</h3><div class="table-scroll"><table><thead><tr><th>Kode</th><th>Nama</th><th>Penyusutan/Bulan</th><th>Akumulasi</th><th>Nilai Buku</th><th>Status</th></tr></thead><tbody id="faDepBody"></tbody></table><h3>Daftar Penyusutan yang Sudah Dibuat</h3><p class="muted">Gunakan tombol Hapus / Proses Ulang untuk membatalkan jurnal penyusutan lalu menghitung kembali periode tersebut.</p><div class="table-scroll"><table><thead><tr><th>Periode</th><th>Aktiva</th><th>Nilai</th><th>Jurnal</th><th>Aksi</th></tr></thead><tbody id="faDepHistory"></tbody></table></div></div></div></div>
<div id="systemInfo" class="page"><div class="card"><div class="row"><h2>Lokasi Database & Backup</h2><button class="secondary" onclick="loadSystemInfo()">↻ Refresh</button></div><p class="help">Informasi ini membantu menemukan database aktif dan folder backup otomatis aplikasi.</p><div class="form-section"><h3>Database Aktif</h3><p><strong>Lokasi file database</strong></p><div id="systemDbPath" style="word-break:break-all;padding:12px;border:1px solid #ccd8dc;border-radius:8px;background:#f7fafb"></div></div><div class="form-section"><h3>Backup Otomatis</h3><p><strong>Lokasi folder backup</strong></p><div id="systemBackupPath" style="word-break:break-all;padding:12px;border:1px solid #ccd8dc;border-radius:8px;background:#f7fafb"></div><p class="help">Backup dibuat otomatis setiap aplikasi/server ditutup secara normal. Sistem menyimpan maksimal 30 backup terbaru.</p></div><p id="systemInfoMsg"></p></div></div>
<div id="settings" class="page"><div class="card"><div class="row"><h2>Profil Perusahaan</h2><button class="secondary" onclick="runRefresh(this,loadCompany,'companyRefreshAt')">↻ Refresh</button><span id="companyRefreshAt" class="muted"></span></div><p class="help">Data ini akan digunakan pada header laporan, nota, dan dokumen perusahaan.</p><div class="row"><label>Nama Perusahaan<input id="coName" placeholder="Nama perusahaan"></label><label>NPWP / ID Pajak<input id="coTax" placeholder="NPWP"></label><label>Kota<input id="coCity" placeholder="Kota"></label></div><div class="row"><label>Telepon<input id="coPhone" placeholder="Telepon"></label><label>Email<input id="coEmail" placeholder="Email"></label><label>Website<input id="coWeb" placeholder="Website"></label></div><label>Alamat<textarea id="coAddress" placeholder="Alamat lengkap"></textarea></label>
<div class="form-section"><h3>Logo Perusahaan</h3><div class="row"><label>Pilih Logo PNG/JPG<input id="coLogoFile" type="file" accept="image/png,image/jpeg" onchange="previewCompanyLogo()"></label><img id="coLogoPreview" alt="Preview Logo" style="max-width:220px;max-height:100px;border:1px solid #ccd8dc;padding:6px;border-radius:8px"></div><small>Ukuran maksimal 2 MB. Logo akan digunakan pada dokumen cetak.</small></div>
<button onclick="saveCompany()">Simpan Profil</button><p id="coMsg"></p></div></div>
<div id="masterExtra" class="page"><div class="card"><input id="brandEditId" type="hidden"><div class="row"><h2>Master Merk</h2><button class="secondary" onclick="runRefresh(this,loadExtraMasters,'extraRefreshAt')">↻ Refresh</button><span id="extraRefreshAt" class="muted"></span></div><p class="help">Merk dipakai untuk pengelompokan barang dan laporan penjualan/pembelian per merk.</p><div class="row"><label>Kode Merk<input id="brandCode" placeholder="Contoh: ABC"></label><label>Nama Merk<input id="brandName" placeholder="Nama merk"></label><button onclick="addBrand()">Simpan Merk</button></div><table><thead><tr><th>Kode</th><th>Nama Merk</th><th>Status</th><th>Aksi</th></tr></thead><tbody id="brandBody"></tbody></table></div><div class="card"><input id="salespersonEditId" type="hidden"><h2>Master Salesman</h2><p class="help">Salesman dapat dipilih pada transaksi penjualan dan dipakai pada laporan penjualan per salesman.</p><div class="row"><label>Kode Salesman<input id="spCode" placeholder="Contoh: SLS01"></label><label>Nama Salesman<input id="spName" placeholder="Nama lengkap"></label><label>Telepon<input id="spPhone" placeholder="Telepon"></label><label>Email<input id="spEmail" placeholder="Email"></label><label>Komisi (%)<input id="spCommission" type="number" step="0.01" value="0"></label><button onclick="addSalesperson()">Simpan Salesman</button></div><table><thead><tr><th>Kode</th><th>Nama</th><th>Telepon</th><th>Komisi</th><th>Status</th><th>Aksi</th></tr></thead><tbody id="salespersonBody"></tbody></table></div></div><div id="servicesPage" class="page">
<div class="card">
  <div class="transaction-title"><div><h2>Daftar Jasa</h2>
  <p class="muted">Jasa tidak memiliki stok dan memiliki setting akun pembelian serta penjualan sendiri.</p></div>
  <button class="secondary" onclick="loadServicesPage()">↻ Refresh</button></div>
  <p id="serviceMsg"></p>
</div>

<div class="service-master-layout">
<div class="card">
  <h3 id="serviceFormTitle">Tambah Jasa</h3>
  <input id="serviceId" type="hidden">
  <div class="field-grid four">
    <label class="field"><span>Kode Jasa *</span><input id="serviceCode" placeholder="JAS001"></label>
    <label class="field"><span>Nama Jasa *</span><input id="serviceName" placeholder="Nama jasa"></label>
    <label class="field"><span>Kategori Jasa</span><select id="serviceCategory"></select></label>
    <label class="field"><span>Satuan (opsional)</span><select id="serviceUnit"></select></label>
    <label class="field"><span>Harga Beli Default</span><input id="serviceBuy" type="number" min="0" value="0"></label>
    <label class="field"><span>Harga Jual Default</span><input id="serviceSell" type="number" min="0" value="0"></label>
    <label class="field"><span>PPN %</span><input id="serviceTax" type="number" min="0" max="100" step="0.01" value="0"></label>
    <label class="field"><span>Status</span><select id="serviceActive"><option value="1">Aktif</option><option value="0">Nonaktif</option></select></label>
    <label class="field"><span>Akun Pembelian *</span><select id="servicePurchaseAccount"></select><small>HPP, Beban, atau Aset.</small></label>
    <label class="field"><span>Akun Penjualan *</span><select id="serviceSalesAccount"></select><small>Pendapatan atau Aset.</small></label>
  </div>
  <label class="field"><span>Keterangan</span><textarea id="serviceNotes" rows="2"></textarea></label>
  <div class="action-bar">
    <button onclick="saveService()">Simpan Jasa</button>
    <button class="secondary" onclick="resetServiceForm()">Form Baru</button>
  </div>
</div>

<div class="card">
  <h3 id="serviceCategoryFormTitle">Kategori Jasa</h3>
  <input id="serviceCategoryId" type="hidden">
  <div class="field-grid two">
    <label class="field"><span>Kode *</span><input id="serviceCategoryCode"></label>
    <label class="field"><span>Nama *</span><input id="serviceCategoryName"></label>
    <label class="field"><span>Status</span><select id="serviceCategoryActive"><option value="1">Aktif</option><option value="0">Nonaktif</option></select></label>
  </div>
  <label class="field"><span>Keterangan</span><textarea id="serviceCategoryNotes" rows="2"></textarea></label>
  <div class="action-bar">
    <button onclick="saveServiceCategory()">Simpan Kategori</button>
    <button class="secondary" onclick="resetServiceCategoryForm()">Form Baru</button>
  </div>
  <div class="table-scroll"><table><thead><tr><th>Kode</th><th>Nama</th><th>Status</th><th>Aksi</th></tr></thead><tbody id="serviceCategoryBody"></tbody></table></div>
</div>
</div>

<div class="card">
  <div class="table-toolbar"><h2>Daftar Jasa</h2>
    <input id="serviceSearch" placeholder="Cari kode atau nama jasa" oninput="loadServices()">
    <select id="serviceCategoryFilter" onchange="loadServices()"></select>
    <span id="serviceCount" class="muted"></span>
  </div>
  <div class="table-scroll"><table><thead><tr>
    <th>Kode</th><th>Nama Jasa</th><th>Kategori</th><th>Satuan</th>
    <th>Harga Beli</th><th>Harga Jual</th><th>PPN</th>
    <th>Akun Pembelian</th><th>Akun Penjualan</th><th>Status</th><th>Aksi</th>
  </tr></thead><tbody id="serviceBody"></tbody></table></div>
</div>
</div>


<div id="priceLevels" class="page"><div class="card"><input id="priceLevelEditId" type="hidden"><h2>Master Tingkatan Harga</h2><div class="field-grid three"><label class="field"><span>Kode *</span><input id="plCode" placeholder="RETAIL"></label><label class="field"><span>Nama *</span><input id="plName" placeholder="Retail"></label><label class="field"><span>Keterangan</span><input id="plDescription"></label></div><div class="action-bar"><button onclick="savePriceLevel()">Simpan</button></div><p id="plMsg"></p></div><div class="card"><h2>Daftar Tingkatan Harga</h2><table><thead><tr><th>Kode</th><th>Nama</th><th>Keterangan</th><th>Status</th><th>Aksi</th></tr></thead><tbody id="priceLevelBody"></tbody></table></div></div>
<div id="products" class="page"><div class="card"><input id="productEditId" type="hidden"><div class="row"><h2>Data Barang / Jasa</h2><button class="secondary" onclick="openMasterImportType('products')">Impor Excel</button></div><p class="help">Kolom bertanda wajib harus diisi. Pilih Jasa bila item tidak memiliki stok.</p><div class="product-recommendation-box"><div class="row"><div><h3 style="margin:0">Rekomendasi Barang Berdasarkan Jenis Usaha</h3><p class="muted" style="margin:4px 0 0">Pilih jenis usaha untuk menampilkan barang yang umum dipakai. Rekomendasi yang ditambahkan menjadi master barang biasa sehingga tetap dapat diubah atau dihapus.</p></div></div><div class="product-recommendation-toolbar"><label class="field"><span>Jenis Usaha</span><select id="productBusinessTemplate" onchange="renderProductRecommendations()"><option value="">-- Pilih Jenis Usaha --</option><option value="retail">Toko / Retail Umum</option><option value="workshop">Bengkel Motor / Mobil</option><option value="pharmacy">Apotek</option><option value="restaurant">Warung / Restoran / Cafe</option><option value="construction">Kontraktor Bangunan</option><option value="interior">Kontraktor Interior / Renovasi</option><option value="mep">Kontraktor MEP / Instalasi</option><option value="school">Sekolah / Pendidikan</option><option value="plantation">Perkebunan / Pertanian</option><option value="distributor">Distributor / Grosir</option><option value="manufacturing">Pabrik / Manufaktur Ringan</option><option value="services">Usaha Jasa Umum</option></select></label><button type="button" class="secondary" onclick="selectAllProductRecommendations(true)">Pilih Semua</button><button type="button" onclick="addSelectedProductRecommendations()">+ Tambahkan Terpilih</button></div><div id="productRecommendationInfo" class="muted" style="margin-top:8px"></div><div id="productRecommendationList" class="product-recommendation-list"></div></div><div class="product-master-grid"><label>Kode Barang / SKU *<input id="pSku" placeholder="Contoh: BRG001" title="Kode unik barang"></label><label>Barcode<input id="pBarcode" placeholder="Opsional"></label><label>Nama Barang / Jasa *<input id="pName" placeholder="Nama item"></label><label>Kategori<select id="pCategory"></select></label><label>Merk<select id="pBrand"></select></label><label>Satuan *<select id="pUnit"></select></label><label>Jenis Item<select id="pType"><option value="STOCK">Barang Stok</option><option value="SERVICE">Jasa</option></select></label></div><div class="product-master-grid"><label>Harga Beli<input id="pBuy" type="number" value="0"></label><label>Harga Jual<input id="pSell" type="number" value="0"></label><label>Gudang Stok Awal<select id="pWarehouse"></select></label><label>Stok Awal<input id="pInitial" type="number" value="0"></label><label>Tanggal Saldo Awal<input id="pOpeningDate" type="date"></label><label>Stok Minimum<input id="pMinimum" type="number" value="0"></label></div>
<div class="form-section" style="margin-top:12px"><h3>Multi Satuan Barang</h3><p class="muted">Satuan utama mengikuti pilihan Satuan di atas. Tambahkan satuan alternatif dan isi rasio terhadap satuan utama.</p><div id="productUnitRows" class="product-unit-editor"></div><div class="action-bar" style="justify-content:flex-start"><button type="button" class="secondary" onclick="addProductUnitRow()">+ Tambah Satuan Alternatif</button></div></div><div class="form-section" style="margin-top:12px"><h3>Harga Jual per Tingkatan</h3><p class="muted">Kosongkan atau isi 0 untuk memakai Harga Jual Default.</p><div id="productPriceLevelGrid" class="field-grid three"></div></div><div class="form-section" style="margin-top:12px"><h3>Setting Akun Barang</h3><p class="muted">Setting ini digunakan otomatis pada pembelian, penjualan, HPP, dan penyesuaian stok.</p>
<div class="field-grid three">
<label class="field"><span>Akun Persediaan *</span><select id="pInventoryAccount"></select></label>
<label class="field"><span>Akun Penjualan *</span><select id="pSalesAccount"></select></label>
<label class="field"><span>Akun HPP *</span><select id="pCogsAccount"></select></label>
</div></div>
<div class="action-bar"><button onclick="addProduct()">Simpan Barang</button></div><p id="pMsg"></p></div><div class="card"><div class="row"><h2>Daftar Barang</h2><button class="secondary" onclick="runRefresh(this,loadProducts,'productsRefreshAt')">↻ Refresh</button><span id="productsRefreshAt" class="muted"></span><input id="productSearch" placeholder="Cari SKU / nama / barcode" oninput="filterProductTable()"></div><div class="table-scroll"><table class="product-stock-table"><thead><tr><th>SKU</th><th>Nama</th><th>Jenis</th><th>Merk</th><th>Stok Satuan 1</th><th>Stok Satuan 2</th><th>Stok Satuan 3</th><th>Harga Jual</th><th>Akun Persediaan</th><th>Akun Penjualan</th><th>Akun HPP</th><th>Aksi</th></tr></thead><tbody id="productBody"></tbody></table></div></div></div>

<div id="customersPage" class="page">
  <div class="card"><input id="customerEditId" type="hidden">
    <h2>Data Pelanggan</h2>
    <p class="help">Saldo Awal Piutang adalah jumlah piutang pelanggan sebelum mulai memakai StokLedger Pro.</p>
    <div class="field-grid three">
      <label class="field"><span>Kode Pelanggan *</span><input id="custCode" placeholder="Contoh: CUST001"></label>
      <label class="field"><span>Nama Pelanggan *</span><input id="custName" placeholder="Nama pelanggan"></label>
      <label class="field"><span>Telepon</span><input id="custPhone"></label>
      <label class="field"><span>Email</span><input id="custEmail"></label>
      <label class="field"><span>Kota</span><input id="custCity"></label>
      <label class="field"><span>Termin Piutang (hari)</span><input id="custTerm" type="number" value="0"></label>
      <label class="field"><span>Batas Kredit</span><input id="custLimit" type="number" value="0"></label><label class="field"><span>Akun Piutang Pelanggan</span><select id="custReceivableAccount"><option value="">Default - Piutang Usaha</option></select><small>Bisa dibedakan per segmen pelanggan.</small></label><label class="field"><span>Tingkatan Harga</span><select id="custPriceLevel"><option value="">Harga Default</option></select></label>
      <label class="field"><span>Saldo Awal Piutang</span><input id="custOpening" type="number" value="0"><small>Otomatis dijurnal ke Piutang Usaha.</small></label><label class="field"><span>Tanggal Saldo Awal</span><input id="custOpeningDate" type="date"></label>
      <label class="field wide-note"><span>Alamat</span><input id="custAddress"></label>
    </div>
    <div class="action-bar"><button onclick="addCustomer()">Simpan Pelanggan</button></div>
    <p id="custMsg"></p>
  </div>
  <div class="card">
    <div class="table-toolbar"><h2>Daftar Pelanggan</h2><button class="secondary" onclick="openMasterImportType('customers')">Impor Excel</button><button onclick="loadCustomersPage()">↻ Refresh</button></div>
    <table><thead><tr><th>Kode</th><th>Nama Pelanggan</th><th>Telepon</th><th>Kota</th><th>Termin</th><th>Tanggal Saldo Awal</th><th>Saldo Awal Piutang</th><th>Aksi</th></tr></thead><tbody id="customersPageBody"></tbody></table>
  </div>
</div>
<div id="suppliersPage" class="page">
  <div class="card"><input id="supplierEditId" type="hidden">
    <h2>Data Pemasok</h2>
    <p class="help">Saldo Awal Hutang adalah jumlah hutang kepada pemasok sebelum mulai memakai StokLedger Pro.</p>
    <div class="field-grid three">
      <label class="field"><span>Kode Pemasok *</span><input id="supCode" placeholder="Contoh: SUP001"></label>
      <label class="field"><span>Nama Pemasok *</span><input id="supName" placeholder="Nama pemasok"></label>
      <label class="field"><span>Telepon</span><input id="supPhone"></label>
      <label class="field"><span>Email</span><input id="supEmail"></label>
      <label class="field"><span>Kota</span><input id="supCity"></label>
      <label class="field"><span>Termin Hutang (hari)</span><input id="supTerm" type="number" value="0"></label><label class="field"><span>Akun Hutang Pemasok</span><select id="supPayableAccount"><option value="">Default - Hutang Usaha</option></select><small>Bisa dibedakan per segmen pemasok.</small></label>
      <label class="field"><span>Saldo Awal Hutang</span><input id="supOpening" type="number" value="0"><small>Otomatis dijurnal ke Hutang Usaha.</small></label><label class="field"><span>Tanggal Saldo Awal</span><input id="supOpeningDate" type="date"></label>
      <label class="field wide-note"><span>Alamat</span><input id="supAddress"></label>
    </div>
    <div class="action-bar"><button onclick="addSupplier()">Simpan Pemasok</button></div>
    <p id="supMsg"></p>
  </div>
  <div class="card">
    <div class="table-toolbar"><h2>Daftar Pemasok</h2><button class="secondary" onclick="openMasterImportType('suppliers')">Impor Excel</button><button onclick="loadSuppliersPage()">↻ Refresh</button></div>
    <table><thead><tr><th>Kode</th><th>Nama Pemasok</th><th>Telepon</th><th>Kota</th><th>Termin</th><th>Tanggal Saldo Awal</th><th>Saldo Awal Hutang</th><th>Aksi</th></tr></thead><tbody id="suppliersPageBody"></tbody></table>
  </div>
</div>

<div id="partners" class="page"><div class="card"><div class="row"><h2>Tambah Pelanggan / Supplier</h2><button class="secondary" onclick="openMasterImportType(bType.value==='SUPPLIER'?'suppliers':'customers')">Impor Excel</button></div><input id="partnerEditId" type="hidden"><div class="row"><select id="bType"><option value="CUSTOMER">Pelanggan</option><option value="SUPPLIER">Supplier</option><option value="BOTH">Keduanya</option></select><input id="bCode" placeholder="Kode"><input id="bName" placeholder="Nama"><input id="bPhone" placeholder="Telepon"><input id="bEmail" placeholder="Email"></div><div class="row" style="margin-top:9px"><input id="bTax" placeholder="NPWP"><input id="bCity" placeholder="Kota"><input id="bTerm" type="number" value="0"><input id="bLimit" type="number" value="0"><input id="bOpening" type="number" value="0" placeholder="Saldo Awal"><input id="bAddress" placeholder="Alamat"><button onclick="addPartner()">Simpan</button></div><p id="bMsg"></p></div><div class="card"><div class="row"><h2>Daftar Pelanggan & Supplier</h2><button class="secondary" onclick="runRefresh(this,loadPartners,'partnersRefreshAt')">↻ Refresh</button><span id="partnersRefreshAt" class="muted"></span><input id="partnerSearch" placeholder="Cari" oninput="loadPartners()"><select id="partnerFilter" onchange="loadPartners()"><option value="">Semua</option><option value="CUSTOMER">Pelanggan</option><option value="SUPPLIER">Supplier</option><option value="BOTH">Keduanya</option></select></div><table><thead><tr><th>Kode</th><th>Nama</th><th>Jenis</th><th>Telepon</th><th>Kota</th><th>Termin</th><th>Aksi</th></tr></thead><tbody id="partnerBody"></tbody></table></div></div>
<div id="masters" class="page"><div class="card"><input id="categoryEditId" type="hidden"><h2>Kategori</h2><div class="row"><input id="cCode"><input id="cName"><button onclick="addCategory()">Tambah</button></div><table><tbody id="catBody"></tbody></table></div><div class="card"><input id="unitEditId" type="hidden"><h2>Satuan</h2><div class="row"><input id="uCode"><input id="uName"><input id="uDecimals" type="number" value="0"><button onclick="addUnit()">Tambah</button></div><table><tbody id="unitBody"></tbody></table></div></div>


<div id="cash" class="page">
<div class="card cash-section cash-accounts"><div class="transaction-title"><div><h2>Akun Kas & Bank</h2><p class="muted">Buat akun kas tunai atau rekening bank yang dipakai pada transaksi.</p></div><div><button class="secondary" onclick="refreshCash(this)">↻ Refresh</button><span id="cashRefreshAt" class="muted"></span></div></div>
<div class="form-section"><h3>Informasi Akun</h3><p class="section-help">Kode dan nama akun wajib diisi. Saldo awal hanya diisi saat pertama kali membuat akun.</p><div class="field-grid three"><label class="field"><span>Kode Akun <b class="required">*</b></span><input id="caCode" placeholder="Contoh: KAS01"></label><label class="field"><span>Nama Akun <b class="required">*</b></span><input id="caName" placeholder="Contoh: Kas Utama"></label><label class="field"><span>Jenis Akun <b class="required">*</b></span><select id="caType"><option value="CASH">Kas</option><option value="BANK">Bank</option></select></label><label class="field"><span>Nama Bank</span><input id="caBank" placeholder="Kosongkan untuk akun kas"></label><label class="field"><span>Nomor Rekening</span><input id="caNumber" placeholder="Opsional"></label><label class="field"><span>Saldo Awal</span><input id="caOpening" type="number" value="0" placeholder="0"><small>Membuat jurnal saldo awal otomatis.</small></label><label class="field"><span>Tanggal Saldo Awal</span><input id="caOpeningDate" type="date"></label><label class="field"><span>COA Kas/Bank</span><select id="caCoaAccount"></select></label></div><div class="action-bar"><button onclick="addCashAccount()">Simpan Akun</button><button class="secondary" onclick="openCashOpeningImport()">Impor Kas/Bank + Saldo Awal</button><button class="secondary" onclick="downloadCashOpeningTemplate()">Download Template Kas/Bank</button></div><p class="section-help"><b>Petunjuk template:</b> Kode, Nama, Jenis CASH/BANK, Nama Bank, Nomor Rekening, Saldo Awal, Tanggal Saldo Awal, Kode COA Kas/Bank.</p></div><p id="caMsg"></p><table><thead><tr><th>Kode</th><th>Nama</th><th>Jenis</th><th>Saldo</th><th>Status</th></tr></thead><tbody id="cashAccountsBody"></tbody></table></div>
<div class="card cash-section cash-entry"><h2>Kas Masuk / Keluar</h2><p class="muted">Gunakan Kas Masuk untuk penerimaan non-penjualan dan Kas Keluar untuk biaya atau pengeluaran lainnya.</p><div class="form-section"><div class="field-grid three"><label class="field"><span>Tanggal Transaksi <b class="required">*</b></span><input id="cashDate" type="date"></label><label class="field"><span>Akun Kas / Bank <b class="required">*</b></span><select id="cashAccount"></select></label><label class="field"><span>Jenis Transaksi <b class="required">*</b></span><select id="cashType"><option value="IN">Kas Masuk</option><option value="OUT">Kas Keluar</option></select></label><label class="field"><span>Akun Lawan Transaksi *</span><select id="cashCounterAccount"></select><small>Kas Masuk: akun lawan dikredit. Kas Keluar: akun lawan didebit.</small></label><label class="field"><span>Jumlah <b class="required">*</b></span><input id="cashAmount" type="number" min="0" placeholder="0"></label><label class="field"><span>Nomor Referensi</span><input id="cashRef" placeholder="Contoh: BKK-001"></label><label class="field"><span>Keterangan <b class="required">*</b></span><input id="cashDesc" placeholder="Tujuan penerimaan/pengeluaran"></label><label class="field"><span>Departemen</span><select id="cashDepartment"></select><small>Opsional. Cost center penerimaan/pengeluaran.</small></label><label class="field"><span>Proyek</span><select id="cashProject"></select><small>Opsional. Proyek terkait transaksi Kas/Bank.</small></label></div><div class="action-bar"><button onclick="saveCashTransaction()">Simpan Transaksi</button><button class="secondary" onclick="downloadImportTemplate('cash-transactions')">Download Template Excel</button><label class="button-like">Impor Excel<input id="cash-transactionsExcelFile" type="file" accept=".xlsx" hidden onchange="importTransactionExcel('cash-transactions')"></label></div></div><p id="cashMsg"></p></div>
<div class="card cash-section cash-transfer"><h2>Transfer Antar Akun</h2><p class="muted">Memindahkan saldo dari satu akun kas/bank ke akun lainnya dalam satu transaksi.</p><div class="form-section"><div class="field-grid three"><label class="field"><span>Tanggal Transfer <b class="required">*</b></span><input id="transferDate" type="date"></label><label class="field"><span>Akun Sumber <b class="required">*</b></span><select id="cashSource"></select></label><label class="field"><span>Akun Tujuan <b class="required">*</b></span><select id="cashTarget"></select></label><label class="field"><span>Jumlah Transfer <b class="required">*</b></span><input id="transferAmount" type="number" min="0" placeholder="0"></label><label class="field"><span>Nomor Referensi</span><input id="transferRef" placeholder="Opsional"></label><label class="field"><span>Keterangan</span><input id="transferDesc" placeholder="Contoh: Pemindahan dana operasional"></label></div><div class="action-bar"><button onclick="saveCashTransfer()">Proses Transfer</button></div></div><p id="transferMsg"></p></div>
<div class="card cash-section cash-history"><div class="table-toolbar"><h2>Riwayat Kas & Bank</h2><button class="secondary" onclick="refreshCash(this)">↻ Refresh</button><span id="cashTxRefreshAt" class="muted"></span><label class="field"><span>Filter Akun</span><select id="cashFilterAccount" onchange="loadCashTransactions()"></select></label><label class="field"><span>Cari Transaksi</span><input id="cashSearch" placeholder="Nomor atau keterangan" oninput="loadCashTransactions()"></label></div><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>Akun</th><th>Jenis</th><th>Jumlah</th><th>Saldo</th><th>Keterangan</th><th>User</th></tr></thead><tbody id="cashTransactionsBody"></tbody></table></div>
</div>


<div id="purchaseReturns" class="page"><div class="card"><h2>Retur Pembelian</h2><p class="help">Dapat ditarik dari invoice pembelian atau dibuat tanpa invoice.</p><div class="field-grid three"><label class="field"><span>Invoice Pembelian (opsional)</span><select id="prInvoice" onchange="loadPurchaseReturnInvoice()"><option value="">Tanpa invoice</option></select></label><label class="field"><span>Tanggal</span><input id="prDate" type="date"></label><label class="field"><span>Pemasok</span><select id="prSupplier"></select></label><label class="field"><span>Gudang</span><select id="prWarehouse"></select></label><label class="field wide-note"><span>Catatan</span><input id="prNotes"></label></div><div class="action-bar"><button onclick="addReturnLine('pr')">Tambah Barang</button><button onclick="savePurchaseReturn()">Simpan Retur Pembelian</button></div><table><thead><tr><th>Barang</th><th>Qty</th><th>Nilai Hutang/Unit</th><th>Aksi</th></tr></thead><tbody id="prBody"></tbody></table><p id="prMsg"></p></div><div class="card"><h2>Daftar Retur Pembelian</h2><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>Pemasok</th><th>Nilai Hutang</th><th>Nilai Persediaan</th><th>Selisih HPP</th><th>Aksi</th></tr></thead><tbody id="prList"></tbody></table></div></div>
<div id="salesReturns" class="page"><div class="card"><h2>Retur Penjualan</h2><p class="help">Dapat ditarik dari invoice penjualan atau dibuat tanpa invoice.</p><div class="field-grid three"><label class="field"><span>Invoice Penjualan (opsional)</span><select id="srInvoice" onchange="loadSalesReturnInvoice()"><option value="">Tanpa invoice</option></select></label><label class="field"><span>Tanggal</span><input id="srDate" type="date"></label><label class="field"><span>Pelanggan</span><select id="srCustomer"></select></label><label class="field"><span>Gudang</span><select id="srWarehouse"></select></label><label class="field wide-note"><span>Catatan</span><input id="srNotes"></label></div><div class="action-bar"><button onclick="addReturnLine('sr')">Tambah Barang</button><button onclick="saveSalesReturn()">Simpan Retur Penjualan</button></div><table><thead><tr><th>Barang/Jasa</th><th>Qty</th><th>Nilai Retur/Unit</th><th>Aksi</th></tr></thead><tbody id="srBody"></tbody></table><p id="srMsg"></p></div><div class="card"><h2>Daftar Retur Penjualan</h2><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>Pelanggan</th><th>Nilai Retur</th><th>Nilai HPP</th><th>Aksi</th></tr></thead><tbody id="srList"></tbody></table></div></div>


<div id="ordersDp" class="page"><div class="card"><h2 id="odPageHeading">Pesanan & Uang Muka</h2><p class="muted">Alur sederhana StokLedger: Pesanan → DP → Invoice → Alokasi DP → Pelunasan.</p><div class="row" id="odSalesTabs"><button onclick="odTab('sales')">Pesanan Penjualan</button><button onclick="odTab('customerDp')">DP Pelanggan</button><button onclick="odTab('allocation')">Alokasi DP Pelanggan</button></div><div class="row" id="odPurchaseTabs"><button onclick="odTab('purchase')">Pesanan Pembelian</button><button onclick="odTab('supplierDp')">DP Pemasok</button><button onclick="odTab('allocation')">Alokasi DP Pemasok</button></div></div>
<div id="odEditor" class="card"><h2 id="odTitle"></h2><div id="odContent"></div><p id="odMsg"></p></div></div>

<div id="sales" class="page"><div class="card sales-section sales-entry"><div class="transaction-title"><div><h2>Transaksi Penjualan</h2><p class="muted">Isi informasi transaksi, tambahkan barang/jasa, lalu periksa ringkasan sebelum disimpan.</p></div><div class="action-bar"><button class="secondary" type="button" onclick="downloadImportTemplate('sales')">Download Format Excel</button><label class="button-like">Impor Faktur Excel<input id="salesExcelFile" type="file" accept=".xlsx" hidden onchange="importTransactionExcel('sales')"></label></div></div>
<div class="form-section"><h3>1. Informasi Penjualan</h3><p class="section-help">Nomor otomatis dapat diedit sebelum transaksi disimpan.</p><div class="field-grid"><label class="field"><span>Nomor Invoice *</span><input id="saleInvoiceNo" placeholder="Otomatis"></label><label class="field"><span>No. Surat Jalan *</span><input id="saleDeliveryNo" placeholder="Otomatis"></label><label class="field"><span>Tanggal Penjualan <b class="required">*</b></span><input id="saleDate" type="date"></label><label class="field"><span>Gudang Pengeluaran <b class="required">*</b></span><select id="saleWarehouse"></select><small>Stok barang diambil dari gudang ini.</small></label><label class="field"><span>Pelanggan</span><select id="saleCustomer"></select><small>Pilih pelanggan atau gunakan pelanggan umum.</small></label><label class="field"><span>Salesman</span><select id="saleSalesperson"></select></label><label class="field"><span>Departemen</span><select id="saleDepartment"></select><small>Opsional. Pilih cost center transaksi.</small></label><label class="field"><span>Proyek</span><select id="saleProject"></select><small>Opsional. Pilih proyek terkait.</small></label></div></div>
<div class="form-section"><h3>2. Pembayaran & Pajak</h3><p class="section-help">Untuk transaksi kredit, isi termin dan jatuh tempo. Untuk tunai/transfer, pilih akun penerimaan.</p><div class="field-grid"><label class="field"><span>Metode Pembayaran <b class="required">*</b></span><select id="salePayment" onchange="paymentChanged()"><option value="CASH">Tunai</option><option value="TRANSFER">Transfer</option><option value="CREDIT">Kredit</option></select></label><label class="field"><span>Akun Kas / Bank</span><select id="saleCashAccount"></select><small>Wajib untuk pembayaran tunai atau transfer.</small></label><label class="field"><span>Termin Pembayaran (hari)</span><input id="saleTerm" type="number" value="0"><small>Jumlah hari sampai jatuh tempo.</small></label><label class="field"><span>Tanggal Jatuh Tempo</span><input id="saleDue" type="date"></label><label class="field"><span>PPN (%)</span><input id="saleTax" type="number" value="0" oninput="estimateSale()"></label><label class="field"><span>Jenis Diskon Transaksi</span><select id="saleDiscountMode"><option value="AMOUNT">Nominal Rupiah</option><option value="PERCENT">Persentase</option></select></label><label class="field"><span>Nilai Diskon Transaksi</span><input id="saleDiscount" type="number" value="0" oninput="estimateSale()"></label><label class="field"><span>Jumlah Dibayar</span><input id="salePaid" type="number" value="0"><small>Untuk kredit dapat diisi sebagai uang muka.</small></label></div></div>
<div class="form-section transaction-lines-section"><div class="transaction-lines-title"><div><h3>3. Detail Barang / Jasa</h3><p class="section-help">Pilih barang, satuan, qty, harga, dan diskon. Subtotal dihitung otomatis per baris.</p></div><button type="button" onclick="addSaleLine()">+ Tambah Item</button></div><div class="transaction-grid-scroll"><div class="line-header sale-grid"><span>No.</span><span>Barang / Jasa</span><span>Satuan</span><span>Deskripsi Invoice</span><span>Qty</span><span>Harga Jual</span><span>Diskon</span><span>Subtotal</span><span>Aksi</span></div><div id="saleLines"></div></div><p class="keyboard-hint">Tip: gunakan Tab untuk berpindah kolom. Tekan Ctrl + Enter untuk menambah baris baru.</p></div>
<div class="form-section"><div class="transaction-lines-title"><div><h3>4. Material Proyek pada Faktur <span class="muted">(Opsional)</span></h3><p class="section-help">Hanya untuk informasi cetak invoice. Tidak menambah tagihan, tidak mengurangi stok, dan tidak membuat jurnal.</p></div><button type="button" class="secondary" onclick="loadSaleInvoiceMaterials()">Muat Material Proyek</button></div><div id="saleInvoiceMaterials" class="invoice-material-box"><span class="muted">Belum ada material yang dipilih.</span></div></div><div class="form-section"><h3>5. Catatan & Ringkasan</h3><div class="field-grid two"><label class="field"><span>Catatan Transaksi</span><textarea id="saleNotes" placeholder="Catatan tambahan untuk transaksi"></textarea></label><div class="summary-box"><div class="summary-row total"><span>Perkiraan Total</span><span id="saleEstimate">Rp0</span></div></div></div><div class="action-bar"><button onclick="saveSale()">Simpan Penjualan</button></div></div><p id="saleMsg"></p></div>
<div class="card sales-section sales-list"><div class="table-toolbar"><h2>Daftar Penjualan</h2><button class="secondary" onclick="runRefresh(this,loadSales,'salesRefreshAt')">↻ Refresh</button><span id="salesRefreshAt" class="muted"></span><label class="field"><span>Cari Invoice / Pelanggan</span><input id="saleSearch" placeholder="Ketik kata kunci" oninput="loadSales()"></label></div><table><thead><tr><th>Tanggal</th><th>Invoice</th><th>Pelanggan</th><th>Salesman</th><th>Metode</th><th>Jatuh Tempo</th><th>PPN</th><th>Total</th><th>Piutang</th><th>Aksi</th><th>Cetak Dokumen</th></tr></thead><tbody id="salesBody"></tbody></table></div></div>
<div id="purchases" class="page">
<div class="card purchase-section purchase-entry"><div class="transaction-title"><div><h2>Transaksi Pembelian</h2><p class="muted">Isi supplier dan tujuan gudang, kemudian tambahkan barang/jasa yang dibeli.</p></div><div class="action-bar"><button class="secondary" type="button" onclick="downloadImportTemplate('purchases')">Download Format Excel</button><label class="button-like">Impor Faktur Excel<input id="purchasesExcelFile" type="file" accept=".xlsx" hidden onchange="importTransactionExcel('purchases')"></label></div></div>
<div class="form-section"><h3>1. Informasi Pembelian</h3><p class="section-help">Nomor referensi pemasok dapat diisi manual. Nomor GR otomatis dapat diedit.</p><div class="field-grid"><label class="field"><span>Nomor Invoice / Referensi</span><input id="purchaseSupplierInvoice" placeholder="Nomor dari pemasok"></label><label class="field"><span>No. Good Receive *</span><input id="purchaseGoodsReceipt" placeholder="Otomatis"></label><label class="field"><span>Tanggal Pembelian <b class="required">*</b></span><input id="purchaseDate" type="date"></label><label class="field"><span>Supplier / Pemasok <b class="required">*</b></span><select id="purchaseSupplier"></select><small id="purchaseSupplierHelp">Pilih pemasok aktif dari Data Pemasok.</small></label><label class="field"><span>Gudang Tujuan <b class="required">*</b></span><select id="purchaseWarehouse"></select><small>Stok pembelian masuk ke gudang ini.</small></label><label class="field"><span>Metode Pembayaran <b class="required">*</b></span><select id="purchasePayment"><option value="CASH">Tunai</option><option value="TRANSFER">Transfer</option><option value="CREDIT">Kredit</option></select></label><label class="field"><span>Departemen</span><select id="purchaseDepartment"></select><small>Opsional. Pilih cost center transaksi.</small></label><label class="field"><span>Proyek</span><select id="purchaseProject"></select><small>Opsional. Pilih proyek terkait.</small></label></div></div>
<div class="form-section"><h3>2. Pembayaran & Pajak</h3><div class="field-grid"><label class="field"><span>Akun Kas / Bank</span><select id="purchaseCashAccount"></select><small>Wajib untuk pembelian tunai/transfer.</small></label><label class="field"><span>Termin Pembayaran (hari)</span><input id="purchaseTerm" type="number" value="0"><small>Jumlah hari sampai jatuh tempo.</small></label><label class="field"><span>Tanggal Jatuh Tempo</span><input id="purchaseDue" type="date"></label><label class="field"><span>PPN (%)</span><input id="purchaseTax" type="number" value="0" oninput="renderPurchaseLines()"></label><label class="field"><span>Jumlah Dibayar</span><input id="purchasePaid" type="number" value="0"><small>Untuk kredit dapat diisi sebagai uang muka.</small></label><label class="field"><span>Jenis Diskon Transaksi</span><select id="purchaseDiscountMode" onchange="renderPurchaseLines()"><option value="AMOUNT">Nominal Rupiah</option><option value="PERCENT">Persentase</option></select></label><label class="field"><span>Nilai Diskon Transaksi</span><input id="purchaseDiscount" type="number" value="0" oninput="renderPurchaseLines()"></label><label class="field"><span>Catatan Pembelian</span><input id="purchaseNotes" placeholder="Opsional"></label></div></div>
<div class="form-section transaction-lines-section"><div class="transaction-lines-title"><div><h3>3. Tambah Barang / Jasa</h3><p class="section-help">Isi item pembelian pada satu baris yang presisi. Baris jasa tidak menambah stok.</p></div></div><div class="purchase-line-editor"><label class="field purchase-product-field"><span>Barang / Jasa <b class="required">*</b></span><select id="purchaseProduct"></select></label><label class="field"><span>Satuan</span><select id="purchaseUnit"></select></label><label class="field numeric-field"><span>Qty <b class="required">*</b></span><input id="purchaseQty" type="number" inputmode="decimal" step="0.0001" value="1"></label><label class="field numeric-field"><span>Harga Beli <b class="required">*</b></span><input id="purchaseCost" type="number" inputmode="decimal" step="0.01" placeholder="0"></label><label class="field discount-field"><span>Diskon Item</span><div class="discount-combo"><select id="purchaseLineDiscountMode"><option value="AMOUNT">Nominal</option><option value="PERCENT">Persen</option></select><input id="purchaseLineDiscount" type="number" inputmode="decimal" step="0.01" value="0"></div></label><button type="button" class="purchase-add-btn" onclick="addPurchaseLine()">+ Tambah Item</button></div></div>
<div class="form-section"><h3>4. Daftar Item & Ringkasan</h3><div class="transaction-grid-scroll"><table class="purchase-lines-table"><thead><tr><th>No.</th><th>Barang / Jasa</th><th>Satuan</th><th class="num">Qty</th><th class="num">Harga</th><th class="num">Diskon</th><th class="num">Subtotal</th><th class="action-col">Aksi</th></tr></thead><tbody id="purchaseLinesBody"></tbody></table></div><div class="action-bar"><div class="summary-box"><div class="summary-row total"><span>Total Pembelian</span><span id="purchaseGrandTotal">Rp0</span></div></div><button onclick="savePurchase()">Simpan Pembelian</button></div></div><p id="purchaseMsg"></p></div>
<div class="card purchase-section purchase-list"><div class="table-toolbar"><h2>Daftar Pembelian</h2><button class="secondary" onclick="runRefresh(this,loadPurchases,'purchasesRefreshAt')">↻ Refresh</button><span id="purchasesRefreshAt" class="muted"></span><label class="field"><span>Cari Nomor / Supplier</span><input id="purchaseSearch" placeholder="Ketik kata kunci" oninput="loadPurchases()"></label><label class="field"><span>Dari Tanggal</span><input id="purchaseFrom" type="date" onchange="loadPurchases()"></label><label class="field"><span>Sampai Tanggal</span><input id="purchaseTo" type="date" onchange="loadPurchases()"></label></div><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>Supplier</th><th>Gudang</th><th>Metode</th><th>Jatuh Tempo</th><th>PPN</th><th>Total</th><th>Hutang</th><th>Aksi</th><th>Cetak Dokumen</th></tr></thead><tbody id="purchasesBody"></tbody></table></div>
</div>

<div id="inventory" class="page">
<div class="card inventory-section inventory-warehouses"><div class="transaction-title"><div><h2>Daftar Nama Gudang</h2><p class="muted">Buat dan kelola lokasi gudang untuk stok multi gudang.</p></div><button class="secondary" onclick="loadWarehouseMaster()">↻ Refresh</button></div><input id="wEditId" type="hidden"><div class="field-grid"><label class="field"><span>Kode Gudang *</span><input id="wCode" placeholder="Contoh: UTAMA"></label><label class="field"><span>Nama Gudang *</span><input id="wName" placeholder="Contoh: Gudang Utama"></label><label class="field"><span>Alamat</span><input id="wAddress" placeholder="Opsional"></label><label class="field"><span>Status Default</span><select id="wDefault"><option value="0">Bukan default</option><option value="1">Jadikan default</option></select></label><label class="field"><span>Status</span><select id="wActive"><option value="1">Aktif</option><option value="0">Nonaktif</option></select></label></div><div class="action-bar"><button onclick="saveWarehouse()" id="wSaveBtn">Simpan Gudang</button><button class="secondary" onclick="resetWarehouseForm()">Batal / Baru</button></div><p id="wMsg"></p><div class="table-scroll"><table><thead><tr><th>Kode</th><th>Nama</th><th>Alamat</th><th>Default</th><th>Status</th><th>Aksi</th></tr></thead><tbody id="warehouseBody"></tbody></table></div></div>
<div class="card inventory-section inventory-transfer"><h2>Transfer Antar Gudang</h2><p class="muted">Memindahkan barang dari gudang asal ke gudang tujuan tanpa mengubah total stok perusahaan.</p><div class="form-section"><div class="field-grid three"><label class="field"><span>Barang <b class="required">*</b></span><select id="tProduct"></select></label><label class="field"><span>Gudang Asal <b class="required">*</b></span><select id="tSource"></select></label><label class="field"><span>Gudang Tujuan <b class="required">*</b></span><select id="tTarget"></select></label><label class="field"><span>Jumlah Transfer <b class="required">*</b></span><input id="tQty" type="number" step="0.0001" placeholder="0"></label><label class="field"><span>Nomor Referensi</span><input id="tRef" placeholder="Opsional"></label><label class="field"><span>Alasan / Keterangan <b class="required">*</b></span><input id="tReason" placeholder="Contoh: Pengisian stok toko"></label></div><div class="action-bar"><button onclick="transferStock()">Proses Transfer</button></div></div><p id="tMsg"></p></div>
<div class="card inventory-section inventory-stock"><div class="row"><h2>Saldo Persediaan per Gudang</h2><button class="secondary" onclick="runRefresh(this,loadBalances,'balancesRefreshAt')">↻ Refresh</button><span id="balancesRefreshAt" class="muted"></span></div><div class="row"><select id="balanceWarehouse" onchange="loadBalances()"></select><input id="balanceSearch" placeholder="Cari barang" oninput="loadBalances()"></div><table><thead><tr><th>Gudang</th><th>SKU</th><th>Barang</th><th>Qty</th><th class="cost-sensitive">Rata-rata</th><th class="cost-sensitive">Nilai</th></tr></thead><tbody id="balanceBody"></tbody></table></div>
<div class="card inventory-section inventory-stock"><div class="row"><h2>Kartu Stok</h2><label class="field" style="min-width:280px"><span>Pilih Barang</span><select id="cardProduct" onchange="loadInventoryCard()"><option value="">Semua barang</option></select></label><button class="secondary" onclick="runRefresh(this,loadInventoryCard,'cardRefreshAt')">↻ Refresh</button><span id="cardRefreshAt" class="muted"></span></div><table><thead><tr><th>Waktu</th><th>Gudang</th><th>Barang</th><th>Jenis</th><th>Perubahan</th><th>Saldo</th><th class="cost-sensitive">Avg Cost</th><th>Dokumen</th></tr></thead><tbody id="cardBody"></tbody></table></div>
</div>

<div id="stock" class="page"><div class="card"><h2>Penyesuaian Stok</h2><p class="hint">Isi nilai positif untuk menambah stok dan nilai negatif untuk mengurangi stok.</p><div class="form-section"><div class="field-grid three"><label class="field"><span>Gudang <b class="required">*</b></span><select id="aWarehouse" onchange="refreshAdjustmentProductStock()"></select></label><label class="field"><span>Barang <b class="required">*</b></span><select id="aProduct"></select></label><label class="field"><span>Perubahan Stok <b class="required">*</b></span><input id="aQty" type="number" step="0.0001" placeholder="Contoh: 5 atau -2"></label><label class="field" id="aAdjustmentAccountField"><span>Akun Penyesuaian *</span><select id="aAdjustmentAccount"></select><small>Lawan jurnal akun persediaan barang. Saat edit, akun lama dipertahankan otomatis.</small></label><label class="field"><span>Nomor Referensi</span><input id="aRef" placeholder="Contoh: SO-001"></label><label class="field"><span>Alasan Penyesuaian <b class="required">*</b></span><input id="aReason" placeholder="Contoh: Hasil stok opname"></label><label class="field"><span>Departemen</span><select id="adjustDepartment"></select><small>Opsional. Cost center penyesuaian.</small></label><label class="field"><span>Proyek</span><select id="adjustProject"></select><small>Opsional. Proyek terkait penyesuaian.</small></label></div><div class="action-bar"><button onclick="adjust()">Simpan Penyesuaian</button></div></div><p id="aMsg"></p></div><div class="card"><div class="table-toolbar"><h2>Riwayat Penyesuaian Stok</h2><button class="secondary" onclick="runRefresh(this,loadMoves,'movesRefreshAt')">↻ Refresh</button><span id="movesRefreshAt" class="muted"></span></div><table><thead><tr><th>Waktu</th><th>Barang</th><th>Perubahan</th><th>Saldo</th><th>Referensi</th><th>Alasan</th></tr></thead><tbody id="moveBody"></tbody></table></div></div>

<div id="receivables" class="page"><div class="card"><div class="transaction-title"><div><h2>Penerimaan Piutang Pelanggan</h2><p class="muted">Catat pembayaran pelanggan untuk invoice kredit yang belum lunas.</p></div><button class="secondary" onclick="loadReceivables()">↻ Refresh</button></div><div class="form-section"><div class="field-grid"><label class="field"><span>Pelanggan</span><select id="rpCustomer" onchange="loadReceivables()"></select></label>
<label class="field"><span>Invoice Outstanding <b class="required">*</b></span><select id="rpInvoice" onchange="fillReceivableAmount()"></select></label><label class="field"><span>Diterima ke Akun <b class="required">*</b></span><select id="rpCash"></select></label><label class="field"><span>Tanggal Penerimaan <b class="required">*</b></span><input id="rpDate" type="date"></label><label class="field"><span>Jumlah Diterima <b class="required">*</b></span><input id="rpAmount" type="number" placeholder="0"></label><label class="field wide-note"><span>Catatan</span><input id="rpNotes" placeholder="Opsional"></label></div><div class="action-bar"><button onclick="receiveAR()">Simpan Penerimaan</button></div></div><p id="rpMsg"></p><div class="table-toolbar"><h3>Daftar Piutang Terbuka</h3><input id="rpSearch" placeholder="Cari invoice / pelanggan..." oninput="loadReceivables()"></div><table><thead><tr><th>Invoice</th><th>Pelanggan</th><th>Jatuh Tempo</th><th>Saldo</th><th>Hari Lewat</th></tr></thead><tbody id="receivableBody"></tbody></table></div></div>
<div id="payables" class="page"><div class="card"><div class="transaction-title"><div><h2>Pembayaran Hutang Pemasok</h2><p class="muted">Catat pembayaran kepada pemasok untuk pembelian kredit yang belum lunas.</p></div><button class="secondary" onclick="loadPayables()">↻ Refresh</button></div><div class="form-section"><div class="field-grid"><label class="field"><span>Pemasok</span><select id="phSupplier" onchange="loadPayables()"></select></label>
<label class="field"><span>Invoice Pembelian Outstanding <b class="required">*</b></span><select id="phPurchase" onchange="fillPayableAmount()"></select></label><label class="field"><span>Dibayar dari Akun <b class="required">*</b></span><select id="phCash"></select></label><label class="field"><span>Tanggal Pembayaran <b class="required">*</b></span><input id="phDate" type="date"></label><label class="field"><span>Jumlah Dibayar <b class="required">*</b></span><input id="phAmount" type="number" placeholder="0"></label><label class="field wide-note"><span>Catatan</span><input id="phNotes" placeholder="Opsional"></label></div><div class="action-bar"><button onclick="payAP()">Simpan Pembayaran</button></div></div><p id="phMsg"></p><div class="table-toolbar"><h3>Daftar Hutang Terbuka</h3><input id="phSearch" placeholder="Cari pembelian / pemasok..." oninput="loadPayables()"></div><table><thead><tr><th>Pembelian</th><th>Pemasok</th><th>Jatuh Tempo</th><th>Saldo</th><th>Hari Lewat</th></tr></thead><tbody id="payableBody"></tbody></table></div></div>


<div id="flexInvoiceDesigner" class="page"><div class="card">
<div class="transaction-title"><div><h2>Desain Invoice Fleksibel</h2><p class="muted">Buat beberapa format invoice: standar, termin proyek, termin + material, atau custom. Susun blok sesuai kebutuhan customer.</p></div><button class="secondary" onclick="newFlexInvoiceTemplate()">+ Template Baru</button></div>
<div class="flex-invoice-layout"><div>
<div class="field-grid two">
<label class="field"><span>Template</span><select id="flexTplSelect" onchange="selectFlexTemplate()"></select></label>
<label class="field"><span>Jenis</span><select id="flexTplKind" onchange="flexKindChanged()"><option value="STANDARD">Invoice Standar</option><option value="TERM">Invoice Termin</option><option value="TERM_MATERIAL">Termin + Material</option><option value="CUSTOM">Custom</option></select></label>
<label class="field"><span>Kode</span><input id="flexTplCode"></label><label class="field"><span>Nama Template</span><input id="flexTplName"></label>
<label class="field"><span>Judul Cetak</span><input id="flexTplTitle" value="INVOICE"></label><label class="field"><span>Kertas</span><select id="flexTplPaper"><option>A4</option><option>A5</option><option>LETTER</option></select></label>
</div>
<div class="designer-checks"><label><input id="flexTplDefault" type="checkbox"> Default</label><label><input id="flexTplActive" type="checkbox" checked> Aktif</label><label><input id="flexTplLogo" type="checkbox" checked> Logo</label><label><input id="flexTplSku" type="checkbox" checked> SKU</label><label><input id="flexTplUnit" type="checkbox" checked> Satuan</label><label><input id="flexTplPrices" type="checkbox" checked> Harga item</label><label><input id="flexTplMaterialValues" type="checkbox" checked> Nilai material</label></div>
<h3>Susunan Blok</h3><div id="flexTplBlocks" class="flex-block-list"></div>
<label class="field"><span>Teks Custom</span><textarea id="flexTplCustom" rows="4" placeholder="{{invoice_no}}, {{customer_name}}, {{project_name}}, {{contract_no}}, {{contract_value}}, {{term_no}}, {{term_percent}}, {{term_value}}, {{retention_value}}, {{total_invoice}}, {{due_date}}, {{progress_percent}}"></textarea></label>
<div class="field-grid two"><label class="field"><span>Tanda Tangan Kiri</span><input id="flexTplLeft"></label><label class="field"><span>Tanda Tangan Kanan</span><input id="flexTplRight"></label></div>
<div class="action-bar"><button onclick="saveFlexInvoiceTemplate()">Simpan</button><button class="secondary" onclick="previewFlexTemplate()">Preview</button><button class="danger" onclick="deleteFlexInvoiceTemplate()">Hapus</button></div><p id="flexTplMsg"></p>
</div><div><h3>Preview</h3><div id="flexTplPreview" class="flex-preview"></div></div></div></div></div>
<div id="projectDocuments" class="page">
 <div class="card">
  <div class="transaction-title"><div><h2>Dokumen Proyek</h2><p class="muted">Arsipkan kontrak, gambar kerja, BAST, invoice, foto progress, dan berkas proyek lainnya. File disimpan di folder terpisah dari database.</p></div><button class="secondary" onclick="loadProjectDocuments()">↻ Refresh</button></div>
  <div class="form-section">
   <input id="projectDocId" type="hidden">
   <div class="field-grid three">
    <label class="field"><span>Proyek <b class="required">*</b></span><select id="projectDocProject"></select></label>
    <label class="field"><span>Kategori</span><select id="projectDocCategory"></select></label>
    <label class="field"><span>Judul Dokumen <b class="required">*</b></span><input id="projectDocTitle" placeholder="Contoh: Kontrak Utama"></label>
    <label class="field"><span>Nomor Dokumen</span><input id="projectDocNo" placeholder="SPK-001/2026"></label>
    <label class="field"><span>Tanggal Dokumen</span><input id="projectDocDate" type="date"></label>
    <label class="field"><span>Berlaku / Expired</span><input id="projectDocValid" type="date"></label>
    <label class="field"><span>File</span><input id="projectDocFile" type="file"><small>PDF, Office, gambar, ZIP, DWG/DXF. Maksimal 20 MB. Kosongkan saat hanya edit metadata.</small></label>
    <label class="field wide-note"><span>Keterangan</span><input id="projectDocDescription" placeholder="Opsional"></label>
   </div>
   <div class="action-bar"><button onclick="saveProjectDocument()">Simpan Dokumen</button><button class="secondary" onclick="resetProjectDocumentForm()">Form Baru</button></div>
  </div>
  <p id="projectDocMsg"></p>
 </div>
 <div class="card">
  <div class="table-toolbar"><h2>Daftar Dokumen</h2>
   <select id="projectDocFilterProject" onchange="loadProjectDocuments()"></select>
   <select id="projectDocFilterCategory" onchange="loadProjectDocuments()"><option value="">Semua Kategori</option></select>
   <input id="projectDocSearch" placeholder="Cari judul / nomor / file..." oninput="projectDocSearchDebounced()">
   <label><input id="projectDocHistory" type="checkbox" onchange="loadProjectDocuments()"> Tampilkan riwayat versi</label>
  </div>
  <div class="table-scroll"><table><thead><tr><th>Proyek</th><th>Kategori</th><th>Dokumen</th><th>Tanggal</th><th>File</th><th>Versi</th><th>Upload</th><th>Aksi</th></tr></thead><tbody id="projectDocBody"></tbody></table></div>
 </div>
</div>

<div id="accounting" class="page"><div class="card accounting-section accounting-coa"><div class="transaction-title"><div><h2>Data COA</h2><p class="muted">Daftar akun untuk pencatatan jurnal dan laporan keuangan.</p></div><button class="secondary" onclick="loadAccounting()">↻ Refresh</button></div>
<div id="coaWizardPanel" class="form-section"><h3>Wizard COA Standar Usaha</h3><p class="section-help">Pilih jenis usaha untuk membuat akun standar secara otomatis. Akun dengan kode yang sudah ada tidak akan ditimpa.</p><div class="field-grid three"><label class="field"><span>Jenis Usaha</span><select id="coaTemplateSelect"><option value="">-- Pilih Standar Usaha --</option><option value="dagang">Usaha Dagang</option><option value="jasa">Perusahaan Jasa</option><option value="bengkel">Bengkel</option><option value="sekolah">Sekolah / Lembaga Pendidikan</option><option value="pabrik">Pabrik / Manufaktur</option><option value="perkebunan">Perkebunan</option><option value="warung">Warung / Toko Kecil</option><option value="apotik">Apotek</option><option value="distributor">Distributor</option><option value="kontraktor">Kontraktor</option></select></label><div class="section-help"><b>Tipe/Subtipe COA:</b> CASH_BANK=Kas/Bank, RECEIVABLE=Piutang, ASSET=Aset, PAYABLE=Hutang, LIABILITY=Kewajiban, EQUITY=Ekuitas, REVENUE=Pendapatan, HPP=Harga Pokok Penjualan, OPERATING_EXPENSE=Beban Operasional.</div><label class="field"><span>Akun Baru</span><input id="coaTemplateNewCount" value="0" readonly></label><label class="field"><span>Akun Sudah Ada</span><input id="coaTemplateExistingCount" value="0" readonly></label></div><div class="action-bar"><button class="secondary" onclick="previewCoaTemplate()">Preview COA</button><button onclick="applyCoaTemplate()">Buat COA Otomatis</button></div><p id="coaTemplateMsg"></p><div class="table-scroll"><table><thead><tr><th>Kode</th><th>Nama Akun</th><th>Tipe</th><th>Status</th></tr></thead><tbody id="coaTemplateBody"><tr><td colspan="4">Pilih jenis usaha lalu klik Preview COA.</td></tr></tbody></table></div></div><div class="form-section"><input id="coaEditId" type="hidden"><div class="field-grid three"><label class="field"><span>Kode Akun <b class="required">*</b></span><input id="coaCode" placeholder="Contoh: 1101"></label><label class="field"><span>Nama Akun <b class="required">*</b></span><input id="coaName" placeholder="Contoh: Kas Kecil"></label><label class="field"><span>Tipe Akun <b class="required">*</b></span><select id="coaType"><option value="CASH_BANK">Kas Bank</option><option value="RECEIVABLE">Piutang</option><option value="PAYABLE">Hutang</option><option value="ASSET">Aset Lain</option><option value="LIABILITY">Kewajiban Lain</option><option value="EQUITY">Ekuitas / Modal</option><option value="REVENUE">Pendapatan</option><option value="HPP">Harga Pokok Penjualan</option><option value="OPERATING_EXPENSE">Biaya Operasional</option></select></label></div><div class="action-bar"><button onclick="addCoa()">Simpan Akun</button><button class="secondary" onclick="resetCoaForm()">Form Baru</button></div></div><p id="coaMsg"></p><table><thead><tr><th>Kode</th><th>Nama Akun</th><th>Tipe</th><th>Saldo Normal</th><th>Status</th><th>Aksi</th></tr></thead><tbody id="coaBody"></tbody></table></div>
<div class="card accounting-section accounting-manual"><h2>Jurnal Manual</h2><p class="muted">Total debit dan kredit wajib sama sebelum jurnal dapat disimpan.</p><div class="form-section"><div class="field-grid three"><label class="field"><span>Tanggal Jurnal <b class="required">*</b></span><input id="jDate" type="date"></label><label class="field"><span>Keterangan Jurnal <b class="required">*</b></span><input id="jDesc" placeholder="Contoh: Koreksi biaya listrik"></label><label class="field"><span>No. Referensi / No. Jurnal</span><input id="jRef" placeholder="Otomatis, tetap bisa diedit"><small>Nomor otomatis ditampilkan. Ubah jika memerlukan referensi khusus.</small></label></div><div class="action-bar"><button class="secondary" onclick="addJLine()">+ Tambah Baris</button><button onclick="saveJournal()">Simpan Jurnal</button><button class="secondary" onclick="downloadJournalTemplate()">Download Template Excel</button><label class="button-like">Impor Excel<input id="journalExcelFile" type="file" accept=".xlsx" hidden onchange="importJournalExcel()"></label></div></div><table><thead><tr><th>Akun</th><th>Kode Pelanggan/Pemasok</th><th>Departemen</th><th>Proyek</th><th>Debit</th><th>Kredit</th><th>Memo</th><th></th></tr></thead><tbody id="jLines"></tbody></table><p class="muted">Departemen dan Proyek dapat dipilih berbeda pada setiap baris. Departemen dan Proyek disimpan pada setiap baris jurnal.</p><p id="jMsg"></p></div>
<div class="card accounting-section accounting-journal-list"><h2>Daftar Jurnal <button onclick="loadAccounting()">↻ Refresh</button></h2><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>Keterangan</th><th>Sumber</th><th>Debit</th><th>Kredit</th></tr></thead><tbody id="journalBody"></tbody></table></div>
<div class="card accounting-section accounting-ledger"><div class="transaction-title"><div><h2>Buku Besar</h2><p class="muted">Lihat saldo awal, mutasi debit/kredit, dan saldo berjalan per akun.</p></div><button class="secondary" onclick="loadLedger()">↻ Refresh</button></div><div class="form-section"><div class="field-grid three"><label class="field"><span>Akun <b class="required">*</b></span><select id="ledgerAccount"></select></label><label class="field"><span>Pelanggan / Pemasok</span><select id="ledgerPartner"><option value="">Semua Partner</option></select><small id="ledgerPartnerHelp">Hanya aktif untuk akun Piutang atau Hutang.</small></label><label class="field"><span>Tanggal Mulai</span><input id="ledgerFrom" type="date"></label><label class="field"><span>Tanggal Akhir</span><input id="ledgerTo" type="date"></label></div></div><div id="ledgerSummary" class="summary-box"></div><table><thead><tr><th>Tanggal</th><th>No. Jurnal</th><th>Keterangan</th><th>Partner</th><th>Referensi</th><th>Debit</th><th>Kredit</th><th>Saldo Berjalan</th></tr></thead><tbody id="ledgerBody"></tbody></table><p id="ledgerUpdated" class="muted"></p></div>
<div class="card accounting-section accounting-trial"><div class="transaction-title"><div><h2>Neraca Saldo</h2><p class="muted">Rekap saldo awal, mutasi periode, dan saldo akhir seluruh akun.</p></div><button class="secondary" onclick="loadTrial()">↻ Refresh</button></div><div class="form-section"><div class="field-grid two"><label class="field"><span>Tanggal Mulai</span><input id="trialFrom" type="date"></label><label class="field"><span>Tanggal Akhir</span><input id="trialTo" type="date"></label></div></div><table><thead><tr><th>Kode</th><th>Akun</th><th>Saldo Awal D</th><th>Saldo Awal K</th><th>Mutasi D</th><th>Mutasi K</th><th>Saldo Akhir D</th><th>Saldo Akhir K</th></tr></thead><tbody id="trialBody"></tbody><tfoot><tr><th colspan="2">TOTAL</th><th id="trialOD"></th><th id="trialOC"></th><th id="trialPD"></th><th id="trialPC"></th><th id="trialED"></th><th id="trialEC"></th></tr></tfoot></table><p id="trialTotal"></p><p id="trialUpdated" class="muted"></p></div></div>
<div id="departments" class="page"><div class="card">
<div class="transaction-title"><div><h2>Master Departemen</h2><p class="muted">Kelola departemen dan cost center.</p></div><div><button class="secondary" onclick="openMasterImportType('departments')">Impor Excel</button> <button class="secondary" onclick="loadDepartments()">↻ Refresh</button></div></div><p id="departmentMsg"></p></div>
<div class="card"><h3 id="departmentFormTitle">Tambah Departemen</h3><input id="departmentId" type="hidden">
<div class="field-grid four"><label class="field"><span>Kode *</span><input id="departmentCode"></label><label class="field"><span>Nama *</span><input id="departmentName"></label><label class="field"><span>Manager</span><input id="departmentManager"></label><label class="field"><span>Status</span><select id="departmentActive"><option value="1">Aktif</option><option value="0">Nonaktif</option></select></label></div>
<label class="field"><span>Keterangan</span><textarea id="departmentNotes" rows="2"></textarea></label><div class="action-bar"><button onclick="saveDepartment()">Simpan</button><button class="secondary" onclick="resetDepartmentForm()">Form Baru</button></div></div>
<div class="card"><div class="table-toolbar"><h2>Daftar Departemen</h2><span id="departmentCount"></span></div><div class="table-scroll"><table><thead><tr><th>Kode</th><th>Nama</th><th>Manager</th><th>Status</th><th>Keterangan</th><th>Aksi</th></tr></thead><tbody id="departmentBody"></tbody></table></div></div></div>

<div id="projects" class="page"><div class="card">
<div class="transaction-title"><div><h2>Master Proyek</h2><p class="muted">Kelola proyek dan pelanggan terkait.</p></div><button class="secondary" onclick="loadProjects()">↻ Refresh</button></div><p id="projectMsg"></p></div>
<div class="card"><h3 id="projectFormTitle">Tambah Proyek</h3><input id="projectId" type="hidden">
<div class="field-grid four"><label class="field"><span>Kode *</span><input id="projectCode"></label><label class="field"><span>Nama Proyek *</span><input id="projectName"></label><label class="field"><span>Pelanggan</span><select id="projectCustomer"></select></label><label class="field"><span>No. Kontrak / SPK</span><input id="projectContractNo"></label><label class="field"><span>Nilai Kontrak</span><input id="projectContractValue" type="number" min="0"></label><label class="field"><span>Lokasi</span><input id="projectLocation"></label><label class="field"><span>PIC / Penanggung Jawab</span><input id="projectPic"></label><label class="field"><span>Jenis Proyek</span><input id="projectType" placeholder="Bangunan / Interior / MEP"></label><label class="field"><span>Retensi Default (%)</span><input id="projectRetention" type="number" min="0" max="100" step="0.01"></label><label class="field"><span>Status Proyek</span><select id="projectStatus"><option value="PLANNED">Direncanakan</option><option value="ACTIVE">Aktif</option><option value="ON_HOLD">Ditunda</option><option value="COMPLETED">Selesai</option><option value="CANCELLED">Dibatalkan</option></select></label><label class="field"><span>Tanggal Mulai</span><input id="projectStart" type="date"></label><label class="field"><span>Tanggal Selesai</span><input id="projectEnd" type="date"></label><label class="field"><span>Status Master</span><select id="projectActive"><option value="1">Aktif</option><option value="0">Nonaktif</option></select></label></div>
<label class="field"><span>Keterangan</span><textarea id="projectNotes" rows="2"></textarea></label><div class="action-bar"><button onclick="saveProject()">Simpan</button><button class="secondary" onclick="resetProjectForm()">Form Baru</button></div></div>
<div class="card"><div class="table-toolbar"><h2>Daftar Proyek</h2><span id="projectCount"></span></div><div class="table-scroll"><table><thead><tr><th>Kode</th><th>Nama</th><th>Pelanggan</th><th>Kontrak</th><th>Progress</th><th>Budget</th><th>Realisasi</th><th>Estimasi Laba</th><th>Termin</th><th>Aksi</th></tr></thead><tbody id="projectBody"></tbody></table></div></div>
<div class="card"><h2>Kartu Proyek Kontraktor</h2><div class="field-grid four"><label class="field"><span>Proyek</span><select id="contractorProject" onchange="loadContractorProject()"></select></label><label class="field"><span>Nilai Kontrak</span><input id="contractorValue" readonly></label><label class="field"><span>Progress Fisik</span><input id="contractorProgress" readonly></label><label class="field"><span>Estimasi Laba</span><input id="contractorProfit" readonly></label></div><div id="contractorSummary" class="project-budget-summary"></div></div>
<div class="card"><h2>Progress Proyek</h2><input id="progressId" type="hidden"><div class="field-grid four"><label class="field"><span>Tanggal</span><input id="progressDate" type="date"></label><label class="field"><span>Progress (%)</span><input id="progressPercent" type="number" min="0" max="100" step="0.01"></label><label class="field"><span>Catatan</span><input id="progressNotes"></label></div><div class="action-bar"><button onclick="saveProjectProgress()">Simpan Progress</button><button class="secondary" onclick="resetProjectProgress()">Baru</button></div><div class="table-scroll"><table><thead><tr><th>Tanggal</th><th>Progress</th><th>Catatan</th><th>Aksi</th></tr></thead><tbody id="progressBody"></tbody></table></div></div>
<div class="card"><h2>Termin & Retensi Proyek</h2><input id="termId" type="hidden"><div class="field-grid four"><label class="field"><span>No. Termin</span><input id="termNo"></label><label class="field"><span>Keterangan</span><input id="termDescription"></label><label class="field"><span>Persentase (%)</span><input id="termPercent" type="number" min="0" step="0.01"></label><label class="field"><span>Nilai Termin</span><input id="termAmount" type="number" min="0"></label><label class="field"><span>Tanggal Tagih</span><input id="termInvoiceDate" type="date"></label><label class="field"><span>Jatuh Tempo</span><input id="termDueDate" type="date"></label><label class="field"><span>Invoice Penjualan</span><select id="termSale"><option value="">Belum dihubungkan</option></select></label><label class="field"><span>Status</span><select id="termStatus"><option value="DRAFT">Draft</option><option value="BILLED">Ditagih</option><option value="PARTIAL">Sebagian</option><option value="PAID">Lunas</option><option value="CANCELLED">Dibatalkan</option></select></label><label class="field"><span>Retensi (%)</span><input id="termRetentionPercent" type="number" min="0" max="100" step="0.01"></label><label class="field"><span>Rencana Cair Retensi</span><input id="termRetentionDue" type="date"></label><label class="field"><span>Status Retensi</span><select id="termRetentionStatus"><option value="PENDING">Belum Cair</option><option value="RELEASED">Sudah Cair</option><option value="CANCELLED">Dibatalkan</option></select></label><label class="field"><span>Catatan</span><input id="termNotes"></label></div><div class="action-bar"><button onclick="saveProjectTerm()">Simpan Termin</button><button class="secondary" onclick="resetProjectTerm()">Baru</button></div><div class="table-scroll"><table><thead><tr><th>Termin</th><th>Nilai</th><th>Jatuh Tempo</th><th>Invoice</th><th>Status</th><th>Retensi</th><th>Aksi</th></tr></thead><tbody id="termBody"></tbody></table></div></div></div>

<div id="projectReports" class="page"><div class="card"><h2>Laporan Proyek</h2><p id="projectReportMsg"></p></div><div class="card"><div class="field-grid four"><label class="field"><span>Jenis</span><select id="projectReportType" onchange="toggleProjectReportFilters()"><option value="project_income">Laba Rugi per Proyek</option><option value="project_summary">Rekap Semua Proyek</option><option value="project_purchases">Pembelian per Proyek</option><option value="project_materials">Pengeluaran Material per Proyek</option><option value="project_cost_detail">Rincian Biaya per Proyek</option></select></label><label class="field" id="projectReportProjectWrap"><span>Proyek</span><select id="projectReportProject" multiple size="5"></select><small>Untuk Laba Rugi, pilih satu atau beberapa proyek (Ctrl/Shift + klik).</small></label><label class="field" id="projectReportStatusWrap"><span>Status</span><select id="projectReportStatus"><option value="">Semua</option><option value="ACTIVE">Aktif</option><option value="COMPLETED">Selesai</option><option value="ON_HOLD">Ditunda</option></select></label><label class="field" id="projectReportSupplierWrap"><span>Pemasok</span><select id="projectReportSupplier"></select></label><label class="field" id="projectReportProductWrap"><span>Barang</span><select id="projectReportProduct"></select></label><label class="field" id="projectReportDepartmentWrap"><span>Departemen</span><select id="projectReportDepartment"></select></label><label class="field" id="projectReportAccountWrap"><span>Akun Biaya</span><select id="projectReportAccount"></select></label><label class="field" id="projectReportWarehouseWrap"><span>Gudang</span><select id="projectReportWarehouse"></select></label><label class="field"><span>Dari</span><input id="projectReportFrom" type="date"></label><label class="field"><span>Sampai</span><input id="projectReportTo" type="date"></label></div><div class="action-bar"><button onclick="loadProjectReport()">Tampilkan</button><button class="secondary" onclick="exportProjectReport('xlsx')">Excel</button><button class="secondary" onclick="exportProjectReport('pdf')">PDF</button></div></div><div class="card"><div id="projectReportHeader"></div><div id="projectReportSummary" class="project-budget-summary"></div><div id="projectReportSpecial"></div><div class="table-scroll"><table><thead id="projectReportHead"></thead><tbody id="projectReportBody"></tbody></table></div></div></div>

<div id="projectMaterialIssues" class="page">
<div class="card">
  <div class="transaction-title"><div>
    <h2>Pengeluaran Material Proyek</h2>
    <p class="muted">Material keluar dari gudang menggunakan average cost dan langsung masuk realisasi budget proyek.</p>
  </div><button class="secondary" onclick="loadProjectMaterialIssues()">↻ Refresh</button></div>
  <p id="projectMaterialMsg"></p>
</div>
<div class="card">
  <div class="field-grid four">
    <label class="field"><span>Tanggal *</span><input id="projectMaterialDate" type="date"></label>
    <label class="field"><span>Proyek *</span><select id="projectMaterialProject"></select></label>
    <label class="field"><span>Departemen</span><select id="projectMaterialDepartment"></select></label>
    <label class="field"><span>Gudang *</span><select id="projectMaterialWarehouse" onchange="refreshProjectMaterialCosts()"></select></label>
    <label class="field"><span>Akun Pengeluaran *</span><select id="projectMaterialAccount"></select><small>Hanya HPP, Beban, atau Aset.</small></label>
  </div>
  <label class="field"><span>Keterangan</span><textarea id="projectMaterialNotes" rows="2"></textarea></label>
  <div class="table-toolbar"><h3>Detail Material</h3><button onclick="addProjectMaterialLine()">+ Tambah Barang</button></div>
  <div class="table-scroll"><table><thead><tr><th>Barang</th><th>Qty</th><th>Average Cost</th><th>Total Cost</th><th></th></tr></thead><tbody id="projectMaterialLines"></tbody><tfoot><tr><th colspan="3">TOTAL</th><th id="projectMaterialGrandTotal">Rp0</th><th></th></tr></tfoot></table></div>
  <div class="action-bar"><button onclick="saveProjectMaterialIssue()">Posting Pengeluaran Material</button><button class="secondary" onclick="resetProjectMaterialIssue()">Form Baru</button></div>
</div>
<div class="card">
  <div class="table-toolbar"><h2>Riwayat Pengeluaran Material</h2><span id="projectMaterialCount"></span></div>
  <div class="table-scroll"><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>Proyek</th><th>Departemen</th><th>Gudang</th><th>Akun</th><th>Total Cost</th><th>Keterangan</th><th>Aksi</th></tr></thead><tbody id="projectMaterialBody"></tbody></table></div>
</div>
</div>

<div id="projectBudgets" class="page">
<div class="card">
  <div class="transaction-title"><div>
    <h2>Budget & Realisasi Proyek</h2>
    <p class="muted">Tetapkan budget material dan biaya proyek. Realisasi material berasal dari Pengeluaran Material Proyek; realisasi biaya berasal dari jurnal HPP/Beban bertag proyek.</p>
  </div><button class="secondary" onclick="loadProjectBudgets()">↻ Refresh</button></div>
  <p id="projectBudgetMsg"></p>
</div>

<div id="projectBudgetSummary" class="project-budget-summary"></div>

<div class="project-budget-layout">
  <div class="card">
    <h3 id="projectBudgetFormTitle">Tambah Budget Proyek</h3>
    <input id="projectBudgetId" type="hidden">
    <div class="field-grid two">
      <label class="field"><span>Proyek *</span><select id="projectBudgetProject" onchange="syncProjectBudgetTotal()"></select></label>
      <label class="field"><span>Total Budget</span><input id="projectBudgetTotal" value="0" readonly></label>
      <label class="field"><span>Budget Material</span><input id="projectBudgetMaterial" type="number" min="0" value="0" oninput="syncProjectBudgetTotal()"></label>
      <label class="field"><span>Budget Biaya Proyek</span><input id="projectBudgetExpense" type="number" min="0" value="0" oninput="syncProjectBudgetTotal()"></label>
    </div>
    <label class="field"><span>Catatan</span><textarea id="projectBudgetNotes" rows="3" placeholder="Catatan atau asumsi penyusunan budget"></textarea></label>
    <div class="action-bar">
      <button onclick="saveProjectBudget()">Simpan Budget</button>
      <button class="secondary" onclick="resetProjectBudgetForm()">Form Baru</button>
    </div>
  </div>

  <div class="card project-budget-control">
    <h3>Kontrol Budget Terpilih</h3>
    <div id="projectBudgetControl" class="project-budget-control-body">
      <p class="muted">Pilih budget pada tabel untuk melihat ringkasan.</p>
    </div>
  </div>
</div>

<div class="card">
  <div class="table-toolbar"><h2>Daftar Budget Proyek</h2><span id="projectBudgetCount" class="muted"></span></div>
  <div class="table-scroll"><table>
    <thead><tr><th>Proyek</th><th>Pelanggan</th><th>Budget Material</th><th>Realisasi Material</th><th>Budget Biaya</th><th>Realisasi Biaya</th><th>Total Budget</th><th>Total Realisasi</th><th>Sisa</th><th>Terpakai</th><th>Aksi</th></tr></thead>
    <tbody id="projectBudgetBody"></tbody>
  </table></div>
</div>
<div class="card">
  <div class="table-toolbar"><h2>Rincian Realisasi Biaya Proyek</h2><span id="projectCostDetailTitle" class="muted">Pilih proyek melalui tombol rincian.</span></div>
  <div class="table-scroll"><table><thead><tr><th>Tanggal</th><th>No. Jurnal</th><th>Sumber</th><th>Referensi</th><th>Akun</th><th>Departemen</th><th>Keterangan</th><th>Debit</th><th>Kredit</th><th>Net Biaya</th></tr></thead><tbody id="projectCostDetailBody"><tr><td colspan="10">Belum ada proyek dipilih.</td></tr></tbody><tfoot id="projectCostDetailFoot"></tfoot></table></div>
</div>
</div>

<div id="users" class="page">
<div class="card">
<div class="transaction-title"><div><h2>User & Hak Akses</h2>
<p class="muted">Kelola pengguna, role, password, status, dan hak akses.</p></div>
<button class="secondary" onclick="loadUserAccess()">↻ Refresh</button></div>
<div class="access-tabs">
<button id="userTabButton" class="active" onclick="showAccessTab('users')">Daftar User</button>
<button id="roleTabButton" onclick="showAccessTab('roles');if(editingAccessRoleCode)renderAccessRoleEditor(editingAccessRoleCode)">Role & Hak Akses</button>
</div><p id="uMsg"></p></div>

<section id="userAccessUsers" class="access-tab-panel">
<div class="card"><h3>Tambah User Baru</h3>
<div class="field-grid four">
<label class="field"><span>Username *</span><input id="nUser" autocomplete="off"></label>
<label class="field"><span>Nama Lengkap *</span><input id="nName"></label>
<label class="field"><span>Password Awal *</span><input id="nPass" type="password" placeholder="Minimal 8 karakter"></label>
<label class="field"><span>Role *</span><select id="nRole"><option value="">Memuat role...</option></select></label>
</div><div class="action-bar"><button onclick="addUser()">Tambah User</button></div></div>
<div class="card"><div class="table-toolbar"><h2>Daftar User</h2><span id="userCount" class="muted"></span></div>
<div class="table-scroll"><table><thead><tr><th>Username</th><th>Nama Lengkap</th><th>Role</th><th>Status</th><th>Dibuat</th><th>Aksi</th></tr></thead><tbody id="userBody"></tbody></table></div></div>
<div class="card"><div class="table-toolbar"><div><h2>Device Aktif</h2><p class="muted">Maksimal sesuai lisensi. Logout normal langsung melepas slot; sesi tanpa heartbeat dilepas otomatis dalam 10 detik.</p></div><button class="secondary" onclick="loadActiveSessions()">↻ Refresh</button></div>
<div class="table-scroll"><table><thead><tr><th>User</th><th>Perangkat</th><th>IP</th><th>Terakhir Aktif</th><th>Aksi</th></tr></thead><tbody id="activeSessionBody"><tr><td colspan="5">Memuat...</td></tr></tbody></table></div></div>
</section>

<section id="userAccessRoles" class="access-tab-panel hidden">
<div class="access-role-layout">
<div class="card"><div class="table-toolbar"><h2>Daftar Role</h2><button onclick="newRoleEditor()">+ Role Baru</button></div><div id="roleList" class="role-list"></div></div>
<div class="card"><h2 id="roleEditorTitle">Role & Hak Akses</h2>
<div class="field-grid two">
<label class="field"><span>Kode Role *</span><input id="roleCode"></label>
<label class="field"><span>Nama Role *</span><input id="roleName"></label>
</div>
<div class="permission-toolbar">
<button class="secondary" onclick="setAllPermissions(true)">Pilih Semua</button>
<button class="secondary" onclick="setAllPermissions(false)">Kosongkan Semua</button>
</div>
<div id="permissionMatrix" class="permission-matrix"></div>
<div class="action-bar"><button onclick="saveRoleAccess()">Simpan Role</button></div>
</div></div></section>
</div><div id="audit" class="page card"><h2>Audit Terakhir</h2><table><tbody id="auditBody"></tbody></table></div><div id="smartImport" class="page"><div class="card"><h2>Smart Import Rekening Koran PDF</h2><p class="help">Mendukung PDF teks BCA, Mandiri, BRI, BNI, CIMB Niaga, Permata, Danamon, OCBC, BSI, Maybank, Panin, dan format bank lain yang memiliki kolom tanggal/mutasi/saldo. Kredit bank = Bank Masuk; debit bank = Bank Keluar.</p><div class="field-grid three"><label class="field"><span>PDF Rekening Koran *</span><input id="pdfBankFile" type="file" accept=".pdf"><small id="pdfFileStatus">Belum ada file dipilih.</small></label><label class="field"><span>Akun Kas / Bank Tujuan *</span><select id="importCash"></select></label><label class="field"><span>Akun Lawan Default</span><select id="importDefaultCoa"></select></label></div><div class="action-bar"><button id="previewPdfBtn" onclick="previewBankPdf()" disabled>Preview PDF</button><button class="secondary" onclick="applyDefaultImportCoa()">Terapkan Akun Default</button><button id="postImportBtn" onclick="postMappedBank()" disabled>Posting Baris Terpilih</button></div><p id="importMsg"></p><div id="pdfImportSummary" class="summary-box"></div><div class="table-toolbar"><label><input id="importCheckAll" type="checkbox" checked onchange="toggleAllImportRows(this.checked)"> Pilih Semua</label><span id="importMappingStatus"></span></div><div class="table-scroll"><table><thead><tr><th>Pilih</th><th>Tanggal</th><th>Keterangan</th><th>Bank Masuk</th><th>Bank Keluar</th><th>Saldo</th><th>Saran Akun</th><th>Akun Lawan</th><th>Partner</th><th>Aksi</th></tr></thead><tbody id="importRows"></tbody></table></div></div></div><div id="docDesign" class="page"><div class="card">
<div class="transaction-title"><div><h2>Desain Dokumen</h2>
<p class="muted">Atur desain dasar dokumen dan lihat preview sebelum disimpan.</p></div>
<button class="secondary" onclick="loadDocumentDesigner()">↻ Refresh</button></div>
<div id="docDesignerTabs" class="doc-tabs">
<button type="button" data-doc-type="SALES_INVOICE">Invoice Penjualan</button>
<button type="button" data-doc-type="DELIVERY_ORDER">Surat Jalan</button>
<button type="button" data-doc-type="GOODS_RECEIPT">Good Receive</button>
<button type="button" data-doc-type="PURCHASE_INVOICE">Faktur Pembelian</button>
</div>
<p id="docDesignerMessage"></p>
<div class="designer-layout">
  <div id="docDesignerEditor"></div>
  <div class="designer-preview-wrap">
    <div class="preview-toolbar">
      <h3>Preview Dokumen</h3>
      <button type="button" class="secondary" onclick="renderDocumentPreview()">↻ Perbarui Preview</button>
    </div>
    <div id="docDesignerPreview" class="document-preview"></div>
  </div>
</div>
</div></div>
<div id="transactionMaintenance" class="page"><div class="card"><div class="table-toolbar"><div><h2 id="tmTitle">Daftar Transaksi</h2><p class="muted">Edit dilakukan sebagai pembalikan transaksi lama dan posting transaksi pengganti agar audit trail tetap utuh.</p></div><button class="secondary" onclick="loadTransactionMaintenance()">↻ Refresh</button></div><div class="field-grid three"><label class="field"><span>Jenis Daftar</span><select id="tmKind" onchange="loadTransactionMaintenance()"><option value="cash">Kas Masuk/Keluar</option><option value="transfer">Transfer Kas/Bank</option><option value="journal">Jurnal Manual</option><option value="adjustment">Adjustment Stok</option><option value="receivable">Terima Piutang</option><option value="payable">Bayar Hutang</option><option value="warehouse_transfer">Transfer Gudang</option></select></label><label class="field"><span>Cari</span><input id="tmSearch" oninput="renderTransactionMaintenance()" placeholder="Nomor, keterangan, pihak..."></label></div><div style="overflow:auto"><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>Informasi</th><th>Nilai</th><th>Status</th><th>Aksi</th></tr></thead><tbody id="tmBody"></tbody></table></div><p id="tmMsg"></p></div></div>

<div id="masterImport" class="page">
 <div class="card"><div class="transaction-title"><div><h2>Impor Data dari Excel</h2><p class="muted">Migrasikan master data dan saldo awal menggunakan template resmi StokLedger. Data diperiksa per baris; baris gagal dapat diunduh sebagai file error.</p></div><button class="secondary" onclick="showModule('master')">Kembali</button></div></div>
 <div class="card"><div class="field-grid two"><label class="field"><span>Jenis Data</span><select id="masterImportType" onchange="masterImportReset()"></select></label><label class="field"><span>File Excel (.xlsx)</span><input id="masterImportFile" type="file" accept=".xlsx"></label></div><div class="action-bar"><button class="secondary" onclick="downloadMasterTemplate()">Download Template</button><button onclick="runMasterImport()">Impor & Validasi</button></div><p id="masterImportMsg"></p></div>
 <div class="card"><h2>Hasil Impor</h2><div class="row"><div class="stat">Baris dibaca<b id="miTotal">0</b></div><div class="stat">Berhasil<b id="miSuccess">0</b></div><div class="stat">Gagal<b id="miFailed">0</b></div></div><div id="miErrorWrap" class="hidden" style="margin-top:15px"><button class="danger" onclick="downloadMasterImportErrors()">Download Error.xlsx</button></div><div class="hint" style="margin-top:15px">Urutan migrasi yang disarankan: COA → kategori/satuan/merk/gudang → pelanggan/pemasok → barang/jasa/kas-bank → aktiva tetap → departemen/project (Ultima).</div></div>
</div>


<div id="ownerCloudPage" class="page"><div class="card"><div class="row"><div><h2>Owner Mobile Cloud</h2><p class="help">Hubungkan StokLedger ke Railway agar owner dapat memantau dashboard secara read-only.</p></div><button class="secondary" onclick="loadOwnerCloud()">↻ Refresh</button></div><div class="form-section"><h3>Koneksi Cloud</h3><label>Cloud URL</label><input id="ocUrl" placeholder="https://stokledger-owner.up.railway.app"><label><input id="ocEnabled" type="checkbox"> Aktifkan sinkronisasi cloud</label><label>Interval sinkronisasi (menit)</label><input id="ocInterval" type="number" min="1" max="60" value="5"><div class="actions"><button onclick="saveOwnerCloud()">Simpan Pengaturan</button><button class="secondary" onclick="registerOwnerCloud()">Daftarkan Instalasi</button><button class="secondary" onclick="pairOwnerCloud()">Buat Kode Pairing</button><button onclick="syncOwnerCloud()">Sinkronkan Sekarang</button></div></div><div class="form-section"><h3>Status</h3><table><tbody><tr><th>Company ID</th><td id="ocCompany">-</td></tr><tr><th>Installation ID</th><td id="ocInstall">-</td></tr><tr><th>Kode Pairing</th><td><strong id="ocPair">-</strong></td></tr><tr><th>Berlaku sampai</th><td id="ocPairExp">-</td></tr><tr><th>Sinkronisasi terakhir</th><td id="ocLastSync">-</td></tr><tr><th>Status</th><td id="ocStatus">-</td></tr></tbody></table></div><p id="ocMsg"></p><div class="form-section"><h3>Log Sinkronisasi</h3><div class="table-wrap"><table><thead><tr><th>Waktu</th><th>Status</th><th>Pesan</th></tr></thead><tbody id="ocLogs"></tbody></table></div></div></div></div>
<script>const byId=id=>document.getElementById(id);
function safeValue(id,def=''){const el=byId(id);return el?el.value:def}

let token=localStorage.getItem('slp_token')||'',deviceId=localStorage.getItem('slp_device_id')||'',heartbeatTimer=null,currentUser=null,products=[],transactionProducts=[],partners=[],warehouses=[],purchaseLines=[],cashAccounts=[],brands=[],salespersons=[];const rup=n=>new Intl.NumberFormat('id-ID').format(Number(n||0));async function api(p,o={}){o.headers=Object.assign({'Content-Type':'application/json'},o.headers||{});if(token)o.headers.Authorization='Bearer '+token;let r=await fetch(p,o),t=await r.text(),d={};try{d=JSON.parse(t)}catch(e){d={error:t}}if(!r.ok)throw Error(d.error||'HTTP '+r.status);return d}function msg(el,text,ok=true){el.className=ok?'ok':'error';el.textContent=text}function ensureDeviceId(){if(!deviceId){deviceId=(crypto&&crypto.randomUUID)?crypto.randomUUID():'DEV-'+Date.now()+'-'+Math.random().toString(36).slice(2);localStorage.setItem('slp_device_id',deviceId)}return deviceId}
function installTypeToSearchSelects(){
  if(window.__slTypeSearchInstalled)return;window.__slTypeSearchInstalled=true;
  const transactionPages=new Set(['sales','purchases','receivables','payables','cash','purchaseReturns','salesReturns','ordersDp','inventory','stock','accounting','transactionMaintenance']);
  let box=null,active=null;
  function closeBox(){if(box){box.remove();box=null}active=null}
  function isCoreItemSearch(sel){return !!(sel&&sel.matches&&sel.matches('.slProduct,#purchaseProduct,.od-product'))}
  function positionBox(){
    if(!box||!active||!active.isConnected)return;
    const r=active.getBoundingClientRect();
    Object.assign(box.style,{position:'fixed',left:Math.max(6,r.left)+'px',top:Math.min(window.innerHeight-280,r.bottom+4)+'px',width:Math.max(260,r.width)+'px',zIndex:'100000'});
  }
  function isSearchable(sel){
    if(!(sel instanceof HTMLSelectElement)||sel.disabled)return false;
    const p=sel.closest('.page');if(!p||!transactionPages.has(p.id))return false;
    // Dropdown dinamis transaksi dengan banyak opsi dibuat searchable. Enum pendek tetap native.
    return sel.options.length>=5 || /Product|Customer|Supplier|Invoice|Purchase|Account|Cash|Warehouse|Salesperson|Partner|Unit|Department|Project/i.test(sel.id||sel.className||'');
  }
  function openSearch(sel){
    closeBox();active=sel;
    const r=sel.getBoundingClientRect();
    box=document.createElement('div');box.className='sl-select-search-popover';
    box.innerHTML='<input class="sl-select-search-input" autocomplete="off" placeholder="Ketik untuk mencari..."><div class="sl-select-search-list"></div>';
    document.body.appendChild(box);
    positionBox();
    const input=box.querySelector('input'),list=box.querySelector('.sl-select-search-list');
    function render(){
      const q=(input.value||'').trim().toLowerCase();
      const opts=[...sel.options].filter(o=>!o.disabled&&o.value!==''&&(!q||String(o.textContent||'').toLowerCase().includes(q))).slice(0,80);
      list.innerHTML=opts.length?opts.map((o,i)=>`<button type="button" class="sl-select-search-option" data-i="${i}">${String(o.textContent||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}</button>`).join(''):'<div class="sl-select-search-empty">Tidak ditemukan</div>';
      [...list.querySelectorAll('button')].forEach((b,i)=>b.onclick=()=>{const o=opts[i];sel.value=o.value;sel.dispatchEvent(new Event('change',{bubbles:true}));closeBox();sel.focus()});
    }
    input.addEventListener('input',render);input.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();closeBox();sel.focus()}else if(e.key==='Enter'){const b=list.querySelector('button');if(b){e.preventDefault();b.click()}}});
    render();setTimeout(()=>input.focus(),0);
  }
  document.addEventListener('mousedown',e=>{const sel=e.target.closest&&e.target.closest('select');if(isSearchable(sel)){e.preventDefault();openSearch(sel)}else if(box&&!box.contains(e.target))closeBox()},true);
  document.addEventListener('keydown',e=>{
    const sel=e.target;if(!isSearchable(sel)||e.ctrlKey||e.altKey||e.metaKey)return;
    if(e.key.length===1&&/[\p{L}\p{N} ._\-]/u.test(e.key)){e.preventDefault();openSearch(sel);const inp=box&&box.querySelector('input');if(inp){inp.value=e.key;inp.dispatchEvent(new Event('input'))}}
    else if((e.key==='Enter'||e.key==='F4'||(e.altKey&&e.key==='ArrowDown'))&&!box){e.preventDefault();openSearch(sel)}
  },true);
  window.addEventListener('resize',()=>{if(active)positionBox()});
  window.addEventListener('scroll',()=>{if(active)positionBox()},true);
}
function showAuthPane(kind){let loginMode=kind!=='signup';authLoginPane.classList.toggle('active',loginMode);authSignupPane.classList.toggle('active',!loginMode);authLoginTab.classList.toggle('active',loginMode);authSignupTab.classList.toggle('active',!loginMode)}async function createTrialAccount(){try{signupMsg.textContent='Membuat akun dan database trial...';signupMsg.className='muted';let d=await api('/api/signup',{method:'POST',body:JSON.stringify({company_name:signupCompany.value,owner_name:signupName.value,email:signupEmail.value,phone:signupPhone.value,password:signupPassword.value})});msg(signupMsg,'Akun berhasil dibuat. Trial 7 hari aktif sampai '+new Date(d.account.trial_expires_at).toLocaleDateString('id-ID')+'. Silakan login.',true);username.value=signupEmail.value;password.value=signupPassword.value;setTimeout(()=>showAuthPane('login'),500)}catch(e){msg(signupMsg,e.message,false)}}async function doLogin(){try{let d=await api('/api/login',{method:'POST',body:JSON.stringify({username:username.value,password:password.value,client_name:navigator.userAgent.includes('Mobile')?'mobile-browser':'desktop-browser',device_id:ensureDeviceId()})});token=d.token;localStorage.setItem('slp_token',token);window.__currentAccount=d.account||null;openApp(d.user)}catch(e){msg(loginMsg,e.message,false)}}function hasPermission(code){const p=currentUser&&currentUser.role&&Array.isArray(currentUser.role.permissions)?currentUser.role.permissions:[];return p.includes('*')||p.includes(code)}async function openApp(u){installTypeToSearchSelects();renderMobileDrawerMenu();currentUser=u;const perms=(u&&u.role&&Array.isArray(u.role.permissions))?u.role.permissions:[];document.body.classList.toggle('hide-cost',!(perms.includes('*')||perms.includes('cost.view')));authShell.classList.add('hidden');authShell.setAttribute('aria-hidden','true');app.classList.remove('hidden');app.setAttribute('aria-hidden','false');window.scrollTo(0,0);who.textContent=u.username+' · '+u.role.name;startHeartbeat();await refreshAll();await refreshSubscriptionChip()}function openPartnerPage(type,b){partnerFilter.value=type;page('partners',b);loadPartners()}function clearTransactionEditState(){window.__maintenanceEdit=null;window.__documentEdit=null;window.__salesReturnEdit=null;window.__purchaseReturnEdit=null}
function discardTransactionDraftForPage(id){
 if(id==='sales'){
  window.__documentEdit=null;window.__sourceSalesOrderId=null;
  if(window.saleLines){saleLines.innerHTML='';try{addSaleLine()}catch(e){}}
  if(window.saleCustomer)saleCustomer.value='';if(window.saleSalesperson)saleSalesperson.value='';if(window.saleCashAccount)saleCashAccount.value='';
  if(window.saleDiscount)saleDiscount.value='0';if(window.saleTax)saleTax.value='0';if(window.salePaid)salePaid.value='0';if(window.saleNotes)saleNotes.value='';
  if(window.saleInvoiceNo)saleInvoiceNo.dataset.edited='';if(window.saleDeliveryNo)saleDeliveryNo.dataset.edited='';
 }else if(id==='purchases'){
  window.__documentEdit=null;window.__sourcePurchaseOrderId=null;purchaseLines=[];try{renderPurchaseLines()}catch(e){}
  if(window.purchaseSupplier)purchaseSupplier.value='';if(window.purchaseSupplierInvoice)purchaseSupplierInvoice.value='';if(window.purchaseCashAccount)purchaseCashAccount.value='';
  if(window.purchaseDiscount)purchaseDiscount.value='0';if(window.purchaseTax)purchaseTax.value='0';if(window.purchasePaid)purchasePaid.value='0';if(window.purchaseNotes)purchaseNotes.value='';
 }
}
function refreshPageData(id){const map={products:()=>Promise.allSettled([loadProducts(),loadMasters()]),partners:()=>loadPartners(),services:()=>loadServices(),receivables:()=>Promise.allSettled([loadSettlementMasters(),loadReceivables()]),payables:()=>Promise.allSettled([loadSettlementMasters(),loadPayables()]),accounting:()=>loadAccounting(),cash:()=>Promise.allSettled([loadCashAccounts(),loadCashTransactions()]),stock:()=>Promise.allSettled([loadProducts(),loadMoves()]),sales:()=>Promise.allSettled([loadSales(),loadProducts(),loadCashAccounts()]),purchases:()=>Promise.allSettled([loadPurchases(),loadProducts(),loadCashAccounts()]),fixedAssetPage:()=>loadFixedAssets(),fixedAssetDepPage:()=>Promise.allSettled([loadFixedAssets(),loadDepreciationHistory()])};try{return map[id]?map[id]():Promise.resolve()}catch(e){console.error('Refresh halaman gagal',id,e);return Promise.resolve()}}
function page(id,b){if(window.__activePageId&&window.__activePageId!==id){discardTransactionDraftForPage(window.__activePageId);clearTransactionEditState();}document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.querySelectorAll('.nav button').forEach(x=>x.classList.remove('active'));let target=document.getElementById(id);if(!target){alert('Halaman '+id+' belum tersedia.');return}target.classList.add('active');if(b)b.classList.add('active');window.__activePageId=id;window.scrollTo({top:0,behavior:'smooth'});setTimeout(()=>refreshPageData(id),0);setTimeout(syncMobileNav,0)}function closePage(id){clearTransactionEditState();window.__activeModuleKey='dashboard';const target=document.getElementById(id||window.__activePageId);if(target)target.classList.remove('active');document.querySelectorAll('.nav button').forEach(x=>x.classList.remove('active'));window.__activePageId='';window.scrollTo({top:0,behavior:'smooth'})}function installPageCloseButtons(){document.querySelectorAll('.page').forEach(section=>{if(section.querySelector(':scope > .page-close-btn'))return;const btn=document.createElement('button');btn.type='button';btn.className='page-close-btn';btn.title='Tutup halaman';btn.setAttribute('aria-label','Tutup halaman');btn.textContent='×';btn.onclick=()=>closePage(section.id);section.insertBefore(btn,section.firstChild)})}async function refreshAll(){
 const safe=async(label,fn)=>{try{return await fn()}catch(e){console.error('Startup '+label+' gagal:',e);return null}};
 const today=new Date().toISOString().slice(0,10);
 const h=await safe('health',()=>api('/api/health'));
 if(h){let lic=h.license||{};let licText=lic.mode==='SUBSCRIPTION'?((lic.plan_name||'LANGGANAN')+' · '+(lic.days_remaining??0)+' hari · '+(lic.max_users??2)+' user'):(lic.mode==='TRIAL'?('TRIAL 7 HARI · sisa '+(lic.days_remaining??0)+' hari · '+(lic.max_users??2)+' user'):(lic.mode==='TRIAL_EXPIRED'||lic.mode==='SUBSCRIPTION_EXPIRED'?'MASA AKSES BERAKHIR':'LISENSI'));if(window.health)health.textContent='Online · v'+h.version+' · port '+h.port+' · '+licText}
 const setValue=(id,v)=>{const el=document.getElementById(id);if(el)el.value=v};
 ['saleDate','rpDate','phDate','jDate','purchaseDate','cashDate','transferDate'].forEach(id=>setValue(id,today));setValue('ledgerTo',today);setValue('trialTo',today);setValue('saleDue','');setValue('purchaseDue','');
 await safe('nomor dokumen',loadDocumentNumbers);
 // Master inti dimuat satu per satu tetapi kegagalan salah satu tidak menghentikan startup.
 await safe('profil perusahaan',loadCompany);await safe('gudang',loadWarehouses);await safe('kas bank',loadCashAccounts);await safe('master',loadMasters);await safe('master tambahan',loadExtraMasters);await safe('produk/jasa',loadProducts);
 // Dropdown transaksi dimuat langsung, terpisah dari halaman daftar partner.
 await safe('pelanggan/pemasok transaksi',loadTransactionPartners);
 await safe('daftar partner',loadPartners);await safe('master settlement',loadSettlementMasters);
 await Promise.allSettled([loadReceivables(),loadPayables(),loadAccounting(),loadTrial(),loadSummary(),loadSales(),loadPurchases(),loadCashTransactions(),loadMoves(),loadBalances(),loadInventoryCard(),loadUsers(),loadAudit(),typeof loadDash==='function'?loadDash():Promise.resolve()]);
 const lines=document.getElementById('saleLines');if(lines&&!lines.children.length)try{addSaleLine()}catch(e){console.error('Baris penjualan awal gagal:',e)}
}async function loadSettlementMasters(){
 const [customers,suppliers]=await Promise.all([api('/api/customers?active=1'),api('/api/suppliers?active=1')]);
 const cv=rpCustomer?.value||'',sv=phSupplier?.value||'';
 rpCustomer.innerHTML='<option value="">Semua Pelanggan</option>'+(customers.items||[]).map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');
 phSupplier.innerHTML='<option value="">Semua Pemasok</option>'+(suppliers.items||[]).map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');
 if([...rpCustomer.options].some(x=>x.value===cv))rpCustomer.value=cv;
 if([...phSupplier.options].some(x=>x.value===sv))phSupplier.value=sv
}
async function loadReceivables(){
 try{
  const q=rpCustomer?.value?'?customer_id='+encodeURIComponent(rpCustomer.value):'';
  const d=await api('/api/receivables'+q),term=String(rpSearch?.value||'').trim().toLowerCase(),items=(d.items||[]).filter(x=>!term||[x.invoice_no,x.customer_code,x.customer_name].some(v=>String(v||'').toLowerCase().includes(term)));
  receivableBody.innerHTML=items.length?items.map(x=>`<tr><td>${x.invoice_no}</td><td>${x.customer_code} - ${x.customer_name}</td><td>${x.due_date||'-'}</td><td>${rup(x.balance_due)}</td><td>${x.days_overdue}</td></tr>`).join(''):'<tr><td colspan="5">Tidak ada piutang outstanding.</td></tr>';
  rpInvoice.innerHTML=items.length?'<option value="">-- Pilih Invoice Outstanding --</option>'+items.map(x=>`<option value="${x.id}" data-balance="${x.balance_due}">${x.invoice_no} | ${x.customer_name} | Sisa ${rup(x.balance_due)}</option>`).join(''):'<option value="">Tidak ada invoice outstanding</option>';
  fillReceivableAmount()
 }catch(e){msg(rpMsg,e.message,false)}
}
function fillReceivableAmount(){const o=rpInvoice?.selectedOptions?.[0];if(o?.dataset?.balance)rpAmount.value=o.dataset.balance}
async function loadPayables(){
 try{
  const q=phSupplier?.value?'?supplier_id='+encodeURIComponent(phSupplier.value):'';
  const d=await api('/api/payables'+q),term=String(phSearch?.value||'').trim().toLowerCase(),items=(d.items||[]).filter(x=>!term||[x.purchase_no,x.supplier_code,x.supplier_name].some(v=>String(v||'').toLowerCase().includes(term)));
  payableBody.innerHTML=items.length?items.map(x=>`<tr><td>${x.purchase_no}</td><td>${x.supplier_code} - ${x.supplier_name}</td><td>${x.due_date||'-'}</td><td>${rup(x.balance_due)}</td><td>${x.days_overdue}</td></tr>`).join(''):'<tr><td colspan="5">Tidak ada hutang outstanding.</td></tr>';
  phPurchase.innerHTML=items.length?'<option value="">-- Pilih Invoice Pembelian Outstanding --</option>'+items.map(x=>`<option value="${x.id}" data-balance="${x.balance_due}">${x.purchase_no} | ${x.supplier_name} | Sisa ${rup(x.balance_due)}</option>`).join(''):'<option value="">Tidak ada invoice outstanding</option>';
  fillPayableAmount()
 }catch(e){msg(phMsg,e.message,false)}
}
function fillPayableAmount(){const o=phPurchase?.selectedOptions?.[0];if(o?.dataset?.balance)phAmount.value=o.dataset.balance}
async function receiveAR(){try{let payload={sale_id:rpInvoice.value,cash_account_id:rpCash.value,payment_date:rpDate.value,amount:rpAmount.value,notes:rpNotes.value};let edited=await commitMaintenanceEdit(payload);let d=edited?{result:{payment_no:'pengganti'}}:await api('/api/receivable-payments',{method:'POST',body:JSON.stringify(payload)});msg(rpMsg,'Penerimaan '+d.result.payment_no+' berhasil.');await Promise.all([loadReceivables(),loadSales(),loadCashAccounts()]);await openFreshTransactionForm('receivable')}catch(e){msg(rpMsg,e.message,false)}}
async function payAP(){try{let payload={purchase_id:phPurchase.value,cash_account_id:phCash.value,payment_date:phDate.value,amount:phAmount.value,notes:phNotes.value};let edited=await commitMaintenanceEdit(payload);let d=edited?{result:{payment_no:'pengganti'}}:await api('/api/payable-payments',{method:'POST',body:JSON.stringify(payload)});msg(phMsg,'Pembayaran '+d.result.payment_no+' berhasil.');await Promise.all([loadPayables(),loadPurchases(),loadCashAccounts()]);await openFreshTransactionForm('payable')}catch(e){msg(phMsg,e.message,false)}}
async function loadSummary(){
  const setText=(id,value)=>{const el=document.getElementById(id);if(el)el.textContent=value};
  try{const d=await api('/api/inventory/summary');setText('sTotal',d.total_products??0);setText('sActive',d.active_products??0);setText('sLow',d.low_stock??0);setText('sValue',rup(d.stock_value??0))}catch(e){console.error('Ringkasan persediaan gagal:',e)}
  try{const s=await api('/api/sales/summary');setText('ssCount',s.transaction_count??0);setText('ssTotal',rup(s.sales_total??0));setText('ssDue',rup(s.receivable_total??0))}catch(e){console.error('Ringkasan penjualan gagal:',e)}
}
async function runRefresh(btn,fn,labelId){let old=btn.textContent;btn.disabled=true;btn.textContent='Memuat...';try{await fn();let el=document.getElementById(labelId);if(el)el.textContent='Terakhir diperbarui: '+new Date().toLocaleTimeString('id-ID')}catch(e){alert(e.message)}finally{btn.disabled=false;btn.textContent=old}}
async function loadCompany(){try{let d=await api('/api/company-profile');coName.value=d.company_name||'';coAddress.value=d.address||'';coCity.value=d.city||'';coPhone.value=d.phone||'';coEmail.value=d.email||'';coTax.value=d.tax_id||'';coWeb.value=d.website||'';if(d.logo_path)coLogoPreview.src='/api/company-logo?token='+encodeURIComponent(token)+'&t='+Date.now()}catch(e){}}
function previewCompanyLogo(){const f=coLogoFile.files[0];if(f)coLogoPreview.src=URL.createObjectURL(f)}
async function fileToDataUrl(file){return await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=reject;r.readAsDataURL(file)})}
async function saveCompany(){try{const f=coLogoFile.files[0];await api('/api/company-profile',{method:'PUT',body:JSON.stringify({company_name:coName.value,address:coAddress.value,city:coCity.value,phone:coPhone.value,email:coEmail.value,tax_id:coTax.value,website:coWeb.value,logo_base64:f?await fileToDataUrl(f):'',logo_filename:f?.name||''})});msg(coMsg,'Profil perusahaan berhasil disimpan.');await loadCompany()}catch(e){msg(coMsg,e.message,false)}}
async function loadExtraMasters(){let b=await api('/api/brands?active=1'),sp=await api('/api/salespersons?active=1');brands=b.items;salespersons=sp.items;brandBody.innerHTML=brands.map(x=>`<tr><td>${x.code}</td><td>${x.name}</td><td>${x.is_active?'Aktif':'Nonaktif'}</td><td><button onclick="editBrand(${x.id})">Edit</button> <button class="danger" onclick="deleteMaster('/api/brands/${x.id}',loadExtraMasters)">Hapus</button></td></tr>`).join('');saleSalesperson.innerHTML='<option value="">Tanpa Salesman</option>'+salespersons.map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');salespersonBody.innerHTML=salespersons.map(x=>`<tr><td>${x.code}</td><td>${x.name}</td><td>${x.phone||''}</td><td>${x.commission_percent}%</td><td>${x.is_active?'Aktif':'Nonaktif'}</td><td><button onclick="editSalesperson(${x.id})">Edit</button> <button class="danger" onclick="deleteMaster('/api/salespersons/${x.id}',loadExtraMasters)">Hapus</button></td></tr>`).join('');pBrand.innerHTML='<option value="">Tanpa Merk</option>'+brands.filter(x=>x.is_active).map(x=>`<option value="${x.id}">${x.name}</option>`).join('')}
async function addBrand(){try{let id=brandEditId.value;await api(id?'/api/brands/'+id:'/api/brands',{method:id?'PUT':'POST',body:JSON.stringify({code:brandCode.value,name:brandName.value,is_active:true})});brandEditId.value='';brandCode.value=brandName.value='';await loadExtraMasters()}catch(e){alert(e.message)}} function editBrand(id){let x=brands.find(v=>v.id===id);if(!x)return;brandEditId.value=id;brandCode.value=x.code;brandName.value=x.name}
async function addSalesperson(){try{let id=salespersonEditId.value;await api(id?'/api/salespersons/'+id:'/api/salespersons',{method:id?'PUT':'POST',body:JSON.stringify({code:spCode.value,name:spName.value,phone:spPhone.value,email:spEmail.value,commission_percent:spCommission.value,is_active:true})});salespersonEditId.value='';spCode.value=spName.value=spPhone.value=spEmail.value='';spCommission.value=0;await loadExtraMasters()}catch(e){alert(e.message)}} function editSalesperson(id){let x=salespersons.find(v=>v.id===id);if(!x)return;salespersonEditId.value=id;spCode.value=x.code;spName.value=x.name;spPhone.value=x.phone||'';spEmail.value=x.email||'';spCommission.value=x.commission_percent||0}
async function loadCashAccounts(){
  const ids=['cashAccount','cashSource','cashTarget','saleCashAccount','purchaseCashAccount','rpCash','phCash','cashFilterAccount','importCash'];
  const selected=Object.fromEntries(ids.map(id=>[id,byId(id)?.value||'']));
  const d=await api('/api/cash-accounts?active=1');cashAccounts=(d.items||[]).filter(x=>x.is_active!==false);
  const opts=cashAccounts.length?cashAccounts.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)} (${rup(x.current_balance)})</option>`).join(''):'<option value="" disabled selected>Belum ada akun kas / bank</option>';
  ['cashAccount','cashSource','cashTarget','saleCashAccount','purchaseCashAccount','rpCash','phCash','importCash'].forEach(id=>{const el=byId(id);if(!el)return;el.innerHTML=opts;if([...el.options].some(o=>o.value===selected[id]))el.value=selected[id];el.disabled=!cashAccounts.length});
  const filter=byId('cashFilterAccount');if(filter){filter.innerHTML='<option value="">Semua Akun</option>'+cashAccounts.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');if([...filter.options].some(o=>o.value===selected.cashFilterAccount))filter.value=selected.cashFilterAccount}
  const body=byId('cashAccountsBody');if(body)body.innerHTML=cashAccounts.length?cashAccounts.map(x=>`<tr><td>${accessEscape(x.code)}</td><td>${accessEscape(x.name)}</td><td>${accessEscape(x.account_type)}</td><td>${rup(x.current_balance)}</td><td>${x.is_active?'Aktif':'Nonaktif'}</td></tr>`).join(''):'<tr><td colspan="5" class="muted">Belum ada akun kas / bank aktif.</td></tr>';
  return cashAccounts;
}
async function loadCashTransactions(){let d=await api('/api/cash-transactions?account_id='+encodeURIComponent(cashFilterAccount?.value||'')+'&q='+encodeURIComponent(cashSearch?.value||''));cashTransactionsBody.innerHTML=d.items.map(x=>`<tr><td>${x.transaction_date}</td><td>${x.transaction_no}</td><td>${x.account_name}</td><td>${x.transaction_type}</td><td>${rup(x.amount)}</td><td>${rup(x.balance_after)}</td><td>${x.description}</td><td>${x.username}</td></tr>`).join('')}
async function refreshCash(btn){await runRefresh(btn,async()=>{await loadCashAccounts();await loadCashTransactions()},'cashRefreshAt');cashTxRefreshAt.textContent='Terakhir diperbarui: '+new Date().toLocaleTimeString('id-ID')}
function refreshCashOpeningCoa(){const el=document.getElementById('caCoaAccount');if(!el)return;const list=(window.coaItems||[]).filter(x=>x.account_subtype==='CASH_BANK');el.innerHTML='<option value="">Otomatis sesuai jenis</option>'+list.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('')}
async function openCashOpeningImport(){await openMasterImport();const e=document.getElementById('masterImportType');if(e){const o=document.createElement('option');o.value='cash_accounts';o.textContent='Kas dan Bank + Saldo Awal';e.appendChild(o);e.value='cash_accounts';masterImportReset()}}
function downloadCashOpeningTemplate(){window.open('/api/master-import/template?type=cash_accounts&token='+encodeURIComponent(token),'_blank')}
async function addCashAccount(){try{await api('/api/cash-accounts',{method:'POST',body:JSON.stringify({code:caCode.value,name:caName.value,account_type:caType.value,bank_name:caBank.value,account_number:caNumber.value,opening_balance:caOpening.value,opening_balance_date:caOpeningDate.value||null,coa_account_id:caCoaAccount.value||null})});msg(caMsg,'Akun berhasil dibuat.');await loadCashAccounts()}catch(e){msg(caMsg,e.message,false)}}
async function saveCashTransaction(){try{
if(!cashAccount.value)throw Error('Pilih akun Kas/Bank.');
if(!cashCounterAccount.value)throw Error('Pilih Akun Lawan Transaksi.');
let payload={transaction_date:cashDate.value,account_id:cashAccount.value,transaction_type:cashType.value,counter_account_id:cashCounterAccount.value,amount:cashAmount.value,reference_no:cashRef.value,description:cashDesc.value,department_id:cashDepartment.value||null,project_id:cashProject.value||null};let edited=await commitMaintenanceEdit(payload);let d=edited?{result:{transaction_no:'pengganti'}}:await api('/api/cash-transactions',{method:'POST',body:JSON.stringify(payload)});msg(cashMsg,'Transaksi '+d.result.transaction_no+' berhasil.');resetTransactionDimensions('cash');await Promise.allSettled([loadCashAccounts(),loadCashTransactions(),loadAccounting(),loadTrial(),loadDash(),loadSummary()]);await openFreshTransactionForm('cash')}catch(e){msg(cashMsg,e.message,false)}}
async function saveCashTransfer(){try{let payload={transaction_date:transferDate.value,source_account_id:cashSource.value,target_account_id:cashTarget.value,amount:transferAmount.value,reference_no:transferRef.value,description:transferDesc.value};let edited=await commitMaintenanceEdit(payload);let d=edited?{result:{transfer_no:'pengganti'}}:await api('/api/cash-transfers',{method:'POST',body:JSON.stringify(payload)});msg(transferMsg,'Transfer '+d.result.transfer_no+' berhasil.');await Promise.all([loadCashAccounts(),loadCashTransactions()]);await openFreshTransactionForm('transfer')}catch(e){msg(transferMsg,e.message,false)}}

function refreshPurchaseProducts(){
  const selected=purchaseProduct?.value||'';
  const source=transactionProducts.filter(x=>x.is_active);
  purchaseProduct.innerHTML=source.length
    ? source.map(x=>`<option value="${x.id}">${x.service_id?'[JASA] ':'[BARANG] '}${x.service_id?x.name:(x.sku+' - '+x.name)}${x.product_type==='STOCK'?' | stok gudang '+warehouseQty(x,purchaseWarehouse?.value):''}</option>`).join('')
    : '<option value="" disabled selected>Belum ada barang / jasa aktif</option>';
  if([...purchaseProduct.options].some(o=>o.value===selected))purchaseProduct.value=selected;
  purchaseProduct.disabled=!source.length;
  if(source.length){
    let p=source.find(x=>String(x.id)===purchaseProduct.value)||source[0];
    purchaseProduct.value=String(p.id);
    purchaseCost.value=p.purchase_price||0;fillPurchaseUnits();
  }else{
    purchaseCost.value=0;
  }
}
purchaseProduct?.addEventListener('change',fillPurchaseUnits);purchaseWarehouse?.addEventListener('change',refreshPurchaseProducts);saleWarehouse?.addEventListener('change',refreshSaleProductOptions)
function purchaseLineTotal(x){return Math.max(0,(Number(x.qty)||0)*(Number(x.unit_cost)||0)-(x.discount_mode==='PERCENT'?(Number(x.qty)||0)*(Number(x.unit_cost)||0)*(Number(x.discount_value)||0)/100:(Number(x.discount_value)||0)))}
function productUnits(p){if(!p)return[];let list=(Array.isArray(p.units)&&p.units.length?p.units:(Array.isArray(p.stock_units)&&p.stock_units.length?p.stock_units:[])).filter(u=>u&&u.unit_id);if(!list.some(u=>String(u.unit_id)===String(p.unit_id))&&p.unit_id)list.unshift({unit_id:p.unit_id,unit_code:p.unit_code||'',unit_name:p.unit_name||p.unit_code||'',conversion_ratio:1,purchase_price:p.purchase_price||0,selling_price:p.selling_price||0,is_base:true});return list.length?list:[{unit_id:p.unit_id,unit_code:p.unit_code||'',unit_name:p.unit_code||'',conversion_ratio:1,purchase_price:p.purchase_price||0,selling_price:p.selling_price||0,is_base:true}]}
function productMatches(p,q){q=String(q||'').trim().toLowerCase();return !q||[p.sku,p.name,p.barcode,p.brand_name].some(v=>String(v||'').toLowerCase().includes(q))}
function filterSaleProducts(q){document.querySelectorAll('.slProduct').forEach(s=>{let old=s.value,items=transactionProducts.filter(p=>p.is_active&&productMatches(p,q));s.innerHTML=items.map(p=>`<option value="${p.id}">${p.service_id?'[JASA] '+p.name:'[BARANG] '+p.sku+' - '+p.name+(p.product_type==='STOCK'?' | stok '+p.stock_qty:'')}</option>`).join('');if(items.some(p=>String(p.id)===String(old)))s.value=old;else if(s.options.length)s.selectedIndex=0;lineProduct(s)})}
function filterPurchaseProducts(q){let old=purchaseProduct?.value||'',items=transactionProducts.filter(p=>p.is_active&&productMatches(p,q));if(!purchaseProduct)return;purchaseProduct.innerHTML=items.map(p=>`<option value="${p.id}">${p.service_id?'[JASA] ':''}${p.sku||''} - ${p.name}</option>`).join('');if(items.some(p=>String(p.id)===String(old)))purchaseProduct.value=old;else if(purchaseProduct.options.length)purchaseProduct.selectedIndex=0;fillPurchaseUnits()}
function fillPurchaseUnits(){let p=transactionProducts.find(x=>String(x.id)===purchaseProduct.value),list=productUnits(p);purchaseUnit.innerHTML=list.map(u=>`<option value="${u.unit_id}">${u.unit_code} · 1 ${u.unit_code} = ${u.conversion_ratio} ${p?.unit_code||''}</option>`).join('');let u=list[0];if(u)purchaseCost.value=u.purchase_price||p.purchase_price||0}
purchaseUnit?.addEventListener('change',()=>{let p=transactionProducts.find(x=>String(x.id)===purchaseProduct.value),u=productUnits(p).find(x=>String(x.unit_id)===purchaseUnit.value);if(u)purchaseCost.value=u.purchase_price||0});
function renderProductUnitRows(rows){
  if(rows!==undefined)window.__productUnits=Array.isArray(rows)?rows:[];
  if(!Array.isArray(window.__productUnits))window.__productUnits=[];
  const container=document.getElementById('productUnitRows');
  const baseSelect=document.getElementById('pUnit');
  if(!container)return;
  const baseId=baseSelect?String(baseSelect.value||''):'';
  const visible=window.__productUnits.map((row,index)=>({row,index})).filter(x=>!x.row.is_base&&String(x.row.unit_id)!==baseId);
  container.innerHTML=visible.length?visible.map(({row,index})=>`<div class="product-unit-row"><label>Satuan Alternatif<select onchange="window.__productUnits[${index}].unit_id=this.value">${(window.unitRecords||[]).filter(u=>String(u.id)!==baseId).map(u=>`<option value="${u.id}" ${String(u.id)===String(row.unit_id)?'selected':''}>${u.code} - ${u.name}</option>`).join('')}</select></label><label>Rasio ke Satuan Dasar<input type="number" step="0.0001" min="0.0001" value="${row.conversion_ratio||1}" onchange="window.__productUnits[${index}].conversion_ratio=this.value"></label><label>Harga Beli / Satuan<input type="number" min="0" value="${row.purchase_price||0}" onchange="window.__productUnits[${index}].purchase_price=this.value"></label><label>Harga Jual / Satuan<input type="number" min="0" value="${row.selling_price||0}" onchange="window.__productUnits[${index}].selling_price=this.value"></label><button type="button" class="danger" onclick="window.__productUnits.splice(${index},1);renderProductUnitRows()">Hapus</button></div>`).join(''):'<div class="muted">Belum ada satuan alternatif.</div>';
}
function syncProductUnitPrice(i){let r=window.__productUnits?.[i];if(!r)return;let ratio=numericValue(r.conversion_ratio)||1;r.purchase_price=(numericValue(pBuy?.value)*ratio).toFixed(2);r.selling_price=(numericValue(pSell?.value)*ratio).toFixed(2);renderProductUnitRows()}
function addProductUnitRow(){let available=(window.unitRecords||[]).find(u=>String(u.id)!==String(pUnit.value)&&!(window.__productUnits||[]).some(x=>String(x.unit_id)===String(u.id)));if(!available){alert('Semua satuan sudah dipakai.');return}(window.__productUnits||(window.__productUnits=[])).push({unit_id:available.id,conversion_ratio:1,purchase_price:0,selling_price:0,is_base:false});renderProductUnitRows(window.__productUnits)}
function collectProductUnits(){return [{unit_id:pUnit.value,conversion_ratio:1,purchase_price:pBuy.value,selling_price:pSell.value,is_base:true},...(window.__productUnits||[]).filter(x=>String(x.unit_id)!==String(pUnit.value)).map(x=>({...x,conversion_ratio:numericValue(x.conversion_ratio||1),purchase_price:numericValue(x.purchase_price),selling_price:numericValue(x.selling_price)}))]}
pUnit?.addEventListener('change',()=>renderProductUnitRows())
function renderPurchaseLines(){purchaseLinesBody.innerHTML=purchaseLines.length?purchaseLines.map((x,i)=>`<tr><td>${i+1}</td><td><span class="item-name">${x.name}</span><span class="item-type">${x.item_type==='SERVICE'?'Jasa':'Barang'}</span></td><td>${x.unit_code||'-'}</td><td class="num">${rup(x.qty)}</td><td class="num">Rp${rup(x.unit_cost)}</td><td class="num">${x.discount_mode==='PERCENT'?rup(x.discount_value)+'%':'Rp'+rup(x.discount_value)}</td><td class="num"><strong>Rp${rup(purchaseLineTotal(x))}</strong></td><td class="action-col"><button type="button" class="danger icon-delete" title="Hapus baris" onclick="purchaseLines.splice(${i},1);renderPurchaseLines()">×</button></td></tr>`).join(''):'<tr><td colspan="8" class="muted" style="text-align:center;padding:22px">Belum ada item pembelian.</td></tr>';let subtotal=purchaseLines.reduce((a,x)=>a+purchaseLineTotal(x),0),dv=Number(purchaseDiscount.value)||0,disc=(purchaseDiscountMode&&purchaseDiscountMode.value==='PERCENT')?subtotal*dv/100:dv,taxable=Math.max(0,subtotal-disc),tax=taxable*(Number(purchaseTax.value)||0)/100,total=taxable+tax;purchaseGrandTotal.textContent=rup(Math.max(0,total))}
purchaseDiscount?.addEventListener('input',renderPurchaseLines)
function addPurchaseLine(){let p=transactionProducts.find(x=>String(x.id)===purchaseProduct.value);if(!p)return;let q=Number(purchaseQty.value),cost=Number(purchaseCost.value),disc=Number(purchaseLineDiscount.value||0);if(!(q>0)||cost<0){msg(purchaseMsg,'Qty atau harga beli tidak valid.',false);return}let u=productUnits(p).find(x=>String(x.unit_id)===String(purchaseUnit.value))||productUnits(p)[0];purchaseLines.push({product_id:p.id,unit_id:u.unit_id,unit_code:u.unit_code,conversion_ratio:u.conversion_ratio,name:(p.service_id?'[JASA] ':'[BARANG] ')+p.name,item_type:p.service_id?'SERVICE':'PRODUCT',service_id:p.service_id||null,qty:q,unit_cost:cost,discount_mode:purchaseLineDiscountMode.value,discount_value:disc});renderPurchaseLines()}
async function savePurchase(){try{if(!purchaseSupplier.value)throw new Error('Supplier / pemasok wajib dipilih. Tambahkan pemasok aktif melalui menu Data Pemasok.');if(!purchaseLines.length)throw new Error('Minimal satu item pembelian wajib diisi.');let edit=window.__documentEdit&&window.__documentEdit.kind==='purchase'?window.__documentEdit:null;let d=await api(edit?'/api/purchases/'+edit.id:'/api/purchases',{method:edit?'PUT':'POST',body:JSON.stringify({purchase_date:purchaseDate.value,supplier_invoice_no:purchaseSupplierInvoice.value,goods_receipt_no:purchaseGoodsReceipt.value,supplier_id:purchaseSupplier.value,warehouse_id:purchaseWarehouse.value,department_id:purchaseDepartment.value||null,project_id:purchaseProject.value||null,payment_method:purchasePayment.value,cash_account_id:purchaseCashAccount.value,payment_term_days:String(document.getElementById('purchaseTerm').value||'0').replace(/[^0-9]/g,'')||'0',due_date:purchaseDue.value,tax_percent:purchaseTax.value,paid_amount:purchasePaid.value,discount_mode:purchaseDiscountMode.value,discount_value:purchaseDiscount.value,notes:purchaseNotes.value,purchase_order_id:window.__sourcePurchaseOrderId||null,items:purchaseLines.map(({name,...x})=>x)})});window.__documentEdit=null;msg(purchaseMsg,(edit?'Pembelian diperbarui: ':'Pembelian ')+d.result.purchase_no+' berhasil disimpan.');purchaseLines=[];renderPurchaseLines();window.__sourcePurchaseOrderId=null;resetTransactionDimensions('purchase');await loadDocumentNumbers();await Promise.all([loadProducts(),loadPurchases(),loadCashAccounts(),loadBalances(),loadInventoryCard(),loadMoves(),loadSummary()]);await loadTransactionPartners();await openFreshTransactionForm('purchase')}catch(e){msg(purchaseMsg,e.message,false)}}async function loadPurchases(){try{let d=await api('/api/purchases?q='+encodeURIComponent(purchaseSearch?.value||'')+'&date_from='+encodeURIComponent(purchaseFrom?.value||'')+'&date_to='+encodeURIComponent(purchaseTo?.value||''));purchasesBody.innerHTML=d.items.map(x=>`<tr><td>${x.purchase_date}</td><td>${x.purchase_no}</td><td>${x.supplier_name}</td><td>${x.warehouse_name}</td><td>${x.payment_method}</td><td>${x.due_date||'-'}</td><td>${rup(x.tax_amount)}</td><td>${rup(x.total_amount)}</td><td>${rup(x.balance_due)}</td><td><button onclick="editPurchase(${x.id})">Edit</button> <button class="danger" onclick="voidPurchase(${x.id})">Hapus</button></td><td><button onclick="openPrint('purchase-invoice',${x.id})">Faktur</button><button onclick="openPrint('goods-receipt',${x.id})">Good Receive</button></td></tr>`).join('')}catch(e){}}


let transactionDepartments=[];
let transactionProjects=[];
let transactionDimensionsLoaded=false;

function dimensionOptionHtml(items,label,selected=''){
  return `<option value="">Tanpa ${label}</option>`+(items||[]).map(item=>
    `<option value="${item.id}" ${String(item.id)===String(selected)?'selected':''}>${accessEscape(item.code)} - ${accessEscape(item.name)}</option>`
  ).join('');
}
function fillDimensionSelect(id,items,label,preserve=true){
  const element=document.getElementById(id);
  if(!element)return;
  const selected=preserve?element.value:'';
  element.innerHTML=dimensionOptionHtml(items,label,selected);
  if(selected&&items.some(item=>String(item.id)===String(selected))){
    element.value=selected;
  }
}
function refreshTransactionDimensionSelects(){
  ['saleDepartment','purchaseDepartment','cashDepartment','adjustDepartment'].forEach(id=>
    fillDimensionSelect(id,transactionDepartments,'Departemen')
  );
  ['saleProject','purchaseProject','cashProject','adjustProject'].forEach(id=>
    fillDimensionSelect(id,transactionProjects,'Proyek')
  );
  if(Array.isArray(journalLines)&&journalLines.length)renderJLines();
}
async function loadTransactionDimensions(force=false){
  if(transactionDimensionsLoaded&&!force){
    refreshTransactionDimensionSelects();
    return;
  }
  const [departments,projects]=await Promise.all([
    hasPermission('departments.view')?api('/api/departments?active=1'):Promise.resolve({items:[]}),
    hasPermission('projects.view')?api('/api/projects?active=1'):Promise.resolve({items:[]})
  ]);
  transactionDepartments=Array.isArray(departments.items)?departments.items:[];
  transactionProjects=Array.isArray(projects.items)?projects.items:[];
  transactionDimensionsLoaded=true;
  refreshTransactionDimensionSelects();
}
function resetTransactionDimensions(prefix){
  const department=document.getElementById(prefix+'Department');
  const project=document.getElementById(prefix+'Project');
  if(department)department.value='';
  if(project)project.value='';
}

let coaItems=[],journalLines=[];
async function loadCoaBusinessTemplates(){
  const select=document.getElementById('coaTemplateSelect');
  const message=document.getElementById('coaTemplateMsg');
  if(!select)return [];
  const current=select.value;
  const fallback=[
    {key:'dagang',name:'Usaha Dagang'},{key:'jasa',name:'Perusahaan Jasa'},
    {key:'bengkel',name:'Bengkel'},{key:'sekolah',name:'Sekolah / Lembaga Pendidikan'},
    {key:'pabrik',name:'Pabrik / Manufaktur'},{key:'perkebunan',name:'Perkebunan'},
    {key:'warung',name:'Warung / Toko Kecil'},{key:'apotik',name:'Apotek'},
    {key:'distributor',name:'Distributor'},{key:'kontraktor',name:'Kontraktor'}
  ];
  const render=items=>{
    select.innerHTML='<option value="">-- Pilih Standar Usaha --</option>'+items.map(x=>`<option value="${x.key}">${x.name}${x.account_count?' ('+x.account_count+' akun)':''}</option>`).join('');
    if(items.some(x=>String(x.key)===String(current)))select.value=current;
    select.disabled=false;
  };
  render(fallback);
  try{
    const response=await api('/api/coa-templates');
    const items=Array.isArray(response.items)&&response.items.length?response.items:fallback;
    render(items);
    if(message)message.textContent='';
    return items;
  }catch(error){
    render(fallback);
    if(message)msg(message,'Pilihan standar usaha lokal digunakan. API template: '+error.message,false);
    return fallback;
  }
}
async function loadCoreAccountingMasters(){
  const response=await api('/api/coa?active=1');
  coaItems=Array.isArray(response.items)?response.items:[];
  coaData=coaItems;window.coaItems=coaItems;
  const body=byId('coaBody');
  if(body)body.innerHTML=coaItems.length?coaItems.map(x=>`<tr><td>${accessEscape(x.code)}</td><td>${accessEscape(x.name)}</td><td>${accountTypeLabel(x.display_type||x.account_type)}</td><td>${accessEscape(x.normal_balance||'')}</td><td>${x.is_active?'Aktif':'Nonaktif'}</td><td><button onclick="editCoa(${x.id})">Edit</button> <button class="danger" onclick="deleteCoa(${x.id})">Hapus</button></td></tr>`).join(''):'<tr><td colspan="6" class="muted">Belum ada akun aktif.</td></tr>';
  const ledger=byId('ledgerAccount');
  if(ledger){const old=ledger.value;ledger.innerHTML=coaItems.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');if(coaItems.some(x=>String(x.id)===String(old)))ledger.value=old}
  try{bindOperationalCoaSelectors();refreshCashOpeningCoa()}catch(e){console.error('bind COA operasional:',e)}
  try{bindSmartImportMasters()}catch(e){console.error('bind smart import:',e)}
  try{if(typeof renderJLines==='function'){if(!journalLines.length){addJLine();addJLine()}else renderJLines()}}catch(e){console.error('render jurnal:',e)}
  return coaItems;
}
async function loadAccounting(){
  let accounts=[];
  try{accounts=await loadCoreAccountingMasters()}catch(e){console.error('COA:',e);const body=byId('coaBody');if(body)body.innerHTML=`<tr><td colspan="6" class="error">${accessEscape(e.message)}</td></tr>`}
  await Promise.allSettled([
    (async()=>{try{await loadCoaBusinessTemplates()}catch(e){console.error('template COA:',e)}})(),
    (async()=>{try{const d=await api('/api/journals');const body=byId('journalBody');if(body)body.innerHTML=(d.items||[]).map(x=>`<tr><td>${accessEscape(x.journal_date)}</td><td>${accessEscape(x.journal_no)}</td><td>${accessEscape(x.description)}</td><td>${accessEscape(x.source_type)}</td><td>${rup(x.total_debit)}</td><td>${rup(x.total_credit)}</td></tr>`).join('')}catch(e){console.error('jurnal list:',e)}})()
  ]);
  if(accounts.length&&byId('ledgerAccount')?.value)try{await loadLedger()}catch(e){console.error('ledger:',e)}
  return accounts;
}
async function loadLedger(){try{if(!ledgerAccount.value)return;let d=await api('/api/general-ledger?account_id='+encodeURIComponent(ledgerAccount.value)+'&date_from='+encodeURIComponent(ledgerFrom.value||'')+'&date_to='+encodeURIComponent(ledgerTo.value||''));ledgerSummary.innerHTML=`<b>${d.account.code} - ${d.account.name}</b><br>Saldo Awal: ${rup(d.opening_balance)} | Mutasi Debit: ${rup(d.period_debit)} | Mutasi Kredit: ${rup(d.period_credit)} | <b>Saldo Akhir: ${rup(d.ending_balance)}</b>`;ledgerBody.innerHTML=d.items.length?d.items.map(x=>`<tr><td>${x.journal_date}</td><td>${x.journal_no}</td><td>${x.description}${x.memo?' - '+x.memo:''}</td><td>${x.reference_no||'-'}</td><td>${rup(x.debit)}</td><td>${rup(x.credit)}</td><td>${rup(x.running_balance)}</td></tr>`).join(''):'<tr><td colspan="7" class="muted">Tidak ada mutasi pada periode ini.</td></tr>';ledgerUpdated.textContent='Terakhir diperbarui: '+new Date().toLocaleTimeString('id-ID')}catch(e){ledgerUpdated.textContent=e.message}}async function loadTrial(){try{let d=await api('/api/trial-balance?date_from='+encodeURIComponent(trialFrom.value||'')+'&date_to='+encodeURIComponent(trialTo.value||''));trialBody.innerHTML=d.items.map(x=>`<tr><td>${x.code}</td><td>${x.name}</td><td>${rup(x.opening_debit)}</td><td>${rup(x.opening_credit)}</td><td>${rup(x.period_debit)}</td><td>${rup(x.period_credit)}</td><td>${rup(x.ending_debit)}</td><td>${rup(x.ending_credit)}</td></tr>`).join('');trialOD.textContent=rup(d.total_opening_debit);trialOC.textContent=rup(d.total_opening_credit);trialPD.textContent=rup(d.total_period_debit);trialPC.textContent=rup(d.total_period_credit);trialED.textContent=rup(d.total_ending_debit);trialEC.textContent=rup(d.total_ending_credit);trialTotal.textContent=d.balanced?'✓ NERACA SALDO SEIMBANG':'⚠ NERACA SALDO TIDAK SEIMBANG';trialTotal.className=d.balanced?'ok':'error';trialUpdated.textContent='Terakhir diperbarui: '+new Date().toLocaleTimeString('id-ID')}catch(e){trialTotal.textContent=e.message;trialTotal.className='error'}}
async function loadWarehouses(){let d=await api('/api/warehouses?active=1');warehouses=d.items;let options=warehouses.map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');saleWarehouse.innerHTML=options;purchaseWarehouse.innerHTML=options;pWarehouse.innerHTML=options;aWarehouse.innerHTML=options;tSource.innerHTML=options;tTarget.innerHTML=options;balanceWarehouse.innerHTML='<option value="">Semua Gudang</option>'+options;tProduct.innerHTML=products.filter(x=>x.product_type==='STOCK').map(x=>`<option value="${x.id}">${x.sku} - ${x.name}</option>`).join('');try{refreshAdjustmentProductStock()}catch(e){console.error(e)}}
let warehouseMasterItems=[];
async function loadWarehouseMaster(){let d=await api('/api/warehouses');warehouseMasterItems=d.items||[];warehouseBody.innerHTML=warehouseMasterItems.map(x=>`<tr><td>${x.code}</td><td>${x.name}</td><td>${x.address||'-'}</td><td>${x.is_default?'Ya':'Tidak'}</td><td>${x.is_active?'Aktif':'Nonaktif'}</td><td><button class="secondary" onclick="editWarehouse(${x.id})">Edit</button> <button class="danger" onclick="deleteWarehouse(${x.id})">Hapus</button></td></tr>`).join('')||'<tr><td colspan="6">Belum ada gudang.</td></tr>'}
function resetWarehouseForm(){wEditId.value='';wCode.value='';wName.value='';wAddress.value='';wDefault.value='0';wActive.value='1';wSaveBtn.textContent='Simpan Gudang';msg(wMsg,'')}
function editWarehouse(id){const x=warehouseMasterItems.find(v=>v.id===id);if(!x)return;wEditId.value=x.id;wCode.value=x.code;wName.value=x.name;wAddress.value=x.address||'';wDefault.value=x.is_default?'1':'0';wActive.value=x.is_active?'1':'0';wSaveBtn.textContent='Update Gudang';window.scrollTo({top:0,behavior:'smooth'})}
async function saveWarehouse(){try{const id=wEditId.value,payload={code:wCode.value,name:wName.value,address:wAddress.value,is_default:wDefault.value==='1',is_active:wActive.value==='1'};await api(id?'/api/warehouses/'+id:'/api/warehouses',{method:id?'PUT':'POST',body:JSON.stringify(payload)});msg(wMsg,id?'Gudang berhasil diperbarui.':'Gudang berhasil dibuat.');resetWarehouseForm();await Promise.all([loadWarehouses(),loadWarehouseMaster(),loadBalances()])}catch(e){msg(wMsg,e.message,false)}}
async function addWarehouse(){return saveWarehouse()}
async function deleteWarehouse(id){if(!confirm('Hapus/nonaktifkan gudang ini? Gudang yang sudah dipakai transaksi akan dinonaktifkan agar riwayat tetap aman.'))return;try{const d=await api('/api/warehouses/'+id,{method:'DELETE'});msg(wMsg,d.result&&d.result.deactivated?'Gudang sudah dipakai transaksi dan berhasil dinonaktifkan.':'Gudang berhasil dihapus.');await Promise.all([loadWarehouses(),loadWarehouseMaster(),loadBalances()])}catch(e){msg(wMsg,e.message,false)}}
async function loadBalances(){try{let d=await api('/api/inventory-balances?warehouse_id='+encodeURIComponent(balanceWarehouse?.value||'')+'&q='+encodeURIComponent(balanceSearch?.value||''));balanceBody.innerHTML=d.items.map(x=>`<tr><td>${x.warehouse_name}</td><td>${x.sku}</td><td>${x.product_name}</td><td>${x.quantity}</td><td class="cost-sensitive">${rup(x.average_cost)}</td><td class="cost-sensitive">${rup(x.stock_value)}</td></tr>`).join('')}catch(e){}}
async function loadInventoryCard(){try{if(window.cardProduct&&cardProduct.options.length<=1){let p=await api('/api/products?active=1');let current=cardProduct.value;cardProduct.innerHTML='<option value="">Semua barang</option>'+(p.items||[]).filter(x=>x.product_type==='STOCK'&&!x.service_id).map(x=>`<option value="${x.id}">${accessEscape(x.sku)} - ${accessEscape(x.name)}</option>`).join('');cardProduct.value=current}let qs=new URLSearchParams({limit:'200'});if(window.cardProduct&&cardProduct.value)qs.set('product_id',cardProduct.value);let d=await api('/api/inventory-card?'+qs.toString());cardBody.innerHTML=d.items.map(x=>`<tr><td>${x.created_at}</td><td>${x.warehouse_code}</td><td>${x.sku} - ${x.product_name}</td><td>${x.movement_type}</td><td>${x.quantity_change}</td><td>${x.quantity_after}</td><td class="cost-sensitive">${rup(x.average_cost_after)}</td><td>${x.reference_no||''}</td></tr>`).join('')||'<tr><td colspan="8">Tidak ada mutasi untuk barang yang dipilih.</td></tr>'}catch(e){cardBody.innerHTML=`<tr><td colspan="8">${accessEscape(e.message)}</td></tr>`}}
async function transferStock(){try{let payload={product_id:tProduct.value,source_warehouse_id:tSource.value,target_warehouse_id:tTarget.value,quantity:tQty.value,reference_no:tRef.value,reason:tReason.value};let edited=await commitMaintenanceEdit(payload);let d=edited?{result:{}}:await api('/api/inventory-transfers',{method:'POST',body:JSON.stringify(payload)});msg(tMsg,edited?'Transfer berhasil diperbarui.':'Transfer berhasil.');await Promise.all([loadProducts(),loadBalances(),loadInventoryCard(),loadMoves(),loadSummary()]);await openFreshTransactionForm('stockTransfer')}catch(e){msg(tMsg,e.message,false)}}
async function loadMasters(){let c=await api('/api/categories?active=1'),u=await api('/api/units?active=1');window.categoryRecords=c.items;window.unitRecords=u.items;catBody.innerHTML=c.items.map(x=>`<tr><td>${x.code}</td><td>${x.name}</td><td><button onclick="editCategory(${x.id})">Edit</button> <button class="danger" onclick="deleteMaster('/api/categories/${x.id}',loadMasters)">Hapus</button></td></tr>`).join('');unitBody.innerHTML=u.items.map(x=>`<tr><td>${x.code}</td><td>${x.name}</td><td>${x.decimals}</td><td><button onclick="editUnit(${x.id})">Edit</button> <button class="danger" onclick="deleteMaster('/api/units/${x.id}',loadMasters)">Hapus</button></td></tr>`).join('');pCategory.innerHTML='<option value="">Tanpa kategori</option>'+c.items.map(x=>`<option value="${x.id}">${x.name}</option>`).join('');pUnit.innerHTML=u.items.map(x=>`<option value="${x.id}">${x.code}</option>`).join('')}function coaLabel(id){let x=(window.coaItems||[]).find(a=>String(a.id)===String(id));return x?x.code+' - '+x.name:'-'}
let serviceRecords=[];
let serviceCategoryRecords=[];
let serviceMasterUnits=[];
let serviceMasterCoa=[];

function serviceAccountOptions(items,selected=''){
  return '<option value="">Pilih Akun</option>'+items.map(item=>
    `<option value="${item.id}" ${String(item.id)===String(selected)?'selected':''}>${accessEscape(item.code)} - ${accessEscape(item.name)}</option>`
  ).join('');
}
function resetServiceForm(){
  serviceId.value='';serviceCode.value='';serviceName.value='';
  serviceCategory.value='';serviceUnit.value='';
  serviceBuy.value='0';serviceSell.value='0';serviceTax.value='0';
  servicePurchaseAccount.value='';serviceSalesAccount.value='';
  serviceNotes.value='';serviceActive.value='1';
  serviceFormTitle.textContent='Tambah Jasa';
}
function resetServiceCategoryForm(){
  serviceCategoryId.value='';serviceCategoryCode.value='';serviceCategoryName.value='';
  serviceCategoryNotes.value='';serviceCategoryActive.value='1';
  serviceCategoryFormTitle.textContent='Kategori Jasa';
}
async function loadServicesPage(){
  const rs=await Promise.allSettled([api('/api/service-categories'),api('/api/units?active=1'),api('/api/coa?active=1')]);
  serviceCategoryRecords=rs[0].status==='fulfilled'?(rs[0].value.items||[]):[];
  serviceMasterUnits=rs[1].status==='fulfilled'?(rs[1].value.items||[]):[];
  serviceMasterCoa=rs[2].status==='fulfilled'?(rs[2].value.items||[]):[];
  const cat=byId('serviceCategory'),fil=byId('serviceCategoryFilter'),unit=byId('serviceUnit');
  if(cat)cat.innerHTML='<option value="">Tanpa Kategori</option>'+serviceCategoryRecords.filter(x=>x.is_active!==false).map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');
  if(fil)fil.innerHTML='<option value="">Semua Kategori</option>'+serviceCategoryRecords.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');
  if(unit)unit.innerHTML='<option value="">Tanpa Satuan (opsional)</option>'+serviceMasterUnits.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');
  const subtype=x=>x.display_type||x.account_subtype||x.account_type;
  const pa=byId('servicePurchaseAccount'),sa=byId('serviceSalesAccount');
  if(pa)pa.innerHTML=serviceAccountOptions(serviceMasterCoa.filter(x=>x.account_type==='EXPENSE'||x.account_type==='ASSET'||['HPP','OPERATING_EXPENSE'].includes(subtype(x))));
  if(sa)sa.innerHTML=serviceAccountOptions(serviceMasterCoa.filter(x=>x.account_type==='REVENUE'||x.account_type==='ASSET'||subtype(x)==='REVENUE'));
  renderServiceCategories();await loadServices();
}
function renderServiceCategories(){
  const body=byId('serviceCategoryBody');if(!body)return;
  body.innerHTML=serviceCategoryRecords.length?serviceCategoryRecords.map(x=>`<tr><td><b>${accessEscape(x.code)}</b></td><td>${accessEscape(x.name)}</td><td>${x.is_active?'Aktif':'Nonaktif'}</td><td><button onclick="editServiceCategory(${x.id})">Edit</button> <button class="danger" onclick="deleteServiceCategory(${x.id})">Hapus</button></td></tr>`).join(''):'<tr><td colspan="4">Belum ada kategori jasa.</td></tr>';
}
async function loadServices(){
  const p=new URLSearchParams({q:byId('serviceSearch')?.value||''});const f=byId('serviceCategoryFilter');if(f?.value)p.set('category_id',f.value);
  const data=await api('/api/services?'+p.toString());serviceRecords=data.items||[];
  const count=byId('serviceCount');if(count)count.textContent=serviceRecords.length+' jasa';
  const body=byId('serviceBody');if(body)body.innerHTML=serviceRecords.length?serviceRecords.map(x=>`<tr><td><b>${accessEscape(x.service_code)}</b></td><td>${accessEscape(x.service_name)}</td><td>${accessEscape(x.category_name||'-')}</td><td>${accessEscape(x.unit_code||'-')}</td><td>${rup(Number(x.purchase_price||0))}</td><td>${rup(Number(x.selling_price||0))}</td><td>${Number(x.tax_percent||0).toFixed(2)}%</td><td>${accessEscape(x.purchase_account_code||'-')} - ${accessEscape(x.purchase_account_name||'-')}</td><td>${accessEscape(x.sales_account_code||'-')} - ${accessEscape(x.sales_account_name||'-')}</td><td>${x.is_active?'Aktif':'Nonaktif'}</td><td><button onclick="editService(${x.id})">Edit</button> <button class="danger" onclick="deleteService(${x.id})">Hapus</button></td></tr>`).join(''):'<tr><td colspan="11">Belum ada jasa sesuai filter.</td></tr>';
  return serviceRecords;
}
function editService(id){
  const x=serviceRecords.find(r=>r.id===id);if(!x)return;const set=(id,v)=>{const el=byId(id);if(el)el.value=v??''};
  set('serviceId',x.id);set('serviceCode',x.service_code);set('serviceName',x.service_name);set('serviceCategory',x.category_id||'');set('serviceUnit',x.unit_id||'');set('serviceBuy',x.purchase_price||0);set('serviceSell',x.selling_price||0);set('serviceTax',x.tax_percent||0);set('servicePurchaseAccount',x.purchase_account_id||'');set('serviceSalesAccount',x.sales_account_id||'');set('serviceNotes',x.notes||'');set('serviceActive',x.is_active?'1':'0');const t=byId('serviceFormTitle');if(t)t.textContent='Edit Jasa: '+x.service_name;
}
async function saveService(){
  try{
    const payload={
      service_code:serviceCode.value,service_name:serviceName.value,
      category_id:serviceCategory.value||null,unit_id:serviceUnit.value||null,
      purchase_price:serviceBuy.value,selling_price:serviceSell.value,
      tax_percent:serviceTax.value,purchase_account_id:servicePurchaseAccount.value,
      sales_account_id:serviceSalesAccount.value,notes:serviceNotes.value,
      is_active:serviceActive.value==='1'
    };
    if(!payload.service_code.trim()||!payload.service_name.trim())throw Error('Kode dan nama jasa wajib diisi.');
    if(!payload.unit_id)throw Error('Satuan jasa wajib dipilih.');
    if(!payload.purchase_account_id)throw Error('Akun Pembelian Jasa wajib dipilih.');
    if(!payload.sales_account_id)throw Error('Akun Penjualan Jasa wajib dipilih.');
    const id=serviceId.value;
    await api(id?'/api/services/'+id:'/api/services',{
      method:id?'PUT':'POST',body:JSON.stringify(payload)
    });
    msg(serviceMsg,id?'Jasa berhasil diperbarui.':'Jasa berhasil dibuat.');
    resetServiceForm();await Promise.all([loadServices(),loadProducts()]);
  }catch(error){msg(serviceMsg,error.message,false)}
}
async function deleteService(id){
  const item=serviceRecords.find(row=>row.id===id);if(!item)return;
  if(!confirm(`Hapus jasa ${item.service_name}?`))return;
  try{
    await api('/api/services/'+id,{method:'DELETE'});
    msg(serviceMsg,'Jasa berhasil dihapus.');resetServiceForm();await Promise.all([loadServices(),loadProducts()]);
  }catch(error){msg(serviceMsg,error.message,false)}
}
function editServiceCategory(id){
  const item=serviceCategoryRecords.find(row=>row.id===id);if(!item)return;
  serviceCategoryId.value=item.id;serviceCategoryCode.value=item.code;
  serviceCategoryName.value=item.name;serviceCategoryNotes.value=item.notes||'';
  serviceCategoryActive.value=item.is_active?'1':'0';
  serviceCategoryFormTitle.textContent='Edit Kategori: '+item.name;
}
async function saveServiceCategory(){
  try{
    const payload={code:serviceCategoryCode.value,name:serviceCategoryName.value,
      notes:serviceCategoryNotes.value,is_active:serviceCategoryActive.value==='1'};
    if(!payload.code.trim()||!payload.name.trim())throw Error('Kode dan nama kategori wajib diisi.');
    const id=serviceCategoryId.value;
    await api(id?'/api/service-categories/'+id:'/api/service-categories',{
      method:id?'PUT':'POST',body:JSON.stringify(payload)
    });
    msg(serviceMsg,id?'Kategori jasa berhasil diperbarui.':'Kategori jasa berhasil dibuat.');
    resetServiceCategoryForm();await loadServicesPage();
  }catch(error){msg(serviceMsg,error.message,false)}
}
async function deleteServiceCategory(id){
  const item=serviceCategoryRecords.find(row=>row.id===id);if(!item)return;
  if(!confirm(`Hapus kategori ${item.name}?`))return;
  try{
    await api('/api/service-categories/'+id,{method:'DELETE'});
    msg(serviceMsg,'Kategori jasa berhasil dihapus.');resetServiceCategoryForm();
    await loadServicesPage();
  }catch(error){msg(serviceMsg,error.message,false)}
}


const PRODUCT_BUSINESS_TEMPLATES={
 retail:[['RTL001','Air Mineral','PCS'],['RTL002','Mi Instan','PCS'],['RTL003','Gula Pasir','KG'],['RTL004','Minyak Goreng','LTR'],['RTL005','Beras','KG'],['RTL006','Kopi Sachet','PCS'],['RTL007','Teh Celup','BOX'],['RTL008','Susu UHT','PCS'],['RTL009','Sabun Mandi','PCS'],['RTL010','Deterjen','PCS']],
 workshop:[['BGL001','Oli Mesin','LTR'],['BGL002','Kampas Rem','SET'],['BGL003','Busi','PCS'],['BGL004','Filter Oli','PCS'],['BGL005','Filter Udara','PCS'],['BGL006','Ban','PCS'],['BGL007','Aki','PCS'],['BGL008','Minyak Rem','LTR'],['BGL009','Coolant Radiator','LTR'],['BGL010','Bearing','PCS']],
 pharmacy:[['APT001','Paracetamol','STRIP'],['APT002','Vitamin C','BOTOL'],['APT003','Antasida','STRIP'],['APT004','Oralit','SACHET'],['APT005','Masker Medis','BOX'],['APT006','Alkohol 70%','BOTOL'],['APT007','Kasa Steril','PCS'],['APT008','Plester Luka','BOX'],['APT009','Sarung Tangan Medis','BOX'],['APT010','Termometer Digital','PCS']],
 restaurant:[['RST001','Beras','KG'],['RST002','Minyak Goreng','LTR'],['RST003','Gula Pasir','KG'],['RST004','Telur','PCS'],['RST005','Tepung Terigu','KG'],['RST006','Ayam','KG'],['RST007','Daging Sapi','KG'],['RST008','Kopi','KG'],['RST009','Teh','BOX'],['RST010','Air Mineral','PCS']],
 construction:[['KTR001','Semen Portland 50 Kg','ZAK'],['KTR002','Besi Beton 10 mm','BATANG'],['KTR003','Besi Beton 12 mm','BATANG'],['KTR004','Pasir Beton','M3'],['KTR005','Batu Split','M3'],['KTR006','Bata Ringan','PCS'],['KTR007','Keramik Lantai','M2'],['KTR008','Cat Tembok','PAIL'],['KTR009','Pipa PVC','BATANG'],['KTR010','Kawat Bendrat','KG']],
 interior:[['INT001','Gypsum Board','LEMBAR'],['INT002','Hollow Galvanis','BATANG'],['INT003','Cat Interior','PAIL'],['INT004','Multiplek','LEMBAR'],['INT005','HPL','LEMBAR'],['INT006','Lem Kayu','KG'],['INT007','Sekrup Gypsum','BOX'],['INT008','Vinyl Flooring','M2'],['INT009','Lampu LED','PCS'],['INT010','Kabel Listrik','ROLL']],
 mep:[['MEP001','Kabel NYM','ROLL'],['MEP002','Kabel NYA','ROLL'],['MEP003','MCB','PCS'],['MEP004','Pipa Conduit','BATANG'],['MEP005','Pipa PVC','BATANG'],['MEP006','Elbow PVC','PCS'],['MEP007','Stop Kontak','PCS'],['MEP008','Saklar','PCS'],['MEP009','Lampu LED','PCS'],['MEP010','Pompa Air','UNIT']],
 school:[['SKL001','Kertas A4','RIM'],['SKL002','Tinta Printer','BOTOL'],['SKL003','Spidol Whiteboard','PCS'],['SKL004','Buku Tulis','PCS'],['SKL005','Pulpen','PCS'],['SKL006','Pensil','PCS'],['SKL007','Penghapus','PCS'],['SKL008','Map Dokumen','PCS'],['SKL009','Toner Printer','PCS'],['SKL010','Kertas Fotokopi F4','RIM']],
 plantation:[['PKB001','Pupuk NPK','ZAK'],['PKB002','Pupuk Urea','ZAK'],['PKB003','Herbisida','LTR'],['PKB004','Fungisida','LTR'],['PKB005','Insektisida','LTR'],['PKB006','Bibit Tanaman','PCS'],['PKB007','Solar','LTR'],['PKB008','Oli Mesin','LTR'],['PKB009','Karung','PCS'],['PKB010','Sarung Tangan Kerja','PASANG']],
 distributor:[['DST001','Karton Packing','PCS'],['DST002','Lakban Packing','ROLL'],['DST003','Plastik Packing','PACK'],['DST004','Label Pengiriman','ROLL'],['DST005','Pallet','PCS'],['DST006','Stretch Film','ROLL'],['DST007','Bubble Wrap','ROLL'],['DST008','Tali Strapping','ROLL'],['DST009','Karung','PCS'],['DST010','Segel Plastik','PCS']],
 manufacturing:[['PBR001','Bahan Baku Utama','KG'],['PBR002','Bahan Penolong','KG'],['PBR003','Kemasan Produk','PCS'],['PBR004','Karton Produk','PCS'],['PBR005','Label Produk','PCS'],['PBR006','Plastik Kemasan','ROLL'],['PBR007','Pelumas Mesin','LTR'],['PBR008','Sarung Tangan Produksi','PASANG'],['PBR009','Masker Produksi','BOX'],['PBR010','Bahan Pembersih','LTR']],
 services:[['JSA001','Kertas A4','RIM'],['JSA002','Tinta Printer','BOTOL'],['JSA003','ATK Umum','SET'],['JSA004','Materai','PCS'],['JSA005','Map Dokumen','PCS'],['JSA006','Air Mineral','PCS'],['JSA007','Tisu','BOX'],['JSA008','Kabel Data','PCS'],['JSA009','Flashdisk','PCS'],['JSA010','Baterai','PCS']]
};
function currentProductRecommendations(){return PRODUCT_BUSINESS_TEMPLATES[productBusinessTemplate?.value]||[]}
function recommendationUnitId(code){const units=window.unitRecords||[];let u=units.find(x=>String(x.code||'').toUpperCase()===String(code||'').toUpperCase());return u?.id||pUnit?.value||units[0]?.id||''}
function renderProductRecommendations(){const list=currentProductRecommendations(),existing=new Set((products||[]).map(x=>String(x.sku||'').toUpperCase()));if(!productRecommendationList)return;productRecommendationInfo.textContent=list.length?`${list.length} rekomendasi. Barang dengan SKU yang sudah ada akan dilewati saat penambahan massal.`:'Pilih jenis usaha untuk melihat rekomendasi.';productRecommendationList.innerHTML=list.map((x,i)=>{const exists=existing.has(String(x[0]).toUpperCase());return `<div class="product-recommendation-item"><input class="product-rec-check" type="checkbox" data-index="${i}" ${exists?'disabled':'checked'}><div><b>${accessEscape(x[0])} · ${accessEscape(x[1])}</b><small>Satuan rekomendasi: ${accessEscape(x[2])}${exists?' · Sudah ada di master':''}</small></div><div class="product-recommendation-actions"><button type="button" class="secondary" onclick="useProductRecommendation(${i})">Gunakan</button></div></div>`}).join('')}
function selectAllProductRecommendations(flag){document.querySelectorAll('.product-rec-check:not(:disabled)').forEach(x=>x.checked=!!flag)}
function useProductRecommendation(index){const x=currentProductRecommendations()[index];if(!x)return;pSku.value=x[0];pName.value=x[1];const uid=recommendationUnitId(x[2]);if(uid)pUnit.value=uid;pType.value='STOCK';pBuy.value=0;pSell.value=0;pInitial.value=0;pMinimum.value=0;productEditId.value='';window.scrollTo({top:document.getElementById('products').offsetTop,behavior:'smooth'});msg(pMsg,`Rekomendasi ${x[1]} dimuat ke form. Silakan lengkapi lalu simpan.`)}
async function addSelectedProductRecommendations(){try{const selected=[...document.querySelectorAll('.product-rec-check:checked')].map(x=>Number(x.dataset.index)),list=currentProductRecommendations();if(!selected.length)throw Error('Pilih minimal satu rekomendasi barang.');if(!pInventoryAccount.value||!pSalesAccount.value||!pCogsAccount.value)throw Error('Pilih Akun Persediaan, Akun Penjualan, dan Akun HPP terlebih dahulu pada Setting Akun Barang.');let created=0,skipped=0,errors=[];const existing=new Set((products||[]).map(x=>String(x.sku||'').toUpperCase()));for(const idx of selected){const x=list[idx];if(!x)continue;if(existing.has(String(x[0]).toUpperCase())){skipped++;continue}const uid=recommendationUnitId(x[2]);if(!uid){errors.push(`${x[0]}: belum ada satuan master yang dapat digunakan`);continue}try{await api('/api/products',{method:'POST',body:JSON.stringify({sku:x[0],name:x[1],unit_id:uid,product_type:'STOCK',purchase_price:0,selling_price:0,initial_stock:0,minimum_stock:0,inventory_account_id:pInventoryAccount.value,sales_account_id:pSalesAccount.value,cogs_account_id:pCogsAccount.value})});created++;existing.add(String(x[0]).toUpperCase())}catch(e){errors.push(`${x[0]}: ${e.message}`)}}await loadProducts();renderProductRecommendations();let text=`${created} barang rekomendasi berhasil ditambahkan.`+(skipped?` ${skipped} dilewati karena sudah ada.`:'');if(errors.length)text+=` Gagal: ${errors.slice(0,3).join('; ')}`;msg(pMsg,text,!errors.length)}catch(e){msg(pMsg,e.message,false)}}

function renderProductTableRows(){
  const stockUnitCell=(x,index)=>{const u=(x.stock_units||[])[index];if(!u)return '<td class="stock-unit-empty">—</td>';const qty=new Intl.NumberFormat('id-ID',{maximumFractionDigits:Math.max(0,Math.min(4,Number(u.decimals||0)))}).format(Number(u.quantity||0));return `<td class="stock-unit-cell"><strong>${qty} ${accessEscape(u.unit_code||'')}</strong><small>${u.is_base?'Satuan dasar':'Konversi '+Number(u.conversion_ratio||1)}</small></td>`};
  const body=byId('productBody');if(body)body.innerHTML=products.length?products.map(x=>`<tr><td>${accessEscape(x.sku)}</td><td>${accessEscape(x.name)}</td><td>${accessEscape(x.product_type)}</td><td>${accessEscape(x.brand_name||'-')}</td>${stockUnitCell(x,0)}${stockUnitCell(x,1)}${stockUnitCell(x,2)}<td>${rup(x.selling_price)}</td><td>${accessEscape(x.inventory_account_name||coaLabel(x.inventory_account_id))}</td><td>${accessEscape(x.sales_account_name||coaLabel(x.sales_account_id))}</td><td>${accessEscape(x.cogs_account_name||coaLabel(x.cogs_account_id))}</td><td><button onclick="editProduct(${x.id})">Edit</button> <button class="danger" onclick="deleteProduct(${x.id})">Hapus</button></td></tr>`).join(''):'<tr><td colspan="12" class="muted">Belum ada barang sesuai pencarian.</td></tr>';
}
function filterProductTable(){
  const search=String(byId('productSearch')?.value||'').trim().toLowerCase();
  const all=window.allProductMasterRows||[];
  products=search?all.filter(x=>[x.sku,x.name,x.barcode,x.brand_name,x.category_name].some(v=>String(v||'').toLowerCase().includes(search))):all.slice();
  renderProductTableRows();
  return products;
}
async function loadProducts(){
  const [a,b]=await Promise.allSettled([api('/api/products'),api('/api/products?active=1')]);
  if(a.status==='rejected'&&b.status==='rejected')throw a.reason;
  const table=a.status==='fulfilled'?a.value:{items:[]},tx=b.status==='fulfilled'?b.value:table;
  window.allProductMasterRows=(table.items||[]).filter(x=>!x.service_id);
  transactionProducts=(tx.items||[]).filter(x=>x.is_active&&(true));
  filterProductTable();
  const adjustment=byId('aProduct'),stock=transactionProducts.filter(x=>x.product_type==='STOCK');
  if(adjustment){const old=adjustment.value;refreshAdjustmentProductStock(old);adjustment.disabled=!stock.length}
  try{refreshSaleProductOptions()}catch(e){console.error(e)}try{refreshPurchaseProducts()}catch(e){console.error(e)}
  if(byId('productBusinessTemplate')&&typeof renderProductRecommendations==='function')try{renderProductRecommendations()}catch(e){console.error(e)}
  const transfer=byId('tProduct');if(transfer&&Array.isArray(warehouses)&&warehouses.length)transfer.innerHTML=stock.map(x=>`<option value="${x.id}">${accessEscape(x.sku)} - ${accessEscape(x.name)}</option>`).join('');
  return products;
}

async function loadPartners(){
  const selectedCustomer=saleCustomer?.value||'';
  const selectedSupplier=purchaseSupplier?.value||'';
  const [tableData,customerData,supplierData,priceLevelData]=await Promise.all([
    api('/api/partners?q='+encodeURIComponent(partnerSearch?.value||'')+'&type='+encodeURIComponent(partnerFilter?.value||'')),
    api('/api/customers?active=1'),
    api('/api/suppliers?active=1'),
    api('/api/price-levels?active=1')
  ]);
  partners=tableData.items;
  partnerBody.innerHTML=partners.length?partners.map(x=>`<tr><td>${x.code}</td><td>${x.name}</td><td>${x.partner_type}</td><td>${x.phone||''}</td><td>${x.city||''}</td><td>${x.payment_term_days} hari</td><td><button onclick="editPartner(${x.id})">Edit</button> <button class="danger" onclick="deleteMaster('/api/partners/${x.id}',loadPartners)">Hapus</button></td></tr>`).join(''):'<tr><td colspan="7" class="muted">Belum ada data sesuai filter.</td></tr>';
  priceLevels=priceLevelData.items||[];renderPriceLevelSelectors();
  const customers=customerData.items.filter(x=>x.is_active);window.transactionCustomers=customers;
  const suppliers=supplierData.items.filter(x=>x.is_active);
  saleCustomer.innerHTML='<option value="">Umum / Tanpa pelanggan</option>'+customers.map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');
  purchaseSupplier.innerHTML=suppliers.length?suppliers.map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join(''):'<option value="" disabled selected>Belum ada data pemasok</option>';
  if([...saleCustomer.options].some(o=>o.value===selectedCustomer))saleCustomer.value=selectedCustomer;
  if([...purchaseSupplier.options].some(o=>o.value===selectedSupplier))purchaseSupplier.value=selectedSupplier;
  purchaseSupplier.disabled=!suppliers.length;
}async function loadTransactionPartners(){
  try{
    const [customerData,supplierData]=await Promise.all([api('/api/customers?active=1'),api('/api/suppliers?active=1')]);
    const customers=(customerData.items||[]).filter(x=>x.is_active!==false),suppliers=(supplierData.items||[]).filter(x=>x.is_active!==false);
    window.transactionCustomers=customers;
    const saleEl=document.getElementById('saleCustomer'),purchaseEl=document.getElementById('purchaseSupplier');
    const saleSelected=saleEl?.value||'',purchaseSelected=purchaseEl?.value||'';
    if(saleEl){saleEl.innerHTML='<option value="">Umum / Tanpa pelanggan</option>'+customers.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');if([...saleEl.options].some(o=>o.value===saleSelected))saleEl.value=saleSelected}
    if(purchaseEl){purchaseEl.innerHTML=suppliers.length?suppliers.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join(''):'<option value="" disabled selected>Belum ada data pemasok</option>';if([...purchaseEl.options].some(o=>o.value===purchaseSelected))purchaseEl.value=purchaseSelected;purchaseEl.disabled=!suppliers.length}
    return {customers,suppliers}
  }catch(e){console.error('Gagal memuat pelanggan/pemasok transaksi:',e);return {customers:[],suppliers:[]}}
}
function warehouseQty(p,wid){let x=(p?.warehouse_stocks||[]).find(v=>String(v.warehouse_id)===String(wid));return Number(x?.quantity||0)} function refreshAdjustmentProductStock(selected){const sel=byId('aProduct');if(!sel)return;const keep=selected!==undefined?String(selected||''):String(sel.value||'');const wid=byId('aWarehouse')?.value||'';const stock=(transactionProducts||[]).filter(x=>x.product_type==='STOCK'&&x.is_active);sel.innerHTML=stock.length?'<option value="">-- Pilih Barang Stok --</option>'+stock.map(x=>`<option value="${x.id}">${accessEscape(x.sku)} - ${accessEscape(x.name)} | stok gudang ${warehouseQty(x,wid)}</option>`).join(''):'<option value="">Belum ada barang stok aktif</option>';if(stock.some(x=>String(x.id)===keep))sel.value=keep;sel.disabled=!stock.length} function productOptions(selected=''){return transactionProducts.filter(x=>x.is_active).map(x=>`<option value="${x.id}" ${String(x.id)===String(selected)?'selected':''}>${x.service_id?'[JASA] '+x.name:'[BARANG] '+x.sku+' - '+x.name+(x.product_type==='STOCK'?' | stok gudang '+warehouseQty(x,saleWarehouse?.value):'')}</option>`).join('')}function renumberSaleLines(){document.querySelectorAll('.sale-line').forEach((r,i)=>{let n=r.querySelector('.line-no');if(n)n.textContent=i+1})}function removeSaleLine(button){let row=button.closest('.sale-line');if(row)row.remove();renumberSaleLines();estimateSale()}function addSaleLine(){let d=document.createElement('div');d.className='sale-line';d.innerHTML=`<span class="line-no"></span><div class="sale-product-picker sale-mobile-field product-field"><span class="sale-mobile-label">Barang / Jasa</span><select class="slProduct" aria-label="Barang atau jasa; ketik untuk mencari" onchange="lineProduct(this)">${productOptions()}</select></div><label class="sale-mobile-field unit-field"><span class="sale-mobile-label">Satuan</span><select class="slUnit" aria-label="Satuan" onchange="lineUnit(this);estimateSale()"></select></label><label class="sale-mobile-field desc-field"><span class="sale-mobile-label">Deskripsi</span><input class="slDescription" type="text" maxlength="255" placeholder="Opsional"></label><label class="sale-mobile-field qty-field"><span class="sale-mobile-label">Qty</span><input class="slQty" type="number" inputmode="decimal" min="0.0001" step="0.0001" value="1" aria-label="Qty" oninput="estimateSale()" onchange="estimateSale()"></label><label class="sale-mobile-field price-field"><span class="sale-mobile-label">Harga</span><input class="slPrice" type="number" inputmode="decimal" min="0" value="0" aria-label="Harga jual" oninput="estimateSale()"></label><div class="discount-combo sale-mobile-field discount-field"><span class="sale-mobile-label">Diskon</span><select class="slDiscountMode" aria-label="Jenis diskon" onchange="estimateSale()"><option value="AMOUNT">Nominal</option><option value="PERCENT">Persen</option></select><input class="slDiscount" type="number" inputmode="decimal" min="0" value="0" aria-label="Nilai diskon" oninput="estimateSale()"></div><div class="sale-mobile-field subtotal-field"><span class="sale-mobile-label">Subtotal</span><span class="line-subtotal">Rp0</span></div><button type="button" class="danger icon-delete" title="Hapus baris" aria-label="Hapus baris" onclick="removeSaleLine(this)">×</button>`;saleLines.appendChild(d);renumberSaleLines();lineProduct(d.querySelector('.slProduct'));let first=d.querySelector('.slProduct');if(first)first.focus()}function filterSaleProduct(input){let row=input.closest('.sale-line'),sel=row?.querySelector('.slProduct');if(!sel)return;let old=sel.value,q=String(input.value||'').trim().toLowerCase();let list=transactionProducts.filter(p=>!q||[p.sku,p.name,p.barcode,p.brand_name].some(v=>String(v||'').toLowerCase().includes(q)));sel.innerHTML=list.map(p=>`<option value="${p.id}" ${String(p.id)===String(old)?'selected':''}>${accessEscape((p.sku||'')+' - '+p.name)}</option>`).join('');if(!sel.value&&sel.options.length)sel.selectedIndex=0;lineProduct(sel)}
function refreshSaleProductOptions(){document.querySelectorAll('.slProduct').forEach(s=>{let v=s.value;s.innerHTML=productOptions(v);if(!s.value&&s.options.length)s.selectedIndex=0;lineProduct(s)})}function lineProduct(s){if(!s)return;let row=s.closest('.sale-line')||s.parentElement;if(!row)return;let p=transactionProducts.find(x=>String(x.id)===String(s.value));if(p){let us=row.querySelector('.slUnit'),price=row.querySelector('.slPrice'),description=row.querySelector('.slDescription'),list=productUnits(p);if(us){let oldUnit=us.value;us.innerHTML=list.map(u=>`<option value="${u.unit_id}">${u.unit_code}</option>`).join('');if([...us.options].some(o=>o.value===oldUnit))us.value=oldUnit;let level=customerPriceLevelId(),custom=level&&p.price_levels?p.price_levels[String(level)]:null,u=list.find(x=>String(x.unit_id)===String(us.value))||list[0];if(price)price.value=(custom&&Number(custom)>0&&u?.is_base)?custom:(u?.selling_price||p.selling_price||0)}if(description)description.placeholder='Default: '+p.name}estimateSale()}function lineUnit(sel){if(!sel)return;let r=sel.closest('.sale-line');if(!r)return;let productSelect=r.querySelector('.slProduct'),price=r.querySelector('.slPrice');if(!productSelect||!price)return;let p=transactionProducts.find(x=>String(x.id)===String(productSelect.value)),u=productUnits(p).find(x=>String(x.unit_id)===String(sel.value));if(u)price.value=u.selling_price||0}function lineDiscount(gross,mode,value){return mode==='PERCENT'?gross*(value||0)/100:(value||0)}function numericValue(v){let s=String(v??'').trim().replace(/\s/g,'');if(s.includes(',')&&!s.includes('.'))s=s.replace(',','.');let n=Number(s);return Number.isFinite(n)?n:0}function estimateSale(){let subtotal=0;document.querySelectorAll('.sale-line').forEach(r=>{let gross=numericValue(r.querySelector('.slQty').value)*numericValue(r.querySelector('.slPrice').value),net=Math.max(0,gross-lineDiscount(gross,r.querySelector('.slDiscountMode').value,numericValue(r.querySelector('.slDiscount').value)));subtotal+=net;let out=r.querySelector('.line-subtotal');if(out)out.textContent='Rp'+rup(net)});let hd=lineDiscount(subtotal,saleDiscountMode.value,numericValue(saleDiscount.value));let tax=Math.max(0,subtotal-hd)*(numericValue(saleTax.value))/100;let total=Math.max(0,subtotal-hd+tax);saleEstimate.textContent=rup(total);if(salePayment.value!=='CREDIT')salePaid.value=total}function paymentChanged(){estimateSale()}

if(!window.__transactionGridKeyboard){window.__transactionGridKeyboard=true;document.addEventListener('keydown',e=>{if(e.ctrlKey&&e.key==='Enter'&&document.getElementById('sales')?.classList.contains('active')){e.preventDefault();addSaleLine()}if(e.ctrlKey&&e.key==='Enter'&&document.getElementById('purchases')?.classList.contains('active')){e.preventDefault();addPurchaseLine()}})}

let saleInvoiceMaterialRows=[];
function renderSaleInvoiceMaterials(){if(!window.saleInvoiceMaterials)return;if(!saleInvoiceMaterialRows.length){saleInvoiceMaterials.innerHTML='<span class="muted">Belum ada material yang dipilih.</span>';return}saleInvoiceMaterials.innerHTML='<div class="invoice-material-row head"><span>Pilih</span><span>Tanggal</span><span>Dokumen</span><span>Material</span><span>Qty</span><span>Sat.</span><span>Nilai Cost</span></div>'+saleInvoiceMaterialRows.map((x,i)=>`<div class="invoice-material-row"><input type="checkbox" ${x.selected?'checked':''} onchange="saleInvoiceMaterialRows[${i}].selected=this.checked"><span>${accessEscape(x.issue_date||'-')}</span><span>${accessEscape(x.issue_no||'-')}</span><span>${accessEscape((x.sku?x.sku+' - ':'')+(x.material_name||''))}</span><input type="number" step="any" value="${x.qty||0}" onchange="saleInvoiceMaterialRows[${i}].qty=Number(this.value||0);saleInvoiceMaterialRows[${i}].total_cost=saleInvoiceMaterialRows[${i}].qty*saleInvoiceMaterialRows[${i}].unit_cost"><span>${accessEscape(x.unit_code||'')}</span><span>${rup(x.total_cost||0)}</span></div>`).join('')}
async function loadSaleInvoiceMaterials(){try{if(!saleProject.value)throw Error('Pilih proyek terlebih dahulu.');const d=await api('/api/project-material-issues?project_id='+encodeURIComponent(saleProject.value));const rows=[];for(const issue of (d.items||[]))for(const it of (issue.items||[]))rows.push({selected:true,project_material_issue_id:issue.id,product_id:it.product_id||null,sku:it.sku||'',material_name:it.product_name||it.name||'',qty:Number(it.qty||0),unit_code:it.unit_code||'',unit_cost:Number(it.average_cost||it.unit_cost||0),total_cost:Number(it.total_cost||0),issue_date:issue.issue_date||'',issue_no:issue.issue_no||''});saleInvoiceMaterialRows=rows;renderSaleInvoiceMaterials();if(!rows.length)msg(saleMsg,'Belum ada pengeluaran material untuk proyek ini.',false)}catch(e){msg(saleMsg,e.message,false)}}
function selectedSaleInvoiceMaterials(){return saleInvoiceMaterialRows.filter(x=>x.selected).map(({selected,...x})=>x)}
if(window.saleCustomer)saleCustomer.addEventListener('change',()=>document.querySelectorAll('.slProduct').forEach(lineProduct));async function saveSale(){try{if(!transactionProducts.length)throw new Error('Belum ada barang / jasa aktif.');if(salePayment.value!=='CREDIT'&&!saleCashAccount.value)throw new Error('Akun kas / bank wajib dipilih untuk penjualan tunai atau transfer.');let items=[...document.querySelectorAll('.sale-line')].map((r,i)=>{let qty=numericValue(r.querySelector('.slQty').value);if(qty<=0)throw new Error('Qty baris '+(i+1)+' harus lebih dari nol.');return {product_id:r.querySelector('.slProduct').value,unit_id:r.querySelector('.slUnit').value,description:r.querySelector('.slDescription').value,qty:r.querySelector('.slQty').value,unit_price:r.querySelector('.slPrice').value,discount_mode:r.querySelector('.slDiscountMode').value,discount_value:r.querySelector('.slDiscount').value}});let edit=window.__documentEdit&&window.__documentEdit.kind==='sale'?window.__documentEdit:null;let d=await api(edit?'/api/sales/'+edit.id:'/api/sales',{method:edit?'PUT':'POST',body:JSON.stringify({invoice_no:saleInvoiceNo.value,delivery_no:saleDeliveryNo.value,sale_date:saleDate.value,warehouse_id:saleWarehouse.value,customer_id:saleCustomer.value,salesperson_id:saleSalesperson.value,department_id:saleDepartment.value||null,project_id:saleProject.value||null,payment_method:salePayment.value,cash_account_id:saleCashAccount.value,payment_term_days:saleTerm.value,due_date:saleDue.value,tax_percent:saleTax.value,discount_mode:saleDiscountMode.value,discount_value:saleDiscount.value,paid_amount:salePaid.value,notes:saleNotes.value,sales_order_id:window.__sourceSalesOrderId||null,invoice_materials:selectedSaleInvoiceMaterials(),items})});window.__documentEdit=null;msg(saleMsg,(edit?'Penjualan diperbarui: ':'Penjualan ')+d.result.invoice_no+' berhasil. Total '+rup(d.result.total_amount));saleLines.innerHTML='';addSaleLine();window.__sourceSalesOrderId=null;saleDiscount.value=saleTax.value=salePaid.value=0;saleNotes.value='';saleInvoiceMaterialRows=[];renderSaleInvoiceMaterials();saleInvoiceNo.dataset.edited='';saleDeliveryNo.dataset.edited='';resetTransactionDimensions('sale');await loadDocumentNumbers();await Promise.all([loadProducts(),loadSales(),loadCashAccounts(),loadSummary(),loadMoves(),loadBalances(),loadInventoryCard()]);await loadTransactionPartners();await openFreshTransactionForm('sale')}catch(e){msg(saleMsg,e.message,false)}}async function loadSales(){let d=await api('/api/sales?q='+encodeURIComponent(saleSearch?.value||''));salesBody.innerHTML=d.items.map(x=>`<tr><td>${x.sale_date}</td><td>${x.invoice_no}</td><td>${x.customer_name||'Umum'}</td><td>${x.salesperson_name||'-'}</td><td>${x.payment_method}</td><td>${x.due_date||'-'}</td><td>${rup(x.tax_amount)}</td><td>${rup(x.total_amount)}</td><td>${rup(x.balance_due)}</td><td><button onclick="editSale(${x.id})">Edit</button> <button class="danger" onclick="voidSale(${x.id})">Hapus</button></td><td><button onclick="openPrint('sales-invoice',${x.id})">Nota</button><button onclick="openPrint('delivery-order',${x.id})">Surat Jalan</button></td></tr>`).join('')}async function addProduct(){try{
if(!pInventoryAccount.value)throw Error('Pilih Akun Persediaan pada Master Barang.');
if(!pSalesAccount.value)throw Error('Pilih Akun Penjualan pada Master Barang.');
if(!pCogsAccount.value)throw Error('Pilih Akun HPP pada Master Barang.');
let wasEdit=Boolean(productEditId.value);await api(productEditId.value?'/api/products/'+productEditId.value:'/api/products',{method:productEditId.value?'PUT':'POST',body:JSON.stringify({sku:pSku.value,barcode:pBarcode.value,name:pName.value,category_id:pCategory.value,brand_id:pBrand.value,unit_id:pUnit.value,product_type:pType.value,purchase_price:pBuy.value,selling_price:pSell.value,warehouse_id:pWarehouse.value,initial_stock:pInitial.value,opening_balance_date:pOpeningDate.value,minimum_stock:pMinimum.value,inventory_account_id:pInventoryAccount.value,sales_account_id:pSalesAccount.value,cogs_account_id:pCogsAccount.value,price_levels:collectProductLevelPrices(),units:collectProductUnits()})});msg(pMsg,wasEdit?'Barang berhasil diperbarui.':'Barang berhasil disimpan.');productEditId.value='';window.__productUnits=[];renderProductUnitRows([]);try{await Promise.all([loadProducts(),loadSummary()])}catch(refreshError){console.error('Refresh setelah simpan barang gagal:',refreshError);msg(pMsg,(wasEdit?'Barang berhasil diperbarui.':'Barang berhasil disimpan.')+' Daftar akan dimuat ulang otomatis saat halaman dibuka kembali.')}}catch(e){msg(pMsg,e.message,false)}}async function addCategory(){try{let id=categoryEditId.value;await api(id?'/api/categories/'+id:'/api/categories',{method:id?'PUT':'POST',body:JSON.stringify({code:cCode.value,name:cName.value,is_active:true})});categoryEditId.value='';cCode.value=cName.value='';await loadMasters()}catch(e){alert(e.message)}} function editCategory(id){let x=(window.categoryRecords||[]).find(v=>v.id===id);if(!x)return;categoryEditId.value=id;cCode.value=x.code;cName.value=x.name}async function addUnit(){try{let id=unitEditId.value;await api(id?'/api/units/'+id:'/api/units',{method:id?'PUT':'POST',body:JSON.stringify({code:uCode.value,name:uName.value,decimals:uDecimals.value,is_active:true})});unitEditId.value='';uCode.value=uName.value='';uDecimals.value=0;await loadMasters()}catch(e){alert(e.message)}} function editUnit(id){let x=(window.unitRecords||[]).find(v=>v.id===id);if(!x)return;unitEditId.value=id;uCode.value=x.code;uName.value=x.name;uDecimals.value=x.decimals}async function adjust(){try{
if(!aProduct.value)throw Error('Pilih barang yang akan disesuaikan.');
if(!aAdjustmentAccount.value)throw Error('Pilih Akun Penyesuaian.');
let payload={warehouse_id:aWarehouse.value,product_id:aProduct.value,qty_change:aQty.value,adjustment_account_id:aAdjustmentAccount.value,reference_no:aRef.value,reason:aReason.value,department_id:adjustDepartment.value||null,project_id:adjustProject.value||null};let edited=await commitMaintenanceEdit(payload);let d=edited?{result:{qty_after:'diperbarui'}}:await api('/api/stock-adjustments',{method:'POST',body:JSON.stringify(payload)});msg(aMsg,'Stok menjadi '+d.result.qty_after);resetTransactionDimensions('adjust');await Promise.all([loadProducts(),loadMoves(),loadSummary(),loadBalances(),loadInventoryCard()]);await openFreshTransactionForm('adjustment')}catch(e){msg(aMsg,e.message,false)}}async function addPartner(){try{await api(partnerEditId.value?'/api/partners/'+partnerEditId.value:'/api/partners',{method:partnerEditId.value?'PUT':'POST',body:JSON.stringify({partner_type:bType.value,code:bCode.value,name:bName.value,phone:bPhone.value,email:bEmail.value,tax_id:bTax.value,city:bCity.value,payment_term_days:bTerm.value,credit_limit:bLimit.value,opening_balance:(window.bOpening?bOpening.value:0),address:bAddress.value})});msg(bMsg,partnerEditId.value?'Data berhasil diperbarui.':'Data berhasil disimpan.');partnerEditId.value='';await loadPartners()}catch(e){msg(bMsg,e.message,false)}}async function loadMoves(){let d=await api('/api/stock-movements?limit=40');moveBody.innerHTML=d.items.map(x=>`<tr><td>${x.created_at}</td><td>${x.sku} - ${x.product_name}</td><td>${x.qty_change}</td><td>${x.qty_after}</td><td>${x.reference_no||''}</td><td>${x.reason}</td></tr>`).join('')}let accessRoleRecords=[];
let accessUserRecords=[];
let accessPermissionRecords=[];
let editingAccessRoleCode='';

function accessEscape(value){
  return String(value??'').replace(/[&<>"']/g,char=>({
    '&':'&amp;',
    '<':'&lt;',
    '>':'&gt;',
    '"':'&quot;',
    "'":'&#039;'
  })[char]);
}

function accessElement(id){
  return document.getElementById(id);
}
function showAccessTab(tab){
  const showUsers=tab==='users';
  accessElement('userAccessUsers')?.classList.toggle('hidden',!showUsers);
  accessElement('userAccessRoles')?.classList.toggle('hidden',showUsers);
  accessElement('userTabButton')?.classList.toggle('active',showUsers);
  accessElement('roleTabButton')?.classList.toggle('active',!showUsers);
}
async function openUserAccess(){
  page('users');
  showAccessTab('users');
  await loadUserAccess();
}
async function loadUserAccess(){
  const message=accessElement('uMsg');
  try{
    if(message){
      message.className='';
      message.textContent='Memuat data user dan hak akses...';
    }
    const results=await Promise.all([
      api('/api/roles'),
      api('/api/users'),
      api('/api/permissions')
    ]);
    const rolesResponse=results[0]||{};
    const usersResponse=results[1]||{};
    const permissionsResponse=results[2]||{};

    const roleItems=Array.isArray(rolesResponse)?rolesResponse:rolesResponse.items;
    const userItems=Array.isArray(usersResponse)?usersResponse:usersResponse.items;
    const permissionItems=Array.isArray(permissionsResponse)?permissionsResponse:permissionsResponse.items;

    if(!Array.isArray(roleItems)){
      throw Error('Data role dari server tidak valid.');
    }
    if(!Array.isArray(userItems)){
      throw Error('Data user dari server tidak valid.');
    }
    if(!Array.isArray(permissionItems)){
      throw Error('Data hak akses dari server tidak valid.');
    }

    accessRoleRecords=roleItems;
    accessUserRecords=userItems;
    accessPermissionRecords=permissionItems;

    renderUserAccessTable();
    renderAccessRoleList();

    if(
      !editingAccessRoleCode ||
      !accessRoleRecords.some(role=>role.code===editingAccessRoleCode)
    ){
      editingAccessRoleCode=accessRoleRecords.length?accessRoleRecords[0].code:'';
    }
    if(editingAccessRoleCode){
      renderAccessRoleEditor(editingAccessRoleCode);
    }else{
      newRoleEditor();
    }

    if(message){
      message.className='ok';
      message.textContent=`${accessUserRecords.length} user dan ${accessRoleRecords.length} role berhasil dimuat.`;
    }
  }catch(error){
    accessRoleRecords=[];
    accessUserRecords=[];
    accessPermissionRecords=[];
    const roleSelect=accessElement('nRole');
    const userBodyElement=accessElement('userBody');
    const roleListElement=accessElement('roleList');
    const matrixElement=accessElement('permissionMatrix');
    if(roleSelect)roleSelect.innerHTML='<option value="">Role gagal dimuat</option>';
    if(userBodyElement)userBodyElement.innerHTML='<tr><td colspan="7">Data user gagal dimuat.</td></tr>';
    if(roleListElement)roleListElement.innerHTML='<p class="error">Data role gagal dimuat.</p><button type="button" onclick="loadUserAccess()">Coba Muat Ulang</button>';
    if(matrixElement)matrixElement.innerHTML='';
    msg(message,error.message,false);
  }
}
async function loadUsers(){
  await loadUserAccess();
  await loadActiveSessions();
}
async function loadActiveSessions(){
  const body=document.getElementById('activeSessionBody');if(!body)return;
  try{const d=await api('/api/active-sessions');const items=d.items||[];body.innerHTML=items.length?items.map(x=>`<tr><td><b>${accessEscape(x.username||'')}</b><br><small>${accessEscape(x.full_name||'')}</small></td><td>${accessEscape(x.client_name||'-')}<br><small>${accessEscape((x.user_agent||'').slice(0,80))}</small></td><td>${accessEscape(x.client_ip||'-')}</td><td>${accessEscape(x.last_seen_at||'-')}</td><td><button class="danger" onclick="forceLogoutSession('${accessEscape(x.session_id)}')">Paksa Logout</button></td></tr>`).join(''):'<tr><td colspan="5">Tidak ada device aktif.</td></tr>'}catch(e){body.innerHTML=`<tr><td colspan="5" class="error">${accessEscape(e.message)}</td></tr>`}}
async function forceLogoutSession(id){if(!confirm('Paksa logout device ini?'))return;try{await api('/api/active-sessions/force-logout',{method:'POST',body:JSON.stringify({session_id:id})});await loadActiveSessions()}catch(e){alert(e.message)}}
function startHeartbeat(){if(heartbeatTimer)clearInterval(heartbeatTimer);if(!token)return;const ping=async()=>{try{await api('/api/session/ping',{method:'POST',body:JSON.stringify({})})}catch(e){if(/401|Sesi tidak aktif/i.test(e.message)){stopHeartbeat();localStorage.removeItem('slp_token');token='';document.getElementById('app').classList.add('hidden');document.getElementById('app').setAttribute('aria-hidden','true');document.getElementById('authShell').classList.remove('hidden');document.getElementById('authShell').setAttribute('aria-hidden','false')}}};ping();heartbeatTimer=setInterval(ping,5000)}
function stopHeartbeat(){if(heartbeatTimer){clearInterval(heartbeatTimer);heartbeatTimer=null}}

function accessRoleOptions(selectedCode=''){
  if(!accessRoleRecords.length){
    return '<option value="">Belum ada role</option>';
  }
  return accessRoleRecords.map(role=>
    `<option value="${accessEscape(role.code)}" ${role.code===selectedCode?'selected':''}>${accessEscape(role.name)}</option>`
  ).join('');
}
function renderUserAccessTable(){
  const roleSelect=accessElement('nRole');
  const userCountElement=accessElement('userCount');
  const userBodyElement=accessElement('userBody');

  if(roleSelect){
    const previous=roleSelect.value;
    roleSelect.innerHTML=accessRoleOptions(previous);
    if(
      previous &&
      accessRoleRecords.some(role=>role.code===previous)
    ){
      roleSelect.value=previous;
    }
  }
  if(userCountElement){
    userCountElement.textContent=`${accessUserRecords.length} user`;
  }
  if(!userBodyElement)return;

  if(!accessUserRecords.length){
    userBodyElement.innerHTML='<tr><td colspan="7">Belum ada user.</td></tr>';
    return;
  }

  userBodyElement.innerHTML=accessUserRecords.map(user=>{
    const role=user.role||{};
    return `<tr>
      <td><b>${accessEscape(user.username||'')}</b></td>
      <td><input id="userName_${user.id}" value="${accessEscape(user.full_name||'')}"></td>
      <td><select id="userRole_${user.id}">${accessRoleOptions(role.code||'')}</select></td>
      <td>
        <label class="status-toggle">
          <input id="userActive_${user.id}" type="checkbox" ${user.is_active?'checked':''}>
          <span>${user.is_active?'Aktif':'Nonaktif'}</span>
        </label>
      </td>
      <td>${accessEscape(user.created_at||'-')}</td>
      <td class="actions-cell">
        <button type="button" onclick="saveExistingUser(${user.id})">Simpan</button>
        <button type="button" class="secondary" onclick='resetExistingUserPassword(${user.id},${JSON.stringify(String(user.username||""))})'>Reset Password</button>
      </td>
    </tr>`;
  }).join('');
}
async function addUser(){
  const usernameInput=accessElement('nUser');
  const nameInput=accessElement('nName');
  const passwordInput=accessElement('nPass');
  const roleInput=accessElement('nRole');
  try{
    const payload={
      username:usernameInput?.value.trim()||'',
      full_name:nameInput?.value.trim()||'',
      password:passwordInput?.value||'',
      role_code:roleInput?.value||''
    };
    if(!payload.username||!payload.full_name||!payload.role_code){
      throw Error('Username, nama lengkap, dan role wajib diisi.');
    }
    if(payload.password.length<8){
      throw Error('Password awal minimal 8 karakter.');
    }
    await api('/api/users',{
      method:'POST',
      body:JSON.stringify(payload)
    });
    usernameInput.value='';
    nameInput.value='';
    passwordInput.value='';
    msg(accessElement('uMsg'),'User baru berhasil dibuat.');
    await loadUserAccess();
  }catch(error){
    msg(accessElement('uMsg'),error.message,false);
  }
}
async function saveExistingUser(id){
  try{
    const fullName=accessElement('userName_'+id)?.value.trim()||'';
    const roleCode=accessElement('userRole_'+id)?.value||'';
    const active=!!accessElement('userActive_'+id)?.checked;
    if(!fullName||!roleCode){
      throw Error('Nama lengkap dan role wajib diisi.');
    }
    const response=await api('/api/users/'+id,{
      method:'PUT',
      body:JSON.stringify({
        full_name:fullName,
        role_code:roleCode,
        is_active:active
      })
    });
    msg(
      accessElement('uMsg'),
      `User ${response.item?.username||''} berhasil diperbarui.`
    );
    await loadUserAccess();
  }catch(error){
    msg(accessElement('uMsg'),error.message,false);
  }
}
async function resetExistingUserPassword(id,usernameValue){
  const passwordValue=prompt(
    `Masukkan password baru untuk ${usernameValue} (minimal 8 karakter):`
  );
  if(passwordValue===null)return;
  try{
    if(passwordValue.length<8){
      throw Error('Password baru minimal 8 karakter.');
    }
    await api(`/api/users/${id}/reset-password`,{
      method:'POST',
      body:JSON.stringify({password:passwordValue})
    });
    msg(
      accessElement('uMsg'),
      `Password ${usernameValue} berhasil direset.`
    );
  }catch(error){
    msg(accessElement('uMsg'),error.message,false);
  }
}
function renderAccessRoleList(){
  const roleListElement=accessElement('roleList');
  if(!roleListElement)return;
  if(!accessRoleRecords.length){
    roleListElement.innerHTML='<p class="muted">Belum ada role.</p>';
    return;
  }
  roleListElement.innerHTML=accessRoleRecords.map(role=>`
    <button type="button"
      class="role-list-item ${editingAccessRoleCode===role.code?'active':''}"
      onclick='renderAccessRoleEditor(${JSON.stringify(String(role.code))})'>
      <b>${accessEscape(role.name||'')}</b>
      <small>${accessEscape(role.code||'')} · ${
        Array.isArray(role.permissions)&&role.permissions.includes('*')
          ?'Semua akses'
          :`${Array.isArray(role.permissions)?role.permissions.length:0} hak akses`
      }</small>
    </button>
  `).join('');
}
function newRoleEditor(){
  editingAccessRoleCode='';
  const editorTitle=accessElement('roleEditorTitle');
  const codeInput=accessElement('roleCode');
  const nameInput=accessElement('roleName');
  if(editorTitle)editorTitle.textContent='Buat Role Baru';
  if(codeInput){
    codeInput.value='';
    codeInput.disabled=false;
  }
  if(nameInput)nameInput.value='';
  renderAccessPermissionMatrix([]);
  renderAccessRoleList();
}
function renderAccessRoleEditor(code){
  editingAccessRoleCode=code||'';
  const role=accessRoleRecords.find(item=>item.code===editingAccessRoleCode);
  if(!role){
    newRoleEditor();
    return;
  }
  const editorTitle=accessElement('roleEditorTitle');
  const codeInput=accessElement('roleCode');
  const nameInput=accessElement('roleName');
  if(editorTitle)editorTitle.textContent='Edit Role: '+role.name;
  if(codeInput){
    codeInput.value=role.code;
    codeInput.disabled=true;
  }
  if(nameInput)nameInput.value=role.name||'';
  renderAccessPermissionMatrix(
    Array.isArray(role.permissions)?role.permissions:[]
  );
  renderAccessRoleList();
}
function renderAccessPermissionMatrix(selectedPermissions){
  const matrixElement=accessElement('permissionMatrix');
  if(!matrixElement)return;

  const selected=Array.isArray(selectedPermissions)
    ?selectedPermissions
    :[];
  const hasAll=selected.includes('*');
  const groups={};

  accessPermissionRecords.forEach(permission=>{
    const group=permission.group||'Lainnya';
    if(!groups[group])groups[group]=[];
    groups[group].push(permission);
  });

  if(!Object.keys(groups).length){
    matrixElement.innerHTML='<p class="muted">Daftar hak akses belum tersedia.</p>';
    return;
  }

  matrixElement.innerHTML=Object.entries(groups).map(([group,items])=>`
    <section class="permission-group">
      <div class="permission-group-title">
        <h3>${accessEscape(group)}</h3>
        <label>
          <input type="checkbox"
            onchange='togglePermissionGroup(${JSON.stringify(group)},this.checked)'>
          Semua ${accessEscape(group)}
        </label>
      </div>
      ${items.map(permission=>`
        <label class="permission-item">
          <input class="permission-check"
            data-group="${accessEscape(group)}"
            type="checkbox"
            value="${accessEscape(permission.code)}"
            ${hasAll||selected.includes(permission.code)?'checked':''}
            ${editingAccessRoleCode==='ADMIN'?'disabled':''}>
          <span>
            <b>${accessEscape(permission.name||permission.code)}</b>
            <small>${accessEscape(permission.description||'')}</small>
          </span>
        </label>
      `).join('')}
    </section>
  `).join('');

  if(editingAccessRoleCode==='ADMIN'){
    const editorTitle=accessElement('roleEditorTitle');
    if(editorTitle){
      editorTitle.textContent='Administrator — Semua Hak Akses';
    }
  }
}
function togglePermissionGroup(group,checked){
  document.querySelectorAll('.permission-check').forEach(item=>{
    if(item.dataset.group===group&&!item.disabled){
      item.checked=checked;
    }
  });
}
function setAllPermissions(checked){
  document.querySelectorAll('.permission-check:not(:disabled)')
    .forEach(item=>item.checked=checked);
}
async function saveRoleAccess(){
  const codeInput=accessElement('roleCode');
  const nameInput=accessElement('roleName');
  try{
    const code=(codeInput?.value||'').trim().toUpperCase();
    const name=(nameInput?.value||'').trim();
    const permissions=[
      ...document.querySelectorAll('.permission-check:checked')
    ].map(item=>item.value);

    if(!code||!name){
      throw Error('Kode dan nama role wajib diisi.');
    }

    const body={code,name,permissions};
    if(editingAccessRoleCode){
      await api('/api/roles/'+encodeURIComponent(editingAccessRoleCode),{
        method:'PUT',
        body:JSON.stringify(body)
      });
      msg(accessElement('uMsg'),'Role berhasil diperbarui.');
    }else{
      await api('/api/roles',{
        method:'POST',
        body:JSON.stringify(body)
      });
      editingAccessRoleCode=code;
      msg(accessElement('uMsg'),'Role baru berhasil dibuat.');
    }
    await loadUserAccess();
    showAccessTab('roles');
  }catch(error){
    msg(accessElement('uMsg'),error.message,false);
  }
}

let departmentRecords=[],projectRecords=[];
function projectStatusLabel(v){return {PLANNED:'Direncanakan',ACTIVE:'Aktif',ON_HOLD:'Ditunda',COMPLETED:'Selesai',CANCELLED:'Dibatalkan'}[v]||v||'-'}
async function loadDepartments(){try{let d=await api('/api/departments');departmentRecords=d.items||[];departmentCount.textContent=departmentRecords.length+' departemen';departmentBody.innerHTML=departmentRecords.length?departmentRecords.map(x=>`<tr><td><b>${accessEscape(x.code)}</b></td><td>${accessEscape(x.name)}</td><td>${accessEscape(x.manager_name||'-')}</td><td>${x.is_active?'Aktif':'Nonaktif'}</td><td>${accessEscape(x.notes||'-')}</td><td><button onclick="editDepartment(${x.id})">Edit</button> <button class="danger" onclick="deleteMaster('/api/departments/${x.id}',loadDepartments)">Hapus</button></td></tr>`).join(''):'<tr><td colspan="7">Belum ada departemen.</td></tr>';msg(departmentMsg,'Data departemen dimuat.')}catch(e){msg(departmentMsg,e.message,false)}}
function resetDepartmentForm(){departmentId.value='';departmentCode.value='';departmentName.value='';departmentManager.value='';departmentNotes.value='';departmentActive.value='1';departmentFormTitle.textContent='Tambah Departemen'}
function editDepartment(id){let x=departmentRecords.find(v=>v.id===id);if(!x)return;departmentId.value=x.id;departmentCode.value=x.code;departmentName.value=x.name;departmentManager.value=x.manager_name||'';departmentNotes.value=x.notes||'';departmentActive.value=x.is_active?'1':'0';departmentFormTitle.textContent='Edit Departemen: '+x.name;window.scrollTo({top:0,behavior:'smooth'})}
async function saveDepartment(){try{let body={code:departmentCode.value,name:departmentName.value,manager_name:departmentManager.value,notes:departmentNotes.value,is_active:departmentActive.value==='1'},id=departmentId.value;if(!body.code.trim()||!body.name.trim())throw Error('Kode dan nama departemen wajib diisi.');await api(id?'/api/departments/'+id:'/api/departments',{method:id?'PUT':'POST',body:JSON.stringify(body)});resetDepartmentForm();await loadDepartments()}catch(e){msg(departmentMsg,e.message,false)}}
async function loadProjects(){try{let [p,c,sales]=await Promise.all([api('/api/projects'),api('/api/customers?active=1'),api('/api/sales?q=')]);projectRecords=p.items||[];projectCustomer.innerHTML='<option value="">Tanpa pelanggan khusus</option>'+(c.items||[]).map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');contractorProject.innerHTML='<option value="">Pilih proyek</option>'+projectRecords.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');termSale.innerHTML='<option value="">Belum dihubungkan</option>'+(sales.items||[]).map(x=>`<option value="${x.id}">${accessEscape(x.invoice_no)} - ${rup(x.total_amount||0)}</option>`).join('');projectCount.textContent=projectRecords.length+' proyek';projectBody.innerHTML=projectRecords.length?projectRecords.map(x=>`<tr><td><b>${accessEscape(x.code)}</b></td><td>${accessEscape(x.name)}</td><td>${accessEscape(x.customer_name||'-')}</td><td>${rup(Number(x.contract_value||0))}</td><td>${Number(x.progress_percent||0).toFixed(1)}%</td><td>${rup(Number(x.total_budget||0))}</td><td>${rup(Number(x.realization_total||0))}</td><td>${rup(Number(x.contract_value||0)-Number(x.realization_total||0))}</td><td>${rup(Number(x.term_total||0))}</td><td><button onclick="editProject(${x.id})">Edit</button> <button class="secondary" onclick="contractorProject.value='${x.id}';loadContractorProject()">Kartu</button></td></tr>`).join(''):'<tr><td colspan="10">Belum ada proyek.</td></tr>';msg(projectMsg,'Data proyek dimuat.')}catch(e){msg(projectMsg,e.message,false)}}
function resetProjectForm(){projectId.value='';projectCode.value='';projectName.value='';projectCustomer.value='';projectContractNo.value='';projectContractValue.value='';projectLocation.value='';projectPic.value='';projectType.value='';projectRetention.value='';projectStatus.value='ACTIVE';projectStart.value='';projectEnd.value='';projectNotes.value='';projectActive.value='1';projectFormTitle.textContent='Tambah Proyek'}
function editProject(id){let x=projectRecords.find(v=>v.id===id);if(!x)return;projectId.value=x.id;projectCode.value=x.code;projectName.value=x.name;projectCustomer.value=x.customer_id||'';projectContractNo.value=x.contract_no||'';projectContractValue.value=x.contract_value||0;projectLocation.value=x.location||'';projectPic.value=x.pic_name||'';projectType.value=x.project_type||'';projectRetention.value=x.retention_percent||0;projectStatus.value=x.status||'ACTIVE';projectStart.value=x.start_date||'';projectEnd.value=x.end_date||'';projectNotes.value=x.notes||'';projectActive.value=x.is_active?'1':'0';projectFormTitle.textContent='Edit Proyek: '+x.name;window.scrollTo({top:0,behavior:'smooth'})}
async function saveProject(){try{let body={code:projectCode.value,name:projectName.value,customer_id:projectCustomer.value||null,contract_no:projectContractNo.value,contract_value:projectContractValue.value||0,location:projectLocation.value,pic_name:projectPic.value,project_type:projectType.value,retention_percent:projectRetention.value||0,start_date:projectStart.value||null,end_date:projectEnd.value||null,status:projectStatus.value,notes:projectNotes.value,is_active:projectActive.value==='1'},id=projectId.value;if(!body.code.trim()||!body.name.trim())throw Error('Kode dan nama proyek wajib diisi.');await api(id?'/api/projects/'+id:'/api/projects',{method:id?'PUT':'POST',body:JSON.stringify(body)});resetProjectForm();await loadProjects()}catch(e){msg(projectMsg,e.message,false)}}


async function loadProjectReportMasters(){const [p,s,pr,d,w,a]=await Promise.all([api('/api/projects?active=1'),api('/api/suppliers?active=1'),api('/api/products?active=1'),api('/api/departments?active=1'),api('/api/warehouses?active=1'),api('/api/project-cost-accounts')]);projectReportProject.innerHTML=(p.items||[]).map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');projectReportSupplier.innerHTML='<option value="">Semua Pemasok</option>'+(s.items||[]).map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');projectReportProduct.innerHTML='<option value="">Semua Barang</option>'+(pr.items||[]).map(x=>`<option value="${x.id}">${accessEscape(x.sku)} - ${accessEscape(x.name)}</option>`).join('');projectReportDepartment.innerHTML='<option value="">Semua Departemen</option>'+(d.items||[]).map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');projectReportWarehouse.innerHTML='<option value="">Semua Gudang</option>'+(w.items||[]).map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');projectReportAccount.innerHTML='<option value="">Semua Akun Biaya</option>'+(a.items||[]).map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');const now=new Date();if(!projectReportFrom.value)projectReportFrom.value=`${now.getFullYear()}-01-01`;if(!projectReportTo.value)projectReportTo.value=now.toISOString().slice(0,10);toggleProjectReportFilters();}
function toggleProjectReportFilters(){const type=projectReportType.value,summary=type==='project_summary',purchase=type==='project_purchases',material=type==='project_materials',costDetail=type==='project_cost_detail';projectReportProjectWrap.style.display=summary?'none':'flex';projectReportStatusWrap.style.display=summary?'flex':'none';projectReportSupplierWrap.style.display=purchase?'flex':'none';projectReportProductWrap.style.display=(purchase||material)?'flex':'none';projectReportDepartmentWrap.style.display=(purchase||material||costDetail)?'flex':'none';projectReportAccountWrap.style.display=costDetail?'flex':'none';projectReportWarehouseWrap.style.display=material?'flex':'none';}
function selectedProjectReportIds(){return Array.from(projectReportProject.selectedOptions||[]).map(o=>o.value).filter(Boolean)}function projectReportParams(){const type=projectReportType.value,p=new URLSearchParams({type,date_from:projectReportFrom.value,date_to:projectReportTo.value}),ids=selectedProjectReportIds();if(type==='project_income'&&ids.length)p.set('project_ids',ids.join(','));else if(type!=='project_summary'&&ids.length)p.set('project_id',ids[0]);if(type==='project_summary'&&projectReportStatus.value)p.set('project_status',projectReportStatus.value);if(type==='project_purchases'&&projectReportSupplier.value)p.set('supplier_id',projectReportSupplier.value);if((type==='project_purchases'||type==='project_materials')&&projectReportProduct.value)p.set('product_id',projectReportProduct.value);if((type==='project_purchases'||type==='project_materials'||type==='project_cost_detail')&&projectReportDepartment.value)p.set('department_id',projectReportDepartment.value);if(type==='project_cost_detail'&&projectReportAccount.value)p.set('account_id',projectReportAccount.value);if(type==='project_materials'&&projectReportWarehouse.value)p.set('warehouse_id',projectReportWarehouse.value);return p;}
function renderProjectReportSummary(s){projectReportSummary.innerHTML=Object.entries(s||{}).filter(([k])=>!['project_id','project_code','project_name','customer_name'].includes(k)).map(([k,v])=>`<div class="project-budget-stat"><span>${accessEscape(k.replaceAll('_',' '))}</span><b>${k.includes('percent')?Number(v||0).toFixed(2)+'%':rup(Number(v||0))}</b></div>`).join('');}
function incomeSection(t,rows,total){return `<section class="financial-section"><h3>${t}</h3>${rows.map(x=>`<div class="financial-line"><span>${accessEscape(x.kode)} · ${accessEscape(x.akun)}</span><b>${rup(x.jumlah)}</b></div>`).join('')||'<div class="financial-line">Tidak ada data</div>'}<div class="financial-total"><span>Total ${t}</span><b>${rup(total||0)}</b></div></section>`;}
async function loadProjectReport(){try{const ids=selectedProjectReportIds();if(projectReportType.value!=='project_summary'&&!ids.length)throw Error('Pilih minimal satu proyek.');const d=await api('/api/reports?'+projectReportParams());if(projectReportType.value==='project_income'){const projects=d.projects||[{summary:d.summary,rows:d.rows||[]}];projectReportHeader.innerHTML=`<div class="psak-report-header"><h2>LAPORAN LABA RUGI PER PROYEK</h2><p>${projectReportFrom.value||''} s.d. ${projectReportTo.value||''} · ${projects.length} proyek</p></div>`;projectReportSummary.innerHTML='';const total=d.summary||{};projectReportSpecial.innerHTML=`<div class="project-income-grid"><div class="project-income-total"><div class="project-budget-summary"><div class="project-budget-stat primary"><span>Total Pendapatan</span><b>${rup(total.pendapatan||0)}</b></div><div class="project-budget-stat"><span>Total HPP</span><b>${rup(total.hpp||0)}</b></div><div class="project-budget-stat"><span>Total Biaya Operasional</span><b>${rup(total.biaya_operasional||0)}</b></div><div class="project-budget-stat"><span>Total Laba Bersih</span><b>${rup(total.laba_bersih||0)}</b></div></div></div>${projects.map(p=>{const s=p.summary||{},r=p.rows||[];return `<section class="project-income-card"><header><h3>${accessEscape(s.project_code||'')} - ${accessEscape(s.project_name||'')}</h3><small>${accessEscape(s.customer_name||'-')}</small></header>${incomeSection('PENDAPATAN',r.filter(x=>x.kelompok==='Pendapatan'),s.pendapatan||0)}${incomeSection('HARGA POKOK PENJUALAN',r.filter(x=>x.kelompok==='Harga Pokok Penjualan'),s.hpp||0)}<div class="financial-highlight"><span>LABA KOTOR</span><b>${rup(s.laba_kotor||0)}</b></div>${incomeSection('BIAYA OPERASIONAL',r.filter(x=>x.kelompok==='Biaya Operasional'),s.biaya_operasional||0)}<div class="financial-highlight secondary"><span>LABA BERSIH</span><b>${rup(s.laba_bersih||0)}</b></div></section>`}).join('')}</div>`;projectReportHead.innerHTML='';projectReportBody.innerHTML='';}else{renderProjectReportSummary(d.summary);projectReportSpecial.innerHTML='';projectReportHeader.innerHTML=`<h2>${accessEscape(d.title||'Laporan Proyek')}</h2>${d.summary?.project_code?`<p><b>${accessEscape(d.summary.project_code)} - ${accessEscape(d.summary.project_name)}</b></p>`:''}`;const cols=d.columns||[];projectReportHead.innerHTML='<tr>'+cols.map(x=>`<th>${accessEscape(x[1])}</th>`).join('')+'</tr>';projectReportBody.innerHTML=(d.rows||[]).length?(d.rows||[]).map(row=>'<tr>'+cols.map(([k])=>{const v=row[k],money=typeof v==='number'&&(/budget|realisasi|sisa|pendapatan|hpp|biaya|laba|harga|diskon|subtotal|cost/.test(k));return `<td class="${typeof v==='number'?'number-cell':''}">${money?rup(v):accessEscape(v)}</td>`}).join('')+'</tr>').join(''):`<tr><td colspan="${cols.length}">Tidak ada data pada filter ini.</td></tr>`;}msg(projectReportMsg,'Laporan berhasil dimuat.');}catch(e){msg(projectReportMsg,e.message,false)}}
function exportProjectReport(fmt){if(projectReportType.value!=='project_summary'&&!selectedProjectReportIds().length){msg(projectReportMsg,'Pilih minimal satu proyek.',false);return;}const p=projectReportParams();p.set('format',fmt);p.set('token',token);window.open('/api/reports/export?'+p,'_blank');}

let projectMaterialIssueRecords=[];
let projectMaterialIssueProducts=[];
let projectMaterialIssueBalances=[];
let projectMaterialIssueLines=[];

function projectMaterialProductOptions(selected=''){
  return '<option value="">Pilih Barang</option>'+projectMaterialIssueProducts.map(item=>
    `<option value="${item.id}" ${String(item.id)===String(selected)?'selected':''}>${accessEscape(item.sku)} - ${accessEscape(item.name)}</option>`
  ).join('');
}
function projectMaterialCost(productId){
  const warehouseId=projectMaterialWarehouse.value;
  const balance=projectMaterialIssueBalances.find(item=>
    String(item.product_id)===String(productId)&&String(item.warehouse_id)===String(warehouseId));
  return balance?Number(balance.average_cost||0):0;
}
function renderProjectMaterialLines(){
  projectMaterialLines.innerHTML=projectMaterialIssueLines.map((line,index)=>{
    const cost=projectMaterialCost(line.product_id);
    line.average_cost=cost;
    line.total_cost=Number(line.qty||0)*cost;
    return `<tr>
      <td><select onchange="projectMaterialIssueLines[${index}].product_id=this.value;renderProjectMaterialLines()">${projectMaterialProductOptions(line.product_id)}</select></td>
      <td><input type="number" min="0.0001" step="0.0001" value="${line.qty||1}" oninput="projectMaterialIssueLines[${index}].qty=this.value;renderProjectMaterialLines()"></td>
      <td class="number-cell">${rup(cost)}</td>
      <td class="number-cell"><b>${rup(line.total_cost)}</b></td>
      <td><button class="danger" onclick="projectMaterialIssueLines.splice(${index},1);renderProjectMaterialLines()">Hapus</button></td>
    </tr>`;
  }).join('');
  const total=projectMaterialIssueLines.reduce((sum,line)=>sum+Number(line.total_cost||0),0);
  projectMaterialGrandTotal.textContent=rup(total);
}
function addProjectMaterialLine(){
  projectMaterialIssueLines.push({product_id:'',qty:1,average_cost:0,total_cost:0});
  renderProjectMaterialLines();
}
function refreshProjectMaterialCosts(){renderProjectMaterialLines()}
async function loadProjectMaterialIssueMasters(){
  const [projectsData,departmentsData,warehousesData,productsData,balancesData,coaDataResponse]=await Promise.all([
    api('/api/projects?active=1'),api('/api/departments?active=1'),
    api('/api/warehouses?active=1'),api('/api/products?active=1'),
    api('/api/inventory-balances'),api('/api/coa?active=1')
  ]);
  projectMaterialIssueProducts=(productsData.items||[]).filter(item=>item.product_type==='STOCK');
  projectMaterialIssueBalances=balancesData.items||[];
  projectMaterialProject.innerHTML='<option value="">Pilih Proyek</option>'+
    (projectsData.items||[]).map(item=>`<option value="${item.id}">${accessEscape(item.code)} - ${accessEscape(item.name)}</option>`).join('');
  projectMaterialDepartment.innerHTML='<option value="">Tanpa Departemen</option>'+
    (departmentsData.items||[]).map(item=>`<option value="${item.id}">${accessEscape(item.code)} - ${accessEscape(item.name)}</option>`).join('');
  projectMaterialWarehouse.innerHTML='<option value="">Pilih Gudang</option>'+
    (warehousesData.items||[]).map(item=>`<option value="${item.id}">${accessEscape(item.code)} - ${accessEscape(item.name)}</option>`).join('');
  projectMaterialAccount.innerHTML='<option value="">Pilih Akun</option>'+
    (coaDataResponse.items||[]).filter(item=>
      item.account_type==='ASSET'||item.account_type==='EXPENSE'||
      ['HPP','OPERATING_EXPENSE'].includes(item.display_type||item.account_subtype)
    ).map(item=>`<option value="${item.id}">${accessEscape(item.code)} - ${accessEscape(item.name)}</option>`).join('');
  if(!projectMaterialDate.value)projectMaterialDate.value=new Date().toISOString().slice(0,10);
  if(!projectMaterialIssueLines.length)addProjectMaterialLine();
  else renderProjectMaterialLines();
}
async function loadProjectMaterialIssues(){
  try{
    const data=await api('/api/project-material-issues');
    projectMaterialIssueRecords=data.items||[];
    projectMaterialCount.textContent=projectMaterialIssueRecords.length+' transaksi';
    projectMaterialBody.innerHTML=projectMaterialIssueRecords.length?projectMaterialIssueRecords.map(item=>`<tr>
      <td>${accessEscape(item.issue_date)}</td><td><b>${accessEscape(item.issue_no)}</b></td>
      <td>${accessEscape(item.project_code)} - ${accessEscape(item.project_name)}</td>
      <td>${accessEscape(item.department_name||'-')}</td><td>${accessEscape(item.warehouse_name)}</td>
      <td>${accessEscape(item.expense_account_code)} - ${accessEscape(item.expense_account_name)}</td>
      <td class="number-cell"><b>${rup(Number(item.total_cost||0))}</b></td>
      <td>${accessEscape(item.notes||'-')}</td><td><button onclick="editProjectMaterialIssue(${item.id})">Edit</button> <button class="danger" onclick="deleteProjectMaterialIssue(${item.id})">Hapus</button></td></tr>`).join(''):'<tr><td colspan="9">Belum ada pengeluaran material proyek.</td></tr>';
  }catch(error){msg(projectMaterialMsg,error.message,false)}
}
function resetProjectMaterialIssue(){
  projectMaterialDate.value=new Date().toISOString().slice(0,10);
  projectMaterialProject.value='';projectMaterialDepartment.value='';
  projectMaterialWarehouse.value='';projectMaterialAccount.value='';
  projectMaterialNotes.value='';
  projectMaterialIssueLines=[{product_id:'',qty:1,average_cost:0,total_cost:0}];
  renderProjectMaterialLines();
}
async function viewProjectMaterialIssue(id){const x=projectMaterialIssueRecords.find(r=>Number(r.id)===Number(id));if(!x)return;await editProjectMaterialIssue(id);window.__projectMaterialEdit=null;activateTransactionViewMode('Pengeluaran Material Proyek')}
async function editProjectMaterialIssue(id){const x=projectMaterialIssueRecords.find(r=>Number(r.id)===Number(id));if(!x)return;projectMaterialDate.value=x.issue_date;projectMaterialProject.value=x.project_id;projectMaterialDepartment.value=x.department_id||'';projectMaterialWarehouse.value=x.warehouse_id;projectMaterialAccount.value=x.expense_account_id;projectMaterialNotes.value=x.notes||'';projectMaterialIssueLines=(x.items||[]).map(i=>({product_id:i.product_id,qty:i.qty,average_cost:i.average_cost,total_cost:i.total_cost}));renderProjectMaterialLines();window.__projectMaterialEdit=id;window.scrollTo({top:0,behavior:'smooth'});}
async function deleteProjectMaterialIssue(id){if(!confirm('Hapus/batalkan pengeluaran material ini? Stok dan jurnal akan dibalik.'))return;try{await api('/api/project-material-issues/'+id,{method:'DELETE'});await loadProjectMaterialIssues();msg(projectMaterialMsg,'Transaksi berhasil dibatalkan.')}catch(e){msg(projectMaterialMsg,e.message,false)}}
async function saveProjectMaterialIssue(){
  try{
    const items=projectMaterialIssueLines.map(line=>({
      product_id:line.product_id,qty:Number(line.qty||0)
    })).filter(line=>line.product_id&&line.qty>0);
    if(!projectMaterialProject.value)throw Error('Proyek wajib dipilih.');
    if(!projectMaterialWarehouse.value)throw Error('Gudang wajib dipilih.');
    if(!projectMaterialAccount.value)throw Error('Akun pengeluaran wajib dipilih.');
    if(!items.length)throw Error('Minimal satu barang wajib diisi.');
    const response=await api('/api/project-material-issues',{
      method:'POST',body:JSON.stringify({
        issue_date:projectMaterialDate.value,project_id:projectMaterialProject.value,
        department_id:projectMaterialDepartment.value||null,
        warehouse_id:projectMaterialWarehouse.value,
        expense_account_id:projectMaterialAccount.value,
        notes:projectMaterialNotes.value,items
      })
    });
    msg(projectMaterialMsg,`Transaksi ${response.result.issue_no} berhasil disimpan. Total ${rup(response.result.total_cost)}.`);window.__projectMaterialEdit=null;
    resetProjectMaterialIssue();
    await Promise.all([
      loadProjectMaterialIssues(),loadProjectBudgets(),loadProjects(),
      loadProducts(),loadBalances(),loadInventoryCard(),loadAccounting()
    ]);
    resetProjectMaterialIssue();window.scrollTo({top:0,behavior:'smooth'});projectMaterialProject?.focus();
  }catch(error){msg(projectMaterialMsg,error.message,false)}
}

let projectBudgetRecords=[];
let projectBudgetProjects=[];

function projectBudgetNumber(value){
  const parsed=Number(numberRaw(value)||0);
  return Number.isFinite(parsed)?parsed:0;
}
function syncProjectBudgetTotal(){
  const total=projectBudgetNumber(projectBudgetMaterial.value)+
    projectBudgetNumber(projectBudgetExpense.value);
  projectBudgetTotal.value=String(total);
  formatNumberInput(projectBudgetTotal);
}
function projectBudgetProgressClass(percent){
  if(percent>100)return 'over';
  if(percent>=80)return 'warning';
  return 'safe';
}
function renderProjectBudgetSummary(summary){
  projectBudgetSummary.innerHTML=`
    <div class="project-budget-stat"><span>Total Proyek</span><b>${Number(summary.project_count||0)}</b></div>
    <div class="project-budget-stat"><span>Proyek Berbudget</span><b>${Number(summary.budgeted_project_count||0)}</b></div>
    <div class="project-budget-stat"><span>Budget Material</span><b>${rup(Number(summary.material_budget||0))}</b></div>
    <div class="project-budget-stat"><span>Budget Biaya</span><b>${rup(Number(summary.expense_budget||0))}</b></div>
    <div class="project-budget-stat primary"><span>Total Budget</span><b>${rup(Number(summary.total_budget||0))}</b></div>
    <div class="project-budget-stat"><span>Realisasi Material</span><b>${rup(Number(summary.realization_material||0))}</b></div>
    <div class="project-budget-stat"><span>Realisasi Biaya</span><b>${rup(Number(summary.realization_expense||0))}</b></div>
    <div class="project-budget-stat"><span>Total Realisasi</span><b>${rup(Number(summary.realization_total||0))}</b></div>
    <div class="project-budget-stat"><span>Sisa Budget</span><b>${rup(Number(summary.remaining_budget||0))}</b></div>`;
}
function renderProjectBudgetControl(item){
  if(!item){
    projectBudgetControl.innerHTML='<p class="muted">Pilih budget pada tabel untuk melihat ringkasan.</p>';
    return;
  }
  const percent=Number(item.usage_percent||0);
  const width=Math.min(Math.max(percent,0),100);
  projectBudgetControl.innerHTML=`
    <div class="project-budget-control-title"><b>${accessEscape(item.project_code)} — ${accessEscape(item.project_name)}</b><span>${accessEscape(item.customer_name||'Tanpa pelanggan')}</span></div>
    <div class="budget-control-section">
      <h4>Material</h4>
      <div class="budget-control-line"><span>Budget Material</span><b>${rup(Number(item.material_budget||0))}</b></div>
      <div class="budget-control-line"><span>Realisasi Material</span><b>${rup(Number(item.realization_material||0))}</b></div>
      <div class="budget-control-line remaining"><span>Sisa Material</span><b>${rup(Number(item.remaining_material_budget||0))}</b></div>
      <div class="budget-progress-head"><span>Pemakaian Material</span><b>${Number(item.material_usage_percent||0).toFixed(1)}%</b></div>
      <div class="budget-progress"><i class="${projectBudgetProgressClass(Number(item.material_usage_percent||0))}" style="width:${Math.min(Math.max(Number(item.material_usage_percent||0),0),100)}%"></i></div>
    </div>
    <div class="budget-control-section">
      <h4>Biaya Proyek</h4>
      <div class="budget-control-line"><span>Budget Biaya</span><b>${rup(Number(item.expense_budget||0))}</b></div>
      <div class="budget-control-line"><span>Realisasi Biaya</span><b>${rup(Number(item.realization_expense||0))}</b></div>
      <div class="budget-control-line remaining"><span>Sisa Biaya</span><b>${rup(Number(item.remaining_expense_budget||0))}</b></div>
      <div class="budget-progress-head"><span>Pemakaian Biaya</span><b>${Number(item.expense_usage_percent||0).toFixed(1)}%</b></div>
      <div class="budget-progress"><i class="${projectBudgetProgressClass(Number(item.expense_usage_percent||0))}" style="width:${Math.min(Math.max(Number(item.expense_usage_percent||0),0),100)}%"></i></div>
    </div>
    <div class="budget-control-line total"><span>Total Budget</span><b>${rup(Number(item.total_budget||0))}</b></div>
    <div class="budget-control-line"><span>Total Realisasi</span><b>${rup(Number(item.realization_total||0))}</b></div>
    <div class="budget-control-line remaining"><span>Total Sisa</span><b>${rup(Number(item.remaining_budget||0))}</b></div>
    <div class="budget-progress-head"><span>Total Pemakaian Budget</span><b>${percent.toFixed(1)}%</b></div>
    <div class="budget-progress"><i class="${projectBudgetProgressClass(percent)}" style="width:${width}%"></i></div>
    <button class="secondary" onclick="loadProjectCostRealizationDetails(${item.project_id})">Lihat Rincian Realisasi Biaya</button>`;
}
async function loadProjectCostRealizationDetails(projectId){
  try{
    const data=await api('/api/project-cost-realizations?project_id='+encodeURIComponent(projectId));
    projectCostDetailTitle.textContent=`${data.project.code} - ${data.project.name}`;
    const items=data.items||[];
    projectCostDetailBody.innerHTML=items.length?items.map(item=>`<tr>
      <td>${accessEscape(item.journal_date)}</td>
      <td><b>${accessEscape(item.journal_no)}</b></td>
      <td>${accessEscape(item.source_type||'MANUAL')}</td>
      <td>${accessEscape(item.reference_no||'-')}</td>
      <td>${accessEscape(item.account_code)} - ${accessEscape(item.account_name)}</td>
      <td>${accessEscape(item.department_name||'-')}</td>
      <td>${accessEscape(item.description||'-')}</td>
      <td class="number-cell">${rup(Number(item.debit||0))}</td>
      <td class="number-cell">${rup(Number(item.credit||0))}</td>
      <td class="number-cell"><b>${rup(Number(item.amount||0))}</b></td>
    </tr>`).join(''):'<tr><td colspan="10">Belum ada biaya proyek dari transaksi lain.</td></tr>';
    const summary=data.summary||{};
    projectCostDetailFoot.innerHTML=`<tr><th colspan="7">TOTAL</th><th>${rup(Number(summary.total_debit||0))}</th><th>${rup(Number(summary.total_credit||0))}</th><th>${rup(Number(summary.net_expense||0))}</th></tr>`;
  }catch(error){
    msg(projectBudgetMsg,error.message,false);
  }
}
async function loadProjectBudgets(){
  try{
    const [budgets,projects,overview]=await Promise.all([
      api('/api/project-budgets'),
      api('/api/projects?active=1'),
      api('/api/project-budgets/overview')
    ]);
    projectBudgetRecords=budgets.items||[];
    projectBudgetProjects=projects.items||[];
    const selected=projectBudgetProject.value;
    projectBudgetProject.innerHTML='<option value="">Pilih Proyek</option>'+
      projectBudgetProjects.map(item=>`<option value="${item.id}">${accessEscape(item.code)} - ${accessEscape(item.name)}</option>`).join('');
    if(selected&&projectBudgetProjects.some(item=>String(item.id)===String(selected))){
      projectBudgetProject.value=selected;
    }
    renderProjectBudgetSummary(overview.summary||{});
    projectBudgetCount.textContent=projectBudgetRecords.length+' budget';
    projectBudgetBody.innerHTML=projectBudgetRecords.length?projectBudgetRecords.map(item=>`
      <tr>
        <td><b>${accessEscape(item.project_code)}</b><br>${accessEscape(item.project_name)}</td>
        <td>${accessEscape(item.customer_name||'-')}</td>
        <td class="number-cell">${rup(Number(item.material_budget||0))}</td>
        <td class="number-cell">${rup(Number(item.realization_material||0))}</td>
        <td class="number-cell">${rup(Number(item.expense_budget||0))}</td>
        <td class="number-cell">${rup(Number(item.realization_expense||0))}</td>
        <td class="number-cell"><b>${rup(Number(item.total_budget||0))}</b></td>
        <td class="number-cell">${rup(Number(item.realization_total||0))}</td>
        <td class="number-cell">${rup(Number(item.remaining_budget||0))}</td>
        <td><span class="budget-badge ${projectBudgetProgressClass(Number(item.usage_percent||0))}">${Number(item.usage_percent||0).toFixed(1)}%</span></td>
        <td class="actions-cell">
          <button onclick="editProjectBudget(${item.id})">Edit</button>
          <button class="secondary" onclick="selectProjectBudget(${item.id})">Lihat</button>
          <button class="danger" onclick="deleteProjectBudget(${item.id})">Hapus</button>
        </td>
      </tr>`).join(''):'<tr><td colspan="11">Belum ada budget proyek.</td></tr>';
    if(projectBudgetRecords.length&&!projectBudgetId.value){
      renderProjectBudgetControl(projectBudgetRecords[0]);
    }
    msg(projectBudgetMsg,'Budget proyek berhasil dimuat.');
    formatAllNumberInputs();
  }catch(error){
    msg(projectBudgetMsg,error.message,false);
  }
}
function resetProjectBudgetForm(){
  projectBudgetId.value='';
  projectBudgetProject.value='';
  projectBudgetMaterial.value='0';
  projectBudgetExpense.value='0';
  projectBudgetTotal.value='0';
  projectBudgetNotes.value='';
  projectBudgetProject.disabled=false;
  projectBudgetFormTitle.textContent='Tambah Budget Proyek';
  renderProjectBudgetControl(null);
  formatAllNumberInputs();
}
function editProjectBudget(id){
  const item=projectBudgetRecords.find(row=>row.id===id);
  if(!item)return;
  projectBudgetId.value=item.id;
  projectBudgetProject.value=item.project_id;
  projectBudgetProject.disabled=true;
  projectBudgetMaterial.value=String(item.material_budget||0);
  projectBudgetExpense.value=String(item.expense_budget||0);
  projectBudgetNotes.value=item.notes||'';
  projectBudgetFormTitle.textContent='Edit Budget: '+item.project_name;
  syncProjectBudgetTotal();
  renderProjectBudgetControl(item);
  window.scrollTo({top:0,behavior:'smooth'});
}
function selectProjectBudget(id){
  const item=projectBudgetRecords.find(row=>row.id===id);
  renderProjectBudgetControl(item);
}
async function saveProjectBudget(){
  try{
    const payload={
      project_id:projectBudgetProject.value||null,
      material_budget:projectBudgetNumber(projectBudgetMaterial.value),
      expense_budget:projectBudgetNumber(projectBudgetExpense.value),
      notes:projectBudgetNotes.value
    };
    if(!payload.project_id)throw Error('Pilih proyek terlebih dahulu.');
    if(payload.material_budget<0||payload.expense_budget<0)throw Error('Budget tidak boleh minus.');
    const id=projectBudgetId.value;
    await api(id?'/api/project-budgets/'+id:'/api/project-budgets',{
      method:id?'PUT':'POST',body:JSON.stringify(payload)
    });
    msg(projectBudgetMsg,id?'Budget proyek berhasil diperbarui.':'Budget proyek berhasil dibuat.');
    resetProjectBudgetForm();
    await Promise.all([loadProjectBudgets(),loadProjects()]);
  }catch(error){
    msg(projectBudgetMsg,error.message,false);
  }
}
async function deleteProjectBudget(id){
  const item=projectBudgetRecords.find(row=>row.id===id);
  if(!item)return;
  if(!confirm(`Hapus budget untuk ${item.project_name}?`))return;
  try{
    await api('/api/project-budgets/'+id,{method:'DELETE'});
    msg(projectBudgetMsg,'Budget proyek berhasil dihapus.');
    resetProjectBudgetForm();
    await Promise.all([loadProjectBudgets(),loadProjects()]);
  }catch(error){
    msg(projectBudgetMsg,error.message,false);
  }
}

async function loadAudit(){try{let d=await api('/api/audit?limit=40');auditBody.innerHTML=d.items.map(x=>`<tr><td>${x.created_at}</td><td>${x.username||'-'}</td><td>${x.action}</td><td>${x.client_ip||'-'}</td></tr>`).join('')}catch(e){}}
async function refreshLoginDatabase(){try{const h=await fetch('/api/health').then(r=>r.json());if(window.loginDatabasePath)loginDatabasePath.textContent=h.database||'-'}catch(e){if(window.loginDatabasePath)loginDatabasePath.textContent='Server sedang memuat database...'}}
async function logout(){stopHeartbeat();try{if(token)await api('/api/logout',{method:'POST',body:JSON.stringify({})})}catch(e){}localStorage.removeItem('slp_token');token='';document.getElementById('app').classList.add('hidden');document.getElementById('app').setAttribute('aria-hidden','true');document.getElementById('authShell').classList.remove('hidden');document.getElementById('authShell').setAttribute('aria-hidden','false');showAuthPane('login');await refreshLoginDatabase();window.scrollTo(0,0)}

let asmEditId=null;let asmMaterialRows=[],asmCostRows=[],asmOutputRows=[],asmCurrentId=null;
let asmProductsCache=[],asmWarehousesCache=[],asmAccountsCache=[];
function asmProductOptions(selected=''){
  const arr=(asmProductsCache||[]).filter(x=>x.product_type==='STOCK'&&x.is_active!==false);
  return '<option value="">Pilih barang</option>'+arr.map(x=>`<option value="${x.id}" ${String(x.id)===String(selected)?'selected':''}>${accessEscape(x.sku)} · ${accessEscape(x.name)}</option>`).join('');
}
function asmAccountOptions(selected='',wip=false){
  const arr=(asmAccountsCache||[]).filter(x=>x.is_active!==false&&(wip?x.account_type==='ASSET':true));
  return '<option value="">Pilih akun</option>'+arr.map(x=>`<option value="${x.id}" ${String(x.id)===String(selected)?'selected':''}>${accessEscape(x.code)} · ${accessEscape(x.name)}</option>`).join('');
}
async function loadAssemblyMasters(){
  const [productResponse,warehouseResponse,accountResponse]=await Promise.all([
    api('/api/products?active=1'),
    api('/api/warehouses?active=1'),
    api('/api/coa?active=1')
  ]);
  asmProductsCache=(productResponse.items||[]).filter(x=>!x.service_id&&x.product_type==='STOCK'&&x.is_active!==false);
  asmWarehousesCache=(warehouseResponse.items||[]).filter(x=>x.is_active!==false);
  asmAccountsCache=(accountResponse.items||[]).filter(x=>x.is_active!==false);
  asmWarehouse.innerHTML='<option value="">Pilih gudang</option>'+asmWarehousesCache.map(x=>`<option value="${x.id}">${accessEscape(x.code||'')} · ${accessEscape(x.name)}</option>`).join('');
  asmWip.innerHTML=asmAccountOptions('',true);
  renderAsmMaterials();renderAsmCosts();
}
function renderAsmMaterials(){asmMaterials.innerHTML=asmMaterialRows.map((r,i)=>`<tr><td><select onchange="asmMaterialRows[${i}].product_id=this.value">${asmProductOptions(r.product_id)}</select></td><td><input type="number" min="0.0001" step="0.0001" value="${r.qty||1}" onchange="asmMaterialRows[${i}].qty=this.value"></td><td><button class="danger" onclick="asmMaterialRows.splice(${i},1);renderAsmMaterials()">Hapus</button></td></tr>`).join('')}
function renderAsmCosts(){asmCosts.innerHTML=asmCostRows.map((r,i)=>`<tr><td><select onchange="asmCostRows[${i}].account_id=this.value">${asmAccountOptions(r.account_id,false)}</select></td><td><input value="${accessEscape(r.description||'')}" onchange="asmCostRows[${i}].description=this.value"></td><td><input type="number" min="0" step="0.01" value="${r.amount||0}" onchange="asmCostRows[${i}].amount=this.value"></td><td><button class="danger" onclick="asmCostRows.splice(${i},1);renderAsmCosts()">Hapus</button></td></tr>`).join('')}
function addAsmMaterial(){asmMaterialRows.push({product_id:'',qty:1});renderAsmMaterials()} function addAsmCost(){asmCostRows.push({account_id:'',description:'',amount:0});renderAsmCosts()}
async function openAssembly(){
  page('assembly');
  asmDate.value=new Date().toISOString().slice(0,10);
  try{
    await loadAssemblyMasters();
    if(!asmMaterialRows.length)addAsmMaterial();
    else renderAsmMaterials();
    renderAsmCosts();
    await loadAssemblies();
    if(!asmWarehousesCache.length)msg(asmMsg,'Belum ada gudang aktif. Tambahkan gudang terlebih dahulu.',false);
    else if(!asmProductsCache.length)msg(asmMsg,'Belum ada barang stok aktif yang dapat dipakai sebagai bahan baku.',false);
    else if(!asmAccountsCache.some(x=>x.account_type==='ASSET'))msg(asmMsg,'Belum ada akun aset aktif untuk Persediaan Dalam Proses.',false);
    else msg(asmMsg,'');
  }catch(e){msg(asmMsg,'Gagal memuat master Assembly: '+e.message,false)}
}
let asmSaving=false;
async function saveAssembly(){if(asmSaving)return;asmSaving=true;try{
  if(!asmWarehouse.value)throw new Error('Pilih gudang terlebih dahulu.');
  if(!asmWip.value)throw new Error('Pilih akun Persediaan Dalam Proses terlebih dahulu.');
  if(!asmMaterialRows.length||asmMaterialRows.some(x=>!x.product_id||Number(x.qty)<=0))throw new Error('Pilih barang dan isi qty bahan baku dengan benar.');
  let payload={assembly_date:asmDate.value,warehouse_id:asmWarehouse.value,wip_account_id:asmWip.value,notes:asmNotes.value,materials:asmMaterialRows,costs:asmCostRows};let d=await api(asmEditId?'/api/assemblies/'+asmEditId:'/api/assemblies',{method:asmEditId?'PUT':'POST',body:JSON.stringify(payload)});msg(asmMsg,`Assembly ${d.result?.assembly_no||d.item?.assembly_no||''} berhasil ${asmEditId?'diubah':'diposting'}.`);asmEditId=null;asmNotes.value='';asmMaterialRows=[];asmCostRows=[];addAsmMaterial();renderAsmCosts();await Promise.all([loadAssemblies(),loadProducts(),loadBalances()]);setTimeout(()=>openAssembly(),250)}catch(e){msg(asmMsg,e.message,false)}finally{asmSaving=false}}
async function loadAssemblies(){try{let d=await api('/api/assemblies');let open=d.items.filter(x=>x.status!=='FINISHED');let fin=d.items.filter(x=>x.status==='FINISHED');asmList.innerHTML=open.map(x=>`<tr><td>${x.assembly_date}</td><td>${accessEscape(x.assembly_no)}</td><td>${accessEscape(x.warehouse_name)}</td><td>${rup(x.material_cost)}</td><td>${rup(x.additional_cost)}</td><td><b>${rup(x.total_cost)}</b></td><td>${x.status}</td><td>${x.status==='OPEN'?`<button onclick="openAssemblyFinish(${x.id})">Finishing</button> <button class="secondary" onclick="editAssembly(${x.id})">Edit</button> <button class="danger" onclick="deleteAssembly(${x.id})">Hapus</button>`:`<button class="secondary" onclick="viewAssembly(${x.id})">Detail</button>`}</td></tr>`).join('');asmFinishList.innerHTML=fin.map(x=>`<tr><td>${x.finished_at||'-'}</td><td>${accessEscape(x.assembly_no)}</td><td>${accessEscape(x.warehouse_name)}</td><td>${rup(x.total_cost)}</td><td><button class="secondary" onclick="viewAssembly(${x.id})">Detail</button></td><td><button onclick="editAssemblyFinish(${x.id})">Edit</button> <button class="danger" onclick="deleteAssemblyFinish(${x.id})">Hapus</button></td></tr>`).join('')}catch(e){msg(asmMsg,e.message,false)}}
async function viewAssembly(id){let d=await api('/api/assemblies/'+id);alert(`${d.assembly_no}
Material: ${rup(d.material_cost)}
Biaya: ${rup(d.additional_cost)}
Total: ${rup(d.total_cost)}
Output: ${d.outputs.map(x=>x.product_name+' '+x.qty).join(', ')||'-'}`)}
async function editAssembly(id){let d=await api('/api/assemblies/'+id);asmEditId=id;asmDate.value=d.assembly_date;asmWarehouse.value=d.warehouse_id;asmWip.value=d.wip_account_id;asmNotes.value=d.notes||'';asmMaterialRows=d.materials.map(x=>({product_id:x.product_id,qty:x.qty}));asmCostRows=d.costs.map(x=>({account_id:x.account_id,description:x.description,amount:x.amount}));renderAsmMaterials();renderAsmCosts();window.scrollTo({top:0,behavior:'smooth'})}
async function deleteAssembly(id){if(!confirm('Batalkan assembly ini? Stok dan jurnal akan dibalik.'))return;try{await api('/api/assemblies/'+id,{method:'DELETE'});await loadAssemblies();await loadProducts();await loadBalances()}catch(e){alert(e.message)}}
async function editAssemblyFinish(id){asmCurrentId=id;let d=await api('/api/assemblies/'+id);asmFinishNo.textContent=d.assembly_no;asmFinishDate.value=d.finished_at||new Date().toISOString().slice(0,10);asmOutputRows=d.outputs.map(x=>({product_id:x.product_id,qty:x.qty,allocation_percent:x.allocation_percent}));renderAsmOutputs();asmFinishMsg.dataset.edit='1';page('assemblyFinish')}
async function deleteAssemblyFinish(id){if(!confirm('Batalkan penyelesaian assembly? Stok barang jadi dan jurnal finishing akan dibalik.'))return;try{await api('/api/assemblies/'+id+'/finish',{method:'DELETE'});await loadAssemblies();await loadProducts();await loadBalances()}catch(e){alert(e.message)}}
function renderAsmOutputs(){asmOutputs.innerHTML=asmOutputRows.map((r,i)=>`<tr><td><select onchange="asmOutputRows[${i}].product_id=this.value">${asmProductOptions(r.product_id)}</select></td><td><input type="number" min="0.0001" step="0.0001" value="${r.qty||1}" onchange="asmOutputRows[${i}].qty=this.value"></td><td><input type="number" min="0" max="100" step="0.0001" placeholder="Otomatis" value="${r.allocation_percent??''}" onchange="asmOutputRows[${i}].allocation_percent=this.value"></td><td><button class="danger" onclick="asmOutputRows.splice(${i},1);renderAsmOutputs()">Hapus</button></td></tr>`).join('')}
function addAsmOutput(){asmOutputRows.push({product_id:'',qty:1,allocation_percent:''});renderAsmOutputs()}
async function openAssemblyFinish(id){asmCurrentId=id;let d=await api('/api/assemblies/'+id);asmFinishNo.textContent=d.assembly_no;asmFinishDate.value=new Date().toISOString().slice(0,10);asmOutputRows=[];addAsmOutput();page('assemblyFinish')}
async function finishAssembly(){try{let editing=asmFinishMsg.dataset.edit==='1';let d=await api(`/api/assemblies/${asmCurrentId}/finish`,{method:editing?'PUT':'POST',body:JSON.stringify({finish_date:asmFinishDate.value,outputs:asmOutputRows})});asmFinishMsg.dataset.edit='';msg(asmFinishMsg,`Finishing ${d.result?.assembly_no||d.item?.assembly_no||''} berhasil.`);await Promise.all([loadProducts(),loadBalances()]);setTimeout(()=>openAssembly(),600)}catch(e){msg(asmFinishMsg,e.message,false)}}

async function requestDatabaseSwitch(){alert('Versi Web menggunakan database server yang dikelola dari Railway Volume.')}
installPageCloseButtons();
refreshLoginDatabase();
(async()=>{if(token)try{let d=await api('/api/me');openApp(d.user)}catch(e){localStorage.removeItem('slp_token');refreshLoginDatabase()}})();
let importBatch=0,importPreviewItems=[],importCoaItems=[],importCustomerItems=[],importSupplierItems=[];
function setCreditUi(){if(window.saleCashAccount){saleCashAccount.disabled=salePayment.value==='CREDIT';if(salePayment.value==='CREDIT')saleCashAccount.value=''}if(window.purchaseCashAccount){purchaseCashAccount.disabled=purchasePayment.value==='CREDIT';if(purchasePayment.value==='CREDIT')purchaseCashAccount.value=''}}
document.addEventListener('change',e=>{if(e.target?.id==='salePayment'||e.target?.id==='purchasePayment')setCreditUi()});
async function openPrint(k,id){
 if(k!=='sales-invoice'){window.open('/print/'+k+'/'+id+'?token='+encodeURIComponent(token),'_blank');return}
 try{const d=await api('/api/flexible-invoice-templates?active=1'),items=d.items||[];if(!items.length){window.open('/print/sales-invoice/'+id+'?token='+encodeURIComponent(token),'_blank');return}
 let chosen=items.find(x=>x.is_default)||items[0];if(items.length>1){const list=items.map((x,i)=>`${i+1}. ${x.name}${x.is_default?' [Default]':''}`).join('\n');const ans=prompt('Pilih template invoice:\n'+list,String(items.indexOf(chosen)+1));if(ans===null)return;const n=Number(ans);if(Number.isInteger(n)&&n>=1&&n<=items.length)chosen=items[n-1]}
 window.open('/print/sales-invoice-flex/'+id+'?template_id='+encodeURIComponent(chosen.id)+'&token='+encodeURIComponent(token),'_blank')}catch(e){alert(e.message)}
}
function chartColors(){return ['#2563eb','#10b981','#f59e0b','#8b5cf6','#ef4444','#06b6d4','#84cc16']}
function drawPie(canvas,rows,opts={}){const ctx=canvas.getContext('2d'),W=canvas.width,H=canvas.height,colors=chartColors(),vals=rows.map(x=>Math.max(0,Math.abs(Number(x.value)||0))),sum=vals.reduce((a,b)=>a+b,0);ctx.clearRect(0,0,W,H);if(!sum){ctx.fillStyle='#718096';ctx.font='600 14px Arial';ctx.textAlign='center';ctx.fillText('Belum ada data',W/2,H/2);return}const cx=opts.cx||W*.42,cy=opts.cy||H*.49,r=opts.r||Math.min(W,H)*.29,inner=opts.inner??r*.48;let angle=-Math.PI/2;rows.forEach((item,i)=>{const next=angle+(vals[i]/sum)*Math.PI*2;ctx.beginPath();ctx.arc(cx,cy,r,angle,next);if(inner>0)ctx.arc(cx,cy,inner,next,angle,true);else ctx.lineTo(cx,cy);ctx.closePath();ctx.fillStyle=item.color||colors[i%colors.length];ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();angle=next});if(opts.centerLabel){ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle='#64748b';ctx.font='600 12px Arial';ctx.fillText(opts.centerLabel,cx,cy-10);ctx.fillStyle=opts.centerColor||'#0f766e';ctx.font='700 15px Arial';ctx.fillText(opts.centerValue||'',cx,cy+12)}}
function renderPieLegend(el,rows,keyFormat='number'){const colors=chartColors(),sum=rows.reduce((a,x)=>a+Math.abs(Number(x.value)||0),0)||1;el.innerHTML=rows.map((x,i)=>{const value=Number(x.value)||0,pct=Math.abs(value)/sum*100,color=x.color||colors[i%colors.length],formatted=keyFormat==='money'?rup(value):new Intl.NumberFormat('id-ID',{maximumFractionDigits:2}).format(value);return `<div class="mini-pie-item"><span><i style="background:${color}"></i><em>${x.name} · ${pct.toFixed(1)}%</em></span><b>${formatted}</b></div>`}).join('')||'<div class="mini-pie-item">Belum ada data</div>'}
function drawProfitLossChart(pl){const profit=Number(pl.profit||0),rows=[{name:'Pendapatan',value:Number(pl.revenue||0),color:'#2563eb'},{name:'HPP',value:Number(pl.cogs||0),color:'#f59e0b'},{name:'Beban',value:Number(pl.expense||0),color:'#ef4444'},{name:profit<0?'Rugi':'Laba',value:profit,color:profit<0?'#991b1b':'#10b981'}];drawPie(pie,rows,{cx:205,cy:164,r:105,inner:54,centerLabel:'Laba / Rugi',centerValue:rup(profit),centerColor:profit<0?'#b91c1c':'#047857'});pieInfo.innerHTML=rows.map(x=>`<div class="pl-item"><span><i style="background:${x.color}"></i>${x.name}</span><b>${rup(x.value)}</b></div>`).join('')}
function drawTopPie(canvas,legend,data,key,format){const rows=(data||[]).slice(0,5).map(x=>({name:x.name||'-',value:Number(x[key]||0)}));drawPie(canvas,rows,{cx:210,cy:132,r:92,inner:40});renderPieLegend(legend,rows,format)}
function dueStatus(days){days=Number(days);if(days<0)return `<span class="badge danger">Terlambat ${Math.abs(days)} hari</span>`;if(days===0)return '<span class="badge warn">Jatuh tempo hari ini</span>';return `<span class="badge">${days} hari lagi</span>`}
async function loadDash(){let d=await api('/api/dashboard-analytics');drawProfitLossChart(d.profit_loss);drawTopPie(topItemsPie,topItems,d.top_items,'qty','number');drawTopPie(topSalesPie,topSales,d.top_sales,'value','money');let ar=[...(d.overdue_receivables||[]).map(x=>({...x,days_left:Math.floor((new Date(x.due_date+'T00:00:00')-new Date(d.period.to+'T00:00:00'))/86400000)})),...(d.receivables_due_week||[])];let ap=[...(d.overdue_payables||[]).map(x=>({...x,days_left:Math.floor((new Date(x.due_date+'T00:00:00')-new Date(d.period.to+'T00:00:00'))/86400000)})),...(d.payables_due_week||[])];dueAr.innerHTML=ar.map(x=>`<tr><td>${x.number}<br>${x.partner}<br>${dueStatus(x.days_left)}</td><td>${x.due_date}</td><td>${rup(x.amount)}</td></tr>`).join('')||'<tr><td>Belum ada</td></tr>';dueAp.innerHTML=ap.map(x=>`<tr><td>${x.number}<br>${x.partner}<br>${dueStatus(x.days_left)}</td><td>${x.due_date}</td><td>${rup(x.amount)}</td></tr>`).join('')||'<tr><td>Belum ada</td></tr>';lowSt.innerHTML=d.low_stock.map(x=>`<tr><td>${x.sku} ${x.name}</td><td>${x.stock}/${x.minimum_stock}</td></tr>`).join('')||'<tr><td>Belum ada</td></tr>';deadSt.innerHTML=d.dead_stock.map(x=>`<tr><td>${x.sku} ${x.name}</td><td>${x.stock}</td><td>${x.last_out||'Belum pernah keluar'}</td></tr>`).join('')||'<tr><td>Belum ada</td></tr>'}
function coaOpts(selected=''){
  return '<option value="">-- Pilih Akun --</option>'+importCoaItems.map(x=>`<option value="${x.id}" ${String(x.id)===String(selected)?'selected':''}>${x.code} - ${x.name} (${accountTypeLabel(x.display_type)})</option>`).join('')
}
function importPartnerOptionsForAccount(accountId,selected=''){
  const account=importCoaItems.find(x=>String(x.id)===String(accountId));
  const subtype=account?.display_type||account?.account_subtype||'';
  const list=subtype==='RECEIVABLE'?importCustomerItems:subtype==='PAYABLE'?importSupplierItems:[];
  if(!list.length)return {required:false,html:'<span class="muted">Tidak diperlukan</span>'};
  const label=subtype==='RECEIVABLE'?'Pelanggan':'Pemasok';
  return {required:true,html:`<select class="import-partner" onchange="statusMap()"><option value="">-- Pilih ${label} --</option>${list.map(x=>`<option value="${x.id}" ${String(x.id)===String(selected)?'selected':''}>${x.code} - ${x.name}</option>`).join('')}</select>`};
}
function accountChanged(id){
  const coa=document.querySelector(`.import-coa[data-id="${id}"]`);
  const cell=document.querySelector(`.import-partner-cell[data-id="${id}"]`);
  if(cell)cell.innerHTML=importPartnerOptionsForAccount(coa?.value||'').html;
  statusMap();
}
function removeImportRow(id){importPreviewItems=importPreviewItems.filter(x=>String(x.id)!==String(id));renderRows();msg(importMsg,'Baris dihapus dari preview dan tidak akan diposting.')}
function renderRows(){
  importRows.innerHTML=importPreviewItems.map(x=>{const s=x.suggestion||null;const txt=s?`${s.account_code} - ${s.account_name}`:'Tidak ada saran';const reason=s?`${s.reason} · keyakinan ${Math.round((s.score||0)*100)}%`:'Pilih akun secara manual';const accountId=s?.counter_coa_id||'';const partner=importPartnerOptionsForAccount(accountId);return `<tr><td><input class="import-check" data-id="${x.id}" type="checkbox" checked onchange="statusMap()"></td><td>${x.transaction_date}</td><td class="import-desc">${x.description}</td><td>${x.credit?rup(x.credit):'-'}</td><td>${x.debit?rup(x.debit):'-'}</td><td>${x.balance==null?'-':rup(x.balance)}</td><td><b>${txt}</b><br><small>${reason}</small></td><td><select class="import-coa" data-id="${x.id}" onchange="accountChanged(${x.id})">${coaOpts(accountId)}</select></td><td class="import-partner-cell" data-id="${x.id}">${partner.html}</td><td><button class="danger" onclick="removeImportRow(${x.id})">Hapus Baris</button></td></tr>`}).join('');statusMap()
}
function toggleAllImportRows(v){document.querySelectorAll('.import-check').forEach(x=>x.checked=v);statusMap()}
function applyDefaultImportCoa(){if(!importDefaultCoa.value)return msg(importMsg,'Pilih akun default.',false);document.querySelectorAll('.import-check:checked').forEach(x=>{const c=document.querySelector(`.import-coa[data-id="${x.dataset.id}"]`);c.value=importDefaultCoa.value});statusMap()}
function statusMap(){
  const rows=[...document.querySelectorAll('.import-check:checked')];
  let mapped=0,partnerReady=0;
  rows.forEach(x=>{
    const id=x.dataset.id,coa=document.querySelector(`.import-coa[data-id="${id}"]`);
    if(!coa?.value)return;
    mapped++;
    const account=importCoaItems.find(a=>String(a.id)===String(coa.value));
    const subtype=account?.display_type||account?.account_subtype||'';
    if(!['RECEIVABLE','PAYABLE'].includes(subtype)||document.querySelector(`.import-partner-cell[data-id="${id}"] .import-partner`)?.value)partnerReady++;
  });
  importMappingStatus.textContent=`${rows.length} dipilih · ${mapped} dimapping · ${partnerReady} partner valid · ${importPreviewItems.length} tersisa di preview`;
  postImportBtn.disabled=!importBatch||!importCash.value||!rows.length||mapped!==rows.length||partnerReady!==rows.length;
}
async function loadSmartImportMasters(){
  const [bankData,coaData,customerData,supplierData]=await Promise.all([
    api('/api/cash-accounts?active=1'),
    api('/api/coa?active=1'),
    api('/api/customers?active=1'),
    api('/api/suppliers?active=1')
  ]);
  importCoaItems=(coaData.items||[]).filter(x=>x.display_type!=='CASH_BANK');
  importCustomerItems=customerData.items||[];
  importSupplierItems=supplierData.items||[];
  const bankItems=bankData.items||[];
  importCash.innerHTML=bankItems.length
    ?bankItems.map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('')
    :'<option value="">Belum ada akun bank</option>';
  importCash.disabled=!bankItems.length;
  importDefaultCoa.innerHTML='<option value="">-- Akun Default --</option>'+
    importCoaItems.map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');
  statusMap();
}
async function previewBankPdf(){try{let f=pdfBankFile.files[0];if(!f)throw Error('Pilih PDF.');let a=new Uint8Array(await f.arrayBuffer()),b='',n=32768;for(let i=0;i<a.length;i+=n)b+=String.fromCharCode(...a.subarray(i,i+n));msg(importMsg,'Membaca PDF...');let d=await api('/api/bank-import/pdf-preview',{method:'POST',body:JSON.stringify({pdf_base64:btoa(b),file_name:f.name})});importBatch=d.result.batch_id;importPreviewItems=d.result.items;pdfImportSummary.innerHTML=`${d.result.row_count} transaksi · Bank Masuk ${rup(d.result.credit_total)} · Bank Keluar ${rup(d.result.debit_total)}`;renderRows();msg(importMsg,'Preview berhasil. Mapping akun lawan per baris.')}catch(e){msg(importMsg,e.message,false)}}
function mappings(){
  const result=[];
  document.querySelectorAll('.import-check:checked').forEach(x=>{
    const id=x.dataset.id;
    const coa=document.querySelector(`.import-coa[data-id="${id}"]`);
    if(!coa.value)throw Error(`Baris ${id} belum dimapping.`);
    const account=importCoaItems.find(a=>String(a.id)===String(coa.value));
    const subtype=account?.display_type||account?.account_subtype||'';
    const partnerEl=document.querySelector(`.import-partner-cell[data-id="${id}"] .import-partner`);
    if(['RECEIVABLE','PAYABLE'].includes(subtype)&&!partnerEl?.value)throw Error(`Baris ${id}: ${subtype==='RECEIVABLE'?'pelanggan':'pemasok'} wajib dipilih.`);
    result.push({
      row_id:Number(id),
      counter_coa_id:Number(coa.value),
      partner_id:partnerEl?.value?Number(partnerEl.value):null
    });
  });
  return result;
}
async function postMappedBank(){try{let m=mappings();if(!m.length)throw Error('Tidak ada baris dipilih.');let d=await api('/api/bank-import/post',{method:'POST',body:JSON.stringify({batch_id:importBatch,cash_account_id:+importCash.value,mappings:m})});msg(importMsg,`${d.result.posted_count} transaksi berhasil diposting.`);let ids=new Set(m.map(x=>x.row_id));importPreviewItems=importPreviewItems.filter(x=>!ids.has(x.id));if(importPreviewItems.length)renderRows();else importRows.innerHTML='<tr><td colspan="10">Semua transaksi telah diposting.</td></tr>'}catch(e){msg(importMsg,e.message,false)}}
pdfBankFile?.addEventListener('change',()=>{let f=pdfBankFile.files[0];pdfFileStatus.textContent=f?`${f.name} · ${(f.size/1024).toFixed(1)} KB`:'Belum ada file dipilih.';previewPdfBtn.disabled=!f});
importCash?.addEventListener('change',statusMap);

let documentDesignerItems=[],activeDocumentType='SALES_INVOICE';
const documentTypeLabels={SALES_INVOICE:'Invoice Penjualan',DELIVERY_ORDER:'Surat Jalan',GOODS_RECEIPT:'Good Receive',PURCHASE_INVOICE:'Faktur Pembelian'};
function designerEscape(value){return String(value??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
async function openDocumentDesigner(){page('docDesign');await loadDocumentDesigner()}
async function loadDocumentDesigner(){
 try{
  const d=await api('/api/document-templates');documentDesignerItems=d.items||[];
  if(!documentDesignerItems.length)throw Error('Template dokumen belum tersedia.');
  if(!documentDesignerItems.some(x=>x.document_type===activeDocumentType))activeDocumentType=documentDesignerItems[0].document_type;
  document.querySelectorAll('#docDesignerTabs button').forEach(btn=>{
    btn.classList.toggle('active',btn.dataset.docType===activeDocumentType);
    btn.onclick=()=>selectDocumentTemplate(btn.dataset.docType);
  });
  renderDocumentDesignerEditor();renderDocumentPreview();
  msg(docDesignerMessage,'Template siap diedit.',true)
 }catch(e){msg(docDesignerMessage,e.message,false);docDesignerEditor.innerHTML='';docDesignerPreview.innerHTML=''}
}
function selectDocumentTemplate(dtype){activeDocumentType=dtype;document.querySelectorAll('#docDesignerTabs button').forEach(btn=>btn.classList.toggle('active',btn.dataset.docType===dtype));renderDocumentDesignerEditor();renderDocumentPreview()}
function activeDocumentTemplate(){return documentDesignerItems.find(x=>x.document_type===activeDocumentType)||null}
function renderDocumentDesignerEditor(){
 const t=activeDocumentTemplate();if(!t){docDesignerEditor.innerHTML='<p>Template tidak ditemukan.</p>';return}
 const o=t.options||{},noPrice=['DELIVERY_ORDER','GOODS_RECEIPT'].includes(t.document_type),w=o.column_widths||{};
 docDesignerEditor.innerHTML=`<div class="card"><h3>${designerEscape(documentTypeLabels[t.document_type]||t.document_type)}</h3>
 <div class="field-grid two">
 <label class="field"><span>Judul Dokumen *</span><input id="ddTitle" value="${designerEscape(t.title||'')}"></label>
 <label class="field"><span>Ukuran Kertas</span><select id="ddPaper"><option value="A5">A5</option><option value="A4">A4</option><option value="LETTER">Letter</option><option value="STRUK58">Struk 58 mm</option><option value="STRUK80">Struk 80 mm</option></select></label>
 </div>
 <label class="field"><span>Teks Header</span><textarea id="ddHeader" rows="3">${designerEscape(t.header_text||'')}</textarea></label>
 <label class="field"><span>Catatan Khusus</span><textarea id="ddSpecial" rows="3">${designerEscape(o.special_note||'')}</textarea></label>
 <label class="field"><span>Teks Footer</span><textarea id="ddFooter" rows="3">${designerEscape(t.footer_text||'')}</textarea></label>
 <div class="field-grid two"><label class="field"><span>Penanda Tangan Kiri</span><input id="ddLeftSigner" value="${designerEscape(o.left_signer||'Disiapkan oleh')}"></label><label class="field"><span>Penanda Tangan Kanan</span><input id="ddRightSigner" value="${designerEscape(o.right_signer||'Diterima oleh')}"></label></div>
 <div class="designer-checks">
 ${designerCheck('ddShowLogo','Tampilkan logo perusahaan',!!t.show_logo)}
 ${designerCheck('ddShowPrices','Tampilkan harga',!!t.show_prices,noPrice)}
 ${designerCheck('ddShowSku','Tampilkan kode/SKU',o.show_sku!==false)}
 ${designerCheck('ddShowUnit','Tampilkan satuan',o.show_unit!==false)}
 ${designerCheck('ddShowWarehouse','Tampilkan gudang',!!o.show_warehouse)}
 ${designerCheck('ddShowDiscount','Tampilkan diskon',!!o.show_discount,noPrice)}
 ${designerCheck('ddShowTax','Tampilkan pajak',!!o.show_tax,noPrice)}
 ${designerCheck('ddShowPaymentTerms','Tampilkan termin pembayaran',o.show_payment_terms!==false,noPrice)}
 ${designerCheck('ddShowPaymentAccountNote','Tampilkan catatan rekening pembayaran',!!o.show_payment_account_note,noPrice)}
 ${designerCheck('ddShowPartnerContact','Tampilkan alamat & kontak pelanggan/pemasok',o.show_partner_contact!==false,false)}
 ${designerCheck('ddShowAmountWords','Tampilkan nominal terbilang',o.show_amount_words!==false,noPrice)}
 </div>
 <label class="field"><span>Catatan Rekening Pembayaran</span><textarea id="ddPaymentAccountNote" rows="3" placeholder="Contoh: Transfer ke BCA 123456789 a.n. PT Contoh">${designerEscape(o.payment_account_note||'')}</textarea></label>
 <div class="designer-widths"><h4>Lebar Kolom Tabel</h4><p class="muted">Naikkan angka untuk memperbesar kolom, kecilkan angka untuk mempersempit. Sistem otomatis menyesuaikan total lebar ke halaman.</p><div class="designer-width-grid">
 ${designerWidthInput('ddWidthNo','No.',w.no??5)}
 ${designerWidthInput('ddWidthSku','SKU',w.sku??13)}
 ${designerWidthInput('ddWidthDescription','Deskripsi',w.description??37)}
 ${designerWidthInput('ddWidthQty','Qty',w.qty??9)}
 ${designerWidthInput('ddWidthUnit','Satuan',w.unit??10)}
 ${designerWidthInput('ddWidthPrice','Harga',w.price??13)}
 ${designerWidthInput('ddWidthAmount','Jumlah',w.amount??13)}
 </div></div>
 <div class="action-bar"><button type="button" onclick="saveDocumentTemplate()">Simpan Desain</button><button type="button" class="secondary" onclick="renderDocumentPreview()">Perbarui Preview</button></div></div>`;
 ddPaper.value=t.paper_size||'A5';docDesignerEditor.querySelectorAll('input,textarea,select').forEach(el=>el.addEventListener('input',renderDocumentPreview));
}
function designerCheck(id,label,checked,disabled=false){return `<label><input id="${id}" type="checkbox" ${checked?'checked':''} ${disabled?'disabled':''}> <span>${label}</span></label>`}
function designerWidthInput(id,label,value){return `<label><span>${label}</span><input id="${id}" type="number" min="2" max="80" step="1" value="${Number(value)||10}"></label>`}
function designerWidthValue(id,fallback){const el=document.getElementById(id),n=Number(el?.value);return Number.isFinite(n)?Math.max(2,Math.min(80,n)):fallback}
function currentDesignerPayload(){return {title:ddTitle.value.trim(),paper_size:ddPaper.value,header_text:ddHeader.value.trim(),footer_text:ddFooter.value.trim(),show_logo:ddShowLogo.checked,show_prices:ddShowPrices.checked,show_sku:ddShowSku.checked,show_unit:ddShowUnit.checked,show_warehouse:ddShowWarehouse.checked,show_discount:ddShowDiscount.checked,show_tax:ddShowTax.checked,show_payment_terms:ddShowPaymentTerms.checked,show_payment_account_note:ddShowPaymentAccountNote.checked,show_partner_contact:ddShowPartnerContact.checked,show_amount_words:ddShowAmountWords.checked,payment_account_note:ddPaymentAccountNote.value.trim(),column_widths:{no:designerWidthValue('ddWidthNo',5),sku:designerWidthValue('ddWidthSku',13),description:designerWidthValue('ddWidthDescription',37),qty:designerWidthValue('ddWidthQty',9),unit:designerWidthValue('ddWidthUnit',10),price:designerWidthValue('ddWidthPrice',13),amount:designerWidthValue('ddWidthAmount',13)},special_note:ddSpecial.value.trim(),left_signer:ddLeftSigner.value.trim(),right_signer:ddRightSigner.value.trim()}}
async function saveDocumentTemplate(){try{const payload=currentDesignerPayload();if(!payload.title)throw Error('Judul dokumen wajib diisi.');const d=await api('/api/document-templates/'+encodeURIComponent(activeDocumentType),{method:'PUT',body:JSON.stringify(payload)});const i=documentDesignerItems.findIndex(x=>x.document_type===activeDocumentType);if(i>=0)documentDesignerItems[i]=d.item;msg(docDesignerMessage,'Desain dokumen berhasil disimpan.',true);renderDocumentDesignerEditor();renderDocumentPreview()}catch(e){msg(docDesignerMessage,e.message,false)}}
function renderDocumentPreview(){
 if(typeof ddTitle==='undefined'||!document.getElementById('ddTitle'))return;
 const p=currentDesignerPayload(),noPrice=['DELIVERY_ORDER','GOODS_RECEIPT'].includes(activeDocumentType),paper=(p.paper_size||'A5').toLowerCase();
 const priceCols=(!noPrice&&p.show_prices)?'<th class="num">Harga</th><th class="num">Jumlah</th>':'';
 const priceCells=(!noPrice&&p.show_prices)?'<td class="num">125.000</td><td class="num">250.000</td>':'';
 const skuHead=p.show_sku?'<th>Kode</th>':'',skuCell=p.show_sku?'<td>BRG-001</td>':'';
 const unitHead=p.show_unit?'<th>Satuan</th>':'',unitCell=p.show_unit?'<td>PCS</td>':'';
 const activeColumns=['no',...(p.show_sku?['sku']:[]),'description','qty',...(p.show_unit?['unit']:[]),...((!noPrice&&p.show_prices)?['price','amount']:[])];
 const widthTotal=activeColumns.reduce((n,k)=>n+Number(p.column_widths?.[k]||10),0)||1;
 const previewColgroup='<colgroup>'+activeColumns.map(k=>`<col style="width:${((Number(p.column_widths?.[k]||10)/widthTotal)*100).toFixed(3)}%">`).join('')+'</colgroup>';
 docDesignerPreview.innerHTML=`<div class="preview-sheet preview-${paper}"><div class="preview-header">${p.show_logo?'<div class="preview-logo">LOGO</div>':'<div></div>'}<div class="preview-company"><strong>Nama Perusahaan</strong><span>Alamat dan kontak perusahaan</span></div><div class="preview-title"><h2>${designerEscape(p.title)}</h2><b>DOC-00001</b></div></div>${p.header_text?`<div class="preview-note">${designerEscape(p.header_text)}</div>`:''}<div class="preview-meta"><div><span>Tanggal</span><b>20/07/2026</b></div><div><span>Pelanggan/Pemasok</span><b>Contoh Mitra</b></div></div>${p.show_partner_contact!==false?`<div class="preview-transaction-note"><b>Alamat / Kontak:</b><br>Jl. Contoh No. 1, Jakarta · 0812-0000-0000 · mitra@email.com</div>`:''}<table class="preview-table">${previewColgroup}<thead><tr><th>No</th>${skuHead}<th>Deskripsi</th><th class="num">Qty</th>${unitHead}${priceCols}</tr></thead><tbody><tr><td>1</td>${skuCell}<td>Contoh barang atau jasa dengan deskripsi yang dapat dibuat lebih panjang untuk melihat hasil pembungkusan teks.</td><td class="num">2</td>${unitCell}${priceCells}</tr></tbody></table>${(!noPrice&&p.show_prices)?'<div class="preview-totals"><div><span>Subtotal</span><b>250.000</b></div><div class="grand"><span>Total</span><b>250.000</b></div></div>':''}${(!noPrice&&p.show_amount_words!==false)?'<div class="preview-transaction-note"><b>Terbilang:</b> Dua Ratus Lima Puluh Ribu Rupiah</div>':''}${p.show_payment_terms?`<div class="preview-transaction-note"><b>Termin Pembayaran:</b> 30 hari · Jatuh tempo 19/08/2026</div>`:''}${p.show_payment_account_note&&p.payment_account_note?`<div class="preview-transaction-note"><b>Catatan Rekening Pembayaran:</b><br>${designerEscape(p.payment_account_note)}</div>`:''}${p.special_note?`<div class="preview-transaction-note">${designerEscape(p.special_note)}</div>`:''}<div class="preview-signatures"><div>${designerEscape(p.left_signer||'Disiapkan oleh')}</div><div>${designerEscape(p.right_signer||'Diterima oleh')}</div></div>${p.footer_text?`<div class="preview-footer">${designerEscape(p.footer_text)}</div>`:''}</div>`
}

const moduleMenus={
 master:{title:'Master Data',description:'Kelola data dasar yang digunakan oleh seluruh transaksi.',items:[
  ['₿','Tingkatan Harga','Retail, grosir, distributor, reseller, dan harga khusus pelanggan',async()=>{page('priceLevels');await loadPriceLevels()}],
  ['⇩','Impor Data Excel','Import seluruh master dan saldo awal dengan template serta validasi.',()=>openMasterImport()],
['⌂','Master Departemen','Kelola departemen dan cost center',async()=>{page('departments');await loadDepartments()}],
  ['▦','Data Barang','Barang stok, harga, merk, satuan, saldo awal, dan setting akun',async()=>{await Promise.all([loadAccounting(),loadProducts(),loadMasters(),loadWarehouses(),loadPriceLevels()]);page('products');bindOperationalCoaSelectors()}],
  ['◇','Daftar Jasa','Kategori jasa, harga default, pajak, dan setting akun',async()=>{page('servicesPage');await loadServicesPage()}],
  ['♙','Data Pelanggan','Input dan daftar pelanggan termasuk saldo awal piutang',()=>{page('customersPage');Promise.all([loadCustomersPage(),loadPriceLevels()])}],
  ['♟','Data Pemasok','Input dan daftar pemasok termasuk saldo awal hutang',()=>{page('suppliersPage');loadSuppliersPage()}],
  ['◆','Data Merk','Input dan daftar merk barang',()=>openExtraMaster('brand')],
  ['♜','Data Salesman','Input dan daftar salesman',()=>openExtraMaster('salesman')],
  ['▣','Daftar Nama Gudang','Buat, edit, dan nonaktifkan lokasi multi gudang',async()=>{page('inventory');document.querySelectorAll('.inventory-section').forEach(x=>x.style.display='none');document.querySelector('.inventory-warehouses').style.display='block';await loadWarehouseMaster()}],
  ['⚙','Kategori & Satuan','Kategori barang dan satuan pengukuran',()=>page('masters')]
 ]},
 sales:{title:'Penjualan',description:'Transaksi penjualan, daftar transaksi, piutang, dan dokumen pelanggan.',items:[
  ['📝','Pesanan & DP Penjualan','Pesanan, penerimaan DP, dan alokasi ke invoice',()=>openOrdersDp('sales')],
  ['⇧','Input Penjualan Baru','Input penjualan barang atau jasa',()=>openSalesSection('entry')],
  ['☷','Daftar Penjualan','Riwayat penjualan serta cetak Nota dan Surat Jalan',()=>openSalesSection('list')],
  ['↩','Retur Penjualan','Retur dengan atau tanpa invoice penjualan',()=>openSalesReturns()],
  ['＋','Penerimaan Piutang Pelanggan','Bayar invoice penjualan kredit yang masih outstanding',async()=>{page('receivables');await loadSettlementMasters();await loadReceivables()}],
  ['▤','Daftar Penerimaan Piutang','Edit dan hapus penerimaan piutang pelanggan',()=>openTransactionMaintenance('receivable')]
 ]},
 purchases:{title:'Pembelian',description:'Transaksi pembelian, daftar transaksi, hutang, dan penerimaan barang.',items:[
  ['📝','Pesanan & DP Pembelian','Pesanan, pembayaran DP, dan alokasi ke invoice',()=>openOrdersDp('purchase')],
  ['⇩','Input Pembelian Baru','Input pembelian barang atau jasa',()=>openPurchaseSection('entry')],
  ['☷','Daftar Pembelian','Riwayat pembelian serta cetak Faktur dan Good Receive',()=>openPurchaseSection('list')],
  ['↩','Retur Pembelian','Retur dengan atau tanpa invoice pembelian',()=>openPurchaseReturns()],
  ['−','Pembayaran Hutang Pemasok','Bayar invoice pembelian kredit yang masih outstanding',async()=>{page('payables');await loadSettlementMasters();await loadPayables()}],
  ['▤','Daftar Pembayaran Hutang','Edit dan hapus pembayaran hutang pemasok',()=>openTransactionMaintenance('payable')]
 ]},
 cash:{title:'Kas & Bank',description:'Kelola penerimaan, pembayaran, transfer, dan rekening koran.',items:[
  ['▤','Daftar Kas Masuk/Keluar','Edit dan hapus transaksi kas',()=>openTransactionMaintenance('cash')],
  ['⇄','Daftar Transfer Kas/Bank','Edit dan hapus transfer',()=>openTransactionMaintenance('transfer')],
  ['＋','Kas Masuk / Keluar','Penerimaan dan pengeluaran non-transaksi',async()=>{openCashSection('entry');await Promise.allSettled([loadCashAccounts(),loadCoreAccountingMasters(),loadTransactionDimensions()]);bindOperationalCoaSelectors()}],
  ['⇄','Transfer Antar Akun','Pindahkan saldo kas atau bank',()=>openCashSection('transfer')],
  ['⇅','Smart Import Rekening Koran','Import PDF mutasi bank dengan preview',async()=>{page('smartImport');document.querySelectorAll('.accounting-section').forEach(x=>x.style.display='none');await loadSmartImportMasters()}],
 ]},
 inventory:{title:'Persediaan',description:'Pantau saldo stok, kartu stok, dan perpindahan gudang.',items:[
  ['▤','Kartu & Saldo Stok','Hanya saldo per gudang dan kartu stok',()=>openInventorySection('stock')],
  ['▤','Daftar Adjustment Stok','Edit dan hapus penyesuaian',()=>openTransactionMaintenance('adjustment')],
  ['⇄','Daftar Transfer Gudang','Edit dan hapus transfer antar gudang',()=>openTransactionMaintenance('warehouse_transfer')],
  ['±','Adjustment Stok','Penyesuaian stok dengan alasan dan audit',async()=>{page('stock');await Promise.allSettled([loadAccounting(),loadProducts(),loadWarehouses(),loadTransactionDimensions()]);try{bindOperationalCoaSelectors()}catch(e){console.error(e)}}],
  ['⇄','Transfer Gudang','Hanya form transfer antar gudang',()=>openInventorySection('transfer')]
 ]},
 assembly:{title:'Assembly',description:'Produksi sederhana dua tahap: bahan dan biaya ke WIP, lalu WIP ke barang jadi.',items:[
  ['⚒','Input Assembly Baru','Ambil bahan baku dan biaya tambahan ke Persediaan Dalam Proses',()=>openAssembly()],
  ['✓','Daftar & Finishing Assembly','Selesaikan assembly dan alokasikan cost ke multi barang jadi',()=>openAssembly()]
 ]},
 fixedassets:{title:'Aktiva Tetap',description:'Pencatatan aset, penyusutan garis lurus, dan laporan nilai buku.',items:[
  ['＋','Aktiva Tetap Baru','Catat perolehan aset dan buat jurnal perolehan otomatis',()=>openFixedAssetNew()],
  ['▦','Daftar Aktiva Tetap','Laporan harga perolehan, akumulasi penyusutan, dan nilai buku',()=>openFixedAssetList()],
  ['↻','Penyusutan Otomatis','Proses jurnal penyusutan sejak bulan perolehan',()=>openFixedAssetDepreciation()]
 ]},
 project:{title:'Proyek',description:'Kelola daftar proyek, budget, dan kontrol realisasi proyek.',items:[
  ['◆','Daftar Proyek','Master proyek, pelanggan, periode, status, dan ringkasan budget',async()=>{page('projects');await loadProjects()}],
  ['▣','Budget & Realisasi Proyek','Input budget material dan biaya serta pantau sisa budget',async()=>{page('projectBudgets');await loadProjectBudgets()}],
  ['⇩','Daftar Pengeluaran Material Proyek','Input, edit, dan hapus pengeluaran material proyek',async()=>{page('projectMaterialIssues');await loadProjectMaterialIssueMasters();await loadProjectMaterialIssues()}],
  ['▧','Dokumen Proyek','Simpan kontrak, SPK, BAST, gambar, foto progress, dan dokumen proyek',async()=>{page('projectDocuments');await loadProjectDocuments()}]
 ]},
 accounting:{title:'Akuntansi',description:'COA, jurnal, buku besar, dan laporan keuangan.',items:[
  ['Σ','Data COA','Kelola chart of accounts',async()=>{openAccountingSection('coa');await loadAccounting()}],
  ['▤','Daftar Jurnal Manual','Edit dan hapus jurnal',()=>openTransactionMaintenance('journal')],
  ['≡','Jurnal Manual','Input jurnal debit dan kredit',async()=>{openAccountingSection('manual');await Promise.allSettled([loadCoreAccountingMasters(),loadTransactionDimensions(),loadDocumentNumbers()]);renderJLines()}],
  ['▥','Buku Besar','Mutasi dan saldo berjalan per akun',()=>openAccountingSection('ledger')],
  ['▦','Neraca Saldo','Saldo debit dan kredit seluruh akun',()=>openAccountingSection('trial')],
 ]},
 reports:{title:'Laporan',description:'Pilih kelompok laporan terlebih dahulu.',items:[
  ['◆','Laporan Proyek','Laba rugi, pembelian, material, dan rekap proyek',async()=>{page('projectReports');await loadProjectReportMasters();}],
  ['⇧','Laporan Penjualan','Penjualan per barang, jasa, pelanggan, salesman, kategori, dan merk',()=>openReportGroup('sales')],
  ['⇩','Laporan Pembelian','Pembelian per barang, pemasok, kategori, dan merk',()=>openReportGroup('purchase')],
  ['▤','Laporan Stok Barang','Stok realtime, valuasi persediaan, HPP, gudang, mutasi, dan adjustment',()=>openReportGroup('stock')],
  ['∑','Laporan Keuangan','Jurnal, Buku Besar, Hutang, Piutang, Neraca Saldo, Neraca, Laba Rugi, dan Arus Kas',()=>openReportGroup('finance')],
  ['▣','Laporan Kas Bank','Buku Kas/Bank, penerimaan, dan pengeluaran Kas/Bank',()=>openReportGroup('cash')]
 ]},
 system:{title:'Sistem',description:'Pengaturan perusahaan, pengguna, audit, langganan, dan desain dokumen.',items:[
  ['★','Trial & Langganan','Lihat status trial/langganan dan simulasi paket',()=>openSubscriptionAdmin()],
  ['♚','User & Hak Akses','Kelola user, role, password, status, dan permission',()=>openUserAccess()],
  ['☷','Audit Log','Riwayat aktivitas pengguna',()=>page('audit')],
  ['▤','Profil Perusahaan','Identitas, alamat, dan logo perusahaan',()=>page('settings')],
  ['▧','Desain Dokumen','Atur nota, surat jalan, faktur, dan good receive',()=>openDocumentDesigner()],
  ['▤','Desain Invoice Fleksibel','Multi-template invoice standar, termin, material proyek, dan custom',async()=>{page('flexInvoiceDesigner');await loadFlexInvoiceTemplates()}],
 ]}
};
function showModule(key,button){window.__activeModuleKey=key;const m=moduleMenus[key];if(!m)return;page('moduleHome',button);moduleTitle.textContent=m.title;moduleDescription.textContent=m.description;moduleGrid.innerHTML=m.items.map((x,index)=>({x,index})).filter(v=>Array.isArray(v.x)&&v.x[1]&&v.x[1]!=='undefined'&&typeof v.x[3]==='function'&&!(v.x[1]==='Trial & Langganan'&&currentUser?.role?.code!=='ADMIN')).map(v=>`<article class="module-card" onclick="openModuleItem('${key}',${v.index})"><div><div class="module-card-icon">${v.x[0]}</div><h3>${v.x[1]}</h3><p>${v.x[2]}</p></div><small>Buka menu →</small></article>`).join('')}
function openModuleItem(key,index){const item=moduleMenus[key]?.items[index];if(Array.isArray(item)&&typeof item[3]==='function')item[3]()}


const mobileModuleMeta={
  dashboard:['⌂','Dashboard','Ringkasan penjualan, stok, kas, dan analitik.'],
  master:['▦','Master Data','Barang, jasa, pelanggan, pemasok, gudang, dan master lainnya.'],
  sales:['⇧','Penjualan','Transaksi jual, pesanan, retur, dan piutang pelanggan.'],
  purchases:['⇩','Pembelian','Transaksi beli, penerimaan barang, retur, dan hutang pemasok.'],
  cash:['▣','Kas & Bank','Kas masuk/keluar, transfer akun, dan mutasi bank.'],
  inventory:['▤','Persediaan','Kartu stok, adjustment, transfer gudang, dan stok opname.'],
  assembly:['⚒','Assembly','Perakitan barang dan resep/bill of materials.'],
  fixedassets:['▦','Aktiva Tetap','Data aset, penyusutan, dan daftar aktiva tetap.'],
  project:['◆','Proyek','Daftar proyek, dokumen, budget, dan progress pekerjaan.'],
  accounting:['∑','Akuntansi','Jurnal, COA, buku besar, dan neraca saldo.'],
  reports:['▥','Laporan','Semua laporan penjualan, pembelian, kas, dan keuangan.'],
  system:['⚙','Sistem','Pengaturan, backup, trial, dan langganan.']
};
function getDesktopNavButtonByKey(key){return [...document.querySelectorAll('.sidebar .module-nav button')].find(btn=>((btn.getAttribute('onclick')||'').includes(`showModule('${key}'`)))}
function setMobileActiveTab(key,btn){document.querySelectorAll('.mobile-tabbar button').forEach(x=>x.classList.remove('active'));let target=btn||document.querySelector(`.mobile-tabbar [data-mobile-tab="${key}"]`)||document.querySelector('.mobile-tabbar [data-mobile-tab="more"]');if(target)target.classList.add('active')}
function renderMobileDrawerMenu(){if(!window.mobileDrawerGrid)return;const entries=['dashboard',...Object.keys(moduleMenus||{})];mobileDrawerGrid.innerHTML=entries.map(key=>{const meta=mobileModuleMeta[key]||['•',key,''];const icon=meta[0],title=meta[1],desc=meta[2]||'';const action=key==='dashboard' ? `openMobileDashboard()` : `openMobileModule('${key}')`;return `<article class="mobile-drawer-card" onclick="${action}"><div class="mobile-drawer-icon">${icon}</div><div><h4>${title}</h4><p>${desc}</p></div></article>`}).join('')}
function openMobileDrawer(btn){renderMobileDrawerMenu();if(window.mobileDrawerBackdrop)mobileDrawerBackdrop.classList.remove('hidden');if(window.mobileDrawer){mobileDrawer.classList.remove('hidden');mobileDrawer.setAttribute('aria-hidden','false')}document.body.classList.add('mobile-drawer-open');setMobileActiveTab('more',btn)}
function closeMobileDrawer(){if(window.mobileDrawerBackdrop)mobileDrawerBackdrop.classList.add('hidden');if(window.mobileDrawer){mobileDrawer.classList.add('hidden');mobileDrawer.setAttribute('aria-hidden','true')}document.body.classList.remove('mobile-drawer-open');syncMobileNav()}
function openMobileDashboard(btn){closeMobileDrawer();window.__activeModuleKey='dashboard';page('dashboard',document.querySelector('.sidebar .module-nav button'));setMobileActiveTab('dashboard',btn)}
function openMobileModule(key,btn){closeMobileDrawer();window.__activeModuleKey=key;const desktopBtn=getDesktopNavButtonByKey(key);showModule(key,desktopBtn||null);setMobileActiveTab(['sales','purchases','cash'].includes(key)?key:'more',btn)}
function syncMobileNav(){if(!window.matchMedia||!window.matchMedia('(max-width:760px)').matches)return;const key=window.__activeModuleKey||((window.__activePageId==='dashboard'||!window.__activePageId)?'dashboard':'more');setMobileActiveTab(['dashboard','sales','purchases','cash'].includes(key)?key:'more')}
window.addEventListener('resize',()=>{if(window.matchMedia && !window.matchMedia('(max-width:760px)').matches)closeMobileDrawer();syncMobileNav()});
window.addEventListener('orientationchange',()=>setTimeout(syncMobileNav,180));
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMobileDrawer()});

async function refreshSubscriptionChip(){try{let x=await api('/api/license-status');let label=x.mode==='SUBSCRIPTION'?((x.plan_name||'Langganan')+' · '+x.days_remaining+' hari'):x.mode==='TRIAL'?('Trial · '+x.days_remaining+' hari'):('Masa akses berakhir');if(window.webSubscriptionChip)webSubscriptionChip.textContent=label+' · '+(x.max_users||2)+' user'}catch(e){}}
async function openSubscriptionAdmin(){if(!currentUser||currentUser.role?.code!=='ADMIN'){alert('Menu ini khusus Administrator.');return}page('subscriptionAdmin');await loadSubscriptionAdmin()}
async function loadSubscriptionAdmin(){try{let x=await api('/api/subscription-admin');subStatus.textContent=x.mode==='SUBSCRIPTION'?(x.plan_name||'Aktif'):x.mode;subDays.textContent=x.days_remaining??0;subUsers.textContent=x.max_users??2;let ex=x.mode==='TRIAL'?x.trial_expires_at:x.expires_at;subExpiry.textContent=ex?new Date(ex).toLocaleDateString('id-ID'):'-';updateSubPrice()}catch(e){msg(subMsg,e.message,false)}}
function updateSubPrice(){let year=subPlan?.value==='YEAR',base=year?2000000:1200000,add=year?200000:100000,n=Math.max(0,Number(subAddon?.value||0)),total=base+n*add;if(window.subPriceInfo)subPriceInfo.innerHTML=`Paket dasar: <b>${rup(base)}</b> · Add-on ${n} user: <b>${rup(n*add)}</b> · Total aktivasi: <b>${rup(total)}</b> · Total user: <b>${2+n}</b>`}
setTimeout(()=>{if(window.subPlan){subPlan.addEventListener('change',updateSubPrice);subAddon.addEventListener('input',updateSubPrice)}},500);
async function openSystemInfo(){page('systemInfo');await loadSystemInfo()}
async function loadSystemInfo(){try{let h=await api('/api/system/storage-info');systemDbPath.textContent=h.database||'-';systemBackupPath.textContent=h.backup_directory||'-';msg(systemInfoMsg,'Storage web aktif. Gunakan Railway Volume agar database dan dokumen persisten.',true)}catch(e){msg(systemInfoMsg,e.message,false)}}


async function initFixedAssetDefaults(){let today=new Date().toISOString().slice(0,10);if(!faDate.value)faDate.value=today;if(!faPeriod.value)faPeriod.value=today.slice(0,7)}
async function openFixedAssetNew(){page('fixedAssetNewPage');initFixedAssetDefaults();await loadFixedAssetAccounts()}
async function openFixedAssetList(){page('fixedAssetListPage');await loadFixedAssets()}
async function openFixedAssetDepreciation(){page('fixedAssetDepPage');initFixedAssetDefaults();await loadFixedAssets();await loadDepreciationHistory()}
async function loadFixedAssetAccounts(){let d=await api('/api/coa?active=1');let opts=(d.items||[]).map(x=>`<option value="${x.id}">${x.code} - ${accessEscape(x.name)}</option>`).join('');[faAssetAccount,faAccumAccount,faExpenseAccount,faContraAccount].forEach(x=>x.innerHTML=opts);let pick=(el,code)=>{let o=[...el.options].find(x=>x.textContent.startsWith(code+' -'));if(o)el.value=o.value};pick(faAssetAccount,'1400');pick(faAccumAccount,'1410');pick(faExpenseAccount,'5200')}
async function saveFixedAsset(){try{let edit=window.__fixedAssetEdit;let payload={asset_code:faCode.value,asset_name:faName.value,acquisition_date:faDate.value,acquisition_cost:faCost.value,residual_value:faResidual.value,useful_life_months:faLife.value,asset_account_id:faAssetAccount.value,accumulated_depreciation_account_id:faAccumAccount.value,depreciation_expense_account_id:faExpenseAccount.value,contra_account_id:faContraAccount.value,notes:faNotes.value};await api(edit?'/api/fixed-assets/'+edit:'/api/fixed-assets',{method:edit?'PUT':'POST',body:JSON.stringify(payload)});window.__fixedAssetEdit=null;msg(faMsg,edit?'Aktiva tetap berhasil diperbarui.':'Aktiva tetap berhasil disimpan dan jurnal perolehan telah dibuat.');faCode.value=faName.value=faNotes.value='';faCost.value=faResidual.value=0;faDate.value=new Date().toISOString().slice(0,10);await loadFixedAssets();faCode.focus()}catch(e){msg(faMsg,e.message,false)}}
async function loadFixedAssets(){try{let d=await api('/api/fixed-assets'),items=d.items||[];let rows=items.map(x=>`<tr><td><b>${accessEscape(x.asset_code)}</b></td><td>${accessEscape(x.asset_name)}</td><td>${x.acquisition_date}</td><td class="number-cell">${rup(x.acquisition_cost)}</td><td class="number-cell">${rup(x.residual_value)}</td><td>${Number(x.useful_life_months)===0?'Tidak disusutkan':x.useful_life_months+' bulan'}</td><td class="number-cell">${rup(x.monthly_depreciation)}</td><td class="number-cell">${rup(x.accumulated_depreciation)}</td><td class="number-cell">${rup(x.book_value)}</td><td>${x.status}</td><td><button onclick="editFixedAsset(${x.id})">Edit</button> <button class="danger" onclick="deleteFixedAsset(${x.id})">Hapus</button></td></tr>`).join('');if(typeof faBody!=='undefined')faBody.innerHTML=rows||'<tr><td colspan="11">Belum ada aktiva tetap.</td></tr>';let totalCost=items.reduce((a,x)=>a+Number(x.acquisition_cost||0),0),totalDep=items.reduce((a,x)=>a+Number(x.accumulated_depreciation||0),0),totalBook=items.reduce((a,x)=>a+Number(x.book_value||0),0);if(typeof faFoot!=='undefined')faFoot.innerHTML=`<tr><th colspan="3">TOTAL</th><th class="number-cell">${rup(totalCost)}</th><th colspan="3"></th><th class="number-cell">${rup(totalDep)}</th><th class="number-cell">${rup(totalBook)}</th><th></th></tr>`;if(typeof faDepBody!=='undefined')faDepBody.innerHTML=items.map(x=>`<tr><td>${accessEscape(x.asset_code)}</td><td>${accessEscape(x.asset_name)}</td><td class="number-cell">${rup(x.monthly_depreciation)}</td><td class="number-cell">${rup(x.accumulated_depreciation)}</td><td class="number-cell">${rup(x.book_value)}</td><td>${x.status}</td></tr>`).join('')||'<tr><td colspan="6">Belum ada aktiva tetap.</td></tr>'}catch(e){if(typeof faMsg!=='undefined')msg(faMsg,e.message,false)}}
async function runFixedAssetDepreciation(){try{let d=await api('/api/fixed-assets/depreciate',{method:'POST',body:JSON.stringify({period:faPeriod.value})});msg(faDepMsg,`Penyusutan ${d.result.period}: ${d.result.count} aktiva, total ${rup(d.result.total)}.`);await loadFixedAssets();await loadDepreciationHistory()}catch(e){msg(faDepMsg,e.message,false)}}

const reportDefinitions={
 sales_product:{title:'Penjualan per Barang',filters:['customer','salesperson','product','category','brand']},
 sales_service:{title:'Penjualan per Jasa',filters:['customer','salesperson','product']},
 sales_customer:{title:'Penjualan per Pelanggan',filters:['customer','salesperson','product','category','brand']},
 sales_salesperson:{title:'Penjualan per Salesman',filters:['customer','salesperson','product','category','brand']},
 sales_category:{title:'Penjualan per Kategori',filters:['customer','salesperson','product','category','brand']},
 sales_brand:{title:'Penjualan per Merk',filters:['customer','salesperson','product','category','brand']},
 sales_detail:{title:'Rincian Penjualan',filters:['customer','salesperson','product','warehouse'],selectableFields:true},
 sales_order_history:{title:'History Pesanan Penjualan',filters:[]},
 sales_dp:{title:'DP Penjualan',filters:[]},
 sales_dp_allocation:{title:'Alokasi DP Penjualan',filters:[]},
 purchase_product:{title:'Pembelian per Barang',filters:['supplier','product','category','brand']},
 purchase_supplier:{title:'Pembelian per Pemasok',filters:['supplier','product','category','brand']},
 purchase_category:{title:'Pembelian per Kategori',filters:['supplier','product','category','brand']},
 purchase_brand:{title:'Pembelian per Merk',filters:['supplier','product','category','brand']},
 purchase_detail:{title:'Rincian Pembelian',filters:['supplier','product','warehouse'],selectableFields:true},
 purchase_order_history:{title:'History Pesanan Pembelian',filters:[]},
 purchase_dp:{title:'DP Pembelian',filters:[]},
 purchase_dp_allocation:{title:'Alokasi DP Pembelian',filters:[]},
 stock_list:{title:'Daftar Stok Barang',filters:['category','brand','inventory_account']},
 stock_valuation_summary:{title:'Ringkasan Valuasi Persediaan',filters:['warehouse','product','category','brand','inventory_account']},
 stock_valuation_detail:{title:'Rincian Valuasi Persediaan',filters:['warehouse','product','category','brand','inventory_account']},
 stock_fast:{title:'Laporan Stok Fast Moving',filters:['category','brand','inventory_account']},
 stock_dead:{title:'Laporan Dead Stock',filters:['category','brand','inventory_account']},
 stock_warehouse:{title:'Qty Barang per Gudang',filters:['warehouse','category','brand','inventory_account']},
 stock_mutation:{title:'Mutasi Barang per Gudang',filters:['warehouse','product','category','brand','inventory_account']},
 stock_adjustment:{title:'Laporan Penyesuaian Barang',filters:['warehouse','product','category','brand','inventory_account']},
 stock_assembly:{title:'Laporan Assembly',filters:[]},
 stock_assembly_finish:{title:'Laporan Finishing Assembly',filters:[]},
 finance_journals:{title:'All Jurnal Transaksi',filters:[]},
 finance_ledger:{title:'Buku Besar',filters:['account','ledger_partner']},
 finance_trial:{title:'Neraca Saldo',filters:[]},
 finance_balance:{title:'Neraca',filters:[]},
 finance_income:{title:'Laporan Laba Rugi',filters:[]},
 finance_cashflow:{title:'Laporan Arus Kas (Metode Langsung)',filters:[]},
 finance_receivables:{title:'Laporan Piutang Pelanggan',filters:['customer']},
 finance_payables:{title:'Laporan Hutang Pemasok',filters:['supplier']},
 cash_book:{title:'Buku Kas/Bank (Mutasi Kas/Bank)',filters:['cash_account']},
 cash_out:{title:'Laporan Pengeluaran Kas/Bank',filters:['cash_account']},
 cash_in:{title:'Laporan Penerimaan Kas/Bank',filters:['cash_account']}
};
let currentReportType='';
async function openSalesSection(section){page('sales');showOnly('.sales-section','sales-'+section);if(section==='entry')await Promise.allSettled([loadTransactionDimensions(),loadTransactionPartners(),loadProducts(),loadDocumentNumbers()]);if(section==='list')loadSales()}
async function openPurchaseSection(section){page('purchases');showOnly('.purchase-section','purchase-'+section);if(section==='entry')await Promise.allSettled([loadTransactionDimensions(),loadTransactionPartners(),loadProducts(),loadDocumentNumbers()]);if(section==='list')loadPurchases()}
function reportOption(items,label){return `<option value="">Semua ${label}</option>`+(items||[]).map(x=>`<option value="${x.id}">${x.code||x.sku||''} - ${x.name||x.product_name||''}</option>`).join('')}
async function loadReportMasters(){
 const [cu,su,sp,p,c,b,w,coa,cash]=await Promise.all([
  api('/api/customers?active=1'),api('/api/suppliers?active=1'),api('/api/salespersons?active=1'),
  api('/api/products?active=1'),api('/api/categories?active=1'),api('/api/brands?active=1'),
  api('/api/warehouses?active=1'),api('/api/coa?active=1'),api('/api/cash-accounts?active=1')]);
 reportCustomer.innerHTML=reportOption(cu.items,'Pelanggan');
 reportSupplier.innerHTML=reportOption(su.items,'Pemasok');
 reportSalesperson.innerHTML=reportOption(sp.items,'Salesman');
 reportProduct.innerHTML=reportOption(p.items,'Barang');
 reportCategory.innerHTML=reportOption(c.items,'Kategori');
 reportBrand.innerHTML=reportOption(b.items,'Merk');
 reportWarehouse.innerHTML=reportOption(w.items,'Gudang');
 window.reportCustomers=cu.items||[];window.reportSuppliers=su.items||[];window.reportCoaItems=coa.items||[];
 reportAccount.innerHTML=reportOption(coa.items,'Akun');reportCashAccount.innerHTML=reportOption(cash.items,'Kas/Bank');
 reportInventoryAccount.innerHTML='<option value="">Semua Akun Persediaan</option>'+
   (coa.items||[]).filter(x=>(x.display_type||x.account_subtype)==='ASSET').map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');
 refreshReportLedgerPartner();
}
function refreshReportLedgerPartner(){
 const account=(window.reportCoaItems||[]).find(x=>String(x.id)===String(reportAccount.value));
 const subtype=(account?.display_type||account?.account_subtype||'').toUpperCase();
 const list=subtype==='RECEIVABLE'?(window.reportCustomers||[]):subtype==='PAYABLE'?(window.reportSuppliers||[]):[];
 reportLedgerPartner.innerHTML='<option value="">Semua</option>'+list.map(x=>`<option value="${x.id}">${financeEscape(x.code)} - ${financeEscape(x.name)}</option>`).join('');
 reportLedgerPartner.disabled=!list.length;
 reportLedgerPartnerHelp.textContent=subtype==='RECEIVABLE'?'Filter Buku Besar Piutang per pelanggan.':subtype==='PAYABLE'?'Filter Buku Besar Hutang per pemasok.':'Aktif hanya untuk akun Piutang atau Hutang.';
 if(!list.length)reportLedgerPartner.value='';
}

const reportGroups={
 sales:{title:'Laporan Penjualan',items:[
  ['⇧','Penjualan per Barang','Rekap qty, nilai, HPP, dan laba kotor',()=>openReport('sales_product')],
  ['◇','Penjualan per Jasa','Rekap transaksi, qty, nilai jasa, biaya, dan laba kotor',()=>openReport('sales_service')],
  ['♙','Penjualan per Pelanggan','Rekap penjualan per pelanggan',()=>openReport('sales_customer')],
  ['♜','Penjualan per Salesman','Rekap penjualan per salesman',()=>openReport('sales_salesperson')],
  ['▦','Penjualan per Kategori','Rekap penjualan per kategori',()=>openReport('sales_category')],
  ['◆','Penjualan per Merk','Rekap penjualan per merk',()=>openReport('sales_brand')],
  ['☷','Rincian Penjualan','Detail transaksi dengan pilihan field/kolom',()=>openReport('sales_detail')],
  ['⌛','History Pesanan Penjualan','Riwayat pesanan penjualan dan realisasinya',()=>openReport('sales_order_history')],
  ['DP','DP Penjualan','Daftar uang muka pelanggan',()=>openReport('sales_dp')],
  ['↳','Alokasi DP Penjualan','Riwayat alokasi DP ke invoice penjualan',()=>openReport('sales_dp_allocation')]]},
 purchase:{title:'Laporan Pembelian',items:[
  ['⇩','Pembelian per Barang','Rekap pembelian per barang',()=>openReport('purchase_product')],
  ['♟','Pembelian per Pemasok','Rekap pembelian per pemasok',()=>openReport('purchase_supplier')],
  ['▦','Pembelian per Kategori','Rekap pembelian per kategori',()=>openReport('purchase_category')],
  ['◆','Pembelian per Merk','Rekap pembelian per merk',()=>openReport('purchase_brand')],
  ['☷','Rincian Pembelian','Detail transaksi dengan pilihan field/kolom',()=>openReport('purchase_detail')],
  ['⌛','History Pesanan Pembelian','Riwayat pesanan pembelian dan realisasinya',()=>openReport('purchase_order_history')],
  ['DP','DP Pembelian','Daftar uang muka pemasok',()=>openReport('purchase_dp')],
  ['↳','Alokasi DP Pembelian','Riwayat alokasi DP ke pembelian',()=>openReport('purchase_dp_allocation')]]},
 stock:{title:'Laporan Stok Barang',items:[
  ['▤','Daftar Stok Barang','Qty realtime dan nilai stok',()=>openReport('stock_list')],
  ['Σ','Ringkasan Valuasi Persediaan','Nilai awal, mutasi masuk/keluar, dan nilai akhir per barang/gudang',()=>openReport('stock_valuation_summary')],
  ['≋','Rincian Valuasi Persediaan','Mutasi stok bernilai dan rekonsiliasi HPP keluar dengan jurnal Buku Besar',()=>openReport('stock_valuation_detail')],
  ['↗','Stok Fast Moving','Aktivitas keluar 90 hari',()=>openReport('stock_fast')],
  ['⚠','Dead Stock','Barang tidak keluar selama 90 hari',()=>openReport('stock_dead')],
  ['⌂','Qty per Gudang','Qty dan nilai per gudang',()=>openReport('stock_warehouse')],
  ['⇄','Mutasi per Gudang','Riwayat mutasi barang per gudang',()=>openReport('stock_mutation')],
  ['±','Penyesuaian Barang','Riwayat adjustment stok',()=>openReport('stock_adjustment')],
  ['⚒','Laporan Assembly','Detail bahan baku, biaya, WIP, dan total cost assembly',()=>openReport('stock_assembly')],
  ['✓','Laporan Finishing Assembly','Detail barang jadi, alokasi cost, dan cost per unit',()=>openReport('stock_assembly_finish')]]},
 finance:{title:'Laporan Keuangan',items:[
  ['≡','All Jurnal Transaksi','Seluruh detail jurnal',()=>openReport('finance_journals')],
  ['▥','Buku Besar','Mutasi dan saldo per akun',()=>openReport('finance_ledger')],
  ['▦','Neraca Saldo','Saldo awal, mutasi, dan saldo akhir',()=>openReport('finance_trial')],
  ['▣','Neraca','Aset, kewajiban, dan ekuitas',()=>openReport('finance_balance')],
  ['◒','Laporan Laba Rugi','Pendapatan, HPP, biaya, dan laba',()=>openReport('finance_income')],
  ['⇅','Arus Kas Langsung','Kas masuk dan keluar',()=>openReport('finance_cashflow')],
  ['◷','Laporan Piutang','Saldo piutang pelanggan dan analisis umur',()=>openReport('finance_receivables')],
  ['◶','Laporan Hutang','Saldo hutang pemasok dan analisis umur',()=>openReport('finance_payables')]]},
 cash:{title:'Laporan Kas Bank',items:[
  ['☷','Buku Kas/Bank','Mutasi lengkap dan saldo Kas/Bank',()=>openReport('cash_book')],
  ['−','Pengeluaran Kas/Bank','Daftar Kas/Bank keluar',()=>openReport('cash_out')],
  ['＋','Penerimaan Kas/Bank','Daftar Kas/Bank masuk',()=>openReport('cash_in')]]}
};
function openReportGroup(group){
 const g=reportGroups[group];if(!g)return;
 moduleTitle.textContent=g.title;moduleDescription.textContent='Pilih laporan yang akan ditampilkan.';
 moduleGrid.innerHTML='';
 g.items.forEach(([icon,title,desc,action])=>{
  const card=document.createElement('button');card.className='module-card';
  card.innerHTML=`<span class="module-card-icon">${icon}</span><h3>${title}</h3><p>${desc}</p>`;
  card.onclick=action;moduleGrid.appendChild(card)
 });
 page('moduleHome')
}

async function openReport(type){
 currentReportType=type;const def=reportDefinitions[type];if(!def)return;
 page('reportsPage');reportTitle.textContent=def.title;reportHelp.textContent=def.selectableFields?'Pilih filter dan field/kolom yang ingin ditampilkan, kemudian tampilkan atau ekspor laporan.':'Gunakan filter yang diperlukan, kemudian tampilkan atau ekspor laporan.';
 await loadReportMasters();
 document.querySelectorAll('.report-filter').forEach(x=>x.style.display=def.filters.includes(x.dataset.filter)?'flex':'none');
 reportFieldSelector.style.display=def.selectableFields?'block':'none';
 if(!def.selectableFields)reportFieldChecks.innerHTML='';
 await loadCurrentReport();
}
function toggleAllReportFields(on){document.querySelectorAll('#reportFieldChecks input[type=checkbox]').forEach(x=>x.checked=on)}
function buildReportFieldSelector(columns){
 if(!reportDefinitions[currentReportType]?.selectableFields)return;
 const existing={};document.querySelectorAll('#reportFieldChecks input[type=checkbox]').forEach(x=>existing[x.value]=x.checked);
 reportFieldChecks.innerHTML=(columns||[]).map(([key,label])=>`<label><input type="checkbox" value="${financeEscape(key)}" ${existing[key]===false?'':'checked'}> <span>${financeEscape(label)}</span></label>`).join('');
}
function reportParams(){
 const p=new URLSearchParams({type:currentReportType});
 const pairs=[['date_from',reportFrom.value],['date_to',reportTo.value],['customer_id',reportCustomer.value],
 ['supplier_id',reportSupplier.value],['salesperson_id',reportSalesperson.value],['product_id',reportProduct.value],
 ['category_id',reportCategory.value],['brand_id',reportBrand.value],['warehouse_id',reportWarehouse.value],
 ['inventory_account_id',reportInventoryAccount.value],['account_id',reportAccount.value],['partner_id',reportLedgerPartner.value],['cash_account_id',reportCashAccount.value]];
 pairs.forEach(([k,v])=>{if(v)p.set(k,v)});
 if(reportDefinitions[currentReportType]?.selectableFields){const fields=[...document.querySelectorAll('#reportFieldChecks input[type=checkbox]:checked')].map(x=>x.value);if(fields.length)p.set('fields',fields.join(','));else if(reportFieldChecks.children.length)p.set('fields','__none__')}
 return p
}
function reportValue(v,key){
 if(v===null||v===undefined)return '';
 if(typeof v==='number'&&(/amount|total|nilai|harga|hpp|penjualan|pembelian|laba|debit|credit|kredit|saldo|kas_|arus/.test(key)))return rup(v);
 return v
}
function financeEscape(value){
 return String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'})[char])
}
function financialPeriodLabel(){
 const from=reportFrom.value||'awal';const to=reportTo.value||'sekarang';
 return currentReportType==='finance_balance'?`Per ${to}`:`Periode ${from} s.d. ${to}`
}
function financialLine(row,valueKey='jumlah'){
 return `<div class="psak-line"><span><small>${financeEscape(row.kode||'')}</small>${financeEscape(row.akun||'')}</span><b>${rup(Number(row[valueKey]||0))}</b></div>`
}
function renderPsakIncome(data){
 const groups=[
  ['Pendapatan','Pendapatan'],
  ['Harga Pokok Penjualan','Harga Pokok Penjualan'],
  ['Biaya Operasional','Beban Operasional']
 ];
 const byGroup=Object.fromEntries(groups.map(([key])=>[key,(data.rows||[]).filter(row=>row.kelompok===key)]));
 const section=(key,label,total,negative=false)=>`<section class="psak-section">
  <h3>${financeEscape(label)}</h3>
  ${byGroup[key].length?byGroup[key].map(row=>financialLine(row)).join(''):'<div class="psak-empty">Tidak ada saldo.</div>'}
  <div class="psak-subtotal"><span>Total ${financeEscape(label)}</span><b>${negative?'('+rup(Math.abs(Number(total||0)))+')':rup(Number(total||0))}</b></div>
 </section>`;
 financialReportView.innerHTML=`<article class="psak-paper">
  <header class="psak-report-header"><h2>LAPORAN LABA RUGI</h2><p>${financialPeriodLabel()}</p></header>
  ${section('Pendapatan','PENDAPATAN',data.summary.pendapatan)}
  ${section('Harga Pokok Penjualan','HARGA POKOK PENJUALAN',data.summary.hpp,true)}
  <div class="psak-grand"><span>LABA KOTOR</span><b>${rup(Number(data.summary.laba_kotor||0))}</b></div>
  ${section('Biaya Operasional','BEBAN OPERASIONAL',data.summary.biaya_operasional,true)}
  <div class="psak-grand final"><span>LABA BERSIH</span><b>${rup(Number(data.summary.laba_bersih||0))}</b></div>
 </article>`
}
function groupBalanceRows(rows){
 const groups={};
 rows.forEach(row=>{
  const key=row.kelompok||row.sisi||'Lainnya';
  (groups[key]??=[]).push(row)
 });
 return groups
}
function renderBalanceColumn(title,rows,total){
 const groups=groupBalanceRows(rows);
 return `<section class="psak-balance-column"><h3>${financeEscape(title)}</h3>
  ${Object.entries(groups).map(([group,items])=>`<div class="psak-balance-group">
   <h4>${financeEscape(group)}</h4>
   ${items.map(row=>financialLine(row,'saldo')).join('')}
   <div class="psak-subtotal"><span>Jumlah ${financeEscape(group)}</span><b>${rup(items.reduce((sum,row)=>sum+Number(row.saldo||0),0))}</b></div>
  </div>`).join('')}
  <div class="psak-column-total"><span>TOTAL ${financeEscape(title)}</span><b>${rup(Number(total||0))}</b></div>
 </section>`
}
function renderPsakBalance(data){
 const asset=(data.rows||[]).filter(row=>row.sisi==='ASET');
 const right=(data.rows||[]).filter(row=>row.sisi==='KEWAJIBAN & EKUITAS');
 const balanced=!!data.summary.balance;
 financialReportView.innerHTML=`<article class="psak-paper psak-balance-paper">
  <header class="psak-report-header"><h2>NERACA</h2><p>${financialPeriodLabel()}</p></header>
  <div class="psak-skonto">
   ${renderBalanceColumn('ASET',asset,data.summary.total_aset)}
   ${renderBalanceColumn('KEWAJIBAN & EKUITAS',right,data.summary.total_kewajiban_ekuitas)}
  </div>
  <div class="psak-balance-status ${balanced?'balanced':'unbalanced'}"><span>${balanced?'NERACA SEIMBANG':'NERACA TIDAK SEIMBANG'}</span><b>Selisih ${rup(Number(data.summary.selisih_neraca||0))}</b></div>
 </article>`
}

function renderPsakLedger(data){
 const s=data.summary||{};
 const renderRows=rows=>rows.length?rows.map(row=>`<tr>
    <td>${financeEscape(row.tanggal)}</td>
    <td><b>${financeEscape(row.nomor)}</b></td>
    <td>${financeEscape(row.keterangan)}</td>
    <td>${financeEscape(row.partner)}</td>
    <td>${financeEscape(row.referensi)}</td>
    <td class="num">${row.debit?rup(row.debit):'-'}</td>
    <td class="num">${row.kredit?rup(row.kredit):'-'}</td>
    <td class="num"><b>${rup(row.saldo)}</b></td>
   </tr>`).join(''):'<tr><td colspan="8" class="psak-empty">Tidak ada mutasi pada periode ini.</td></tr>';
 const accountBlock=section=>`<section class="ledger-account-section">
  <div class="ledger-account-head">
   <div><span>Kode Akun</span><b>${financeEscape(section.kode_akun||'-')}</b></div>
   <div><span>Nama Akun</span><b>${financeEscape(section.nama_akun||'-')}</b></div>
   <div><span>Tipe Akun</span><b>${financeEscape(section.tipe_akun||'-')}</b></div>
   <div><span>Pelanggan / Pemasok</span><b>${financeEscape(section.partner||'Semua')}</b></div>
  </div>
  <div class="ledger-opening"><span>Saldo Awal</span><b>${rup(Number(section.saldo_awal||0))}</b></div>
  <div class="ledger-table-wrap"><table class="ledger-report-table">
   <thead><tr><th>Tanggal</th><th>No. Bukti</th><th>Keterangan</th><th>Partner</th><th>Referensi</th><th>Debit</th><th>Kredit</th><th>Saldo</th></tr></thead>
   <tbody>${renderRows(section.rows||[])}</tbody>
  </table></div>
  <div class="ledger-totals">
   <div><span>Total Debit</span><b>${rup(Number(section.total_debit||0))}</b></div>
   <div><span>Total Kredit</span><b>${rup(Number(section.total_kredit||0))}</b></div>
   <div class="final"><span>Saldo Akhir</span><b>${rup(Number(section.saldo_akhir||0))}</b></div>
  </div>
 </section>`;
 const sections=s.all_accounts?(s.sections||[]):[{...s,rows:data.rows||[]}];
 financialReportView.innerHTML=`<article class="psak-paper ledger-paper">
  <header class="psak-report-header"><h2>BUKU BESAR</h2><p>${financialPeriodLabel()}</p></header>
  ${s.all_accounts?`<div class="ledger-account-head"><div><span>Cakupan</span><b>Semua Akun</b></div><div><span>Jumlah Akun</span><b>${Number(s.jumlah_akun||0)}</b></div><div><span>Total Debit</span><b>${rup(Number(s.total_debit||0))}</b></div><div><span>Total Kredit</span><b>${rup(Number(s.total_kredit||0))}</b></div></div>`:''}
  ${sections.length?sections.map(accountBlock).join(''):'<div class="psak-empty">Tidak ada akun aktif.</div>'}
 </article>`
}
function cashFlowSection(title,rows,total){
 return `<section class="cashflow-section"><h3>${financeEscape(title)}</h3>
  ${rows.length?rows.map(row=>`<div class="cashflow-line">
   <span><b>${financeEscape(row.uraian)}</b><small>${financeEscape(row.tanggal)} · ${financeEscape(row.nomor)} · ${financeEscape(row.akun_lawan)}</small></span>
   <strong class="${Number(row.arus_bersih)<0?'negative':''}">${Number(row.arus_bersih)<0?'('+rup(Math.abs(Number(row.arus_bersih)))+')':rup(Number(row.arus_bersih))}</strong>
  </div>`).join(''):'<div class="psak-empty">Tidak ada arus kas.</div>'}
  <div class="cashflow-total"><span>Kas Bersih ${financeEscape(title)}</span><b class="${Number(total)<0?'negative':''}">${Number(total)<0?'('+rup(Math.abs(Number(total)))+')':rup(Number(total||0))}</b></div>
 </section>`
}
function renderPsakCashFlow(data){
 const rows=data.rows||[],s=data.summary||{};
 const operating=rows.filter(row=>row.aktivitas==='Aktivitas Operasi');
 const investing=rows.filter(row=>row.aktivitas==='Aktivitas Investasi');
 const financing=rows.filter(row=>row.aktivitas==='Aktivitas Pendanaan');
 financialReportView.innerHTML=`<article class="psak-paper cashflow-paper">
  <header class="psak-report-header"><h2>LAPORAN ARUS KAS</h2><p>Metode Langsung · ${financialPeriodLabel()}</p></header>
  ${cashFlowSection('AKTIVITAS OPERASI',operating,s.aktivitas_operasi)}
  ${cashFlowSection('AKTIVITAS INVESTASI',investing,s.aktivitas_investasi)}
  ${cashFlowSection('AKTIVITAS PENDANAAN',financing,s.aktivitas_pendanaan)}
  <section class="cashflow-reconciliation">
   <div><span>Saldo Awal Kas dan Setara Kas</span><b>${rup(Number(s.saldo_awal_kas||0))}</b></div>
   <div><span>Kenaikan / (Penurunan) Bersih Kas</span><b class="${Number(s.kenaikan_penurunan_kas)<0?'negative':''}">${rup(Number(s.kenaikan_penurunan_kas||0))}</b></div>
   <div class="final"><span>Saldo Akhir Kas dan Setara Kas</span><b>${rup(Number(s.saldo_akhir_kas||0))}</b></div>
  </section>
 </article>`
}
async function loadCurrentReport(){
 try{
  if(!currentReportType)return;
  reportMessage.textContent='Memuat laporan...';
  const d=await api('/api/reports?'+reportParams().toString());
  if(reportDefinitions[currentReportType]?.selectableFields)buildReportFieldSelector(d.available_columns||d.columns||[]);
  const special=['finance_income','finance_balance','finance_ledger','finance_cashflow'].includes(currentReportType);
  financialReportView.style.display=special?'block':'none';
  reportTableContainer.style.display=special?'none':'block';
  if(currentReportType==='finance_income')renderPsakIncome(d);
  else if(currentReportType==='finance_balance')renderPsakBalance(d);
  else if(currentReportType==='finance_ledger')renderPsakLedger(d);
  else if(currentReportType==='finance_cashflow')renderPsakCashFlow(d);
  else{
   reportHead.innerHTML='<tr>'+d.columns.map(x=>`<th>${financeEscape(x[1])}</th>`).join('')+'</tr>';
   reportBody.innerHTML=d.rows.length?d.rows.map(r=>'<tr>'+d.columns.map(x=>`<td>${financeEscape(reportValue(r[x[0]],x[0]))}</td>`).join('')+'</tr>').join(''):
    `<tr><td colspan="${d.columns.length}" class="muted">Tidak ada data sesuai filter.</td></tr>`;
  }
  if(special){
   // Laporan PSAK memiliki ringkasan visual sendiri. Jangan render object/array mentah
   // seperti sections menjadi [object Object].
   reportSummary.innerHTML='';reportSummary.style.display='none';
  }else{
   reportSummary.style.display='block';
   reportSummary.innerHTML=Object.entries(d.summary||{})
    .filter(([k,v])=>!['balance','sections'].includes(k)&&v!==null&&typeof v!=='object')
    .map(([k,v])=>`<div class="summary-row"><span>${financeEscape(k.replaceAll('_',' '))}</span><b>${financeEscape(reportValue(v,k))}</b></div>`).join('');
  }
  reportMessage.textContent=`${d.rows.length} baris ditampilkan.`;
 }catch(e){msg(reportMessage,e.message,false)}
}

function exportCurrentReport(format){
 if(!currentReportType)return;
 const p=reportParams();p.set('format',format);p.set('token',token);
 window.open('/api/reports/export?'+p.toString(),'_blank')
}
function resetReportFilters(){
 document.querySelectorAll('#reportsPage input,#reportsPage select').forEach(x=>x.value='');
 loadCurrentReport()
}

function showOnly(selector, activeClass){
  document.querySelectorAll(selector).forEach(el=>el.style.display=el.classList.contains(activeClass)?'block':'none');
}
function openCashSection(section){
  page('cash');
  showOnly('.cash-section','cash-'+section);
  if(section==='history')loadCashTransactions();
}
function openInventorySection(section){
  page('inventory');
  showOnly('.inventory-section','inventory-'+section);
  if(section==='stock'){loadBalances();loadInventoryCard()}
}
function openAccountingSection(section){
  page('accounting');
  showOnly('.accounting-section','accounting-'+section);
  if(section==='coa'||section==='journal-list')loadAccounting();
  if(section==='ledger')loadLedger();
  if(section==='trial')loadTrial();if(section==='income')loadIncomeStatement();
}
function openExtraMaster(section){
  page('masterExtra');
  const cards=document.querySelectorAll('#masterExtra>.card');
  cards.forEach((card,index)=>card.style.display=(section==='brand'?index===0:index===1)?'block':'none');
  loadExtraMasters();
}

let priceLevels=[],priceLevelRecords=[];
async function loadPriceLevels(){let d=await api('/api/price-levels');priceLevels=d.items||[];priceLevelRecords=priceLevels;priceLevelBody.innerHTML=priceLevels.map(x=>`<tr><td>${accessEscape(x.code)}</td><td>${accessEscape(x.name)}</td><td>${accessEscape(x.description||'')}</td><td>${x.is_active?'Aktif':'Nonaktif'}</td><td><button onclick="editPriceLevel(${x.id})">Edit</button> <button class="danger" onclick="deletePriceLevel(${x.id})">Hapus</button></td></tr>`).join('')||'<tr><td colspan="5">Belum ada tingkatan harga.</td></tr>';renderPriceLevelSelectors()}
function renderPriceLevelSelectors(){if(window.custPriceLevel){let v=custPriceLevel.value;custPriceLevel.innerHTML='<option value="">Harga Default</option>'+priceLevels.filter(x=>x.is_active).map(x=>`<option value="${x.id}">${accessEscape(x.name)}</option>`).join('');custPriceLevel.value=v}if(window.productPriceLevelGrid){let current=window.__productLevelPrices||{};productPriceLevelGrid.innerHTML=priceLevels.filter(x=>x.is_active).map(x=>`<label class="field"><span>${accessEscape(x.name)}</span><input class="product-level-price" data-level-id="${x.id}" type="number" min="0" value="${current[String(x.id)]||0}"></label>`).join('')}}
async function savePriceLevel(){try{let id=priceLevelEditId.value;await api(id?'/api/price-levels/'+id:'/api/price-levels',{method:id?'PUT':'POST',body:JSON.stringify({code:plCode.value,name:plName.value,description:plDescription.value,is_active:true})});priceLevelEditId.value='';plCode.value=plName.value=plDescription.value='';msg(plMsg,id?'Tingkatan harga diperbarui.':'Tingkatan harga disimpan.');await loadPriceLevels()}catch(e){msg(plMsg,e.message,false)}}
function editPriceLevel(id){let x=priceLevelRecords.find(v=>v.id===id);if(!x)return;priceLevelEditId.value=x.id;plCode.value=x.code;plName.value=x.name;plDescription.value=x.description||''}
async function deletePriceLevel(id){if(!confirm('Nonaktifkan tingkatan harga ini?'))return;await api('/api/price-levels/'+id,{method:'DELETE'});await loadPriceLevels()}
function collectProductLevelPrices(){return [...document.querySelectorAll('.product-level-price')].map(x=>({price_level_id:x.dataset.levelId,selling_price:x.value||0}))}
function customerPriceLevelId(){let c=transactionCustomers?.find?.(x=>String(x.id)===String(saleCustomer.value));return c?.price_level_id||null}

let customerPageRecords=[],supplierPageRecords=[];
async function loadPartnerAccountOptions(){
  const d=await api('/api/coa?active=1'),rows=d.items||[];
  const rec=rows.filter(x=>(x.display_type||x.account_subtype)==='RECEIVABLE'),pay=rows.filter(x=>(x.display_type||x.account_subtype)==='PAYABLE');
  if(window.custReceivableAccount)custReceivableAccount.innerHTML='<option value="">Default - Piutang Usaha</option>'+rec.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');
  if(window.supPayableAccount)supPayableAccount.innerHTML='<option value="">Default - Hutang Usaha</option>'+pay.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');
}

async function loadCustomersPage(){
  await loadPartnerAccountOptions();
  const d=await api('/api/customers?active=1');customerPageRecords=d.items||[];
  customersPageBody.innerHTML=customerPageRecords.map(x=>`<tr><td>${accessEscape(x.code)}</td><td>${accessEscape(x.name)}</td><td>${accessEscape(x.phone||'')}</td><td>${accessEscape(x.city||'')}</td><td>${x.payment_term_days||0} hari</td><td>${x.opening_balance_date||'-'}</td><td>${rup(x.opening_balance)}</td><td><button onclick="editCustomer(${x.id})">Edit</button> <button class="danger" onclick="deleteCustomer(${x.id})">Hapus</button></td></tr>`).join('')||'<tr><td colspan="8">Belum ada pelanggan.</td></tr>';
}
async function loadSuppliersPage(){
  await loadPartnerAccountOptions();
  const d=await api('/api/suppliers?active=1');supplierPageRecords=d.items||[];
  suppliersPageBody.innerHTML=supplierPageRecords.map(x=>`<tr><td>${accessEscape(x.code)}</td><td>${accessEscape(x.name)}</td><td>${accessEscape(x.phone||'')}</td><td>${accessEscape(x.city||'')}</td><td>${x.payment_term_days||0} hari</td><td>${x.opening_balance_date||'-'}</td><td>${rup(x.opening_balance)}</td><td><button onclick="editSupplier(${x.id})">Edit</button> <button class="danger" onclick="deleteSupplier(${x.id})">Hapus</button></td></tr>`).join('')||'<tr><td colspan="8">Belum ada pemasok.</td></tr>';
}
function resetCustomerForm(){customerEditId.value='';custCode.value=custName.value=custPhone.value=custEmail.value=custCity.value=custAddress.value='';custTerm.value=0;custLimit.value=0;custOpening.value=0;custOpeningDate.value='';if(window.custPriceLevel)custPriceLevel.value='';if(window.custReceivableAccount)custReceivableAccount.value=''}
function resetSupplierForm(){supplierEditId.value='';supCode.value=supName.value=supPhone.value=supEmail.value=supCity.value=supAddress.value='';supTerm.value=0;supOpening.value=0;supOpeningDate.value='';if(window.supPayableAccount)supPayableAccount.value=''}
function editCustomer(id){const x=customerPageRecords.find(v=>v.id===id);if(!x)return;const set=(id,v)=>{const e=document.getElementById(id);if(e)e.value=v??''};set('customerEditId',x.id);set('custCode',x.code);set('custName',x.name);set('custPhone',x.phone);set('custEmail',x.email);set('custCity',x.city);set('custTerm',x.payment_term_days||0);set('custLimit',x.credit_limit||0);set('custOpening',x.opening_balance||0);set('custOpeningDate',x.opening_balance_date);set('custAddress',x.address);set('custPriceLevel',x.price_level_id);set('custReceivableAccount',x.receivable_account_id);document.getElementById('customersPage')?.scrollIntoView({behavior:'smooth',block:'start'})}
function editSupplier(id){const x=supplierPageRecords.find(v=>v.id===id);if(!x)return;const set=(id,v)=>{const e=document.getElementById(id);if(e)e.value=v??''};set('supplierEditId',x.id);set('supCode',x.code);set('supName',x.name);set('supPhone',x.phone);set('supEmail',x.email);set('supCity',x.city);set('supTerm',x.payment_term_days||0);set('supOpening',x.opening_balance||0);set('supOpeningDate',x.opening_balance_date);set('supAddress',x.address);set('supPayableAccount',x.payable_account_id);document.getElementById('suppliersPage')?.scrollIntoView({behavior:'smooth',block:'start'})}
async function deleteCustomer(id){if(!confirm('Nonaktifkan pelanggan ini? Riwayat transaksi tetap tersimpan.'))return;try{await api('/api/partners/'+id,{method:'DELETE'});resetCustomerForm();await Promise.all([loadCustomersPage(),loadTransactionPartners()])}catch(e){alert(e.message)}}
async function deleteSupplier(id){if(!confirm('Nonaktifkan pemasok ini? Riwayat transaksi tetap tersimpan.'))return;try{await api('/api/partners/'+id,{method:'DELETE'});resetSupplierForm();await Promise.all([loadSuppliersPage(),loadTransactionPartners()])}catch(e){alert(e.message)}}
async function addCustomer(){
  try{const id=customerEditId.value;
    await api(id?'/api/partners/'+id:'/api/partners',{method:id?'PUT':'POST',body:JSON.stringify({
      partner_type:'CUSTOMER',code:custCode.value,name:custName.value,
      phone:custPhone.value,email:custEmail.value,city:custCity.value,
      payment_term_days:custTerm.value,credit_limit:custLimit.value,
      opening_balance:custOpening.value,opening_balance_date:custOpeningDate.value,address:custAddress.value,price_level_id:custPriceLevel.value||null,receivable_account_id:custReceivableAccount.value||null,is_active:true
    })});
    msg(custMsg,id?'Pelanggan berhasil diperbarui.':'Pelanggan berhasil disimpan.');resetCustomerForm();
    await Promise.all([loadCustomersPage(),loadTransactionPartners()]);
  }catch(e){msg(custMsg,e.message,false)}
}
async function addSupplier(){
  try{const id=supplierEditId.value;
    await api(id?'/api/partners/'+id:'/api/partners',{method:id?'PUT':'POST',body:JSON.stringify({
      partner_type:'SUPPLIER',code:supCode.value,name:supName.value,
      phone:supPhone.value,email:supEmail.value,city:supCity.value,
      payment_term_days:supTerm.value,opening_balance:supOpening.value,opening_balance_date:supOpeningDate.value,
      address:supAddress.value,payable_account_id:supPayableAccount.value||null,is_active:true
    })});
    msg(supMsg,id?'Pemasok berhasil diperbarui.':'Pemasok berhasil disimpan.');resetSupplierForm();
    await Promise.all([loadSuppliersPage(),loadTransactionPartners()]);
  }catch(e){msg(supMsg,e.message,false)}
}

function accountTypeLabel(v){return ({CASH_BANK:'Kas Bank',RECEIVABLE:'Piutang',PAYABLE:'Hutang',ASSET:'Aset Lain',LIABILITY:'Kewajiban Lain',EQUITY:'Ekuitas',REVENUE:'Pendapatan',HPP:'Harga Pokok Penjualan',OPERATING_EXPENSE:'Biaya Operasional'})[v]||v}
const _oldLoadAccounting=loadAccounting;
loadAccounting=async function(){
 const templatePromise=loadCoaBusinessTemplates();
 const [c,j,cu,su]=await Promise.all([api('/api/coa?active=1'),api('/api/journals'),api('/api/customers?active=1'),api('/api/suppliers?active=1')]);
 await templatePromise;
 coaItems=c.items;coaData=c.items;window.journalCustomers=cu.items;window.journalSuppliers=su.items;
 coaBody.innerHTML=c.items.map(x=>`<tr><td>${x.code}</td><td>${x.name}</td><td>${accountTypeLabel(x.display_type)}</td><td>${x.normal_balance}</td><td>${x.is_active?'Aktif':'Nonaktif'}</td><td><button onclick=\"editCoa(${x.id})\">Edit</button> <button class=\"danger\" onclick=\"deleteCoa(${x.id})\">Hapus</button></td></tr>`).join('');
 ledgerAccount.innerHTML=c.items.map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');
 journalBody.innerHTML=j.items.map(x=>`<tr><td>${x.journal_date}</td><td>${x.journal_no}</td><td>${x.description}</td><td>${x.source_type}</td><td>${rup(x.total_debit)}</td><td>${rup(x.total_credit)}</td></tr>`).join('');
 if(!journalLines.length){addJLine();addJLine()}else renderJLines();refreshLedgerPartner();bindSmartImportMasters();if(c.items.length)await loadLedger();
}
function refreshLedgerPartner(){const a=coaItems.find(x=>String(x.id)===ledgerAccount.value),t=a?.display_type,list=t==='RECEIVABLE'?(window.journalCustomers||[]):t==='PAYABLE'?(window.journalSuppliers||[]):[];ledgerPartner.innerHTML='<option value="">Semua Partner</option>'+list.map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');ledgerPartner.disabled=!list.length;ledgerPartnerHelp.textContent=t==='RECEIVABLE'?'Filter Buku Besar Piutang per pelanggan.':t==='PAYABLE'?'Filter Buku Besar Hutang per pemasok.':'Hanya aktif untuk akun Piutang atau Hutang.'}
loadLedger=async function(){try{if(!ledgerAccount.value)return;refreshLedgerPartner();let d=await api('/api/general-ledger?account_id='+encodeURIComponent(ledgerAccount.value)+'&partner_id='+encodeURIComponent(ledgerPartner.value||'')+'&date_from='+encodeURIComponent(ledgerFrom.value||'')+'&date_to='+encodeURIComponent(ledgerTo.value||''));ledgerSummary.innerHTML=`<b>${d.account.code} - ${d.account.name}</b>${d.partner?'<br>Partner: '+d.partner.code+' - '+d.partner.name:''}<br>Saldo Awal: ${rup(d.opening_balance)} | Mutasi Debit: ${rup(d.period_debit)} | Mutasi Kredit: ${rup(d.period_credit)} | <b>Saldo Akhir: ${rup(d.ending_balance)}</b>`;ledgerBody.innerHTML=d.items.length?d.items.map(x=>`<tr><td>${x.journal_date}</td><td>${x.journal_no}</td><td>${x.description}${x.memo?' - '+x.memo:''}</td><td>${x.partner_name||'-'}</td><td>${x.reference_no||'-'}</td><td>${rup(x.debit)}</td><td>${rup(x.credit)}</td><td>${rup(x.running_balance)}</td></tr>`).join(''):'<tr><td colspan="8">Tidak ada mutasi.</td></tr>';ledgerUpdated.textContent='Terakhir diperbarui: '+new Date().toLocaleTimeString('id-ID')}catch(e){ledgerUpdated.textContent=e.message}}
ledgerAccount?.addEventListener('change',()=>{refreshLedgerPartner();loadLedger()});ledgerPartner?.addEventListener('change',loadLedger);
async function previewCoaTemplate(){
  const select=document.getElementById('coaTemplateSelect'),newCount=document.getElementById('coaTemplateNewCount'),existingCount=document.getElementById('coaTemplateExistingCount'),body=document.getElementById('coaTemplateBody'),message=document.getElementById('coaTemplateMsg');
  try{
    if(!select||!select.value)throw Error('Pilih jenis usaha terlebih dahulu.');
    const d=await api('/api/coa-template-preview?template='+encodeURIComponent(select.value));
    if(newCount)newCount.value=d.new_count||0;if(existingCount)existingCount.value=d.existing_count||0;
    if(body)body.innerHTML=(d.items||[]).map(x=>`<tr><td>${x.code}</td><td>${x.name}${x.existing_name&&x.existing_name!==x.name?`<br><small>Akun saat ini: ${x.existing_name}</small>`:''}</td><td>${accountTypeLabel(x.account_subtype)}</td><td>${x.status==='NEW'?'<b style="color:#087f5b">Akan dibuat</b>':'<span class="muted">Sudah ada — dilewati</span>'}</td></tr>`).join('')||'<tr><td colspan="4">Template tidak memiliki akun.</td></tr>';
    if(message)msg(message,`Preview ${d.name}: ${d.new_count} akun baru, ${d.existing_count} akun sudah ada.`);
    return d;
  }catch(e){if(message)msg(message,e.message,false);throw e}
}
async function applyCoaTemplate(){
  const select=document.getElementById('coaTemplateSelect'),message=document.getElementById('coaTemplateMsg');
  try{
    if(!select||!select.value)throw Error('Pilih jenis usaha terlebih dahulu.');
    await previewCoaTemplate();
    const label=select.options[select.selectedIndex]?.text||select.value;
    if(!confirm(`Buat seluruh akun baru dari standar ${label}? Akun yang sudah ada tidak akan ditimpa.`))return;
    const d=await api('/api/coa-template-apply',{method:'POST',body:JSON.stringify({template:select.value})});
    const created=Number(d.result?.created_count||0),skipped=Number(d.result?.skipped_count||0);
    await loadAccounting();
    const panel=document.getElementById('coaWizardPanel');
    if(panel)panel.classList.add('hidden');
    const target=document.getElementById('coaBody');
    if(target)target.closest('table')?.scrollIntoView({behavior:'smooth',block:'start'});
    const coaMessage=document.getElementById('coaMsg');
    if(coaMessage)msg(coaMessage,`COA standar ${label} berhasil diterapkan: ${created} akun baru, ${skipped} akun dilewati. Daftar akun sudah diperbarui.`);
    alert(`COA standar ${label} berhasil dibuat.\n\n${created} akun baru dibuat.\n${skipped} akun dilewati karena sudah ada.\n\nWizard akan ditutup dan Daftar Akun sudah diperbarui.`);
  }catch(e){if(message)msg(message,e.message,false)}
}
function resetCoaForm(){coaEditId.value='';coaCode.value='';coaName.value='';coaType.value='ASSET'}
function editCoa(id){const x=(coaItems||[]).find(a=>Number(a.id)===Number(id));if(!x)return;coaEditId.value=x.id;coaCode.value=x.code;coaName.value=x.name;coaType.value=x.display_type||x.account_subtype||x.account_type;coaCode.focus()}
async function deleteCoa(id){if(!confirm('Hapus/nonaktifkan akun ini? Akun yang sudah memiliki transaksi akan dinonaktifkan agar histori tetap aman.'))return;try{await api('/api/coa/'+id,{method:'DELETE'});msg(coaMsg,'Akun berhasil dihapus/dinonaktifkan.');resetCoaForm();await loadAccounting()}catch(e){msg(coaMsg,e.message,false)}}
function addCoa(){const id=coaEditId.value;api(id?'/api/coa/'+id:'/api/coa',{method:id?'PUT':'POST',body:JSON.stringify({code:coaCode.value,name:coaName.value,account_subtype:coaType.value,is_active:true})}).then(()=>{msg(coaMsg,id?'Akun berhasil diperbarui.':'Akun berhasil disimpan.');resetCoaForm();loadAccounting()}).catch(e=>msg(coaMsg,e.message,false))}
function addJLine(){journalLines.push({account_id:coaItems[0]?.id||'',partner_id:'',department_id:'',project_id:'',debit:0,credit:0,memo:''});renderJLines()}
function partnerOptions(line){const a=coaItems.find(x=>String(x.id)===String(line.account_id)),t=a?.display_type,list=t==='RECEIVABLE'?(window.journalCustomers||[]):t==='PAYABLE'?(window.journalSuppliers||[]):[];return {active:list.length>0,html:'<option value="">-- Pilih Partner --</option>'+list.map(x=>`<option value="${x.id}" ${String(x.id)===String(line.partner_id)?'selected':''}>${x.code} - ${x.name}</option>`).join('')}}
function renderJLines(){
  const body=byId('jLines');if(!body)return;
  const accounts=Array.isArray(coaItems)?coaItems:[];
  body.innerHTML=journalLines.map((x,i)=>{const p=partnerOptions(x);return `<tr><td><select onchange="journalLines[${i}].account_id=this.value;journalLines[${i}].partner_id='';renderJLines()"><option value="">-- Pilih Akun --</option>${accounts.map(a=>`<option value="${a.id}" ${String(a.id)===String(x.account_id)?'selected':''}>${accessEscape(a.code)} - ${accessEscape(a.name)} (${accountTypeLabel(a.display_type||a.account_subtype||a.account_type)})</option>`).join('')}</select></td><td><select ${p.active?'':'disabled'} onchange="journalLines[${i}].partner_id=this.value">${p.html}</select></td><td><select onchange="journalLines[${i}].department_id=this.value">${dimensionOptionHtml(transactionDepartments,'Departemen',x.department_id)}</select></td><td><select onchange="journalLines[${i}].project_id=this.value">${dimensionOptionHtml(transactionProjects,'Proyek',x.project_id)}</select></td><td><input type="number" value="${x.debit||0}" oninput="journalLines[${i}].debit=this.value"></td><td><input type="number" value="${x.credit||0}" oninput="journalLines[${i}].credit=this.value"></td><td><input value="${accessEscape(x.memo||'')}" oninput="journalLines[${i}].memo=this.value"></td><td><button class="danger" onclick="journalLines.splice(${i},1);renderJLines()">Hapus</button></td></tr>`}).join('')
}
async function saveJournal(){try{for(const line of journalLines){const a=coaItems.find(x=>String(x.id)===String(line.account_id)),t=a?.display_type||a?.account_subtype;if((t==='RECEIVABLE'||t==='PAYABLE')&&!line.partner_id)throw new Error((t==='RECEIVABLE'?'Pelanggan':'Pemasok')+' wajib dipilih untuk akun '+(a?.code||'')+' - '+(a?.name||''));}let payload={journal_date:jDate.value,description:jDesc.value,reference_no:jRef.value,lines:journalLines};let edited=await commitMaintenanceEdit(payload);let d=edited||await api('/api/manual-journals',{method:'POST',body:JSON.stringify(payload)});msg(jMsg,'Jurnal '+d.result.journal_no+' berhasil.');journalLines=[];addJLine();addJLine();await loadAccounting();await openFreshTransactionForm('journal')}catch(e){msg(jMsg,e.message,false)}}
async function loadIncomeStatement(){try{let d=await api('/api/income-statement?date_from='+encodeURIComponent(incomeFrom.value||'')+'&date_to='+encodeURIComponent(incomeTo.value||''));const rows=(title,a,total)=>`<h3>${title}</h3>${a.map(x=>`<div class="income-row"><span>${x.code} - ${x.name}</span><b>${rup(x.amount)}</b></div>`).join('')}<div class="income-total"><span>Total ${title}</span><b>${rup(total)}</b></div>`;incomeReport.innerHTML=rows('Pendapatan',d.revenue_items,d.revenue)+rows('Harga Pokok Penjualan',d.hpp_items,d.hpp)+`<div class="income-grand gross"><span>LABA KOTOR</span><b>${rup(d.gross_profit)}</b></div>`+rows('Biaya Operasional',d.expense_items,d.operating_expense)+`<div class="income-grand net"><span>LABA BERSIH</span><b>${rup(d.net_profit)}</b></div>`}catch(e){incomeReport.innerHTML='<p class="error">'+e.message+'</p>'}}
function bindSmartImportMasters(){if(window.importCash){importCash.innerHTML=(cashAccounts||[]).length?cashAccounts.map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join(''):'<option value="">Belum ada akun Kas/Bank</option>';importCash.disabled=!(cashAccounts||[]).length}if(window.importCoa){let a=(coaItems||[]).filter(x=>x.display_type!=='CASH_BANK');importCoa.innerHTML=a.length?a.map(x=>`<option value="${x.id}">${x.code} - ${x.name} (${accountTypeLabel(x.display_type)})</option>`).join(''):'<option value="">Belum ada akun lawan</option>';importCoa.disabled=!a.length}}



function bindOperationalCoaSelectors(){
  const active=Array.isArray(coaItems)?coaItems:[];
  const subtype=x=>x.display_type||x.account_subtype||x.account_type;
  const fill=(id,items,empty)=>{const el=byId(id);if(!el)return;const old=el.value;el.innerHTML=items.length?'<option value="">-- Pilih Akun --</option>'+items.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)} (${accountTypeLabel(subtype(x))})</option>`).join(''):`<option value="">${empty}</option>`;el.disabled=!items.length;if(items.some(x=>String(x.id)===String(old)))el.value=old};
  fill('pInventoryAccount',active.filter(x=>['ASSET','INVENTORY'].includes(subtype(x))),'Belum ada akun aset/persediaan');
  fill('pSalesAccount',active.filter(x=>['REVENUE','INCOME'].includes(subtype(x))||x.account_type==='REVENUE'),'Belum ada akun pendapatan');
  fill('pCogsAccount',active.filter(x=>['HPP','COGS'].includes(subtype(x))),'Belum ada akun HPP');
  const operational=active.filter(x=>!['CASH_BANK','RECEIVABLE','PAYABLE'].includes(subtype(x)));
  fill('cashCounterAccount',operational,'Belum ada akun lawan');
  fill('aAdjustmentAccount',operational,'Belum ada akun penyesuaian');
}
async function loadDocumentNumbers(preferredDate=''){
 try{
  const activeDate=preferredDate||document.getElementById('saleDate')?.value||document.getElementById('purchaseDate')?.value||document.getElementById('jDate')?.value||'';const d=await api('/api/document-numbers?date='+encodeURIComponent(activeDate));
  if(window.saleInvoiceNo&&!saleInvoiceNo.dataset.edited)saleInvoiceNo.value=d.invoice_no||'';
  if(window.saleDeliveryNo&&!saleDeliveryNo.dataset.edited)saleDeliveryNo.value=d.delivery_no||'';
  if(window.purchaseGoodsReceipt&&!purchaseGoodsReceipt.dataset.edited)purchaseGoodsReceipt.value=d.goods_receipt_no||'';
  if(window.jRef&&!jRef.dataset.edited)jRef.value=d.journal_no||'';
 }catch(e){}
}
['saleInvoiceNo','saleDeliveryNo','purchaseGoodsReceipt','jRef'].forEach(id=>document.getElementById(id)?.addEventListener('input',e=>e.target.dataset.edited='1'));
document.getElementById('saleDate')?.addEventListener('change',()=>{const a=document.getElementById('saleInvoiceNo'),b=document.getElementById('saleDeliveryNo');if(a)a.dataset.edited='';if(b)b.dataset.edited='';loadDocumentNumbers(document.getElementById('saleDate')?.value||'')});
document.getElementById('purchaseDate')?.addEventListener('change',()=>{const a=document.getElementById('purchaseGoodsReceipt');if(a)a.dataset.edited='';loadDocumentNumbers(document.getElementById('purchaseDate')?.value||'')});
document.getElementById('jDate')?.addEventListener('change',()=>{const a=document.getElementById('jRef');if(a)a.dataset.edited='';loadDocumentNumbers(document.getElementById('jDate')?.value||'')});

let suppressNumberBlur=false;
function numberRaw(v){
 let s=String(v??'').trim().replace(/\s/g,'');
 if(!s)return '';
 if(s.includes(',')&&s.includes('.'))s=s.replace(/\./g,'').replace(',','.');
 else if(s.includes(','))s=s.replace(',','.');
 else if(/^[-+]?\d{1,3}(\.\d{3})+$/.test(s))s=s.replace(/\./g,'');
 return s;
}
function formatNumberInput(el){
 if(!el||el.type==='date'||el.value==='')return;
 const raw=numberRaw(el.value),num=Number(raw);
 if(!Number.isFinite(num))return;
 const decimals=(raw.split('.')[1]||'').length;
 el.value=new Intl.NumberFormat('id-ID',{maximumFractionDigits:Math.min(decimals,4)}).format(num);
}
function stripNumberInputs(){document.querySelectorAll('input[data-number-format="1"]').forEach(el=>el.value=numberRaw(el.value))}
function formatAllNumberInputs(){document.querySelectorAll('input[data-number-format="1"]').forEach(formatNumberInput)}
document.querySelectorAll('input[type="number"]').forEach(el=>{
 el.dataset.numberFormat='1';el.dataset.step=el.step;el.type='text';el.inputMode='decimal';
 el.addEventListener('focus',()=>{el.value=numberRaw(el.value)});
 el.addEventListener('blur',()=>{if(!suppressNumberBlur)formatNumberInput(el)});
});
document.addEventListener('pointerdown',e=>{if(e.target.closest('button')){suppressNumberBlur=true;stripNumberInputs()}},true);
document.addEventListener('click',e=>{if(e.target.closest('button'))setTimeout(()=>{suppressNumberBlur=false;formatAllNumberInputs()},0)},true);
setTimeout(formatAllNumberInputs,0);



async function openFreshTransactionForm(kind){
 // Membuka form baru selalu keluar dari mode edit maintenance sebelumnya.
 // Tanpa reset ini, Simpan dapat mengirim PUT ke transaksi yang sudah dihapus/VOID.
 window.__maintenanceEdit=null;
 const today=new Date().toISOString().slice(0,10);
 try{
  if(kind==='sale'){
   window.__documentEdit=null;window.__sourceSalesOrderId=null;
   if(window.saleDate)saleDate.value=today;if(window.saleCustomer)saleCustomer.value='';if(window.saleSalesperson)saleSalesperson.value='';
   if(window.salePayment)salePayment.value='CREDIT';if(window.saleCashAccount)saleCashAccount.value='';
   if(window.saleTerm)saleTerm.value='0';if(window.saleDue)saleDue.value='';if(window.saleTax)saleTax.value='0';
   if(window.saleDiscount)saleDiscount.value='0';if(window.salePaid)salePaid.value='0';if(window.saleNotes)saleNotes.value='';
   if(window.saleInvoiceNo){saleInvoiceNo.dataset.edited='';}if(window.saleDeliveryNo){saleDeliveryNo.dataset.edited='';}
   if(window.saleLines){saleLines.innerHTML='';addSaleLine()}
   if(typeof saleInvoiceMaterialRows!=='undefined'){saleInvoiceMaterialRows=[];if(typeof renderSaleInvoiceMaterials==='function')renderSaleInvoiceMaterials()}
   resetTransactionDimensions('sale');await openSalesSection('entry');await loadDocumentNumbers();if(typeof setCreditUi==='function')setCreditUi();document.getElementById('saleCustomer')?.focus()
  }else if(kind==='purchase'){
   window.__documentEdit=null;window.__sourcePurchaseOrderId=null;
   if(window.purchaseDate)purchaseDate.value=today;if(window.purchaseSupplierInvoice)purchaseSupplierInvoice.value='';
   if(window.purchaseGoodsReceipt){purchaseGoodsReceipt.dataset.edited='';}
   if(window.purchaseSupplier)purchaseSupplier.value='';if(window.purchasePayment)purchasePayment.value='CREDIT';
   if(window.purchaseCashAccount)purchaseCashAccount.value='';if(window.purchaseDue)purchaseDue.value='';
   if(window.purchaseTax)purchaseTax.value='0';if(window.purchasePaid)purchasePaid.value='0';if(window.purchaseDiscount)purchaseDiscount.value='0';
   if(window.purchaseNotes)purchaseNotes.value='';purchaseLines=[];renderPurchaseLines();resetTransactionDimensions('purchase');
   await openPurchaseSection('entry');await loadDocumentNumbers();if(typeof setCreditUi==='function')setCreditUi();document.getElementById('purchaseSupplier')?.focus()
  }else if(kind==='cash'){
   if(window.cashDate)cashDate.value=today;if(window.cashAmount)cashAmount.value='';if(window.cashRef)cashRef.value='';if(window.cashDesc)cashDesc.value='';
   resetTransactionDimensions('cash');openCashSection('entry');document.getElementById('cashAmount')?.focus()
  }else if(kind==='transfer'){
   if(window.transferDate)transferDate.value=today;if(window.transferAmount)transferAmount.value='';if(window.transferRef)transferRef.value='';if(window.transferDesc)transferDesc.value='';
   openCashSection('transfer');document.getElementById('transferAmount')?.focus()
  }else if(kind==='journal'){
   if(window.jDate)jDate.value=today;if(window.jDesc)jDesc.value='';if(window.jRef){jRef.value='';jRef.dataset.edited='';}
   journalLines=[];addJLine();addJLine();openAccountingSection('manual');await loadDocumentNumbers(document.getElementById('jDate')?.value||'');document.getElementById('jDesc')?.focus()
  }else if(kind==='receivable'){
   window.__maintenanceEdit=null;if(window.rpAmount)rpAmount.value='';if(window.rpNotes)rpNotes.value='';if(window.rpDate)rpDate.value=today;document.getElementById('rpInvoice')?.focus()
  }else if(kind==='payable'){
   window.__maintenanceEdit=null;if(window.phAmount)phAmount.value='';if(window.phNotes)phNotes.value='';if(window.phDate)phDate.value=today;document.getElementById('phPurchase')?.focus()
  }else if(kind==='salesReturn'){
   window.__salesReturnEdit=null;srLines=[];addReturnLine('sr');if(window.srDate)srDate.value=today;if(window.srNotes)srNotes.value='';await openSalesReturns()
  }else if(kind==='purchaseReturn'){
   window.__purchaseReturnEdit=null;prLines=[];addReturnLine('pr');if(window.prDate)prDate.value=today;if(window.prNotes)prNotes.value='';await openPurchaseReturns()
  }else if(kind==='adjustment'){
   if(window.aQty)aQty.value='';if(window.aRef)aRef.value='';if(window.aReason)aReason.value='';if(window.aAdjustmentAccountField)aAdjustmentAccountField.style.display='';resetTransactionDimensions('adjust');document.getElementById('aQty')?.focus()
  }else if(kind==='stockTransfer'){
   if(window.tQty)tQty.value='';if(window.tRef)tRef.value='';if(window.tReason)tReason.value='';document.getElementById('tQty')?.focus()
  }
 }catch(e){console.error('Gagal menyiapkan form transaksi baru',kind,e)}
}

function downloadJournalTemplate(){
 window.open('/api/manual-journals/template?token='+encodeURIComponent(token),'_blank')
}
async function importJournalExcel(){
 try{
  const f=journalExcelFile.files[0];if(!f)return;
  const bytes=new Uint8Array(await f.arrayBuffer());let binary='',chunk=32768;
  for(let i=0;i<bytes.length;i+=chunk)binary+=String.fromCharCode(...bytes.subarray(i,i+chunk));
  const d=await api('/api/manual-journals/import-excel',{method:'POST',
    body:JSON.stringify({file_name:f.name,excel_base64:btoa(binary)})});
  msg(jMsg,`${d.result.journal_count} jurnal berhasil diimpor.`);
  journalExcelFile.value='';await loadAccounting()
 }catch(e){msg(jMsg,e.message,false)}
}


function downloadImportTemplate(kind){
 window.open('/api/'+kind+'/template?token='+encodeURIComponent(token),'_blank')
}
async function importTransactionExcel(kind){
 try{
  const input=document.getElementById(kind+'ExcelFile');const f=input.files[0];if(!f)return;
  const bytes=new Uint8Array(await f.arrayBuffer());let binary='',chunk=32768;
  for(let i=0;i<bytes.length;i+=chunk)binary+=String.fromCharCode(...bytes.subarray(i,i+chunk));
  const d=await api('/api/'+kind+'/import-excel',{method:'POST',
    body:JSON.stringify({file_name:f.name,excel_base64:btoa(binary)})});
  alert(`${d.result.transaction_count} transaksi berhasil diimpor.`);
  input.value='';
  if(kind==='sales'){await Promise.all([loadSales(),loadProducts()]);await openFreshTransactionForm('sale')}
  else if(kind==='purchases'){await Promise.all([loadPurchases(),loadProducts()]);await openFreshTransactionForm('purchase')}
  else await Promise.all([loadCashTransactions(),loadCashAccounts(),loadAccounting()])
 }catch(e){alert(e.message)}
}

setTimeout(()=>{let t=new Date().toISOString().slice(0,10);if(window.pOpeningDate&&!pOpeningDate.value)pOpeningDate.value=t;if(window.custOpeningDate&&!custOpeningDate.value)custOpeningDate.value=t;if(window.supOpeningDate&&!supOpeningDate.value)supOpeningDate.value=t},300);

let prLines=[],srLines=[];
function returnProductOptions(stockOnly=false){return '<option value="">Pilih</option>'+transactionProducts.filter(x=>!stockOnly||x.product_type==='STOCK').map(x=>`<option value="${x.id}">${x.sku} - ${x.name}</option>`).join('')}
function addReturnLine(k,item={}){let a=k==='pr'?prLines:srLines;a.push({product_id:item.product_id||'',qty:item.qty||1,unit_value:item.unit_value||0});renderReturnLines(k)}
function renderReturnLines(k){let a=k==='pr'?prLines:srLines,b=document.getElementById(k+'Body');b.innerHTML=a.map((x,i)=>`<tr><td><select onchange="${k}Lines[${i}].product_id=this.value">${returnProductOptions(k==='pr')}</select></td><td><input type="number" min="0.0001" step="0.0001" value="${x.qty}" onchange="${k}Lines[${i}].qty=this.value"></td><td><input type="number" min="0" step="0.01" value="${x.unit_value}" onchange="${k}Lines[${i}].unit_value=this.value"></td><td><button class="danger" onclick="${k}Lines.splice(${i},1);renderReturnLines('${k}')">Hapus</button></td></tr>`).join('');a.forEach((x,i)=>{let s=b.rows[i].cells[0].querySelector('select');s.value=x.product_id})}
async function openPurchaseReturns(){page('purchaseReturns');prDate.value=new Date().toISOString().slice(0,10);await loadReturnMasters();await loadPurchaseReturns();if(!prLines.length)addReturnLine('pr')}
async function openSalesReturns(){page('salesReturns');srDate.value=new Date().toISOString().slice(0,10);await loadReturnMasters();await loadSalesReturns();if(!srLines.length)addReturnLine('sr')}
async function loadReturnMasters(){let [ps,ss]=await Promise.all([api('/api/purchases'),api('/api/sales')]);prInvoice.innerHTML='<option value="">Tanpa invoice</option>'+ps.items.map(x=>`<option value="${x.id}">${x.purchase_no} - ${x.supplier_name}</option>`).join('');srInvoice.innerHTML='<option value="">Tanpa invoice</option>'+ss.items.map(x=>`<option value="${x.id}">${x.invoice_no} - ${x.customer_name||'Umum'}</option>`).join('');prSupplier.innerHTML=partners.filter(x=>['SUPPLIER','BOTH'].includes(x.partner_type)).map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');srCustomer.innerHTML=partners.filter(x=>['CUSTOMER','BOTH'].includes(x.partner_type)).map(x=>`<option value="${x.id}">${x.code} - ${x.name}</option>`).join('');let wo=warehouses.map(x=>`<option value="${x.id}">${x.name}</option>`).join('');prWarehouse.innerHTML=srWarehouse.innerHTML=wo}
async function loadPurchaseReturnInvoice(){if(!prInvoice.value)return;let x=await api('/api/purchases/'+prInvoice.value);prSupplier.value=x.supplier_id;prWarehouse.value=x.warehouse_id;prLines=x.items.filter(i=>i.product_type==='STOCK').map(i=>({product_id:i.product_id,qty:i.qty,unit_value:i.line_total/i.qty}));renderReturnLines('pr')}
async function loadSalesReturnInvoice(){if(!srInvoice.value)return;let x=await api('/api/sales/'+srInvoice.value);if(x.customer_id)srCustomer.value=x.customer_id;srWarehouse.value=x.warehouse_id;srLines=x.items.map(i=>({product_id:i.product_id,qty:i.qty,unit_value:i.line_total/i.qty}));renderReturnLines('sr')}
async function savePurchaseReturn(){try{let payload={purchase_id:prInvoice.value||null,return_date:prDate.value,supplier_id:prSupplier.value,warehouse_id:prWarehouse.value,notes:prNotes.value,items:prLines};let id=window.__purchaseReturnEdit;let r=await api(id?'/api/purchase-returns/'+id:'/api/purchase-returns',{method:id?'PUT':'POST',body:JSON.stringify(payload)});window.__purchaseReturnEdit=null;msg(prMsg,(id?'Retur diperbarui ':'Tersimpan ')+(r.result.return_no||''));prLines=[];addReturnLine('pr');await loadPurchaseReturns();await openFreshTransactionForm('purchaseReturn')}catch(e){msg(prMsg,e.message,false)}}
async function saveSalesReturn(){try{let payload={sale_id:srInvoice.value||null,return_date:srDate.value,customer_id:srCustomer.value,warehouse_id:srWarehouse.value,notes:srNotes.value,items:srLines};let id=window.__salesReturnEdit;let r=await api(id?'/api/sales-returns/'+id:'/api/sales-returns',{method:id?'PUT':'POST',body:JSON.stringify(payload)});window.__salesReturnEdit=null;msg(srMsg,(id?'Retur diperbarui ':'Tersimpan ')+(r.result.return_no||''));srLines=[];addReturnLine('sr');await loadSalesReturns();await openFreshTransactionForm('salesReturn')}catch(e){msg(srMsg,e.message,false)}}
async function loadPurchaseReturns(){let d=await api('/api/purchase-returns');prList.innerHTML=d.items.map(x=>`<tr><td>${x.return_date}</td><td>${x.return_no}</td><td>${x.supplier_name}</td><td>${rup(x.total_payable)}</td><td>${rup(x.total_inventory)}</td><td>${rup(x.difference)}</td><td>${x.status==='VOID'?'':`<button onclick="editPurchaseReturn(${x.id})">Edit</button> <button class="danger" onclick="deletePurchaseReturn(${x.id})">Hapus</button>`}</td></tr>`).join('')}
async function loadSalesReturns(){let d=await api('/api/sales-returns');srList.innerHTML=d.items.map(x=>`<tr><td>${x.return_date}</td><td>${x.return_no}</td><td>${x.customer_name}</td><td>${rup(x.total_sales)}</td><td>${rup(x.total_cogs)}</td><td>${x.status==='VOID'?'':`<button onclick="editSalesReturn(${x.id})">Edit</button> <button class="danger" onclick="deleteSalesReturn(${x.id})">Hapus</button>`}</td></tr>`).join('')}
async function viewPurchaseReturn(id){try{await editPurchaseReturn(id);window.__purchaseReturnEdit=null;activateTransactionViewMode('Retur Pembelian')}catch(e){alert(e.message)}}
async function viewSalesReturn(id){try{await editSalesReturn(id);window.__salesReturnEdit=null;activateTransactionViewMode('Retur Penjualan')}catch(e){alert(e.message)}}
async function editPurchaseReturn(id){let d=await api('/api/purchase-returns/'+id);await openPurchaseReturns();prDate.value=d.return_date;prInvoice.value=d.purchase_id||'';prSupplier.value=d.supplier_id;prWarehouse.value=d.warehouse_id;prNotes.value=d.notes||'';prLines=(d.items||[]).map(i=>({product_id:i.product_id,qty:i.qty,unit_value:i.unit_value}));renderReturnLines('pr');window.__purchaseReturnEdit=id;msg(prMsg,'Mode edit retur pembelian. Simpan untuk membuat pembalikan dan transaksi pengganti.')}
async function editSalesReturn(id){let d=await api('/api/sales-returns/'+id);await openSalesReturns();srDate.value=d.return_date;srInvoice.value=d.sale_id||'';srCustomer.value=d.customer_id;srWarehouse.value=d.warehouse_id;srNotes.value=d.notes||'';srLines=(d.items||[]).map(i=>({product_id:i.product_id,qty:i.qty,unit_value:i.unit_value}));renderReturnLines('sr');window.__salesReturnEdit=id;msg(srMsg,'Mode edit retur penjualan. Simpan untuk membuat pembalikan dan transaksi pengganti.')}
async function deletePurchaseReturn(id){if(!confirm('Batalkan retur pembelian ini? Stok dan jurnal akan dibalik.'))return;try{await api('/api/purchase-returns/'+id,{method:'DELETE'});await loadPurchaseReturns()}catch(e){alert(e.message)}}
async function deleteSalesReturn(id){if(!confirm('Batalkan retur penjualan ini? Stok dan jurnal akan dibalik.'))return;try{await api('/api/sales-returns/'+id,{method:'DELETE'});await loadSalesReturns()}catch(e){alert(e.message)}}


let tmItems=[];
const tmLabels={cash:'Daftar Kas Masuk/Keluar',transfer:'Daftar Transfer Kas/Bank',journal:'Daftar Jurnal Manual',adjustment:'Daftar Adjustment Stok',receivable:'Daftar Terima Piutang',payable:'Daftar Bayar Hutang',warehouse_transfer:'Daftar Transfer Gudang'};
async function openTransactionMaintenance(kind){page('transactionMaintenance');tmKind.value=kind;await loadTransactionMaintenance()}
async function loadTransactionMaintenance(){try{const kind=tmKind.value;tmTitle.textContent=tmLabels[kind];const d=await api('/api/transaction-maintenance/'+kind);tmItems=d.items||[];renderTransactionMaintenance()}catch(e){msg(tmMsg,e.message,false)}}
function tmInfo(x){return [x.account_name,x.source_account&&x.source_account+' → '+x.target_account,x.partner_name,x.invoice_no,x.sku&&x.sku+' - '+x.product_name,x.description].filter(Boolean).join(' · ')}
function renderTransactionMaintenance(){const q=(tmSearch.value||'').toLowerCase();tmBody.innerHTML=tmItems.filter(x=>!x.is_void&&JSON.stringify(x).toLowerCase().includes(q)).map(x=>`<tr><td>${x.date||''}</td><td>${x.number||''}</td><td>${tmInfo(x)}</td><td class="num">${rup(x.amount||0)}</td><td>${x.is_void?'<span class="badge danger">DIBATALKAN</span>':'<span class="badge success">AKTIF</span>'}</td><td>${x.is_void?'':`<button class="secondary" onclick="editMaintainedTransaction('${tmKind.value}','${x.key}')">Edit</button> <button class="danger" onclick="deleteMaintainedTransaction('${tmKind.value}','${x.key}')">Hapus</button>`}</td></tr>`).join('')}
async function deleteMaintainedTransaction(kind,key){if(!confirm('Hapus/batalkan transaksi ini? Sistem akan membuat pembalikan otomatis.'))return;clearTransactionEditState();try{await api('/api/transaction-maintenance/'+kind+'/'+encodeURIComponent(key),{method:'DELETE',body:JSON.stringify({reason:'Dihapus dari daftar transaksi'})});clearTransactionEditState();if(window.aAdjustmentAccountField)aAdjustmentAccountField.style.display='';msg(tmMsg,'Transaksi berhasil dihapus dari daftar aktif.');await loadTransactionMaintenance();if(kind==='cash')await Promise.allSettled([loadCashAccounts(),loadCashTransactions(),loadAccounting(),loadTrial(),loadDash(),loadSummary()]);else if(kind==='journal'){journalLines=[];try{renderJLines()}catch(e){};if(window.jDesc)jDesc.value='';if(window.jRef)jRef.value='';await Promise.allSettled([loadAccounting(),loadTrial(),loadDash(),loadCashAccounts()]);}else if(kind==='receivable'||kind==='payable')await Promise.allSettled([loadReceivables(),loadPayables(),loadCashAccounts(),loadAccounting(),loadDash()])}catch(e){msg(tmMsg,e.message,false)}}
async function editMaintainedTransaction(kind,key){const x=tmItems.find(i=>String(i.key)===String(key));if(!x)return;alert('Transaksi akan dibuka pada formulir asal. Setelah data diperbaiki dan disimpan, gunakan tombol Simpan Perubahan pada dialog berikut.');
  if(kind==='cash'){await Promise.all([loadCashAccounts(),loadAccounting(),loadTransactionDimensions()]);openCashSection('entry');cashDate.value=x.date||'';cashAccount.value=x.account_id||'';cashType.value=x.type||'IN';const counterId=String(x.counter_account_id||'');if(counterId&&!Array.from(cashCounterAccount.options).some(o=>String(o.value)===counterId)){const opt=document.createElement('option');opt.value=counterId;opt.textContent=((x.counter_account_code||'')+(x.counter_account_code?' - ':'')+(x.counter_account_name||'Akun lawan transaksi')+' (akun transaksi lama)');cashCounterAccount.appendChild(opt);cashCounterAccount.disabled=false}cashCounterAccount.value=counterId;cashAmount.value=x.amount||0;cashRef.value=x.reference_no||'';cashDesc.value=x.description||''}
  else if(kind==='transfer'){await loadCashAccounts();openCashSection('transfer');transferDate.value=x.date||'';cashSource.value=x.source_account_id||'';cashTarget.value=x.target_account_id||'';transferAmount.value=x.amount||0;transferRef.value=x.reference_no||'';transferDesc.value=x.description||''}
  else if(kind==='journal'){await Promise.all([loadAccounting(),loadTransactionDimensions()]);openAccountingSection('manual');const d=await api('/api/transaction-maintenance/journal/'+key);jDate.value=d.journal_date;jDesc.value=d.description;jRef.value=d.reference_no||d.journal_no||'';jRef.dataset.edited='1';journalLines=(d.lines||[]).map(l=>({account_id:l.account_id,partner_id:l.partner_id||'',department_id:l.department_id||'',project_id:l.project_id||'',debit:l.debit,credit:l.credit,memo:l.memo||''}));renderJLines()}
  else if(kind==='adjustment'){await Promise.all([loadAccounting(),loadProducts(),loadWarehouses(),loadTransactionDimensions()]);page('stock');aWarehouse.value=x.warehouse_id;aProduct.value=x.product_id;aQty.value=x.amount;aRef.value=x.reference_no||'';aReason.value=x.description||'';if(x.adjustment_account_id)aAdjustmentAccount.value=x.adjustment_account_id;if(window.aAdjustmentAccountField)aAdjustmentAccountField.style.display='none'}
  else if(kind==='receivable'){page('receivables');await Promise.all([loadSettlementMasters(),loadCashAccounts()]);if(x.customer_id)rpCustomer.value=String(x.customer_id);await loadReceivables();const target=String(x.sale_id||'');if(target&&!Array.from(rpInvoice.options).some(o=>String(o.value)===target)){const opt=document.createElement('option');opt.value=target;opt.textContent=(x.invoice_no||x.number||'Piutang transaksi lama')+' | '+(x.partner_name||'')+' (transaksi lama)';rpInvoice.appendChild(opt)}rpInvoice.value=target;rpCash.value=x.cash_account_id;rpDate.value=x.date;rpAmount.value=x.amount;rpNotes.value=x.description||''}
  else if(kind==='payable'){page('payables');await Promise.all([loadSettlementMasters(),loadCashAccounts()]);if(x.supplier_id)phSupplier.value=String(x.supplier_id);await loadPayables();const target=String(x.purchase_id||'');if(target&&!Array.from(phPurchase.options).some(o=>String(o.value)===target)){const opt=document.createElement('option');opt.value=target;opt.textContent=(x.invoice_no||x.number||'Hutang transaksi lama')+' | '+(x.partner_name||'')+' (transaksi lama)';phPurchase.appendChild(opt)}phPurchase.value=target;phCash.value=x.cash_account_id;phDate.value=x.date;phAmount.value=x.amount;phNotes.value=x.description||''}
  else if(kind==='warehouse_transfer'){await Promise.all([loadProducts(),loadWarehouses()]);page('stock');tProduct.value=x.product_id||'';tSource.value=x.source_warehouse_id||'';tTarget.value=x.target_warehouse_id||'';tQty.value=x.amount||0;tRef.value=x.reference_no||'';tReason.value=x.description||''}
  window.__maintenanceEdit={kind,key};
}
async function commitMaintenanceEdit(payload){if(!window.__maintenanceEdit)return false;const {kind,key}=window.__maintenanceEdit;try{const result=await api('/api/transaction-maintenance/'+kind+'/'+encodeURIComponent(key),{method:'PUT',body:JSON.stringify(payload)});window.__maintenanceEdit=null;if(window.aAdjustmentAccountField)aAdjustmentAccountField.style.display='';return result}catch(e){if(/sudah dihapus\/dibatalkan|sudah dibatalkan|tidak ditemukan/i.test(String(e.message||''))){clearTransactionEditState();if(window.aAdjustmentAccountField)aAdjustmentAccountField.style.display='';return false}throw e}}

function activateTransactionViewMode(title){
  const visible=[...document.querySelectorAll('.page')].find(p=>getComputedStyle(p).display!=='none');
  if(!visible)return;
  visible.querySelectorAll('input,select,textarea').forEach(el=>el.disabled=true);
  visible.querySelectorAll('button').forEach(el=>{if(!/Kembali|Tutup|Daftar/i.test(el.textContent||''))el.disabled=true});
  const card=visible.querySelector('.card');if(card){const note=document.createElement('div');note.className='summary-box';note.innerHTML='<b>Mode Lihat:</b> '+accessEscape(title||'Transaksi')+' — data hanya dapat dibaca.';card.prepend(note)}
}
async function viewMaintainedTransaction(kind,key){try{const x=tmItems.find(i=>String(i.key)===String(key));await editMaintainedTransaction(kind,key);window.__maintenanceEdit=null;activateTransactionViewMode((x&&x.number)||tmLabels[kind])}catch(e){msg(tmMsg,e.message,false)}}
async function viewFixedAsset(id){try{await editFixedAsset(id);window.__fixedAssetEdit=null;activateTransactionViewMode('Aktiva Tetap')}catch(e){alert(e.message)}}
async function editFixedAsset(id){try{const d=await api('/api/fixed-assets/'+id);await openFixedAssetNew();faCode.value=d.asset_code;faName.value=d.asset_name;faDate.value=d.acquisition_date;faCost.value=d.acquisition_cost;faResidual.value=d.residual_value;faLife.value=d.useful_life_months;faAssetAccount.value=d.asset_account_id;faAccumAccount.value=d.accumulated_depreciation_account_id;faExpenseAccount.value=d.depreciation_expense_account_id;faContraAccount.value=d.contra_account_id;faNotes.value=d.notes||'';window.__fixedAssetEdit=id;msg(faMsg,'Mode edit aktiva tetap.')}catch(e){alert(e.message)}}
async function deleteFixedAsset(id){if(!confirm('Hapus aktiva tetap ini? Jurnal perolehan akan dibatalkan.'))return;try{await api('/api/fixed-assets/'+id,{method:'DELETE'});await loadFixedAssets()}catch(e){alert(e.message)}}
async function viewDepreciation(id){try{const d=await api('/api/fixed-assets/depreciations');const x=(d.items||[]).find(v=>Number(v.id)===Number(id));if(!x)throw Error('Penyusutan tidak ditemukan.');faPeriod.value=x.period;await loadFixedAssets();page('fixedAssetDepPage');activateTransactionViewMode('Penyusutan '+x.period+' - '+x.asset_code+' '+x.asset_name)}catch(e){alert(e.message)}}
async function deleteDepreciation(id){if(!confirm('Hapus penyusutan periode ini dan batalkan jurnalnya?'))return;await api('/api/fixed-assets/depreciations/'+id,{method:'DELETE'});await loadFixedAssets();await loadDepreciationHistory()}
async function loadDepreciationHistory(){try{const d=await api('/api/fixed-assets/depreciations');const items=d.items||[];if(typeof faDepHistory!=='undefined')faDepHistory.innerHTML=items.map(x=>`<tr><td>${x.period}</td><td>${accessEscape(x.asset_code)} - ${accessEscape(x.asset_name)}</td><td class="number-cell">${rup(x.amount)}</td><td>${accessEscape(x.journal_no||'-')}</td><td><button class="danger" onclick="deleteDepreciation(${x.id})">Hapus</button></td></tr>`).join('')||'<tr><td colspan="5">Belum ada penyusutan yang diproses.</td></tr>'}catch(e){if(typeof faDepHistory!=='undefined')faDepHistory.innerHTML=`<tr><td colspan="5" class="error">${accessEscape(e.message)}</td></tr>`}}
async function viewSale(id){await editSale(id);window.__documentEdit=null;activateTransactionViewMode('Penjualan')}
async function viewPurchase(id){await editPurchase(id);window.__documentEdit=null;activateTransactionViewMode('Pembelian')}
async function editSale(id){const d=await api('/api/sales/'+id);window.__documentEdit={kind:'sale',id};await openSalesSection('entry');saleInvoiceNo.value=d.invoice_no||'';saleDeliveryNo.value=d.delivery_no||'';saleDate.value=d.sale_date;saleCustomer.value=d.customer_id||'';saleSalesperson.value=d.salesperson_id||'';saleWarehouse.value=d.warehouse_id||'';salePayment.value=d.payment_method||'CREDIT';saleCashAccount.value=d.cash_account_id||'';saleTerm.value=0;saleDue.value=d.due_date||'';saleTax.value=d.tax_percent||0;salePaid.value=d.paid_amount||0;saleDiscount.value=d.discount_amount||0;saleNotes.value=d.notes||'';saleInvoiceMaterialRows=(d.invoice_materials||[]).map(x=>({...x,selected:true}));renderSaleInvoiceMaterials();saleLines.innerHTML='';(d.items||[]).forEach(i=>{addSaleLine();let r=saleLines.lastElementChild;r.querySelector('.slProduct').value=i.product_id;lineProduct(r.querySelector('.slProduct'));r.querySelector('.slDescription').value=i.product_name||'';if(i.unit_id)r.querySelector('.slUnit').value=i.unit_id;r.querySelector('.slQty').value=i.qty;r.querySelector('.slPrice').value=i.unit_price});window.__documentEdit={kind:'sale',id};estimateSale();msg(saleMsg,'Mode edit penjualan. Perubahan disimpan pada transaksi dan jurnal yang sama.')}
async function editPurchase(id){const d=await api('/api/purchases/'+id);window.__documentEdit={kind:'purchase',id};await openPurchaseSection('entry');purchaseDate.value=d.purchase_date;purchaseSupplierInvoice.value=d.supplier_invoice_no||'';purchaseGoodsReceipt.value=d.goods_receipt_no||'';purchaseSupplier.value=d.supplier_id;purchaseWarehouse.value=d.warehouse_id;purchasePayment.value=d.payment_method||'CREDIT';purchaseCashAccount.value=d.cash_account_id||'';purchaseDue.value=d.due_date||'';purchaseTax.value=d.tax_percent||0;purchasePaid.value=d.paid_amount||0;purchaseDiscount.value=d.discount_amount||0;purchaseNotes.value=d.notes||'';purchaseLines=(d.items||[]).map(i=>({product_id:i.product_id,qty:i.qty,unit_id:i.unit_id,unit_code:i.unit_code,conversion_ratio:i.conversion_ratio,unit_cost:i.unit_cost,discount_mode:'AMOUNT',discount_value:i.discount_amount||0,name:i.product_name}));renderPurchaseLines();window.__documentEdit={kind:'purchase',id};msg(purchaseMsg,'Mode edit pembelian. Perubahan disimpan pada transaksi dan jurnal yang sama.')}
async function voidSale(id){if(!confirm('Hapus/batalkan penjualan ini? Stok, kas dan jurnal akan dibalik bila transaksi belum terkait retur atau pembayaran lain.'))return;try{await api('/api/sales/'+id,{method:'DELETE'});await Promise.all([loadSales(),loadProducts(),loadSummary(),loadBalances(),loadInventoryCard(),loadCashAccounts()])}catch(e){alert(e.message)}}
async function voidPurchase(id){if(!confirm('Hapus/batalkan pembelian ini? Stok, kas dan jurnal akan dibalik bila transaksi belum terkait retur atau pembayaran lain.'))return;try{await api('/api/purchases/'+id,{method:'DELETE'});await Promise.all([loadPurchases(),loadProducts(),loadSummary(),loadBalances(),loadInventoryCard(),loadCashAccounts()])}catch(e){alert(e.message)}}


let odData={partners:[],products:[],warehouses:[],cash:[],salesOrders:[],purchaseOrders:[]};let odEditOrderId=null;
async function openOrdersDp(tab='sales'){window.odMode=(tab==='purchase'?'purchase':'sales');page('ordersDp');odPageHeading.textContent=window.odMode==='sales'?'Pesanan & DP Penjualan':'Pesanan & DP Pembelian';odSalesTabs.style.display=window.odMode==='sales'?'flex':'none';odPurchaseTabs.style.display=window.odMode==='purchase'?'flex':'none';await odLoadMaster();await odTab(tab)}
async function odLoadMaster(){let [p,pr,w,c,so,po]=await Promise.all([api('/api/partners'),api('/api/products?active=1'),api('/api/warehouses?active=1'),api('/api/cash-accounts?active=1'),api('/api/sales-orders'),api('/api/purchase-orders')]);odData.partners=p.items||[];odData.products=pr.items||[];odData.warehouses=w.items||[];odData.cash=c.items||[];odData.salesOrders=so.items||[];odData.purchaseOrders=po.items||[]}
function odOpts(a,val='id',label='name'){return a.map(x=>`<option value="${x[val]}">${accessEscape(x[label]||x.name||x.code)}</option>`).join('')}
function odProductUnits(pid){let p=odData.products.find(x=>String(x.id)===String(pid));if(!p)return[];let source=(Array.isArray(p.units)&&p.units.length?p.units:(p.stock_units||[]));let u=source.map(x=>({unit_id:x.unit_id,unit_code:x.unit_code,conversion_ratio:Number(x.conversion_ratio||1),selling_price:Number(x.selling_price||0),purchase_price:Number(x.purchase_price||0),is_base:!!x.is_base}));if(p.unit_id&&!u.some(x=>String(x.unit_id)===String(p.unit_id)))u.unshift({unit_id:p.unit_id,unit_code:p.unit_code||'',conversion_ratio:1,selling_price:Number(p.selling_price||0),purchase_price:Number(p.purchase_price||0),is_base:true});return u}
function odProductOptions(selected='',q=''){q=String(q||'').toLowerCase();return '<option value="">-- Pilih Barang / Jasa --</option>'+odData.products.filter(x=>!q||[x.sku,x.name,x.barcode,x.brand_name].some(v=>String(v||'').toLowerCase().includes(q))).map(x=>`<option value="${x.id}" ${String(x.id)===String(selected)?'selected':''}>${accessEscape((x.sku||'')+' - '+x.name)}</option>`).join('')}
function odUnitOptions(pid,selected=''){let u=odProductUnits(pid);return u.length?u.map(x=>`<option value="${x.unit_id}" ${String(x.unit_id)===String(selected)?'selected':''}>${accessEscape(x.unit_code||'-')}${x.conversion_ratio!==1?' (x'+x.conversion_ratio+')':''}</option>`).join(''):'<option value="">Satuan tidak tersedia</option>'}
function odItemLine(kind,item={}){let sale=kind==='sales',pid=item.product_id||'';return `<div class="od-line-block"><div class="od-line od-line-unit"><select class="od-product" onchange="odProductChanged(this,'${kind}')">${odProductOptions(pid)}</select><select class="od-unit" onchange="odUnitChanged(this,'${kind}')">${odUnitOptions(pid,item.unit_id||'')}</select><input class="od-desc" value="${accessEscape(item.description||'')}" placeholder="Deskripsi"><input class="od-qty" type="number" value="${item.qty||1}" step="0.01"><input class="od-price" type="number" value="${item[sale?'unit_price':'unit_cost']||0}"><input class="od-disc" type="number" value="${item.discount_amount||0}" placeholder="Diskon"><button class="danger" onclick="this.closest('.od-line-block').remove()">Hapus</button></div></div>`}
function odFilterOrderProduct(i){let b=i.closest('.od-line-block'),s=b.querySelector('.od-product'),old=s.value;s.innerHTML=odProductOptions(old,i.value)}
function odProductChanged(s,kind){let l=s.closest('.od-line'),u=l.querySelector('.od-unit'),p=odData.products.find(x=>String(x.id)===String(s.value));u.innerHTML=odUnitOptions(s.value,'');let x=odProductUnits(s.value)[0];if(p)l.querySelector('.od-price').value=kind==='sales'?Number(x?.selling_price||p.selling_price||0):Number(x?.purchase_price||p.purchase_price||0)}
function odUnitChanged(s,kind){let l=s.closest('.od-line'),p=odData.products.find(x=>String(x.id)===String(l.querySelector('.od-product').value)),u=odProductUnits(p?.id).find(x=>String(x.unit_id)===String(s.value));if(p&&u)l.querySelector('.od-price').value=kind==='sales'?Number(u.selling_price||p.selling_price||0):Number(u.purchase_price||p.purchase_price||0)}
function odAddLine(kind,item={}){document.getElementById('odLines').insertAdjacentHTML('beforeend',odItemLine(kind,item))}
async function odTab(tab){window.odCurrent=tab;odTitle.textContent=({sales:'Pesanan Penjualan',purchase:'Pesanan Pembelian',customerDp:'Penerimaan DP Pelanggan',supplierDp:'Pembayaran DP Pemasok',allocation:window.odMode==='purchase'?'Alokasi DP Pemasok':'Alokasi DP Pelanggan'})[tab];if(tab==='sales'||tab==='purchase')return odOrderScreen(tab);if(tab==='customerDp'||tab==='supplierDp')return odDpScreen(tab);return odAllocationScreen()}
async function odOrderScreen(kind){let sale=kind==='sales',orders=(await api('/api/'+(sale?'sales-orders':'purchase-orders'))).items||[],partners=odData.partners.filter(x=>['BOTH',sale?'CUSTOMER':'SUPPLIER'].includes(x.partner_type));odEditOrderId=null;odContent.innerHTML=`<div class="field-grid three"><label class="field"><span>Nomor Pesanan</span><input id="odOrderNo" placeholder="Kosong = otomatis"></label><label class="field"><span>Tanggal Pesanan</span><input id="odDate" type="date" value="${new Date().toISOString().slice(0,10)}"></label><label class="field"><span>${sale?'Pelanggan':'Pemasok'}</span><select id="odPartner">${odOpts(partners)}</select></label>${sale?'':`<label class="field"><span>Gudang Penerimaan</span><select id="odWarehouse">${odOpts(odData.warehouses)}</select></label>`}<label class="field"><span>Estimasi ${sale?'Pengiriman':'Penerimaan'}</span><input id="odExpected" type="date"></label><label class="field"><span>PPN %</span><input id="odTax" type="number" value="0"></label><label class="field"><span>Diskon Header</span><input id="odDiscount" type="number" value="0"></label><label class="field wide-note"><span>Catatan</span><input id="odNotes"></label></div><div class="od-line-labels od-line-labels-unit"><span>Barang/Jasa</span><span>Satuan</span><span>Deskripsi</span><span>Qty</span><span>${sale?'Harga Jual':'Harga Beli'}</span><span>Diskon</span><span>Aksi</span></div><div id="odLines">${odItemLine(kind)}</div><button onclick="odAddLine('${kind}')">+ Item</button> <button id="odSaveBtn" onclick="odSaveOrder('${kind}')">Simpan Pesanan</button> <button id="odCancelEdit" class="secondary hidden" onclick="odOrderScreen('${kind}')">Batal Edit</button><hr><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>Partner</th><th>Total</th><th>DP</th><th>Status</th><th>Aksi</th></tr></thead><tbody>${orders.map(x=>`<tr><td>${x.order_date}</td><td>${x.order_no}</td><td>${accessEscape(x.partner_name)}</td><td>${rup(x.total_amount)}</td><td>${rup(x.dp_total)}</td><td>${x.status}</td><td>${['CANCELLED','COMPLETED'].includes(x.status)?`<span class="muted">${x.status}</span>`:`<button onclick="odEditOrder('${kind}',${x.id})">Edit</button> <button onclick="odMakeInvoice('${kind}',${x.id})">Buat Invoice</button> <button class="danger" onclick="odDeleteOrder('${kind}',${x.id})">Batal</button>`}</td></tr>`).join('')}</tbody></table>`}
async function odEditOrder(kind,id){try{let x=await api('/api/'+(kind==='sales'?'sales-orders':'purchase-orders')+'/'+id);odEditOrderId=id;odOrderNo.value=x.order_no||'';odDate.value=x.order_date||'';odPartner.value=kind==='sales'?x.customer_id:x.supplier_id;if(kind==='purchase')odWarehouse.value=x.warehouse_id||'';odExpected.value=x.expected_date||'';odTax.value=x.tax_percent||0;odDiscount.value=x.discount_amount||0;odNotes.value=x.notes||'';odLines.innerHTML='';(x.items||[]).forEach(i=>odAddLine(kind,i));odSaveBtn.textContent='Simpan Perubahan';odCancelEdit.classList.remove('hidden')}catch(e){msg(odMsg,e.message,false)}}
async function odSaveOrder(kind){try{let sale=kind==='sales',items=[...document.querySelectorAll('.od-line')].map(r=>({product_id:r.querySelector('.od-product').value,unit_id:r.querySelector('.od-unit').value,description:r.querySelector('.od-desc').value,qty:r.querySelector('.od-qty').value,[sale?'unit_price':'unit_cost']:r.querySelector('.od-price').value,discount_amount:r.querySelector('.od-disc').value}));let body={order_no:odOrderNo.value,order_date:odDate.value,[sale?'customer_id':'supplier_id']:odPartner.value,expected_date:odExpected.value,tax_percent:odTax.value,discount_amount:odDiscount.value,notes:odNotes.value,items};if(!sale)body.warehouse_id=odWarehouse.value;let ep='/api/'+(sale?'sales-orders':'purchase-orders')+(odEditOrderId?'/'+odEditOrderId:'');let rr=await api(ep,{method:odEditOrderId?'PUT':'POST',body:JSON.stringify(body)});msg(odMsg,'Pesanan '+rr.result.order_no+(odEditOrderId?' diperbarui.':' tersimpan.'));odEditOrderId=null;await odLoadMaster();odTab(kind)}catch(e){msg(odMsg,e.message,false)}}
async function odDeleteOrder(kind,id){if(!confirm('Batalkan pesanan ini?'))return;try{await api('/api/'+(kind==='sales'?'sales-orders':'purchase-orders')+'/'+id,{method:'DELETE'});await odLoadMaster();odTab(kind)}catch(e){alert(e.message)}}
async function odMakeInvoice(kind,id){let x=await api('/api/'+(kind==='sales'?'sales-orders':'purchase-orders')+'/'+id);if(kind==='sales'){await openSalesSection('entry');saleCustomer.value=x.customer_id||'';saleTax.value=x.tax_percent||0;saleDiscount.value=x.discount_amount||0;window.__sourceSalesOrderId=x.id;saleNotes.value='Dari pesanan '+x.order_no;saleLines.innerHTML='';x.items.forEach(i=>{addSaleLine();let r=saleLines.lastElementChild;r.querySelector('.slProduct').value=i.product_id;lineProduct(r.querySelector('.slProduct'));if(i.unit_id)r.querySelector('.slUnit').value=i.unit_id;r.querySelector('.slDescription').value=i.description||'';r.querySelector('.slQty').value=i.qty;r.querySelector('.slPrice').value=i.unit_price});estimateSale()}else{await openPurchaseSection('entry');purchaseSupplier.value=x.supplier_id||'';purchaseWarehouse.value=x.warehouse_id||'';purchaseTax.value=x.tax_percent||0;purchaseDiscount.value=x.discount_amount||0;window.__sourcePurchaseOrderId=x.id;purchaseNotes.value='Dari pesanan '+x.order_no;purchaseLines=(x.items||[]).map(i=>({product_id:i.product_id,name:(odData.products.find(p=>String(p.id)===String(i.product_id))||{}).name||'',qty:i.qty,unit_id:i.unit_id,unit_code:i.unit_code,conversion_ratio:i.conversion_ratio,unit_cost:i.unit_cost,discount_mode:'AMOUNT',discount_value:i.discount_amount}));renderPurchaseLines()}}
async function odDpScreen(tab){let customer=tab==='customerDp',kind=customer?'customer':'supplier',partners=odData.partners.filter(x=>['BOTH',customer?'CUSTOMER':'SUPPLIER'].includes(x.partner_type)),orders=customer?odData.salesOrders:odData.purchaseOrders,dps=(await api('/api/'+kind+'-downpayments')).items||[];window.odDpRows=dps;odContent.innerHTML=`<div class="field-grid three"><label class="field"><span>Tanggal</span><input id="dpDate" type="date" value="${new Date().toISOString().slice(0,10)}"></label><label class="field"><span>Partner</span><select id="dpPartner">${odOpts(partners)}</select></label><label class="field"><span>Pesanan (opsional)</span><select id="dpOrder"><option value="">Tanpa pesanan</option>${orders.map(x=>`<option value="${x.id}">${x.order_no} - ${accessEscape(x.partner_name)}</option>`).join('')}</select></label><label class="field"><span>Kas/Bank</span><select id="dpCash">${odOpts(odData.cash)}</select></label><label class="field"><span>Jumlah DP</span><input id="dpAmount" type="number"></label><label class="field"><span>Catatan</span><input id="dpNotes"></label></div><button onclick="odSaveDp('${kind}')">Simpan DP</button><hr><h3>Daftar DP ${customer?'Pelanggan':'Pemasok'}</h3><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>Partner</th><th>Pesanan</th><th>Jumlah</th><th>Terpakai</th><th>Tersedia</th><th>Aksi</th></tr></thead><tbody>${dps.map(x=>`<tr><td>${x.dp_date}</td><td>${x.dp_no}</td><td>${accessEscape(x.partner_name)}</td><td>${x.order_no||'-'}</td><td>${rup(x.amount)}</td><td>${rup(x.allocated_amount)}</td><td>${rup(x.available_amount)}</td><td><button onclick="odEditDp('${kind}',${x.id})">Edit</button> <button class="danger" onclick="odDeleteDp('${kind}',${x.id})">Hapus</button></td></tr>`).join('')}</tbody></table>`}
async function odEditDp(kind,id){let x=(window.odDpRows||[]).find(v=>v.id===id);if(!x)return;let amount=prompt('Jumlah DP',x.amount);if(amount===null)return;let dt=prompt('Tanggal DP (YYYY-MM-DD)',x.dp_date);if(dt===null)return;try{await api('/api/'+kind+'-downpayments/'+id,{method:'PUT',body:JSON.stringify({dp_date:dt,amount:amount})});odTab(kind==='customer'?'customerDp':'supplierDp')}catch(e){alert(e.message)}}
async function odDeleteDp(kind,id){if(!confirm('Hapus DP ini? Jurnal dan kas/bank akan dibalik.'))return;try{await api('/api/'+kind+'-downpayments/'+id,{method:'DELETE'});odTab(kind==='customer'?'customerDp':'supplierDp')}catch(e){alert(e.message)}}
async function odSaveDp(kind){try{let customer=kind==='customer',r=await api('/api/'+kind+'-downpayments',{method:'POST',body:JSON.stringify({dp_date:dpDate.value,[customer?'customer_id':'supplier_id']:dpPartner.value,order_id:dpOrder.value||null,cash_account_id:dpCash.value,amount:dpAmount.value,notes:dpNotes.value})});msg(odMsg,'DP '+r.result.dp_no+' tersimpan.');await odLoadMaster();odTab(customer?'customerDp':'supplierDp')}catch(e){msg(odMsg,e.message,false)}}
async function odAllocationScreen(){
  if(window.odMode==='purchase'){
    let sd=(await api('/api/supplier-downpayments')).items.filter(x=>x.available_amount>0),purchases=((await api('/api/payables')).items||[]).filter(x=>numericValue(x.balance_due)>0);
    let allocs=(await api('/api/supplier-downpayment-allocations')).items||[];window.odAllocationRows=allocs;odContent.innerHTML=`<div class="field-grid three"><label class="field"><span>Tanggal</span><input id="alDate" type="date" value="${new Date().toISOString().slice(0,10)}"></label></div><div class="card"><h3>Alokasi DP Pemasok</h3><label class="field"><span>DP Pemasok</span><select id="alSDp">${sd.map(x=>`<option value="${x.id}">${x.dp_no} - ${accessEscape(x.partner_name)} (${rup(x.available_amount)})</option>`).join('')}</select></label><label class="field"><span>Invoice Pembelian</span><select id="alSInv">${purchases.map(x=>`<option value="${x.id}">${x.purchase_no} - ${accessEscape(x.supplier_name)} (${rup(x.balance_due)})</option>`).join('')}</select></label><label class="field"><span>Jumlah Alokasi</span><input id="alSAmt" type="number" placeholder="Jumlah"></label><button onclick="odAllocate('supplier')">Alokasikan DP Pemasok</button></div><h3>Daftar Alokasi DP Pemasok</h3><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>DP</th><th>Invoice</th><th>Jumlah</th><th>Aksi</th></tr></thead><tbody>${allocs.map(x=>`<tr><td>${x.allocation_date}</td><td>${x.allocation_no}</td><td>${x.dp_no}</td><td>${x.invoice_no}</td><td>${rup(x.amount)}</td><td><button onclick="odEditAllocation('supplier',${x.id})">Edit</button> <button class="danger" onclick="odDeleteAllocation('supplier',${x.id})">Hapus</button></td></tr>`).join('')}</tbody></table>`;
  }else{
    let cd=(await api('/api/customer-downpayments')).items.filter(x=>x.available_amount>0),sales=((await api('/api/receivables')).items||[]).filter(x=>numericValue(x.balance_due)>0);
    let allocs=(await api('/api/customer-downpayment-allocations')).items||[];window.odAllocationRows=allocs;odContent.innerHTML=`<div class="field-grid three"><label class="field"><span>Tanggal</span><input id="alDate" type="date" value="${new Date().toISOString().slice(0,10)}"></label></div><div class="card"><h3>Alokasi DP Pelanggan</h3><label class="field"><span>DP Pelanggan</span><select id="alCDp">${cd.map(x=>`<option value="${x.id}">${x.dp_no} - ${accessEscape(x.partner_name)} (${rup(x.available_amount)})</option>`).join('')}</select></label><label class="field"><span>Invoice Penjualan</span><select id="alCInv">${sales.map(x=>`<option value="${x.id}">${x.invoice_no} - ${accessEscape(x.customer_name)} (${rup(x.balance_due)})</option>`).join('')}</select></label><label class="field"><span>Jumlah Alokasi</span><input id="alCAmt" type="number" placeholder="Jumlah"></label><button onclick="odAllocate('customer')">Alokasikan DP Pelanggan</button></div><h3>Daftar Alokasi DP Pelanggan</h3><table><thead><tr><th>Tanggal</th><th>Nomor</th><th>DP</th><th>Invoice</th><th>Jumlah</th><th>Aksi</th></tr></thead><tbody>${allocs.map(x=>`<tr><td>${x.allocation_date}</td><td>${x.allocation_no}</td><td>${x.dp_no}</td><td>${x.invoice_no}</td><td>${rup(x.amount)}</td><td><button onclick="odEditAllocation('customer',${x.id})">Edit</button> <button class="danger" onclick="odDeleteAllocation('customer',${x.id})">Hapus</button></td></tr>`).join('')}</tbody></table>`;
  }
}
async function odEditAllocation(kind,id){let x=(window.odAllocationRows||[]).find(v=>v.id===id);if(!x)return;let amount=prompt('Jumlah alokasi',x.amount);if(amount===null)return;let dt=prompt('Tanggal alokasi (YYYY-MM-DD)',x.allocation_date);if(dt===null)return;try{await api('/api/'+kind+'-downpayment-allocations/'+id,{method:'PUT',body:JSON.stringify({allocation_date:dt,amount:amount})});odAllocationScreen()}catch(e){alert(e.message)}}
async function odDeleteAllocation(kind,id){if(!confirm('Hapus alokasi DP ini? Saldo DP dan tagihan akan dikembalikan.'))return;try{await api('/api/'+kind+'-downpayment-allocations/'+id,{method:'DELETE'});odAllocationScreen()}catch(e){alert(e.message)}}
async function odAllocate(kind){try{let customer=kind==='customer',r=await api('/api/'+kind+'-downpayment-allocations',{method:'POST',body:JSON.stringify({allocation_date:alDate.value,downpayment_id:(customer?alCDp:alSDp).value,invoice_id:(customer?alCInv:alSInv).value,amount:(customer?alCAmt:alSAmt).value})});msg(odMsg,'Alokasi '+r.result.allocation_no+' berhasil.');odAllocationScreen()}catch(e){msg(odMsg,e.message,false)}}



let masterImportErrorFile=null, masterImportErrorName='Error_Import.xlsx';

async function deleteMaster(url,reload){if(!confirm('Nonaktifkan data ini?'))return;try{await api(url,{method:'DELETE'});await reload()}catch(e){alert(e.message)}}
function openMasterImportType(type){openMasterImport().then(()=>{const el=document.getElementById('masterImportType');if(el&&[...el.options].some(o=>o.value===type))el.value=type;masterImportReset()})}

async function deleteProduct(id){if(!confirm('Nonaktifkan barang ini? Riwayat transaksi dan stok lama tetap tersimpan.'))return;try{await api('/api/products/'+id,{method:'DELETE'});if(String(productEditId.value)===String(id))productEditId.value='';msg(pMsg,'Barang berhasil dinonaktifkan.');await Promise.all([loadProducts(),loadSummary()])}catch(e){msg(pMsg,e.message,false)}}
function editProduct(id){let x=products.find(v=>v.id===id);if(!x)return;const set=(id,v)=>{const e=document.getElementById(id);if(e)e.value=v??''};set('productEditId',id);set('pSku',x.sku);set('pBarcode',x.barcode);set('pName',x.name);set('pCategory',x.category_id);set('pBrand',x.brand_id);set('pUnit',x.unit_id);set('pType',x.product_type||'STOCK');set('pBuy',x.purchase_price||0);set('pSell',x.selling_price||0);set('pMinimum',x.minimum_stock||0);set('pInitial',x.opening_stock_qty||0);set('pOpeningDate',x.opening_balance_date||'');set('pWarehouse',x.opening_warehouse_id||'');set('pInventoryAccount',x.inventory_account_id);set('pSalesAccount',x.sales_account_id);set('pCogsAccount',x.cogs_account_id);window.__productLevelPrices=x.price_levels||{};renderPriceLevelSelectors();renderProductUnitRows((x.units||[]).filter(u=>!u.is_base));document.getElementById('products')?.scrollIntoView({behavior:'smooth',block:'start'})}
function editPartner(id){let x=partners.find(v=>v.id===id);if(!x)return;partnerEditId.value=id;bType.value=x.partner_type;bCode.value=x.code||'';bName.value=x.name||'';bPhone.value=x.phone||'';bEmail.value=x.email||'';bTax.value=x.tax_id||'';bCity.value=x.city||'';bTerm.value=x.payment_term_days||0;bLimit.value=x.credit_limit||0;bOpening.value=0;bAddress.value=x.address||'';window.scrollTo({top:0,behavior:'smooth'})}

function masterImportElement(id){return document.getElementById(id)}
async function openMasterImport(){
  page('masterImport');
  const typeEl=masterImportElement('masterImportType'),messageEl=masterImportElement('masterImportMsg');
  try{
    if(!typeEl)throw new Error('Form impor belum siap. Tutup halaman lalu buka kembali.');
    const d=await api('/api/master-import/types');
    typeEl.innerHTML=(d.items||[]).filter(x=>x.key!=='cash_accounts').map(x=>`<option value="${x.key}">${x.title}</option>`).join('');
    masterImportReset();
  }catch(e){if(messageEl)msg(messageEl,e.message,false)}
}
function masterImportReset(){
  masterImportErrorFile=null;
  const total=masterImportElement('miTotal'),success=masterImportElement('miSuccess'),failed=masterImportElement('miFailed');
  const errorWrap=masterImportElement('miErrorWrap'),messageEl=masterImportElement('masterImportMsg');
  if(total)total.textContent='0';
  if(success)success.textContent='0';
  if(failed)failed.textContent='0';
  if(errorWrap)errorWrap.classList.add('hidden');
  if(messageEl)msg(messageEl,'');
}
function downloadMasterTemplate(){
  const typeEl=masterImportElement('masterImportType');
  if(!typeEl||!typeEl.value){const messageEl=masterImportElement('masterImportMsg');if(messageEl)msg(messageEl,'Pilih jenis data terlebih dahulu.',false);return}
  window.open('/api/master-import/template?type='+encodeURIComponent(typeEl.value)+'&token='+encodeURIComponent(token),'_blank');
}
async function runMasterImport(){
  const typeEl=masterImportElement('masterImportType'),fileEl=masterImportElement('masterImportFile'),messageEl=masterImportElement('masterImportMsg');
  try{
    if(!typeEl||!fileEl||!messageEl)throw new Error('Form impor belum siap. Tutup halaman lalu buka kembali.');
    const importType=typeEl.value;
    const f=fileEl.files&&fileEl.files[0];
    if(!f)throw new Error('Pilih file Excel terlebih dahulu.');
    msg(messageEl,'Memproses file...');
    if(!/\.xlsx$/i.test(f.name))throw new Error('Gunakan file .xlsx dari template aplikasi.');
    if(f.size>25*1024*1024)throw new Error('Ukuran file maksimal 25 MB.');
    const dataUrl=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=()=>reject(new Error('File tidak dapat dibaca.'));r.readAsDataURL(f)});
    const d=await api('/api/master-import',{method:'POST',body:JSON.stringify({type:importType,file_name:f.name,excel_base64:dataUrl})});
    const result=d.result||{};
    const total=masterImportElement('miTotal'),success=masterImportElement('miSuccess'),failed=masterImportElement('miFailed'),errorWrap=masterImportElement('miErrorWrap');
    if(total)total.textContent=result.total_rows??0;
    if(success)success.textContent=result.success_count??0;
    if(failed)failed.textContent=result.failed_count??0;
    masterImportErrorFile=result.error_file_base64||null;
    masterImportErrorName=result.error_filename||'Error_Import.xlsx';
    if(errorWrap)errorWrap.classList.toggle('hidden',!masterImportErrorFile);
    msg(messageEl,`${result.success_count||0} baris berhasil, ${result.failed_count||0} baris gagal.`,Number(result.failed_count||0)===0);
    fileEl.value='';
    // Refresh hanya modul yang relevan. Kegagalan refresh tidak membatalkan hasil impor.
    try{
      if(importType==='products')await Promise.all([loadProducts(),loadSummary()]);
      else if(importType==='customers')await Promise.all([loadCustomersPage(),loadTransactionPartners()]);
      else if(importType==='suppliers')await Promise.all([loadSuppliersPage(),loadTransactionPartners()]);
      else if(importType==='categories')await Promise.all([loadMasters(),loadServicesPage()]);
      else await refreshAll();
    }catch(refreshError){console.warn('Master import refresh warning:',refreshError)}
  }catch(e){if(messageEl)msg(messageEl,e.message,false)}
}
function downloadMasterImportErrors(){if(!masterImportErrorFile)return;const raw=atob(masterImportErrorFile),a=new Uint8Array(raw.length);for(let i=0;i<raw.length;i++)a[i]=raw.charCodeAt(i);const url=URL.createObjectURL(new Blob([a],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}));const link=document.createElement('a');link.href=url;link.download=masterImportErrorName;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}



let projectDocumentRecords=[];
let projectDocSearchTimer=null;
function projectDocSearchDebounced(){clearTimeout(projectDocSearchTimer);projectDocSearchTimer=setTimeout(loadProjectDocuments,300)}
function projectDocBytes(n){n=Number(n||0);if(n<1024)return n+' B';if(n<1048576)return (n/1024).toFixed(1)+' KB';return (n/1048576).toFixed(1)+' MB'}
async function loadProjectDocuments(){
 try{
  let url='/api/project-documents?project_id='+encodeURIComponent(projectDocFilterProject?.value||'')+'&category='+encodeURIComponent(projectDocFilterCategory?.value||'')+'&q='+encodeURIComponent(projectDocSearch?.value||'')+'&history='+(projectDocHistory?.checked?'1':'0');
  let [p,d]=await Promise.all([api('/api/projects'),api(url)]);
  let projects=p.items||[];projectDocumentRecords=d.items||[];
  const pop=(el,includeAll=false)=>{let old=el.value;el.innerHTML=(includeAll?'<option value="">Semua Proyek</option>':'<option value="">Pilih Proyek</option>')+projects.map(x=>`<option value="${x.id}">${accessEscape(x.code)} - ${accessEscape(x.name)}</option>`).join('');if([...el.options].some(o=>o.value===old))el.value=old};
  pop(projectDocProject,false);pop(projectDocFilterProject,true);
  let cats=d.categories||[];
  let selected=projectDocCategory.value;projectDocCategory.innerHTML=cats.map(x=>`<option value="${accessEscape(x)}">${accessEscape(x)}</option>`).join('');if(cats.includes(selected))projectDocCategory.value=selected;
  let oldCat=projectDocFilterCategory.value;projectDocFilterCategory.innerHTML='<option value="">Semua Kategori</option>'+cats.map(x=>`<option value="${accessEscape(x)}">${accessEscape(x)}</option>`).join('');projectDocFilterCategory.value=oldCat;
  projectDocBody.innerHTML=projectDocumentRecords.length?projectDocumentRecords.map(x=>`<tr>
   <td><b>${accessEscape(x.project_code)}</b><br><small>${accessEscape(x.project_name)}</small></td>
   <td>${accessEscape(x.category)}</td>
   <td><b>${accessEscape(x.title)}</b><br><small>${accessEscape(x.document_no||'-')}</small><br><small>${accessEscape(x.description||'')}</small></td>
   <td>${accessEscape(x.document_date||'-')}${x.valid_until?`<br><small>Expired: ${accessEscape(x.valid_until)}</small>`:''}</td>
   <td>${accessEscape(x.original_filename)}<br><small>${projectDocBytes(x.file_size)}</small></td>
   <td>v${Number(x.version_no||1)} ${x.is_current?'<span class="status-badge">Aktif</span>':'<span class="muted">History</span>'}</td>
   <td>${accessEscape(x.uploaded_by_username||'-')}<br><small>${accessEscape(x.created_at||'')}</small></td>
   <td><button class="secondary" onclick="openProjectDocument(${x.id})">Lihat</button> <button onclick="editProjectDocument(${x.id})">Edit</button> <button class="danger" onclick="deleteProjectDocument(${x.id})">Hapus</button></td>
  </tr>`).join(''):'<tr><td colspan="8">Belum ada dokumen proyek.</td></tr>';
  msg(projectDocMsg,projectDocumentRecords.length+' dokumen dimuat.',true)
 }catch(e){msg(projectDocMsg,e.message,false)}
}
function resetProjectDocumentForm(){projectDocId.value='';projectDocTitle.value='';projectDocNo.value='';projectDocDate.value='';projectDocValid.value='';projectDocDescription.value='';projectDocFile.value='';if(projectDocCategory.options.length)projectDocCategory.selectedIndex=0}
function editProjectDocument(id){let x=projectDocumentRecords.find(z=>Number(z.id)===Number(id));if(!x)return;projectDocId.value=x.id;projectDocProject.value=x.project_id;projectDocCategory.value=x.category;projectDocTitle.value=x.title||'';projectDocNo.value=x.document_no||'';projectDocDate.value=x.document_date||'';projectDocValid.value=x.valid_until||'';projectDocDescription.value=x.description||'';projectDocFile.value='';window.scrollTo({top:0,behavior:'smooth'});msg(projectDocMsg,'Edit metadata. Pilih file baru hanya jika ingin membuat versi baru.',true)}
async function saveProjectDocument(){
 try{
  if(!projectDocProject.value)throw Error('Pilih proyek.');
  if(!projectDocTitle.value.trim())throw Error('Judul dokumen wajib diisi.');
  let f=projectDocFile.files&&projectDocFile.files[0],fileData='';
  if(f){
   if(f.size>20*1024*1024)throw Error('Ukuran file maksimal 20 MB.');
   fileData=await new Promise((resolve,reject)=>{let r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=()=>reject(Error('File tidak dapat dibaca.'));r.readAsDataURL(f)})
  }
  let body={project_id:projectDocProject.value,category:projectDocCategory.value,title:projectDocTitle.value,document_no:projectDocNo.value,document_date:projectDocDate.value||null,valid_until:projectDocValid.value||null,description:projectDocDescription.value,file_name:f?f.name:'',file_base64:fileData};
  let id=projectDocId.value;
  await api(id?'/api/project-documents/'+id:'/api/project-documents',{method:id?'PUT':'POST',body:JSON.stringify(body)});
  msg(projectDocMsg,id?(f?'Versi dokumen baru berhasil disimpan.':'Metadata dokumen diperbarui.'):'Dokumen proyek berhasil disimpan.',true);
  resetProjectDocumentForm();await loadProjectDocuments()
 }catch(e){msg(projectDocMsg,e.message,false)}
}
function openProjectDocument(id){window.open('/api/project-documents/file?id='+encodeURIComponent(id)+'&token='+encodeURIComponent(token),'_blank')}
async function deleteProjectDocument(id){if(!confirm('Hapus dokumen/versi ini? File fisik versi tersebut juga akan dihapus.'))return;try{await api('/api/project-documents/'+id,{method:'DELETE'});await loadProjectDocuments()}catch(e){msg(projectDocMsg,e.message,false)}}


let flexInvoiceTemplates=[],flexInvoiceBlocks=[],activeFlexTemplateId=null,flexWorkingBlocks=[];
async function loadFlexInvoiceTemplates(){try{const d=await api('/api/flexible-invoice-templates');flexInvoiceTemplates=d.items||[];flexInvoiceBlocks=d.blocks||[];flexTplSelect.innerHTML=flexInvoiceTemplates.map(x=>`<option value="${x.id}">${accessEscape(x.name)}${x.is_default?' [Default]':''}</option>`).join('');if(!activeFlexTemplateId&&flexInvoiceTemplates.length)activeFlexTemplateId=flexInvoiceTemplates[0].id;if(activeFlexTemplateId)flexTplSelect.value=activeFlexTemplateId;selectFlexTemplate()}catch(e){msg(flexTplMsg,e.message,false)}}
function defaultFlexBlocks(kind){let keys=kind==='TERM'?['company_header','customer_info','project_info','contract_info','term_summary','retention','tax_totals','custom_text','transaction_notes','signatures','footer']:kind==='TERM_MATERIAL'?['company_header','customer_info','project_info','contract_info','project_materials','term_summary','retention','tax_totals','custom_text','transaction_notes','signatures','footer']:['company_header','customer_info','project_info','invoice_items','tax_totals','transaction_notes','signatures','footer'];let labels=Object.fromEntries(flexInvoiceBlocks.map(x=>[x.key,x.label]));return keys.map(k=>({key:k,label:labels[k]||k,enabled:true}))}
function selectFlexTemplate(){activeFlexTemplateId=Number(flexTplSelect.value||0)||null;let x=flexInvoiceTemplates.find(z=>Number(z.id)===Number(activeFlexTemplateId));if(!x){newFlexInvoiceTemplate();return}let o=x.options||{};flexTplCode.value=x.code||'';flexTplName.value=x.name||'';flexTplKind.value=x.template_kind||'STANDARD';flexTplTitle.value=o.title||'INVOICE';flexTplPaper.value=o.paper_size||'A4';flexTplDefault.checked=!!x.is_default;flexTplActive.checked=x.is_active!==false;flexTplLogo.checked=o.show_logo!==false;flexTplSku.checked=o.show_sku!==false;flexTplUnit.checked=o.show_unit!==false;flexTplPrices.checked=o.show_prices!==false;flexTplMaterialValues.checked=o.show_material_values!==false;flexTplCustom.value=o.custom_text||'';flexTplLeft.value=o.left_signer||'Dibuat oleh';flexTplRight.value=o.right_signer||'Disetujui / Diterima oleh';flexWorkingBlocks=(x.blocks||defaultFlexBlocks(x.template_kind)).map(b=>({...b}));renderFlexBlocks();previewFlexTemplate()}
function newFlexInvoiceTemplate(){activeFlexTemplateId=null;flexTplSelect.value='';flexTplCode.value='';flexTplName.value='';flexTplKind.value='STANDARD';flexTplTitle.value='INVOICE';flexTplPaper.value='A4';flexTplDefault.checked=false;flexTplActive.checked=true;flexTplLogo.checked=true;flexTplSku.checked=true;flexTplUnit.checked=true;flexTplPrices.checked=true;flexTplMaterialValues.checked=true;flexTplCustom.value='Pembayaran mohon dilakukan sesuai jatuh tempo yang tercantum pada invoice.';flexTplLeft.value='Dibuat oleh';flexTplRight.value='Disetujui / Diterima oleh';flexWorkingBlocks=defaultFlexBlocks('STANDARD');renderFlexBlocks();previewFlexTemplate()}
function flexKindChanged(){if(confirm('Atur ulang susunan blok sesuai jenis template?')){flexWorkingBlocks=defaultFlexBlocks(flexTplKind.value);flexTplTitle.value=flexTplKind.value==='STANDARD'?'INVOICE':'INVOICE TERMIN';renderFlexBlocks();previewFlexTemplate()}}
function renderFlexBlocks(){let present=new Set(flexWorkingBlocks.map(x=>x.key));for(const b of flexInvoiceBlocks)if(!present.has(b.key))flexWorkingBlocks.push({key:b.key,label:b.label,enabled:false});flexTplBlocks.innerHTML=flexWorkingBlocks.map((b,i)=>`<div class="flex-block-row"><input type="checkbox" ${b.enabled?'checked':''} onchange="flexWorkingBlocks[${i}].enabled=this.checked;previewFlexTemplate()"><span>${accessEscape(b.label)}</span><button class="secondary" onclick="moveFlexBlock(${i},-1)">↑</button><button class="secondary" onclick="moveFlexBlock(${i},1)">↓</button></div>`).join('')}
function moveFlexBlock(i,d){let j=i+d;if(j<0||j>=flexWorkingBlocks.length)return;[flexWorkingBlocks[i],flexWorkingBlocks[j]]=[flexWorkingBlocks[j],flexWorkingBlocks[i]];renderFlexBlocks();previewFlexTemplate()}
function flexPayload(){return {code:flexTplCode.value.trim(),name:flexTplName.value.trim(),template_kind:flexTplKind.value,blocks:flexWorkingBlocks,is_default:flexTplDefault.checked,is_active:flexTplActive.checked,options:{title:flexTplTitle.value.trim(),paper_size:flexTplPaper.value,orientation:'portrait',show_logo:flexTplLogo.checked,show_sku:flexTplSku.checked,show_unit:flexTplUnit.checked,show_prices:flexTplPrices.checked,show_material_values:flexTplMaterialValues.checked,custom_text:flexTplCustom.value,left_signer:flexTplLeft.value,right_signer:flexTplRight.value}}}
async function saveFlexInvoiceTemplate(){try{let p=flexPayload();if(!p.code||!p.name)throw Error('Kode dan nama template wajib diisi.');const d=await api(activeFlexTemplateId?'/api/flexible-invoice-templates/'+activeFlexTemplateId:'/api/flexible-invoice-templates',{method:activeFlexTemplateId?'PUT':'POST',body:JSON.stringify(p)});activeFlexTemplateId=d.item.id;msg(flexTplMsg,'Template invoice berhasil disimpan.',true);await loadFlexInvoiceTemplates()}catch(e){msg(flexTplMsg,e.message,false)}}
async function deleteFlexInvoiceTemplate(){if(!activeFlexTemplateId||!confirm('Hapus template invoice ini?'))return;try{await api('/api/flexible-invoice-templates/'+activeFlexTemplateId,{method:'DELETE'});activeFlexTemplateId=null;await loadFlexInvoiceTemplates();msg(flexTplMsg,'Template dihapus.',true)}catch(e){msg(flexTplMsg,e.message,false)}}
function previewFlexTemplate(){if(!document.getElementById('flexTplPreview'))return;let p=flexPayload(),enabled=p.blocks.filter(x=>x.enabled);const sample={company_header:'<b>LOGO & NAMA PERUSAHAAN</b><span style="float:right"><b>'+accessEscape(p.options.title||'INVOICE')+'</b><br>INV-000123</span>',customer_info:'Pelanggan: PT Contoh · Tanggal: 10/08/2026 · Jatuh Tempo: 24/08/2026',project_info:'<b>PROYEK</b><br>PRJ-001 · Renovasi Gedung PT Contoh',contract_info:'No. SPK: SPK-001/2026 · Nilai Kontrak: Rp1.000.000.000',term_summary:'<b>TERMIN II</b> · Progress 30% · Nilai Rp300.000.000',invoice_items:'<table><tr><th>Item</th><th>Qty</th><th>Jumlah</th></tr><tr><td>Jasa / pekerjaan</td><td>1</td><td>300.000.000</td></tr></table>',project_materials:'<table><tr><th>Material</th><th>Qty</th><th>Nilai</th></tr><tr><td>Semen</td><td>100</td><td>7.500.000</td></tr></table>',project_progress:'Progress pekerjaan ██████░░░░ 60%',retention:'Retensi 5%: Rp15.000.000',tax_totals:'<b style="float:right">TOTAL TAGIHAN Rp316.350.000</b><br>',custom_text:accessEscape(p.options.custom_text||''),transaction_notes:'Catatan transaksi / pembayaran.',signatures:'Dibuat oleh　　　　　　　　　Disetujui / Diterima oleh',footer:'Footer perusahaan'};flexTplPreview.innerHTML='<div class="flex-preview-paper">'+enabled.map(x=>`<div class="pv-block">${sample[x.key]||accessEscape(x.label)}</div>`).join('')+'</div>'}
async function openOwnerCloud(){page('ownerCloudPage');await loadOwnerCloud()}
async function loadOwnerCloud(){try{let d=await api('/api/owner-cloud/status');ocUrl.value=d.cloud_url||'';ocEnabled.checked=!!d.enabled;ocInterval.value=d.sync_interval_minutes||5;ocCompany.textContent=d.company_id||'-';ocInstall.textContent=d.installation_id||'-';ocPair.textContent=d.pairing_code||'-';ocPairExp.textContent=d.pairing_expires_at||'-';ocLastSync.textContent=d.last_sync_at||'-';ocStatus.textContent=d.last_sync_status||'Belum sinkron';if(d.last_error)msg(ocMsg,d.last_error,false);else msg(ocMsg,d.registered?'Instalasi sudah terdaftar.':'Isi Cloud URL lalu daftarkan instalasi.',true);let l=await api('/api/owner-cloud/logs');ocLogs.innerHTML=(l.items||[]).map(x=>`<tr><td>${accessEscape(x.created_at||'')}</td><td>${accessEscape(x.status||'')}</td><td>${accessEscape(x.message||'')}</td></tr>`).join('')||'<tr><td colspan="3">Belum ada log.</td></tr>'}catch(e){msg(ocMsg,e.message,false)}}
async function saveOwnerCloud(){try{await api('/api/owner-cloud/settings',{method:'PUT',body:JSON.stringify({cloud_url:ocUrl.value,enabled:ocEnabled.checked,sync_interval_minutes:ocInterval.value})});msg(ocMsg,'Pengaturan cloud disimpan.');await loadOwnerCloud()}catch(e){msg(ocMsg,e.message,false)}}
async function registerOwnerCloud(){try{await saveOwnerCloud();await api('/api/owner-cloud/register',{method:'POST',body:JSON.stringify({})});msg(ocMsg,'Instalasi berhasil didaftarkan.');await loadOwnerCloud()}catch(e){msg(ocMsg,e.message,false)}}
async function pairOwnerCloud(){try{await api('/api/owner-cloud/pairing-code',{method:'POST',body:JSON.stringify({})});msg(ocMsg,'Kode pairing baru dibuat.');await loadOwnerCloud()}catch(e){msg(ocMsg,e.message,false)}}
async function syncOwnerCloud(){try{msg(ocMsg,'Mengirim snapshot dashboard...');await api('/api/owner-cloud/sync',{method:'POST',body:JSON.stringify({})});msg(ocMsg,'Sinkronisasi berhasil.');await loadOwnerCloud()}catch(e){msg(ocMsg,e.message,false)}}

let contractorData=null;
async function loadContractorProject(){const id=contractorProject.value;if(!id){contractorSummary.innerHTML='';return}try{contractorData=await api('/api/project-contractor-dashboard?project_id='+id);const z=contractorData.summary||{};contractorValue.value=rup(z.contract_value||0);contractorProgress.value=Number(z.latest_progress||0).toFixed(1)+'%';contractorProfit.value=rup(z.estimated_profit||0);contractorSummary.innerHTML=[['Budget',z.budget],['Realisasi',z.realization],['Termin',z.term_total],['Termin Lunas',z.term_paid],['Retensi Belum Cair',z.retention_pending]].map(x=>`<div class="project-budget-stat"><span>${x[0]}</span><b>${rup(x[1]||0)}</b></div>`).join('');renderProjectProgress();renderProjectTerms()}catch(e){msg(projectMsg,e.message,false)}}
function renderProjectProgress(){const rows=contractorData?.progress||[];progressBody.innerHTML=rows.length?rows.map(x=>`<tr><td>${accessEscape(x.progress_date)}</td><td>${Number(x.progress_percent||0).toFixed(1)}%</td><td>${accessEscape(x.notes||'-')}</td><td><button onclick='editProjectProgress(${JSON.stringify(x)})'>Edit</button> <button class="danger" onclick="deleteProjectProgress(${x.id})">Hapus</button></td></tr>`).join(''):'<tr><td colspan="4">Belum ada progress.</td></tr>'}
function resetProjectProgress(){progressId.value='';progressDate.value=new Date().toISOString().slice(0,10);progressPercent.value='';progressNotes.value=''}
function editProjectProgress(x){progressId.value=x.id;progressDate.value=x.progress_date;progressPercent.value=x.progress_percent;progressNotes.value=x.notes||''}
async function saveProjectProgress(){try{if(!contractorProject.value)throw Error('Pilih proyek.');let body={project_id:contractorProject.value,progress_date:progressDate.value,progress_percent:progressPercent.value,notes:progressNotes.value};await api(progressId.value?'/api/project-progress/'+progressId.value:'/api/project-progress',{method:progressId.value?'PUT':'POST',body:JSON.stringify(body)});resetProjectProgress();await loadProjects();contractorProject.value=body.project_id;await loadContractorProject()}catch(e){msg(projectMsg,e.message,false)}}
async function deleteProjectProgress(id){if(!confirm('Hapus progress ini?'))return;await api('/api/project-progress/'+id,{method:'DELETE'});await loadContractorProject()}
function renderProjectTerms(){const rows=contractorData?.terms||[];termBody.innerHTML=rows.length?rows.map(x=>`<tr><td>${accessEscape(x.term_no)}<br><small>${accessEscape(x.description||'')}</small></td><td>${rup(x.amount||0)}</td><td>${accessEscape(x.due_date||'-')}</td><td>${accessEscape(x.invoice_no||'-')}</td><td>${accessEscape(x.status)}</td><td>${rup(x.retention_amount||0)} · ${accessEscape(x.retention_status)}</td><td><button onclick='editProjectTerm(${JSON.stringify(x)})'>Edit</button> <button class="danger" onclick="deleteProjectTerm(${x.id})">Hapus</button></td></tr>`).join(''):'<tr><td colspan="7">Belum ada termin.</td></tr>'}
function resetProjectTerm(){termId.value='';termNo.value='';termDescription.value='';termPercent.value='';termAmount.value='';termInvoiceDate.value='';termDueDate.value='';termSale.value='';termStatus.value='DRAFT';termRetentionPercent.value=(projectRecords.find(x=>String(x.id)===String(contractorProject.value))||{}).retention_percent||0;termRetentionDue.value='';termRetentionStatus.value='PENDING';termNotes.value=''}
function editProjectTerm(x){termId.value=x.id;termNo.value=x.term_no;termDescription.value=x.description||'';termPercent.value=x.percentage||0;termAmount.value=x.amount||0;termInvoiceDate.value=x.invoice_date||'';termDueDate.value=x.due_date||'';termSale.value=x.sale_id||'';termStatus.value=x.status||'DRAFT';termRetentionPercent.value=x.retention_percent||0;termRetentionDue.value=x.retention_due_date||'';termRetentionStatus.value=x.retention_status||'PENDING';termNotes.value=x.notes||''}
async function saveProjectTerm(){try{if(!contractorProject.value)throw Error('Pilih proyek.');let body={project_id:contractorProject.value,term_no:termNo.value,description:termDescription.value,percentage:termPercent.value||0,amount:termAmount.value||0,invoice_date:termInvoiceDate.value||null,due_date:termDueDate.value||null,sale_id:termSale.value||null,status:termStatus.value,retention_percent:termRetentionPercent.value||0,retention_due_date:termRetentionDue.value||null,retention_status:termRetentionStatus.value,notes:termNotes.value};await api(termId.value?'/api/project-terms/'+termId.value:'/api/project-terms',{method:termId.value?'PUT':'POST',body:JSON.stringify(body)});resetProjectTerm();await loadProjects();contractorProject.value=body.project_id;await loadContractorProject()}catch(e){msg(projectMsg,e.message,false)}}
async function deleteProjectTerm(id){if(!confirm('Hapus termin ini?'))return;await api('/api/project-terms/'+id,{method:'DELETE'});await loadContractorProject()}
</script></body></html>"""
