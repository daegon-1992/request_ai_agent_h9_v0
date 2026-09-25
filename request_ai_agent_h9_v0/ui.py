"""Single page UI for the request assistant."""

from __future__ import annotations


HTML_TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>CAE Request Assistant __APP_VERSION__</title>
  <style>
    :root{
      /* Engineering UI Design Standard v3.0 foundation tokens. */
      --ui-content-max:1400px;
      --ui-agent-width:390px;
      --ui-agent-width-compact:360px;
      --ui-panel-split:14px;
      --ui-workspace-padding:24px;
      --ui-page:#F7F8FA;
      --ui-header:#FFFFFF;
      --ui-surface:#FFFFFF;
      --ui-surface-subtle:#F6F7F9;
      --ui-text-primary:#111214;
      --ui-text-secondary:#50535A;
      --ui-text-muted:#7A7E86;
      --ui-border:#D3D6DB;
      --ui-border-subtle:#E7E9EC;
      --ui-active:#34373E;
      --ui-primary:#56595E;
      --ui-primary-hover:#45484D;
      --ui-step-inactive:#B8BCC3;
      --ui-step-complete:#4CAF68;
      --ui-agent-blue:#5F8FEA;
      --ui-user-bubble:#EDF2F9;
      --ui-warning-bg:#FEF9EA;
      --ui-warning-border:#F2D58A;
      --ui-warning:#F2B447;
      --ui-warning-text:#7A3B16;
      --ui-error:#DA1E28;
      --ui-error-bg:#FFF1F1;
      --ui-disabled-bg:#F3F4F5;
      --ui-disabled-text:#A5A8AE;
      --ui-disabled-border:#E0E2E5;
      --ui-control-border:#BFC4CB;
      --ui-control-hover:#9FA5AD;
      --ui-control-focus:#62676E;
      --ui-field-label:#34373E;
      --ui-field-value:#242629;
      --ui-agent-surface:#F8F9FA;
      --ui-radius-control:7px;
      --ui-radius-panel:8px;
      --ui-shadow-panel:0 1px 2px rgba(17,24,39,.04),0 5px 14px rgba(17,24,39,.045);
      --ui-shadow-control:0 1px 2px rgba(17,24,39,.035);
      --ui-select-picker-max-height:320px;
      --ui-shadow-header:0 1px 2px rgba(17,24,39,.035),0 3px 8px rgba(17,24,39,.035);

      /* Compatibility aliases while screen-specific CSS is migrated in later patches. */
      --ink:var(--ui-text-primary);
      --muted:var(--ui-text-muted);
      --paper:var(--ui-surface);
      --soft:var(--ui-surface-subtle);
      --line:var(--ui-border-subtle);
      --line-strong:var(--ui-border);
      --brand:var(--ui-primary);
      --brand-strong:var(--ui-primary);
      --accent:var(--ui-active);
      --danger:var(--ui-error);
      --warning:var(--ui-warning-text);
      --ok:var(--ui-active);
      --disabled-bg:var(--ui-disabled-bg);
      --disabled-text:var(--ui-disabled-text);
      --shadow:0 1px 3px rgba(0,0,0,.03);
      --global-header-height:60px;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      color:var(--ink);
      background:var(--ui-page);
      border:0;
      border-radius:0;
      box-shadow:none;
      font-family:"Noto Sans KR","Malgun Gothic","Segoe UI",sans-serif;
      font-size:14px;
      font-weight:400;
      line-height:1.6;
      overflow-x:hidden;overflow-y:auto;
    }
    button,input,textarea,select{font-family:inherit}
    [hidden]{display:none!important}
    button{
      min-height:40px;
      border:1px solid var(--ui-border);
      border-radius:var(--ui-radius-control);
      background:var(--ui-surface);
      color:var(--ui-text-primary);
      cursor:pointer;
      font-size:14px;
      font-weight:500;
      padding:7px 11px;
    }
    button.primary{border-color:var(--ui-primary);background:var(--ui-primary);color:#fff}
    button.primary:hover:not(:disabled){border-color:var(--ui-primary-hover);background:var(--ui-primary-hover)}
    button.danger{border-color:var(--ui-error);background:var(--ui-surface);color:var(--ui-error)}
    button.icon{width:34px;padding:0;display:grid;place-items:center}
    button.ghost{background:var(--ui-surface);border-color:var(--ui-border)}
    button.ghost:hover:not(:disabled){border-color:var(--ui-border);background:var(--ui-surface-subtle)}
    button:disabled{border-color:var(--ui-disabled-border);background:var(--ui-disabled-bg);color:var(--ui-disabled-text);cursor:not-allowed}
    input,textarea,select{
      width:100%;
      min-width:0;
      min-height:40px;
      border:1px solid var(--ui-border);
      border-radius:var(--ui-radius-control);
      background:var(--ui-surface);
      color:var(--ui-text-primary);
      padding:10px 12px;
      font-size:14px;
    }
    textarea{min-height:70px;resize:vertical;line-height:1.45}
    label{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:500;color:var(--ink)}
    button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible,[tabindex]:focus-visible{border-color:var(--ui-active);outline:2px solid rgba(52,55,62,.18);outline-offset:1px}
    .topbar{
      height:var(--global-header-height);
      padding:0 24px;
      display:grid;
      grid-template-columns:minmax(0,1fr) auto;
      gap:18px;
      align-items:center;
      border-bottom:1px solid var(--ui-border-subtle);
      background:var(--ui-header);
      box-shadow:var(--ui-shadow-header);
    }
    .brand{display:flex;align-items:center;gap:18px;min-width:0}
    .brand-mark{
      width:auto;height:auto;border-radius:0;display:grid;place-items:center;
      color:var(--ui-text-primary);background:transparent;
      font-size:17px;font-weight:700;letter-spacing:normal;
    }
    h1{margin:0;font-size:16px;line-height:1.2;letter-spacing:0}
    .portal-heading{flex:0 0 auto;min-width:0;padding-left:0;border-left:0}
    .portal-heading::before{content:"";display:inline-block;width:1px;height:24px;margin-right:18px;vertical-align:middle;background:#DDE0E4}
    .portal-heading h1{display:inline;font-size:16px;font-weight:600;letter-spacing:normal;vertical-align:middle}
    .header-request-summary{display:flex;align-items:center;gap:10px;min-width:0;margin-left:8px;padding-left:0;border-left:0}
    .header-request-title{min-width:0;max-width:560px;margin:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#525252;font-size:12px;font-weight:400;line-height:1.35;letter-spacing:-.01em}
    .header-request-number{flex:0 0 auto;margin:0;padding-left:0;border-left:0;color:#8A8A8A;font-size:11px;font-weight:400;line-height:1.35;font-variant-numeric:tabular-nums;white-space:nowrap}
    .subtitle{margin-top:2px;color:var(--muted);font-size:12px}
    .top-meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:4px}
    .request-pill{
      display:inline-flex;align-items:center;min-height:24px;border:1px solid var(--line);
      border-radius:8px;background:var(--soft);color:var(--ink);padding:2px 8px;
      font-size:12px;font-weight:500;
    }
    .request-pill.ok{border-color:#c6c6c6;background:#f7f7f7;color:var(--ok)}
    .request-pill.blocking{border-color:#bdbdbd;background:#f3f3f3;color:var(--danger)}
    .rag-toggle{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:500;color:var(--ink)}
    .rag-toggle input{width:auto}
    .top-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap;justify-content:flex-end}
    .top-actions button{min-height:36px;padding:7px 14px;border-radius:var(--ui-radius-control)}
    .header-request-preview{margin-left:8px;min-height:32px;padding:5px 10px;font-size:12px}
    .top-actions #newRequestBtn{height:36px;min-height:36px;padding:0 15px;border:0;border-radius:6px;background:#34373E;color:#fff;font-size:13px;font-weight:600}
    .top-actions #newRequestBtn:hover:not(:disabled){background:#2F3033;border-color:#2F3033}
    .layout{
      height:auto;min-height:calc(100vh - var(--global-header-height));
      display:grid;
      grid-template-columns:minmax(0,1fr);
      grid-template-areas:"workspace-content";
      grid-template-rows:auto;
      gap:0;
      padding:16px;
      width:100%;
      margin:0 auto;
      justify-content:center;
      border:0;border-radius:0;background:transparent;box-shadow:none;
    }
    .panel{
      min-height:0;
      border:1px solid var(--ui-border);
      border-radius:var(--ui-radius-panel);
      background:var(--ui-surface);
      box-shadow:var(--ui-shadow-panel);
      overflow:hidden;
    }
    .rail{display:grid;grid-template-rows:auto minmax(0,1fr)}
    .rail-head{padding:12px;border-bottom:1px solid var(--line);background:var(--soft)}
    .rail-list{overflow:auto;padding:10px;display:flex;flex-direction:column;gap:8px}
    .main{display:grid;grid-template-rows:minmax(0,1fr)}
    .workspace-shell{display:contents}
    .step-navigation{min-width:0}
    .screen-map{
      display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:0;min-height:56px;padding:10px 14px;
      overflow-x:auto;overflow-y:hidden;scrollbar-width:thin;background:var(--ui-nav-bg);border-bottom:1px solid var(--ui-border-subtle);isolation:isolate;
    }
    .screen-map-item{
      position:relative;display:flex;flex-direction:row;align-items:center;justify-content:center;gap:8px;min-width:0;
      padding:2px 0;border:0;border-radius:var(--ui-radius-control);background:transparent;color:var(--ui-text-secondary);
      font-size:13px;font-weight:500;line-height:1.25;text-align:left;cursor:pointer;
    }
    .screen-map-item:hover:not([aria-disabled="true"]){background:transparent;color:var(--ui-text-primary)}
    .screen-map-item:focus-visible{z-index:1;outline:2px solid rgba(52,55,62,.18);outline-offset:2px}
    .screen-map-item[aria-current="page"]{background:transparent;color:var(--ui-text-primary)}
    .screen-map-number{
      width:32px;height:32px;flex:0 0 32px;display:grid;place-items:center;border-radius:50%;
      background:var(--ui-step-inactive);color:#fff;font-size:13px;font-weight:600;line-height:1;letter-spacing:0;white-space:nowrap;
    }
    .screen-map-label{max-width:100%;display:flex;align-items:center;justify-content:flex-start;gap:5px;white-space:nowrap}
    .screen-map-item[aria-current="page"] .screen-map-number{background:var(--ui-active);color:#fff}
    .screen-map-item[aria-current="page"] .screen-map-label{color:var(--ui-text-primary);font-weight:600}
    .screen-map-lock{display:none;width:12px;height:12px;flex:0 0 12px;place-items:center}
    .screen-map-lock svg{width:12px;height:12px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:2}
    .screen-map-item[aria-disabled="true"]{cursor:not-allowed}
    .screen-map-item[aria-disabled="true"] .screen-map-number{background:var(--ui-step-inactive);opacity:.72}
    .screen-map-item[aria-disabled="true"] .screen-map-label{color:var(--ui-text-muted);opacity:.72}
    .screen-map-item[aria-disabled="true"] .screen-map-lock{display:grid;opacity:.65}
    .screen-group{min-width:0}
    .screen-heading{margin:0 0 6px;padding:0;font-size:22px;font-weight:600;line-height:1.35;letter-spacing:normal;color:var(--muted)}
    .screen-heading span{color:var(--ink)}
    .title-with-icon{display:flex;align-items:center;gap:7px}
    .title-icon{width:29px;height:29px;display:inline-grid;flex:0 0 29px;place-items:center;border:0;border-radius:var(--ui-radius-panel);background:var(--ui-user-bubble);color:var(--ui-agent-blue)}
    .title-icon svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:1.8}
    .screen-heading-code{color:var(--muted)!important}
    .workspace{min-height:0;overflow:visible;padding:var(--ui-workspace-padding);border:0;border-radius:0;background:transparent;box-shadow:none}
    .workspace-tab{display:none;min-height:0}
    .workspace-tab.active{display:block}
    .workspace-form{
      width:100%;
      max-width:1120px;
      margin:0 auto;
    }
    .request-prep-card{
      margin:0;
      border:0;
      border-radius:0;
      background:transparent;
      box-shadow:none;
      overflow:visible;
    }
    .request-prep-card[hidden]{display:none}
    .prep-head{
      display:flex;
      gap:12px;
      align-items:flex-start;
      min-height:86px;
      padding:16px;
      border:1px solid var(--line-strong);
      border-radius:var(--ui-radius-panel);
      background:var(--ui-surface-subtle);
    }
    .prep-info-icon{width:20px;height:20px;display:grid;flex:0 0 20px;place-items:center;margin-top:1px;color:#303234}
    .prep-info-icon svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:1.8}
    .prep-actions{display:flex;gap:7px;align-items:center;flex-wrap:wrap;justify-content:flex-end}
    .prep-body{padding:0;display:grid;gap:24px}
    .prep-flow{display:none}
    .prep-flow.active{display:grid;gap:10px}
    .prep-quick-groups{display:grid;grid-template-columns:1fr;gap:24px;align-items:start}
    .prep-quick-group{min-width:0;padding:0;border:0;background:transparent}
    .prep-quick-group-analysis{padding:24px 0 0;border-top:1px solid var(--ui-border-subtle)}
    .prep-quick-group-title{margin:0 0 13px;font-size:16px;font-weight:600;line-height:1.45;color:var(--ink)}
    .prep-quick-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));column-gap:12px;row-gap:14px;align-items:end}
    .prep-analysis-grid{display:grid;grid-template-columns:minmax(240px,.38fr) minmax(0,.62fr);gap:24px;align-items:start}
    .analysis-scope-field{grid-column:1/-1;display:grid;gap:7px}
    .analysis-scope-label{color:var(--ink);font-size:13px;font-weight:500}
    .direct-choice,.analysis-scope-tabs{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
    .direct-choice button,.analysis-scope-tabs button{min-height:34px;padding:6px 13px;border:1px solid var(--ui-border);border-radius:7px;background:var(--ui-surface);color:var(--ui-text-secondary);font-size:13px;font-weight:500}
    .direct-choice button[aria-pressed="true"],.analysis-scope-tabs button[aria-selected="true"]{border-color:#34373E;background:#34373E;color:#fff;font-weight:600;box-shadow:0 0 0 2px rgba(52,55,62,.12)}
    .analysis-scope-tabs{margin:0 0 8px;padding-bottom:12px;border-bottom:1px solid var(--ui-border-subtle)}
    .analysis-scope-tab-status{font-weight:400}
    .analysis-scope-context{margin:0 0 18px;color:var(--ui-text-primary);font-size:14px;font-weight:600}
    .analysis-type-detail{min-width:0;padding-left:24px;border-left:1px solid var(--ui-border-subtle)}
    .analysis-type-detail-eyebrow{margin:0 0 8px;color:var(--ui-text-muted);font-size:12px;font-weight:500}
    .analysis-type-detail-title{margin:0 0 12px;color:var(--ink);font-size:16px;font-weight:600}
    .analysis-type-detail-description{margin:0;color:var(--ui-text-secondary);font-size:14px;line-height:1.65;white-space:pre-line}
    .analysis-type-detail-subheading{margin:18px 0 8px;color:var(--ink);font-size:13px;font-weight:600}
    .analysis-type-detail-list{margin:0;padding-left:20px;color:var(--ui-text-secondary);font-size:13px;line-height:1.65}
    .prep-start-actions{display:flex;justify-content:flex-end;margin:20px 0 0;padding:10px 0 0;border-top:1px solid var(--ui-border-subtle);background:var(--ui-surface)}
    .prep-start-actions .primary{min-width:0;width:auto;height:36px;min-height:36px;padding:0 13px;border:0;border-radius:6px;background:#2F3033;color:#fff;font-size:13px;font-weight:600}
    .prep-custom-control{display:grid;grid-template-columns:minmax(0,1fr) 42px;gap:6px;align-items:center}
    .prep-custom-control button{width:42px;min-width:42px;height:46px;min-height:46px;padding:0;font-size:18px;line-height:1}
    .prep-summary{
      min-height:240px;
      border:1px solid var(--ui-border);
      border-radius:var(--ui-radius-panel);
      background:var(--ui-surface);
      padding:16px;
      font-size:12px;
      line-height:1.5;
      display:grid;
      grid-template-columns:minmax(0,1fr) auto;
    }
    .prep-summary > strong{display:block;grid-column:1 / -1;font-size:15px;font-weight:600;color:var(--ink);margin-bottom:14px}
    .prep-summary-values{grid-column:1 / -1;display:grid;gap:0;border:1px solid var(--ui-border);border-radius:var(--ui-radius-panel);background:var(--ui-surface-subtle);overflow:hidden}
    .prep-summary-item{display:grid;grid-template-columns:140px minmax(0,1fr);align-items:center;min-width:0;min-height:60px;padding:12px 16px}
    .prep-summary-item + .prep-summary-item{border-top:1px solid var(--line-strong)}
    .prep-summary-label{align-self:stretch;display:flex;align-items:center;border-right:1px solid var(--line-strong);color:#45484B;font-size:13px;font-weight:500}
    .prep-summary-value{padding-left:24px;font-size:15px;font-weight:600;color:var(--ink);overflow-wrap:anywhere}
    .prep-summary-actions{grid-column:1 / -1;grid-row:3;display:flex;justify-content:flex-end;margin-top:16px}
    .prep-summary-actions .primary{min-width:164px;min-height:44px;padding:0 18px;border-radius:8px;font-size:15px;font-weight:600}
    .context-chip-bar{
      margin-bottom:10px;
      border:1px solid var(--line);
      border-radius:8px;
      background:var(--soft);
      padding:10px;
      display:block;
      gap:10px;
      align-items:center;
    }
    .context-chip-bar[hidden]{display:none}
    .context-chip-list{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
    .context-chip-list .chip{font-size:12px}
    .context-chip-copy{margin-top:6px;color:var(--muted);font-size:12px;font-weight:500}
    .context-lock-gate{
      margin-bottom:10px;
      border:1px dashed var(--line);
      border-radius:8px;
      background:var(--soft);
      padding:18px;
      text-align:center;
      color:var(--ink);
      font-size:13px;
      line-height:1.5;
      font-weight:500;
    }
    .context-lock-gate[hidden]{display:none}
    .gate{
      max-width:760px;
      margin:0 0 10px;
      border:1px dashed var(--line);
      border-radius:8px;
      background:var(--soft);
      padding:22px;
      text-align:center;
    }
    .gate strong{display:block;margin-bottom:8px;font-size:18px;color:var(--ink)}
    .section{
      margin-bottom:10px;
      border:1px solid var(--ui-border);
      border-radius:var(--ui-radius-panel);
      background:var(--ui-surface);
      overflow:hidden;
    }
    .section-head{
      min-height:42px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      padding:8px 11px;
      background:var(--soft);
      cursor:pointer;
    }
    .section-title{display:flex;align-items:center;gap:8px;min-width:0}
    .chev{width:20px;color:var(--muted);font-weight:500}
    .section h3{margin:0;font-size:16px;font-weight:600;color:var(--ink);letter-spacing:0}
    .section-body{display:none;border-top:1px solid var(--line);padding:11px 13px}
    .section.open .section-body{display:block}
    .section.open .chev{transform:rotate(90deg)}
    .request-content-screen .section-body{display:block}
    .request-content-screen .section-head{cursor:default}
    .geometry-screen .section-body{display:block}
    .stage-static-screen .section-body{display:block}
    .geometry-screen .section-head,
    .stage-static-screen .section-head{cursor:default}
    .geometry-screen .section-meta{display:none}
    .section-meta{display:flex;gap:6px;align-items:center;flex-wrap:wrap;justify-content:flex-end}
    .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}
    .grid.compact{grid-template-columns:repeat(3,minmax(0,1fr))}
    .request-basic-grid{grid-template-columns:repeat(4,minmax(0,1fr));column-gap:12px;row-gap:14px;align-items:end}
    .request-type-field{grid-column:span 1}
    .request-project-field{grid-column:span 3}
    .request-basic-row2-start{grid-column-start:1}
    .request-basic-divider{grid-column:1/-1;border-top:1px solid var(--line);margin:3px 0}
    .grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}
    .wide{grid-column:1/-1}
    .custom-input{margin-top:5px}
    .dropdown-custom-control .custom-input{margin-top:0}
    .undecided-field{display:flex;min-width:0;flex-direction:column;gap:4px}
    .undecided-combobox,.pms-combobox{
      position:relative;min-width:0;height:36px;display:grid;grid-template-columns:minmax(0,1fr) 36px;
      border:1px solid var(--line);border-radius:7px;background:var(--paper)
    }
    .undecided-combobox:focus-within,.pms-combobox:focus-within{outline:2px solid rgba(52,55,62,.18);outline-offset:2px}
    .undecided-combobox input,.pms-combobox input{height:34px;min-height:34px;border:0;border-radius:6px 0 0 6px;padding:8px 9px;background:transparent}
    .undecided-combobox input:focus-visible,
    .undecided-combobox-toggle:focus-visible{outline:0}
    .undecided-combobox input[readonly]{background:transparent;cursor:default}
    .undecided-combobox-toggle{
      width:36px;height:34px;min-height:34px;padding:0;
      display:grid;place-items:center;border:0;border-radius:0 6px 6px 0;
      background:transparent;color:var(--muted)
    }
    .undecided-combobox-toggle:hover{background:var(--soft);color:var(--ink)}
    .pms-combobox .undecided-combobox-toggle:hover{background:transparent;color:#525252}
    .undecided-combobox-toggle svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:2}
    .undecided-combobox-menu,.pms-combobox-menu{
      position:absolute;z-index:40;top:calc(100% + 4px);left:-1px;right:-1px;padding:0;
      max-height:var(--ui-select-picker-max-height);overflow-y:auto;overscroll-behavior:contain;
      border:1px solid var(--line);border-radius:0;background:var(--paper);box-shadow:none
    }
    .select-picker-menu{position:fixed;z-index:200;max-height:var(--ui-select-picker-max-height);overflow-y:auto;overscroll-behavior:contain;border:1px solid var(--ui-control-border);border-radius:var(--ui-radius-control);background:var(--ui-surface);box-shadow:0 8px 20px rgba(17,24,39,.14)}
    .select-picker-option{display:block;width:100%;min-height:40px;border:0;border-radius:0;background:transparent;padding:8px 10px;color:var(--ui-field-value);font:inherit;text-align:left;cursor:pointer}
    .select-picker-option:hover,.select-picker-option:focus,.select-picker-option[aria-selected="true"]{background:var(--soft);outline:0}
    .select-picker-option:disabled{color:var(--disabled-text);cursor:not-allowed}
    .undecided-combobox-option{
      width:100%;min-height:30px;display:flex;align-items:center;
      border:0;border-radius:0;background:transparent;padding:5px 8px;text-align:left;cursor:default
    }
    .undecided-combobox-option:hover,
    .undecided-combobox-option:focus,
    .undecided-combobox-option[data-undecided-active="true"]{
      background-color:var(--brand)!important;color:#ffffff!important;outline:0
    }
    .pms-combobox-option{width:100%;display:block;border:0;background:transparent;padding:7px 8px;text-align:left;cursor:default}
    .pms-combobox-option:hover,.pms-combobox-option:focus,.pms-combobox-option[data-pms-active="true"]{background-color:var(--brand)!important;color:#fff!important;outline:0}
    .pms-combobox-option small{display:block;margin-top:2px;color:var(--muted);font-size:12px}.pms-combobox-option:hover small,.pms-combobox-option:focus small,.pms-combobox-option[data-pms-active="true"] small{color:inherit}
    .pms-project-helper{margin:0;color:var(--muted);font-size:12px;line-height:1.35}
    .request-detail-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;align-items:start}
    .request-detail-grid textarea{min-height:52px}
    .custom-input[hidden]{display:none}
    .subhead{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:10px 0 7px}
    .subhead strong{font-size:12px;color:var(--ink)}
    .row-list{display:flex;flex-direction:column;gap:7px}
    .row-item{display:grid;grid-template-columns:minmax(0,1fr) 34px;gap:6px;align-items:center}
    .row-item.dual{grid-template-columns:minmax(0,1fr) minmax(0,1fr) 34px;align-items:end}
    .product-input-area{display:grid;gap:10px}
    .product-panel{border:1px solid var(--line);border-radius:9px;background:var(--soft);padding:10px}
    .product-panel-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px}
    .product-panel-head strong{font-size:14px;color:var(--ink)}
    .product-panel-copy{margin:2px 0 0;color:var(--muted);font-size:12px;line-height:1.4}
    .product-card{position:relative;border:1px solid var(--line);border-radius:8px;background:var(--paper);padding:10px}
    .product-card + .product-card{margin-top:8px}
    .product-card-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:9px}
    .product-card-head h4{margin:0;color:var(--ink);font-size:13px;font-weight:600}
    .product-table{display:flex;flex-direction:column;border:1px solid var(--ui-border);border-radius:7px;overflow:hidden;background:var(--ui-surface)}
    .product-table .row-list{display:flex;flex-direction:column;gap:0}
    .product-table-row{display:grid;grid-template-columns:100px minmax(230px,.9fr) minmax(270px,1.1fr) 56px;align-items:stretch;border-bottom:1px solid var(--ui-border-subtle)}
    .product-table .row-list .product-table-row:last-child{border-bottom:0}
    .product-table-row>*{min-width:0;padding:8px 10px;display:flex;align-items:center}
    .product-table-row>*:not(:last-child){border-right:1px solid #EEF0F2}
    .product-table-head{align-items:stretch;background:#F7F8FA;color:#45484D;font-size:13px;font-weight:500}
    .product-table-head>*{min-height:40px}
    .product-table-head .product-action-heading{justify-content:center}
    .product-table .row-list .product-table-row>*{min-height:56px}
    .product-table-row label{margin:0}
    .product-table-row label>input{width:100%}
    .product-geometry-name,.base-product-description{display:flex;align-items:center;min-height:34px;padding:8px 9px;color:var(--ink);font-size:13px;font-weight:400;line-height:1.45}
    .product-card-actions{display:flex;justify-content:flex-end;margin-top:9px}
    .product-card-actions .icon{width:34px;min-width:34px}
    .geometry-policy-guidance{display:flex;gap:12px;align-items:flex-start;margin:0 0 14px;padding:14px 15px;border:1px solid #D9DCE1;border-radius:8px;background:#F8F9FA;color:var(--request-workspace-ink)}
    .geometry-policy-guidance .prep-info-icon{width:19px;height:19px;flex:0 0 19px;color:#62676E}
    .geometry-policy-copy{min-width:0}
    .geometry-policy-heading{display:block;color:#34373E;font-size:13px;font-weight:600;line-height:1.45}
    .geometry-policy-body{margin:4px 0 0;color:#62666D;font-size:12px;font-weight:400;line-height:1.5}
    .changed-part-area{margin-top:10px}
    .part-input-area{border:1px solid var(--line);border-radius:8px;padding:10px;background:var(--paper)}
    .part-input-area .subhead{margin-top:0}
    .part-input-area.is-disabled{opacity:.55}
    .product-row-actions{display:flex;gap:4px;align-items:center}
    .product-row-actions .icon{width:30px;min-width:30px}
    .product-empty{margin:0;color:var(--muted);font-size:12px}
    .toggle-line{display:flex;flex-direction:row;align-items:center;gap:8px;font-size:13px;font-weight:500;margin:8px 0}
    .toggle-line input{width:auto}
    .condition-input-screen .condition-group{overflow:visible;border:0;border-radius:0;margin:0;background:transparent}
    .condition-parent-label{display:inline-flex;align-items:center;min-height:22px;padding:0 7px;border-radius:999px;background:var(--soft);color:var(--ink);font-size:11px;font-weight:500}
    .condition-group h4{margin:0;padding:9px 10px;border-bottom:1px solid var(--line);font-size:13px;color:var(--ink)}
    .condition-input-screen .condition-group-head{display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:0;padding:0 0 13px;border-bottom:0;background:transparent}
    .condition-input-screen .condition-group-head h3{margin:0;color:var(--ink);font-family:var(--request-workspace-font);font-size:16px;font-weight:600}
    .condition-group-head-actions{display:flex;align-items:center;gap:6px}
    .condition-group-head-actions button{min-height:30px;padding:5px 9px}
    .condition-group-head-actions select{min-height:30px;width:156px;padding:5px 28px 5px 9px}
    .condition-group-head h4{border:0;padding:0;margin:0}
    .condition-group-guidance{margin:5px 0 0;color:var(--muted);font-size:12px;line-height:1.45}
    .condition-option-line{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:500;color:var(--ink);white-space:nowrap}
    .condition-option-line input{width:auto}
    .operation-mode-control{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:500;color:var(--ink)}
    .operation-mode-control select{width:auto;min-width:116px;padding:6px 8px}
    .condition-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;padding:10px}
    .heat-exchanger-grid{grid-template-columns:repeat(5,minmax(120px,1fr));overflow:auto}
    .condition-card-layout{display:grid;gap:0}
    .condition-primary-grid{display:grid;grid-template-columns:1fr;gap:0}
    .condition-primary-grid .condition-card-type-heat_exchanger{grid-column:auto}
    .condition-primary-grid .condition-card-type-operating{
      grid-column:1/-1;width:100%
    }
    .condition-primary-grid .condition-group + .condition-group{margin-top:24px;padding-top:24px;border-top:1px solid var(--ui-border-subtle)}
    .condition-environment-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:24px;padding-top:24px;border-top:1px solid var(--ui-border-subtle)}
    .condition-environment-grid > .condition-group + .condition-group{padding-left:24px;border-left:1px solid var(--ui-border-subtle)}
    .workspace-shell .condition-input-screen .condition-temperature-guidance{margin:12px 0 0;color:#70747A;font-size:12px;font-weight:400;line-height:1.5}
    .condition-card-type-space_environment,.condition-card-type-supply_air{overflow:visible}
    .condition-card-type-space_environment:focus-within,.condition-card-type-supply_air:focus-within{position:relative;z-index:45}
    .condition-card-type-space_environment .condition-group-head,.condition-card-type-supply_air .condition-group-head{border-radius:0}
    .condition-card-rows{display:grid;gap:0;padding:0}
    .condition-card-row{display:grid;grid-template-columns:repeat(var(--field-count),minmax(0,1fr)) max-content;gap:9px;align-items:end;padding:10px 0;border-bottom:1px solid #EEF0F2}
    .condition-card-row:last-child{border-bottom:0}
    .condition-card-type-heat_exchanger .condition-card-row{grid-template-columns:64px repeat(3,minmax(0,1.15fr)) repeat(2,minmax(0,1fr)) max-content;gap:9px}
    .condition-card-type-heat_exchanger .condition-card-row>label{min-width:0;white-space:normal;overflow-wrap:break-word}
    .condition-card-type-heat_exchanger .condition-spec-name{padding-inline:4px;white-space:nowrap}
    .condition-card-type-operating .condition-card-row{grid-template-columns:64px 100px minmax(260px,1fr) max-content;align-items:end}
    .condition-card-type-operating .condition-row-actions{grid-column:4;grid-row:1}
    .condition-card-type-operating .condition-spec-name{padding-inline:3px;white-space:nowrap}
    .fan-rpm-editor{--fan-rotation-control-width:186px;display:flex;gap:8px;align-items:end;min-width:0}
    .fan-rpm-editor.single{display:flex}
    .fan-rpm-editor.mode-pending{display:flex}
    .fan-rpm-editor>select[data-fan-rpm-mode]{flex:0 0 var(--fan-rotation-control-width);width:var(--fan-rotation-control-width);max-width:100%;box-sizing:border-box}
    .fan-rpm-control{display:flex;flex:0 1 auto;width:auto;max-width:100%;align-items:center;gap:8px;min-width:0}
    .fan-rpm-control input{flex:0 0 var(--fan-rotation-control-width);width:var(--fan-rotation-control-width);max-width:100%;box-sizing:border-box}
    .fan-rpm-unit{flex:0 0 auto;font-size:13px;font-weight:500;color:var(--muted)}
    .fan-detail-toggle{white-space:nowrap}
    .fan-detail{grid-column:1/-1;grid-row:2}
    .fan-detail[hidden]{display:none}
    .fan-detail-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
    .fan-input-set{display:grid;grid-template-columns:30px minmax(100px,1fr) minmax(90px,120px);gap:10px;align-items:end}
    .fan-input-column{display:flex;flex-direction:column;gap:6px;min-width:0}
    .fan-input-column>span{font-size:13px;font-weight:500;line-height:1.45;color:var(--ink)}
    .fan-input-column input{width:100%}
    .fan-count-custom-control{grid-template-columns:minmax(0,1fr) 42px;gap:4px;width:90px}
    .fan-count-custom-control button{width:42px;min-width:42px}
    .fan-count-custom-control input{min-width:0}
    .condition-card-row input,.condition-card-row select{width:100%}
    .condition-row-actions{display:flex;gap:4px;align-items:center}
    .condition-row-action{width:34px;min-width:34px;height:34px;min-height:34px;padding:0;display:grid;place-items:center;border-radius:6px;font-size:17px;line-height:1}
    .condition-row-action.primary{border-color:#34373E;background:#34373E;color:#fff}
    .condition-row-action.remove{border-color:#C9CDD3;background:#fff;color:#444}
    .row-identity{font-size:13px;font-weight:600;line-height:1.45;color:var(--ink)}
    .condition-field{border:1px solid var(--line);border-radius:8px;padding:9px;background:var(--paper)}
    .condition-head{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:7px}
    .condition-title strong{display:block;font-size:13px;color:var(--ink);overflow-wrap:anywhere}
    .chips{display:flex;gap:5px;flex-wrap:wrap;align-items:center}
    .chip{
      display:inline-flex;align-items:center;min-height:22px;border:1px solid var(--line);
      border-radius:8px;background:var(--soft);color:var(--muted);padding:2px 7px;
      font-size:11px;font-weight:500;line-height:1.2;
    }
    .chip.required{border-color:#c6c6c6;background:#f7f7f7;color:#4a4a4a}
    .chip.blocking{border-color:var(--ui-error);background:var(--ui-error-bg);color:var(--ui-error)}
    .chip.warning{border-color:var(--ui-warning-border);background:var(--ui-warning-bg);color:var(--ui-warning-text)}
    .chip.info{border-color:var(--ui-border);background:var(--ui-surface-subtle);color:var(--ui-agent-blue)}
    .chip.ok{border-color:var(--ui-border);background:var(--ui-surface-subtle);color:var(--ok)}
    .chip.candidate{border-color:var(--ui-border);background:var(--ui-surface-subtle);color:var(--ui-text-secondary)}
    .field-status-note{margin-top:6px;color:var(--muted);font-size:12px;font-weight:500}
    .matrix-wrap{overflow:auto;border:1px solid var(--line);border-radius:8px;background:var(--paper)}
    .case-source-reference{display:grid;margin-bottom:24px;padding-bottom:20px;border-bottom:1px solid var(--divider)}
    .case-source-head{display:grid;grid-template-columns:auto 1fr auto;gap:18px;align-items:center}
    .case-source-head h4{margin:0;color:var(--ink);font-size:14px;font-weight:600;line-height:1.45}
    .case-source-counts{display:flex;align-items:center;gap:22px;min-width:0;color:#525252;font-size:12px;line-height:1.45}
    .case-source-counts span{white-space:nowrap}
    .case-source-counts b{color:#34373E;font-weight:500}
    .case-source-toggle{height:30px;min-height:30px;padding:0 9px;border:1px solid #D5D8DD;border-radius:6px;background:var(--paper);color:#555;font-size:12px;font-weight:500}
    .case-source-content{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr) minmax(0,1.15fr);gap:0;margin-top:14px;padding-top:14px;border-top:1px solid #EEF0F2}
    .case-source-content[hidden]{display:none}
    .case-source-column{min-width:0;padding:0 18px}
    .case-source-column:first-child{padding-left:0}
    .case-source-column:last-child{padding-right:0}
    .case-source-column + .case-source-column{border-left:1px solid #EEF0F2}
    .case-source-column h5{margin:0 0 8px;color:#34373E;font-size:13px;font-weight:500;line-height:1.45}
    .case-source-list{display:grid;margin:0;padding:0;list-style:none}
    .case-source-list li{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:6px;align-items:start;min-width:0;padding:3px 0}
    .case-source-name{color:#6B7078;font-size:12px;font-weight:500;line-height:1.45;overflow-wrap:anywhere}
    .case-source-details{min-width:0;color:#34373E;font-size:12px;font-weight:500;line-height:1.45;overflow-wrap:anywhere;white-space:normal}
    .case-matrix-toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 10px}
    .case-matrix-title{display:flex;align-items:center;gap:9px;min-width:0;flex-wrap:wrap}
    .case-matrix-title h4{margin:0;color:var(--ink);font-size:14px;font-weight:600;line-height:1.45}
    .case-count{color:#777;font-size:11px;font-weight:400;line-height:1.4}
    .case-validation-status{display:inline-flex;align-items:center;color:#55585B;font-size:11px;font-weight:500;line-height:1.4}
    .case-validation-status.error{color:var(--ui-error)}
    .case-validation-status.warning{color:var(--ui-warning-text)}
    .case-validation-status.ok{color:#3F7E51}
    .case-validation-status.pending{color:#55585B}
    .case-matrix-toolbar>[data-action="add-case"]{height:36px;min-height:36px;padding:0 11px;border:0;border-radius:7px;background:#34373E;color:#fff;font-size:13px;font-weight:600;white-space:nowrap}
    .case-select-field{display:grid;width:100%;min-width:0;gap:2px;align-content:start}
    .case-select-field select{display:block;width:100%;min-width:0}
    .case-readonly-value{min-width:0;padding:0 2px;color:var(--ui-field-value);font-size:13px;font-weight:500;line-height:1.45;overflow-wrap:anywhere;white-space:normal}
    .case-select-summary{min-width:0;padding:0 2px;color:#5F646C;font-size:11px;font-weight:500;line-height:1.3;overflow-wrap:anywhere;white-space:normal}
    .case-select-summary[hidden]{display:none}
    .case-number{width:54px;color:#45484B;font-size:14px;font-weight:600;text-align:center}
    .case-remove-cell{width:64px;text-align:center}
    .geometry-drawing-warning:empty,.geometry-cad-warning:empty,.condition-duplicate-warning:empty,.case-duplicate-warning:empty,.case-coverage-status:empty,#previewCoverageWarning:empty{display:none}
    .case-review-message{display:grid;gap:7px;position:relative;margin-top:10px;padding:8px 10px;border-radius:8px;color:#242424;font-size:12px;line-height:1.4}
    .case-review-message.error{border:1px solid var(--ui-error);background:var(--ui-error-bg)}
    .case-review-message.warning{border:1px solid var(--ui-warning-border);background:var(--ui-warning-bg)}
    .coverage-warning-head{display:flex;align-items:center;gap:6px}
    .coverage-warning-icon{display:inline-grid;flex:0 0 16px;width:16px;height:16px;place-items:center;color:var(--ui-warning);font-size:14px;line-height:1}
    .case-review-message.error .coverage-warning-icon{color:var(--ui-error)}
    .coverage-warning-icon svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:2}
    .coverage-warning-title{color:#242424;font-size:13px;font-weight:600}
    .coverage-warning-copy{margin:0;color:#333333;font-size:12px}
    .coverage-unused-list{display:grid;gap:3px}
    .coverage-unused-row{display:grid;grid-template-columns:minmax(72px,120px) minmax(0,1fr);gap:10px;color:#242424;font-size:12px}
    .coverage-unused-label{font-weight:600}
    .coverage-unused-options{color:#333333}
    .case-action-notice{display:grid;gap:3px;margin-top:8px;padding:8px 10px;border:1px solid var(--ui-border);border-left:3px solid var(--ui-text-muted);border-radius:var(--ui-radius-panel);background:var(--ui-surface-subtle);color:var(--ui-text-primary);font-size:12px;line-height:1.4}
    #previewCoverageWarning button{justify-self:start;min-height:36px;padding:7px 11px;border-radius:8px}
    .case-toolbar{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px}
    table{width:100%;border-collapse:collapse;min-width:540px;font-size:12px}
    .combination-summary{display:flex;gap:7px;flex-wrap:wrap;padding:9px;border:1px solid var(--line);border-radius:8px;background:var(--soft);font-size:12px}
    .combination-list{display:grid;gap:8px}
    .combination-card{border:1px solid var(--line);border-radius:8px;background:var(--paper);padding:10px;display:grid;gap:8px}
    .combination-card-head{display:flex;justify-content:space-between;gap:8px;align-items:center}
    .combination-picker{display:flex;gap:6px;flex-wrap:wrap}
    .combination-picker label{display:inline-flex;flex-direction:row;align-items:center;gap:4px;padding:4px 6px;border:1px solid var(--line);border-radius:6px;background:var(--soft);font-size:11px}
    .combination-picker input{width:auto}
    th,td{border-bottom:1px solid var(--line);padding:8px;text-align:left;vertical-align:middle;overflow-wrap:anywhere}
    th{position:sticky;top:0;background:var(--soft);color:var(--ink);font-weight:600}
    tr.excluded td{color:#8a8a8a;background:#f3f3f3;text-decoration:line-through}
    .empty{border:1px dashed var(--line);border-radius:8px;background:var(--soft);color:var(--muted);padding:12px;font-size:13px;line-height:1.45}
    .common-block{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
    .review-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-bottom:10px}
    .metric{border:1px solid var(--line);border-radius:8px;background:var(--paper);padding:9px}
    .metric span{display:block;color:var(--muted);font-size:11px;font-weight:500}
    .metric strong{display:block;margin-top:3px;font-size:15px}
    .issue-list{display:flex;flex-direction:column;gap:7px}
    .issue{border:1px solid var(--line);border-radius:8px;padding:9px;background:var(--paper);font-size:12px;line-height:1.45}
    .issue.blocking{border-color:var(--ui-error);background:var(--ui-error-bg)}
    .issue.warning{border-color:var(--ui-warning-border);background:var(--ui-warning-bg)}
    .issue.info{border-color:var(--ui-border);background:var(--ui-surface-subtle)}
    .issue button{margin-top:7px}
    .issue code{display:block;margin-top:3px;color:var(--muted);font-size:11px;white-space:normal}
    .inline-issue{display:none;margin-top:4px;font-size:11px;line-height:1.35}
    .field-touched .inline-issue{display:block}
    .field-highlight{outline:2px solid rgba(52,55,62,.18);outline-offset:3px;border-radius:var(--ui-radius-panel)}
    .required-field-highlight{outline:0;border-color:#E7A1A1;box-shadow:0 0 0 2px rgba(220,38,38,.10),0 2px 5px rgba(220,38,38,.08);border-radius:var(--ui-radius-control)}
    .analysis-scope-field .direct-choice button.required-field-highlight{border-color:#E7A1A1;box-shadow:0 0 0 2px rgba(220,38,38,.10),0 2px 5px rgba(220,38,38,.08)}
    .draft-output{margin-top:10px;border:1px solid var(--line);border-radius:8px;background:var(--soft);padding:10px;white-space:pre-wrap;font-size:12px;line-height:1.5}
    .preview-doc{display:grid;gap:10px}
    .preview-section{border:1px solid var(--line);border-radius:8px;background:var(--paper);padding:10px}
    .preview-section h4{margin:0 0 8px;font-size:13px;color:var(--ink)}
    .preview-kv{display:grid;grid-template-columns:140px minmax(0,1fr);gap:8px;padding:5px 0;border-top:1px solid var(--line);font-size:12px}
    .preview-kv:first-of-type{border-top:0}
    .preview-kv > span:first-child{color:var(--muted);font-weight:500}
    .preview-field-label,.preview-condition-item,.word-export-required-warning{display:inline-flex;align-items:center;gap:4px}
    .preview-condition-list{display:flex;align-items:center;gap:5px;flex-wrap:wrap}
    .preview-condition-separator{color:var(--muted)}
    .preview-missing-icon{width:14px;height:14px;display:inline-grid;flex:0 0 14px;place-items:center;color:var(--ui-error)}
    .preview-missing-icon svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:2}
    .preview-table{width:100%;border-collapse:collapse;font-size:12px}
    .preview-table caption{text-align:left;padding:7px 0;font-weight:600;color:var(--ink)}
    .chat{display:grid;grid-template-rows:auto minmax(0,1fr) auto}
    .agent-dock{grid-area:agent;height:100%;min-width:0;transition:opacity .18s ease,transform .18s ease}
    .panel-resizer{display:none}
    .layout.agent-hidden{grid-template-columns:minmax(0,1fr);grid-template-areas:"workspace-content"}
    .layout.agent-hidden .agent-dock{display:none}
    .chat-head{height:58px;min-height:58px;display:flex;align-items:center;justify-content:space-between;gap:9px;padding:0 15px;border-bottom:1px solid var(--ui-border-subtle);background:var(--ui-surface)}
    .chat-head-actions{display:flex;align-items:center;gap:6px}
    .chat-head-actions button{width:34px;min-width:34px;height:34px;min-height:34px;padding:0;display:inline-grid;place-items:center;border-radius:7px;background:var(--ui-surface);color:var(--ui-text-muted);font-size:0;line-height:1}
    .chat-head-actions button:hover{border-color:#C9CDD3;background:var(--ui-surface-subtle);color:var(--ui-text-primary)}
    .chat-head-actions button svg{
      width:17px;height:17px;display:block;fill:none;stroke:currentColor;stroke-width:1.8;
      stroke-linecap:round;stroke-linejoin:round;pointer-events:none;
    }
    .stage-assist{display:grid;gap:8px}
    .stage-assist-title{display:block;font-size:18px;font-weight:600;color:#151617}
    .stage-assist-copy{margin:0;color:var(--muted);font-size:12.5px;line-height:1.45}
    .stage-assist-actions{display:grid;gap:6px}
    .stage-assist-action{width:100%;min-height:34px;text-align:left;background:var(--paper);border-color:var(--line);color:var(--ink);font-weight:500;white-space:normal}
    .stage-assist-action:hover{border-color:var(--accent);background:var(--soft)}
    .chat-log{min-height:0;overflow:auto;padding:18px 16px 20px 12px;background:var(--ui-agent-surface)}
    .msg{max-width:92%;margin-bottom:9px;border-radius:8px;padding:9px 10px;font-size:13px;line-height:1.45;white-space:pre-wrap}
    .msg.assistant{border:1px solid var(--line);background:var(--paper)}
    .msg.user{margin-left:auto;border:1px solid var(--line);background:var(--soft);color:var(--ink)}
    .rec-list{display:flex;flex-direction:column;gap:6px;margin-top:8px}
    .rec-list button{text-align:left;background:var(--paper)}
    .proposal-card{display:grid;gap:8px;border-color:var(--line);background:var(--paper)}
    .proposal-card strong{font-size:13px;color:var(--ink)}
    .proposal-list{display:grid;gap:5px;margin:0;padding:0;list-style:none}
    .proposal-list li{border:1px solid var(--line);border-radius:8px;background:var(--paper);padding:7px 8px}
    .proposal-actions{display:flex;gap:8px;flex-wrap:wrap}
    .proposal-actions button{min-width:74px}
    .quick-action-card{
       border:1px solid var(--line);
      border-radius:8px;
       background:var(--soft);
      padding:10px;
      white-space:normal;
    }
    .quick-action-title{display:block;margin-bottom:2px;color:var(--brand-strong)}
    .quick-action-copy{line-height:1.45}
    .quick-actions button{
      min-height:34px;
      background:var(--paper);
       border-color:var(--line);
      color:var(--ink);
      font-weight:500;
    }
    .loading-message{display:flex;align-items:center;gap:8px}
    .spinner{
      width:16px;height:16px;border-radius:50%;
       border:2px solid var(--line);border-top-color:var(--brand);
      animation:spin .8s linear infinite;flex:0 0 auto;
    }
    @keyframes spin{to{transform:rotate(360deg)}}
    .chat-input{padding:11px;border-top:1px solid var(--ui-border-subtle);background:var(--ui-surface)}
    .chat-row{display:flex;gap:8px;align-items:center}
    .chat-row textarea{height:42px;min-height:42px;max-height:150px;padding:10px;border:1.5px solid var(--ui-control-border);border-radius:var(--ui-radius-control);background:var(--ui-surface);color:var(--ui-field-value);font-size:13px;font-weight:400;line-height:1.45;box-shadow:var(--ui-shadow-control)}
    .chat-row .primary{height:42px;min-width:56px;min-height:42px;padding:0 13px;border:0;border-radius:6px;background:#2F3033;color:#fff;font-size:13px;font-weight:600}
    .chat-row button{align-self:center}
    .orchestrator-readonly{margin-top:6px;border-top:1px solid var(--line);padding-top:6px;color:var(--muted);font-size:11px;line-height:1.45}
    .orchestrator-proposal{margin-top:6px;border:1px solid var(--line);border-radius:7px;padding:7px;color:var(--ink);font-size:12px;line-height:1.45}
    .submit-modal{
      position:fixed;inset:0;display:grid;place-items:center;
       background:rgba(0,0,0,.28);z-index:20;padding:20px;
    }
    .submit-dialog{
       width:min(420px,100%);border:1px solid var(--line);border-radius:10px;
       background:var(--paper);box-shadow:var(--shadow);
      padding:22px;text-align:center;
    }
    .submit-dialog strong{display:block;font-size:20px;color:var(--ink);margin-bottom:14px}
    .submit-modal[hidden]{display:none}
    .request-preview-modal{align-items:stretch;padding:32px}
    .request-preview-dialog{display:grid;grid-template-rows:auto minmax(0,1fr);width:min(1120px,100%);max-height:calc(100vh - 64px);padding:0;text-align:left}
    .request-preview-dialog-head{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:18px 22px;border-bottom:1px solid var(--line)}
    .request-preview-dialog-head strong{margin:0;font-size:18px}
    .request-preview-dialog-body{overflow-y:auto;padding:22px}
    .request-preview-dialog-body .case-review-message{gap:5px;margin-top:8px;padding:9px 10px;border-radius:8px;font-size:12px}
    .request-preview-dialog-body .coverage-warning-title{font-size:12px}
    .request-preview-dialog-body .coverage-warning-copy{font-size:11px;line-height:1.45}
    .request-preview-dialog-body .preview-field-missing{color:inherit}
    .request-preview-dialog-body .preview-table-value.preview-field-missing{color:#5F646C}
    .request-preview-dialog-body .request-preview-case-errors{gap:8px;margin-top:12px;padding:12px 14px}
    .request-preview-dialog-body .request-preview-case-errors>.coverage-warning-head{padding-bottom:7px;border-bottom:1px solid #F1C8C8}
    .request-preview-dialog-body .request-preview-case-error-scope{display:grid;gap:4px}
    .request-preview-dialog-body .request-preview-case-error-scope+.request-preview-case-error-scope{padding-top:8px;border-top:1px solid #F4DADA}
    .request-preview-dialog-body .request-preview-case-errors .request-preview-case-error-scope>.coverage-warning-head{display:none}
    .request-preview-dialog-body .request-preview-case-errors .preview-scope-heading{margin:0;color:#242424;font-size:12px;font-weight:600;line-height:1.4}
    .context-change-actions{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:14px}
    @media (max-width:1180px){
      .condition-grid,.heat-exchanger-grid,.review-grid,.prep-quick-groups,.condition-primary-grid,.condition-environment-grid{grid-template-columns:1fr}
      .prep-quick-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
      .prep-analysis-grid{grid-template-columns:1fr}
      .analysis-type-detail{padding-left:0;padding-top:20px;border-left:0;border-top:1px solid var(--ui-border-subtle)}
      .condition-primary-grid .condition-card-type-operating{width:100%}
      .condition-environment-grid > .condition-group + .condition-group{padding-left:0;border-left:0;padding-top:24px;border-top:1px solid var(--ui-border-subtle)}
      .grid,.grid.compact,.grid.two,.request-basic-grid,.request-detail-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
      .prep-actions{justify-content:flex-start}
    }
    @media (max-width:760px){
      .condition-card-type-operating .condition-card-row{grid-template-columns:56px 90px minmax(0,1fr) max-content}
      .fan-rpm-editor{grid-template-columns:1fr}
      .fan-detail-grid{grid-template-columns:1fr}
    }
    @media (max-width:1039px){
      body{overflow:auto;overflow-x:hidden}
      .agent-dock{
        position:fixed;z-index:14;right:12px;bottom:12px;width:min(340px,calc(100vw - 24px));
        height:min(620px,calc(100vh - 24px));min-height:440px;box-shadow:var(--shadow);
      }
      .layout.agent-hidden .agent-dock{display:grid;opacity:0;pointer-events:none;transform:translateX(calc(100% + 24px));visibility:hidden}
    }
    @media (max-width:720px){
      .case-source-content{grid-template-columns:1fr}
      .case-source-column{padding:12px 0 0}
      .case-source-column:first-child{padding-top:0}
      .case-source-column + .case-source-column{border-left:0;border-top:1px solid #EEF0F2}
      .screen-map{grid-template-columns:repeat(6,max-content);gap:18px;min-height:0;overflow-x:auto;overscroll-behavior-x:contain;scrollbar-width:thin}
      .screen-map-item{min-height:36px}
      .grid,.grid.compact,.grid.two,.request-basic-grid,.request-detail-grid,.prep-quick-grid{grid-template-columns:1fr}
      .request-type-field,.request-project-field{grid-column:auto}
    }
    /* T2-01A: completed Shell, SCREEN-01/02, and Agent Dock share the design-lock surface system. */
    .section h3,.screen-heading span{color:var(--ink)}
    .chip{border-color:var(--line);background:var(--soft);color:var(--muted)}
    .chip.info{border-color:var(--line);background:var(--soft);color:var(--brand)}
    .chip.required{border-color:#c6c6c6;background:#f7f7f7;color:var(--warning)}
    .screen-heading-code{font-size:12px;font-weight:500}
    .screen-action-bar{display:flex;flex:0 0 auto;justify-content:space-between;gap:10px;margin-top:auto;padding:10px 0 0;border-top:1px solid var(--ui-border-subtle);background:var(--ui-surface)}
    /* SCREEN-01~06 workspace-only visual surface; Agent Dock is a sibling of .workspace-shell. */
    .workspace-shell{
      --request-workspace-font:"Noto Sans KR","Malgun Gothic","Segoe UI",sans-serif;
      --request-workspace-surface:var(--ui-surface);
      --request-workspace-border:var(--ui-border);
      --request-workspace-ink:var(--ui-text-primary);
      --request-workspace-muted:var(--ui-text-muted);
      --request-workspace-accent:var(--ui-active);
      --request-workspace-radius:var(--ui-radius-panel);
      --request-workspace-shadow:none;
      --request-workspace-card-section-gap:16px;
      font-family:var(--request-workspace-font);
      color:var(--request-workspace-ink);
    }
    .screen-navigation-status{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap}
    .workspace-shell .workspace-form{font-family:var(--request-workspace-font)}
    .workspace-shell .workspace-form .screen-heading{color:var(--request-workspace-muted)}
    .workspace-shell .workspace-form .screen-heading span{color:var(--request-workspace-ink)}
    .workspace-shell .screen-group > .section{border-color:var(--request-workspace-border);border-radius:var(--request-workspace-radius);background:var(--request-workspace-surface);box-shadow:var(--request-workspace-shadow)}
    .workspace-shell .screen-group > .request-prep-card{border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}
    .workspace-shell .request-prep-card .prep-head{min-height:0;padding:0;border:0;background:transparent}
    .workspace-shell .request-prep-card .prep-actions:has(button:not([hidden])){margin-bottom:13px}
    .workspace-shell .screen-group > .section > .section-head{background:var(--request-workspace-surface);border-color:var(--request-workspace-border)}
    .workspace-shell .screen-group > .section > .section-body{border-color:var(--request-workspace-border)}
    .workspace-shell .condition-input-screen > .screen-scroll-content > #section-conditions{
      margin-bottom:0;
      border:0;
      border-radius:0;
      background:transparent;
      box-shadow:none;
      overflow:visible;
    }
    .workspace-shell .condition-input-screen > .screen-scroll-content > #section-conditions > .section-body{padding:0;border:0}
    .workspace-shell .screen-group > .section > .section-head h3{color:var(--request-workspace-ink);font-size:16px;font-weight:600}
    .workspace-shell .section-title-icon{width:20px;height:20px;display:inline-grid;flex:0 0 20px;place-items:center;color:var(--request-workspace-accent)}
    .workspace-shell .section-title-icon svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:1.8}
    .workspace-shell .workspace-form :is(label,.field-label){gap:6px;color:var(--ui-field-label);font-size:13px;font-weight:500;line-height:1.45}
    .workspace-shell .workspace-form :is(input,select){font-family:var(--request-workspace-font);font-size:14px;font-weight:500;color:var(--ui-field-value);background-color:var(--request-workspace-surface);border:1.5px solid var(--ui-control-border);border-radius:var(--ui-radius-control);box-shadow:var(--ui-shadow-control)}
    .workspace-shell .workspace-form textarea{font-family:var(--request-workspace-font);font-size:14px;font-weight:400;color:var(--ui-field-value);background-color:var(--request-workspace-surface);border:1.5px solid var(--ui-control-border);border-radius:var(--ui-radius-control);box-shadow:var(--ui-shadow-control)}
    .workspace-shell .workspace-form :is(input,textarea)::placeholder{color:#8A8A8A;font-weight:400;opacity:1}
    .workspace-shell .request-content-screen :is(input,select,textarea){font-family:var(--request-workspace-font);font-size:14px;font-style:normal;line-height:1.45;letter-spacing:normal;color:var(--ui-field-value)}
    .workspace-shell .geometry-screen :is(input,select,textarea,.analysis-result-guidance){font-family:var(--request-workspace-font);font-size:14px;font-style:normal;line-height:1.45;letter-spacing:normal;color:var(--request-workspace-ink)}
    .workspace-shell .stage-static-screen[data-screen="SCREEN-04"] :is(input,select,textarea,.analysis-result-guidance){font-family:var(--request-workspace-font);font-size:14px;font-style:normal;line-height:1.45;letter-spacing:normal;color:var(--request-workspace-ink)}
    .workspace-shell .workspace-form :is(input,textarea,select):hover:not(:disabled){border-color:var(--ui-control-hover);box-shadow:0 1px 3px rgba(17,24,39,.05)}
    .workspace-shell .workspace-form :is(input,textarea,select):disabled{border-color:var(--ui-disabled-border);background-color:var(--ui-disabled-bg);color:#9A9EA5;opacity:1}
    .workspace-shell .workspace-form input:focus-visible,.workspace-shell .workspace-form select:focus-visible,.workspace-shell .workspace-form textarea:focus-visible{border-color:var(--ui-control-focus);outline:0;box-shadow:0 0 0 2px rgba(52,55,62,.10),0 1px 3px rgba(17,24,39,.05)}
    .workspace-shell .workspace-form :is(input,textarea,select).required-field-highlight,
    .workspace-shell .workspace-form :is(input,textarea,select).required-field-highlight:focus-visible{border-color:#E7A1A1;outline:0;box-shadow:0 0 0 2px rgba(220,38,38,.12),0 2px 5px rgba(220,38,38,.10)}
    .workspace-shell .workspace-form select{
      appearance:none;-webkit-appearance:none;height:40px;min-height:40px;padding:0 38px 0 10px;
      border:1.5px solid var(--ui-control-border);border-radius:var(--ui-radius-control);background-color:#fff;
      background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23525252' stroke-linecap='round' stroke-linejoin='round' stroke-width='2'%3E%3Cpath d='m7 9 5 5 5-5'/%3E%3C/svg%3E");
      background-repeat:no-repeat;background-position:right 11px center;background-size:16px 16px;
      color:var(--ui-field-value);font-size:14px;font-weight:500;box-shadow:var(--ui-shadow-control);
    }
    .workspace-shell .workspace-form select:disabled{
      background-color:var(--ui-disabled-bg);
      background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%239A9EA5' stroke-linecap='round' stroke-linejoin='round' stroke-width='2'%3E%3Cpath d='m7 9 5 5 5-5'/%3E%3C/svg%3E");
    }
    .workspace-shell .workspace-form button{font-family:var(--request-workspace-font);font-weight:500;border-color:var(--request-workspace-border);background-color:var(--request-workspace-surface);color:var(--request-workspace-ink);box-shadow:none}
    .workspace-shell .workspace-form .direct-choice button[aria-pressed="true"],.workspace-shell .workspace-form .analysis-scope-tabs button[aria-selected="true"]{border-color:#34373E;background:#34373E;color:#fff;font-weight:600;box-shadow:0 0 0 2px rgba(52,55,62,.12)}
    .workspace-shell .workspace-form button.primary{border-color:var(--ui-primary);background-color:var(--ui-primary);color:#fff}
    .workspace-shell .workspace-form button.primary:hover:not(:disabled){border-color:var(--ui-primary-hover);background:var(--ui-primary-hover)}
    .workspace-shell .workspace-form button:disabled{border-color:var(--line);background:var(--disabled-bg);color:var(--disabled-text)}
    .workspace-shell .workspace-form table{color:var(--request-workspace-ink);border-color:var(--request-workspace-border)}
    .workspace-shell .request-content-screen > .screen-scroll-content > #section-overview{background:var(--request-workspace-surface)}
    .workspace-shell .request-content-screen > .screen-scroll-content > #section-overview .analysis-result-guidance{border-color:var(--request-workspace-border);background:var(--soft)}
    .workspace-shell .screen-action-bar{border-color:var(--ui-border-subtle);background:var(--ui-surface)}
    .workspace-shell :is(.screen-action-bar button,.workflow-action-button){min-width:0;width:auto;height:36px;min-height:36px;padding:0 13px;border-radius:6px;font-size:13px;font-weight:600}
    .workspace-shell :is(.screen-action-bar button.primary,.workflow-action-button.primary){border-color:#2F3033;background:#2F3033;color:#fff}
    .workspace-shell :is(.screen-action-bar button.primary,.workflow-action-button.primary):hover:not(:disabled){border-color:#252629;background:#252629}
    .workspace-shell .screen-action-bar button:not(.primary){border:1px solid #C9CDD3;background:#fff;color:#404348}
    .workspace-shell :is(.screen-action-bar button,.workflow-action-button):disabled{border-color:var(--ui-disabled-border);background:var(--ui-disabled-bg);color:var(--ui-disabled-text)}
    .workspace-shell .prep-start-actions #prepStartBtn{background:#2F3033;color:#fff}
    .workspace-shell .screen-map-item:focus-visible{outline-color:rgba(52,55,62,.18)}
    .topbar .subtitle{display:none}
    .workspace-shell .screen-heading-code{display:none}
    .workspace-shell .screen-description{margin:0 0 26px;color:#525252;font-size:14px;font-weight:400;line-height:1.55}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .section-head h3{color:var(--request-workspace-ink)}
    .workspace-shell .geometry-screen .chev,
    .workspace-shell .stage-static-screen .chev,
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .chev{display:none}
    .workspace-shell .geometry-screen .section-meta,
    .workspace-shell .stage-static-screen .section-meta,
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .section-meta{display:none}
    .workspace-shell .product-panel{border-color:var(--request-workspace-border);background:var(--soft)}
    .workspace-shell .product-panel-head strong,
    .workspace-shell .product-card-head h4{color:var(--request-workspace-accent)}
    .workspace-shell .product-panel-copy{color:var(--request-workspace-muted)}
    .workspace-shell .product-card{border-color:var(--request-workspace-border);box-shadow:none}
    .workspace-shell .condition-input-screen .condition-group{border-radius:0;box-shadow:none}
    .workspace-shell .case-toolbar{border-color:var(--request-workspace-border);background:var(--soft)}
    .workspace-shell .preview-actions{display:flex;align-items:center;justify-content:flex-end;gap:9px;margin-top:24px;border-top:1px solid var(--request-workspace-border);padding-top:16px}
    .workspace-shell .word-export-required-warning{color:var(--ui-error);font-size:12px;font-weight:600!important}
    .workspace-shell .request-content-screen > .screen-scroll-content > .section{margin:0;border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}
    .workspace-shell .request-content-screen > .screen-scroll-content > .section + .section{margin-top:24px;padding-top:24px;border-top:1px solid var(--ui-border-subtle)}
    .workspace-shell .request-content-screen > .screen-scroll-content > #analysisGate + .section{margin-top:24px;padding-top:24px;border-top:1px solid var(--ui-border-subtle)}
    .workspace-shell .request-content-screen > .screen-scroll-content > .section > .section-head{min-height:0;padding:0;background:transparent;border-bottom:0}
    .workspace-shell .request-content-screen > .screen-scroll-content > .section > .section-body{padding:13px 0 0;border-top:0}
    .workspace-shell .request-content-screen > .screen-scroll-content > .section > .section-head h3{margin:0;line-height:1.45;color:var(--ink)}
    .workspace-shell .geometry-screen > .screen-scroll-content > #section-geometry{margin:0;border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}
    .workspace-shell .geometry-screen > .screen-scroll-content > #section-geometry > .section-head{min-height:0;padding:0;background:transparent;border-bottom:0}
    .workspace-shell .geometry-screen > .screen-scroll-content > #section-geometry > .section-body{padding:0;border-top:0}
    .workspace-shell .geometry-screen > .screen-scroll-content > #section-geometry > .section-head h3{margin:0 0 13px;color:var(--ink)}
    /* SCREEN-04 group heading typography and spacing are owned by the base condition-input-screen component. */
    .workspace-shell .condition-group-head-actions button{min-height:24px;height:24px;padding:2px 7px}
    .workspace-shell .request-content-screen input,.workspace-shell .request-content-screen select{height:40px;min-height:40px;padding:0 10px;background-color:var(--paper);color:var(--ui-field-value);font-weight:500}
    .workspace-shell .request-content-screen :is(.undecided-combobox,.pms-combobox){height:40px;min-height:40px;grid-template-columns:minmax(0,1fr) 38px;border:1.5px solid var(--ui-control-border);border-radius:var(--ui-radius-control);background:var(--paper);box-shadow:var(--ui-shadow-control)}
    .workspace-shell .request-content-screen .undecided-combobox:hover{border-color:var(--ui-control-hover);box-shadow:0 1px 3px rgba(17,24,39,.05)}
    .workspace-shell .request-content-screen .undecided-combobox:focus-within{border-color:var(--ui-control-focus);outline:0;box-shadow:0 0 0 2px rgba(52,55,62,.10),0 1px 3px rgba(17,24,39,.05)}
    .workspace-shell .request-content-screen .pms-combobox:hover{border-color:var(--ui-control-hover);box-shadow:0 1px 3px rgba(17,24,39,.05)}
    .workspace-shell .request-content-screen .pms-combobox:focus-within{border-color:var(--ui-control-focus);outline:0;box-shadow:0 0 0 2px rgba(52,55,62,.10),0 1px 3px rgba(17,24,39,.05)}
    .workspace-shell .request-content-screen .pms-combobox[data-disabled="true"]{border-color:var(--ui-disabled-border);background:var(--ui-disabled-bg);box-shadow:none}
    .workspace-shell .request-content-screen .pms-combobox[data-disabled="true"] input:disabled{background:transparent;color:var(--ui-disabled-text);cursor:not-allowed;opacity:1}
    .workspace-shell .request-content-screen .pms-combobox[data-disabled="true"] .undecided-combobox-toggle:disabled{background:transparent;color:var(--ui-disabled-text);cursor:not-allowed;opacity:1}
    .workspace-shell .request-content-screen :is(.undecided-combobox,.pms-combobox) input{height:38px;min-height:38px;padding:0 10px;border:0;border-radius:6px 0 0 6px;background:transparent;box-shadow:none;font-weight:500}
    .workspace-shell .request-content-screen .undecided-combobox input:focus-visible,
    .workspace-shell .request-content-screen .pms-combobox input:focus-visible,
    .workspace-shell .request-content-screen .undecided-combobox-toggle:focus-visible{border:0;outline:0;outline-offset:0}
    .workspace-shell .request-content-screen .undecided-combobox-toggle{width:38px;height:38px;min-height:38px;border:0;border-radius:0 6px 6px 0;background:transparent;color:#525252}
    .workspace-shell .request-content-screen .request-model-field .undecided-combobox{position:relative;grid-template-columns:minmax(0,1fr)}
    .workspace-shell .request-content-screen .request-model-field .undecided-combobox-toggle{
      position:absolute;right:1px;top:1px;width:36px;height:36px;min-height:36px;opacity:0;pointer-events:none;transition:opacity .12s ease;
    }
    .workspace-shell .request-content-screen .request-model-field .undecided-combobox:hover .undecided-combobox-toggle,
    .workspace-shell .request-content-screen .request-model-field .undecided-combobox:focus-within .undecided-combobox-toggle{opacity:1;pointer-events:auto}
    .workspace-shell .request-content-screen .dropdown-custom-control{grid-template-columns:minmax(0,1fr) 38px}
    .workspace-shell .request-content-screen .dropdown-custom-control > button{width:38px;min-width:38px;height:40px;min-height:40px}
    .workspace-shell .geometry-screen input{min-height:40px;padding:0 10px;background:var(--paper);color:var(--ui-field-value)}
    .workspace-shell .geometry-screen .product-geometry-name{min-height:40px;padding:8px 10px}
    .workspace-shell .geometry-screen .base-product-description{min-height:40px;padding:8px 10px;font-size:14px;font-weight:400}
    .workspace-shell .geometry-screen .condition-row-actions{min-height:40px;align-items:center;justify-content:center}
    .workspace-shell .condition-input-screen .condition-card-row :is(input,select){min-height:40px;padding:0 10px;background-color:var(--paper)}
    .workspace-shell .condition-input-screen .condition-spec-name{min-height:40px;padding-block:0}
    .workspace-shell .condition-input-screen .condition-temperature-combobox{height:40px;min-height:40px;grid-template-columns:minmax(0,1fr) 38px;border:1.5px solid var(--ui-control-border);border-radius:var(--ui-radius-control);background:var(--paper);box-shadow:var(--ui-shadow-control)}
    .workspace-shell .condition-input-screen .condition-temperature-combobox:hover{border-color:var(--ui-control-hover);box-shadow:0 1px 3px rgba(17,24,39,.05)}
    .workspace-shell .condition-input-screen .condition-temperature-combobox:focus-within{border-color:var(--ui-control-focus);outline:0;box-shadow:0 0 0 2px rgba(52,55,62,.10),0 1px 3px rgba(17,24,39,.05)}
    .workspace-shell .condition-input-screen .condition-temperature-combobox input{height:38px;min-height:38px;padding:0 10px;border:0;border-radius:6px 0 0 6px;background:transparent;box-shadow:none}
    .workspace-shell .condition-input-screen .condition-temperature-combobox input:focus-visible,
    .workspace-shell .condition-input-screen .condition-temperature-combobox .undecided-combobox-toggle:focus-visible{border:0;outline:0;outline-offset:0}
    .workspace-shell .condition-input-screen .condition-temperature-combobox .undecided-combobox-toggle{width:38px;height:38px;min-height:38px;border:0;border-radius:0 6px 6px 0;background:transparent;color:#525252}
    .workspace-shell .condition-input-screen .heat-exchanger-custom-control{grid-template-columns:minmax(0,1fr) 38px}
    .workspace-shell .condition-input-screen :is(.heat-exchanger-custom-control,.fan-count-custom-control) > button{width:38px;min-width:38px;height:40px;min-height:40px}
    .workspace-shell .condition-input-screen .fan-count-custom-control input{padding-inline:6px}
    .workspace-shell .condition-input-screen .fan-detail-toggle{min-height:36px;justify-self:start;padding:0 11px;display:inline-flex;align-items:center;justify-content:center;gap:6px;border:1px solid var(--line-strong);border-radius:8px;background:var(--paper);color:var(--ink);font-size:14px;font-weight:500;line-height:1.2}
    .workspace-shell .condition-input-screen .fan-detail-toggle:hover{border-color:#BFC1C3;background:var(--soft)}
    .workspace-shell .condition-input-screen .fan-detail-toggle[aria-expanded="true"]{border-color:#BFC1C3;background:#F7F7F7}
    .workspace-shell .condition-input-screen .fan-detail-toggle svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:2;transition:transform .16s ease}
    .workspace-shell .condition-input-screen .fan-detail-toggle[aria-expanded="true"] svg{transform:rotate(180deg)}
    .workspace-shell .condition-input-screen .fan-detail{margin-top:6px;padding:16px;border:1px solid var(--ui-border);border-radius:var(--ui-radius-panel);background:var(--ui-surface-subtle);box-shadow:none}
    .workspace-shell .condition-input-screen .fan-detail-title{margin:0 0 12px;padding:0;border:0;color:var(--ink);font-size:15px;font-weight:600;line-height:1.55}
    .workspace-shell .condition-input-screen .fan-input-set{padding:12px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}
    .workspace-shell .condition-input-screen .fan-input-order{width:24px;height:24px;align-self:center;display:grid;place-items:center;border:1px solid var(--line);border-radius:8px;background:var(--soft);color:#55585B;font-size:11px;font-weight:500;line-height:1.2}
    .workspace-shell .condition-input-screen .condition-row-actions{min-height:40px;align-items:center}
    .workspace-shell .stage-static-screen[data-screen="SCREEN-05"] > .screen-scroll-content > #section-case{margin:0;border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}
    .workspace-shell .stage-static-screen[data-screen="SCREEN-05"] > .screen-scroll-content > #section-case > .section-head{min-height:0;padding:0 0 13px;border-bottom:0;background:transparent}
    .workspace-shell .stage-static-screen[data-screen="SCREEN-05"] > .screen-scroll-content > #section-case > .section-body{padding:0;border-top:0}
    .workspace-shell .stage-static-screen[data-screen="SCREEN-05"] > .screen-scroll-content > #section-case > .section-head h3{color:var(--ink)}
    .workspace-shell .case-matrix-wrap{border-radius:7px}
    .workspace-shell .case-matrix-grid{min-width:900px;width:100%;table-layout:fixed}
    .workspace-shell .case-matrix-grid th{font-size:13px;font-weight:500;line-height:1.45}
    .workspace-shell .case-matrix-grid .case-col-case_no{width:5%}
    .workspace-shell .case-matrix-grid .case-col-geometry_id{width:17%}
    .workspace-shell .case-matrix-grid .case-col-fan{width:16%}
    .workspace-shell .case-matrix-grid .case-col-heat_exchanger{width:24%}
    .workspace-shell .case-matrix-grid .case-col-space_environment{width:16%}
    .workspace-shell .case-matrix-grid .case-col-supply_air{width:16%}
    .workspace-shell .case-matrix-grid .case-col-remove{width:6%}
    .workspace-shell .case-matrix-grid th,
    .workspace-shell .case-matrix-grid td{border-right:1px solid var(--line)}
    .workspace-shell .case-matrix-grid th:last-child,
    .workspace-shell .case-matrix-grid td:last-child{border-right:0}
    .workspace-shell .case-matrix-grid tbody td{height:62px;padding:6px 8px;vertical-align:top}
    .workspace-shell .stage-static-screen[data-screen="SCREEN-05"] #section-case .matrix-wrap tbody td.case-number,
    .workspace-shell .stage-static-screen[data-screen="SCREEN-05"] #section-case .matrix-wrap tbody td.case-remove-cell{vertical-align:middle}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] > .screen-scroll-content > #section-preview{margin-bottom:var(--request-workspace-card-section-gap);border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] > .screen-scroll-content > #section-preview > .section-head{min-height:0;padding:0 0 13px;border-bottom:0;background:transparent}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] > .screen-scroll-content > #section-preview > .section-body{padding:0;border-top:0}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] > .screen-scroll-content > #section-preview > .section-head h3{color:var(--ink)}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-doc{display:block}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-section{padding:0;border:0;border-radius:0;background:transparent;box-shadow:none}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-section + .preview-section{margin-top:24px;padding-top:24px;border-top:1px solid var(--ui-border-subtle)}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-section h4{margin:0 0 13px;color:var(--ink);font-size:16px;font-weight:600;line-height:1.45}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-kv-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 24px}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-kv{grid-template-columns:150px minmax(0,1fr);gap:10px;padding:0;border-top:0;font-size:14px;font-weight:400;line-height:1.45}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-kv > span:first-child{color:#45484B;font-size:13px;font-weight:500;line-height:1.45}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-kv > span:last-child{color:var(--ink);font-size:14px;font-weight:400;line-height:1.45}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-review-narrative{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:18px;padding-top:18px;border-top:1px solid var(--ui-border-subtle)}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-review-narrative .preview-kv{display:block}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-review-narrative .preview-kv > span:first-child{display:block}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-review-narrative .preview-kv > span:last-child{display:block;margin-top:6px;line-height:1.55}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-table-wrap{border:1px solid var(--ui-border);border-radius:7px;overflow:auto}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-table th{padding:8px 9px;background:#F7F8FA;text-align:left;font-size:13px;font-weight:500;line-height:1.45}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-table td{padding:8px 9px;font-size:14px;font-weight:400;line-height:1.45}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-product-table{table-layout:fixed}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-product-table :is(th,td){overflow-wrap:anywhere}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-product-role{width:14%}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-product-drawing{width:26%}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-product-change{width:60%}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-specification-table{table-layout:fixed}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-spec-name{width:14%}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] :is(.preview-spec-type,.preview-spec-dimension,.preview-spec-fin){width:22%}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] :is(.preview-spec-rows,.preview-spec-pitch){width:10%}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-table-value{display:inline-flex;align-items:center;gap:4px}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-table.case-matrix-grid th{padding:8px;background:var(--soft)}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-table.case-matrix-grid td{padding:6px 8px}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-condition-block + .preview-condition-block{margin-top:20px;padding-top:20px;border-top:1px solid var(--ui-border-subtle)}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-scope-group + .preview-scope-group{margin-top:24px;padding-top:24px;border-top:1px solid var(--ui-border-subtle)}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-scope-heading{margin:0 0 14px;color:var(--ink);font-size:15px;font-weight:600;line-height:1.45}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-condition-block h5,
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-condition-pair h5{margin:0 0 10px;color:var(--ink);font-size:13px;font-weight:500;line-height:1.45}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-condition-pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:20px;padding-top:20px;border-top:1px solid var(--ui-border-subtle)}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-condition-pair>div:only-child{grid-column:1/-1}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-condition-pair>div+div{padding-left:24px;border-left:1px solid var(--ui-border-subtle)}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-condition-pair .preview-kv-grid{grid-template-columns:1fr}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] :is(.preview-missing-icon,.preview-missing-icon svg){width:14px;height:14px}
    .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-missing-icon{flex:0 0 14px;color:var(--ui-error)}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .case-review-message{display:grid;gap:12px;position:relative;margin-top:12px;padding:16px;border-radius:10px;box-shadow:none;color:var(--ink)}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .case-review-message:empty{display:none}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .case-review-message.error{border:1px solid var(--ui-error);background:var(--ui-error-bg)}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .case-review-message.warning{border:1px solid var(--ui-warning-border);background:var(--ui-warning-bg)}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .coverage-warning-head{display:flex;align-items:flex-start;gap:12px}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .coverage-warning-icon{display:inline-grid;flex:0 0 20px;width:20px;height:20px;place-items:center;color:var(--ui-warning);font-size:18px;line-height:1}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .case-review-message.error .coverage-warning-icon{color:var(--ui-error)}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .coverage-warning-icon svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:2}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .coverage-warning-title{color:var(--ink);font-size:15px;font-weight:600;line-height:1.55}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .coverage-warning-copy{margin:0;color:#55585B;font-size:13px;font-weight:400;line-height:1.55}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .coverage-unused-list{display:grid;gap:6px}
    .workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],.screen-group[data-screen="SCREEN-06"]) .coverage-unused-row{font-size:13px;font-weight:400;line-height:1.55}
    .workspace-shell :is(.request-content-screen,.geometry-screen,.stage-static-screen) > .section > .section-head h3{color:var(--ui-text-primary)}
    .workspace-shell .request-content-screen textarea{min-height:96px;padding:10px 11px;background:var(--paper);font-size:14px;font-weight:400;line-height:1.55;resize:vertical}
    .workspace-content{grid-area:workspace-content;min-width:0;min-height:0;display:grid;grid-template-rows:auto auto;align-content:start;gap:0;overflow:visible}
    .workspace-shell .main{overflow:visible}
    .workspace-shell .request-content-screen{background:transparent}
    .workspace-shell .request-content-screen .analysis-result-guidance-icon{display:none}
    .workspace-shell .screen-map-item[aria-current="page"]{z-index:2}
    @media (max-width:1039px){
      .product-table-row{grid-template-columns:92px minmax(126px,1fr) minmax(220px,1.8fr) 34px}
    }
    /* Desktop workspace fills the available canvas; active screens own their vertical flex layout. */
    @media (min-width:1040px){
      body{display:grid;grid-template-rows:auto minmax(0,1fr);overflow:hidden}
      .layout{
        height:100%;max-height:none;min-height:0;
        width:min(calc(100% - 48px),var(--ui-content-max));padding:10px 0 16px;
        grid-template-columns:minmax(0,1fr) var(--ui-panel-split) var(--ui-agent-width);
        grid-template-areas:"workspace-content panel-resizer agent";
        grid-template-rows:minmax(0,1fr);
        column-gap:0;row-gap:0;
      }
      .panel-resizer{
        position:relative;z-index:6;grid-area:panel-resizer;display:grid;place-items:center;
        justify-self:center;width:14px;min-width:14px;height:100%;margin:0;
        cursor:col-resize;touch-action:none;user-select:none;
      }
      .panel-resizer::before{content:"";width:1px;height:46px;border-radius:999px;background:#d4d5d5;transition:background .15s ease,width .15s ease,height .15s ease}
      .panel-resizer:hover::before,.panel-resizer.is-dragging::before{width:3px;height:72px;background:var(--brand)}
      body.panel-resizing{cursor:col-resize;user-select:none}
      .layout.agent-hidden .panel-resizer{display:none}
      .workspace-content{height:100%;grid-template-rows:56px 10px minmax(0,1fr);row-gap:0;overflow:visible}
      .step-navigation{grid-row:1}
      .workspace-shell .panel.main{grid-row:3}
      .workspace-shell .main{min-height:0;overflow:hidden}
      .workspace-shell .workspace{height:100%;min-height:0;padding:0;overflow:hidden}
      .workspace-tab.active{height:100%;min-height:0}
      .workspace-form{height:100%;min-height:0;display:flex;flex-direction:column}
      .workspace-form > .screen-group:not([hidden]){min-height:100%;display:flex;flex-direction:column}
      .workspace-form > .screen-group[data-screen="SCREEN-01"]:not([hidden]){padding:var(--ui-workspace-padding)}
      .workspace-form > .screen-group[data-screen="SCREEN-02"]:not([hidden]),.workspace-form > .screen-group[data-screen="SCREEN-03"]:not([hidden]),.workspace-form > .screen-group[data-screen="SCREEN-04"]:not([hidden]),.workspace-form > .screen-group[data-screen="SCREEN-05"]:not([hidden]),.workspace-form > .screen-group[data-screen="SCREEN-06"]:not([hidden]){height:100%;min-height:0;display:grid;grid-template-rows:minmax(0,1fr) auto}
      .workspace-form > .screen-group:not([hidden]) > .screen-scroll-content{min-height:0;padding:var(--ui-workspace-padding) var(--ui-workspace-padding) 0;overflow-y:auto;overscroll-behavior:contain}
      .workspace-form > .screen-group:not([hidden]) > .screen-action-bar{flex:0 0 auto;margin:0 var(--ui-workspace-padding) var(--ui-workspace-padding)}
      .chat-log{min-height:0;overflow-y:auto;overscroll-behavior:contain}
      .chat-input{position:relative;z-index:1}
    }
    @media (min-width:1040px) and (max-width:1450px){
      .layout{grid-template-columns:minmax(0,1fr) var(--ui-panel-split) var(--ui-agent-width-compact)}
    }
    /* Engineering UI Design Standard v3.0: common shell/component foundation. */
    .step-navigation{background:transparent}
    .workspace-shell .screen-map{
      min-height:56px;padding:10px 14px;gap:0;border:0;border-radius:0;
      overflow-x:auto;overflow-y:hidden;scrollbar-width:thin;background:transparent;box-shadow:none;
    }
    .workspace-shell .screen-map-item{
      min-height:36px;padding:2px 0;background:transparent;color:var(--ui-text-secondary);
    }
    .workspace-shell .screen-map-item:hover:not([aria-disabled="true"]){background:transparent;color:var(--ui-text-primary)}
    .workspace-shell .screen-map-item[aria-current="page"]{background:transparent;color:var(--ui-text-primary)}
    .workspace-shell .screen-map-number{
      width:32px;height:32px;flex-basis:32px;border-radius:50%;background:var(--ui-step-inactive);
      color:#fff;font-size:13px;font-weight:600;line-height:1;
    }
    .workspace-shell .screen-map-item[data-completed="true"] .screen-map-number{background:var(--ui-step-complete);color:#fff;font-size:16px}
    .workspace-shell .screen-map-item[data-completed="true"] .screen-map-label{color:var(--ui-text-primary)}
    .workspace-shell .screen-map-item[aria-current="page"]:not([data-completed="true"]) .screen-map-number{background:var(--ui-active);color:#fff;font-size:13px}
    .workspace-shell .screen-map-label{font-size:13px;font-weight:500;line-height:1.25;color:var(--ui-text-secondary)}
    .workspace-shell .screen-map-item[aria-current="page"] .screen-map-label{color:var(--ui-text-primary);font-weight:600}
    .msg{max-width:100%;margin-bottom:12px;border-radius:9px;padding:11px 12px;font-size:14px;font-weight:400;line-height:1.65}
    .msg.assistant{border-color:var(--ui-border-subtle);background:var(--ui-surface);box-shadow:none}
    .msg.user{border-color:var(--ui-border-subtle);background:var(--ui-user-bubble)}
    @media (max-width:1180px){
      .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-review-narrative,
      .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-condition-pair{grid-template-columns:1fr}
      .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-condition-pair>div+div{padding-left:0;padding-top:20px;border-left:0;border-top:1px solid var(--ui-border-subtle)}
    }
    @media (max-width:720px){
      .workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-kv-grid{grid-template-columns:1fr}
    }
    @media (max-width:1180px){
      .topbar{
        height:var(--global-header-height);grid-template-columns:auto minmax(220px,1fr);align-items:center;
      }
      .header-request-title{max-width:340px}
    }
    @media (max-width:1039px){
      .header-request-title{max-width:260px}
      .agent-dock{right:16px;bottom:16px;width:min(380px,calc(100vw - 32px));height:min(640px,calc(100vh - 32px))}
    }
    @media (max-width:720px){
      .topbar{height:auto;grid-template-columns:1fr;padding:10px 14px;gap:8px}
      .brand{gap:10px;flex-wrap:wrap}
      .brand-mark{width:36px;height:36px}
      h1{font-size:16px}
      .header-request-summary{width:calc(100% - 46px);margin-left:46px;padding-left:0;border-left:0;gap:9px}
      .header-request-title{max-width:none;flex:1;font-size:13px}
      .header-request-number{font-size:12px}
      .top-actions{justify-content:flex-end}
      .top-actions button{min-height:36px;padding:7px 10px}
      .layout{padding:12px}
      .workspace-shell .screen-map{grid-template-columns:repeat(6,max-content);gap:18px;padding:8px 12px;overflow-x:auto;overscroll-behavior-x:contain;scrollbar-width:thin}
      .workspace-shell .screen-map-item{min-height:36px}
      .prep-summary-item{grid-template-columns:1fr;gap:6px}
      .prep-summary-actions{grid-column:1;margin-left:0}
    }

  </style>
</head>
<body>
  <header class="topbar" data-shell="GlobalHeader">
    <div class="brand">
      <div class="brand-mark">CAE</div>
      <div class="portal-heading">
        <h1>해석 의뢰 Agent</h1>
        <div class="subtitle">__APP_VERSION__</div>
      </div>
      <div class="header-request-summary" aria-label="현재 의뢰 정보">
        <h2 class="header-request-title" id="heroTitle">해석 의뢰를 시작해 주세요.</h2>
        <p class="header-request-number" id="requestNoDisplay">-</p>
        <button class="ghost header-request-preview" id="requestPreviewBtn" type="button" aria-haspopup="dialog" aria-controls="requestPreviewModal">의뢰서 미리보기</button>
      </div>
    </div>
    <div class="top-actions" aria-label="request actions">
      <button class="ghost" id="agentOpenBtn" type="button" aria-controls="agentDock" aria-expanded="false" hidden>Agent 열기</button>
      <label class="rag-toggle" hidden aria-hidden="true"><input type="checkbox" id="ragToggle" /> RAG</label>
      <button class="primary" id="newRequestBtn" type="button">새 의뢰 시작</button>
    </div>
  </header>

  <main class="layout">
    <div class="workspace-shell" data-shell="MainWorkspace">
      <div class="workspace-content">
      <nav class="step-navigation" data-shell="StepNavigation" aria-label="6개 화면군">
        <div class="screen-map" aria-label="화면 순서">
          <span class="screen-map-item" data-screen="SCREEN-01" data-step-number="01"><span class="screen-map-number">01</span><span class="screen-map-label"><span>의뢰 대상·시작</span></span></span>
          <span class="screen-map-item" data-screen="SCREEN-02" data-step-number="02"><span class="screen-map-number">02</span><span class="screen-map-label"><span class="screen-map-lock" aria-hidden="true"><svg viewBox="0 0 16 16"><rect x="3" y="7" width="10" height="7" rx="1.5"></rect><path d="M5 7V5a3 3 0 0 1 6 0v2"></path></svg></span><span>요청 내용</span></span></span>
          <span class="screen-map-item" data-screen="SCREEN-03" data-step-number="03"><span class="screen-map-number">03</span><span class="screen-map-label"><span class="screen-map-lock" aria-hidden="true"><svg viewBox="0 0 16 16"><rect x="3" y="7" width="10" height="7" rx="1.5"></rect><path d="M5 7V5a3 3 0 0 1 6 0v2"></path></svg></span><span>해석 제품</span></span></span>
          <span class="screen-map-item" data-screen="SCREEN-04" data-step-number="04"><span class="screen-map-number">04</span><span class="screen-map-label"><span class="screen-map-lock" aria-hidden="true"><svg viewBox="0 0 16 16"><rect x="3" y="7" width="10" height="7" rx="1.5"></rect><path d="M5 7V5a3 3 0 0 1 6 0v2"></path></svg></span><span>해석 조건</span></span></span>
          <span class="screen-map-item" data-screen="SCREEN-05" data-step-number="05"><span class="screen-map-number">05</span><span class="screen-map-label"><span class="screen-map-lock" aria-hidden="true"><svg viewBox="0 0 16 16"><rect x="3" y="7" width="10" height="7" rx="1.5"></rect><path d="M5 7V5a3 3 0 0 1 6 0v2"></path></svg></span><span>Case Matrix</span></span></span>
          <span class="screen-map-item" data-screen="SCREEN-06" data-step-number="06"><span class="screen-map-number">06</span><span class="screen-map-label"><span>최종 검토</span></span></span>
        </div>
        <div class="screen-navigation-status" id="screenNavigationStatus" role="status" aria-live="polite"></div>
      </nav>

    <section class="panel main" data-shell="MainWorkspaceContent">
      <div class="workspace">
        <div class="workspace-tab active" id="tab-write">
          <div class="workspace-form" id="formView">
          <section class="screen-group" data-screen="SCREEN-01" aria-labelledby="screen01Heading">
          <h2 class="screen-heading" id="screen01Heading"><span class="screen-heading-code">01</span> <span>의뢰 대상·시작</span></h2>
          <p class="screen-description">해석 대상 제품과 수행할 해석유형을 선택합니다.</p>
          <section class="request-prep-card" id="requestPrepCard">
            <div class="prep-head">
              <div class="prep-actions"><button class="ghost" id="contextChangeBtn" type="button" hidden>의뢰대상 변경</button><button class="primary" id="nextRequestContentBtn" type="button" data-screen-action="SCREEN-02" hidden>다음: 요청 내용</button></div>
            </div>
            <div class="prep-body">
              <div class="prep-flow active" id="quickPrepFlow">
                <div class="prep-quick-groups">
                  <section class="prep-quick-group" aria-labelledby="productClassificationHeading">
                    <h4 class="prep-quick-group-title" id="productClassificationHeading">제품 분류</h4>
                    <div class="prep-quick-grid">
                      <label>Division<select id="quickDivisionSelect"></select></label>
                      <label>Product Line-up<select id="quickProductLineupSelect"></select></label>
                      <label>Platform<select id="quickPlatformSelect"></select></label>
                      <label>Chassis<select id="quickChassisSelect"></select></label>
                    </div>
                  </section>
                  <section class="prep-quick-group prep-quick-group-analysis" aria-labelledby="analysisSettingHeading">
                    <h4 class="prep-quick-group-title" id="analysisSettingHeading">해석 설정</h4>
                    <div class="prep-analysis-grid">
                      <label>해석유형<select id="quickAnalysisTypeSelect"></select></label>
                      <div class="analysis-type-detail" id="analysisTypeDetail" aria-live="polite">
                        <p class="analysis-type-detail-eyebrow">선택한 해석유형</p>
                        <p class="analysis-type-detail-description">해석유형을 선택하면 해당 해석의 목적과 적합한 활용 사례를 확인할 수 있습니다.</p>
                      </div>
                      <div class="analysis-scope-field" id="analysisScopeField" hidden>
                        <span class="analysis-scope-label">해석 범위</span>
                        <div class="direct-choice" role="group" aria-label="해석 범위">
                          <button type="button" data-analysis-scope="indoor" aria-pressed="false">실내측</button>
                          <button type="button" data-analysis-scope="outdoor" aria-pressed="false">실외측</button>
                          <button type="button" data-analysis-scope="both" aria-pressed="false">실내·실외 모두</button>
                        </div>
                      </div>
                    </div>
                  </section>
                </div>
              </div>
              <div class="prep-start-actions"><button class="primary" id="prepStartBtn" type="button">의뢰서 작성 시작</button></div>
            </div>
          </section>

          <section class="context-chip-bar" id="contextChipBar" hidden>
            <div>
              <div class="context-chip-list" id="contextChipList"></div>
              <div class="context-chip-copy">이 조합 기준으로 입력항목이 준비되었습니다.</div>
            </div>
          </section>

          </section>

          <section class="screen-group request-content-screen" data-screen="SCREEN-02" aria-labelledby="screen02Heading">
          <div class="screen-scroll-content">
          <h2 class="screen-heading" id="screen02Heading"><span class="screen-heading-code">02</span> <span>요청 내용</span></h2>
          <p class="screen-description">의뢰 정보와 해석 요청 내용을 입력합니다.</p>
          <section class="section open" id="section-basic" data-section="basic_info">
            <div class="section-head">
              <div class="section-title"><h3>의뢰자 정보</h3></div>
              <div class="section-meta" id="meta-basic_info" hidden aria-hidden="true"></div>
            </div>
            <div class="section-body">
              <div class="grid request-basic-grid">
                <label>사업부<select data-dropdown-path="basic_info.division"></select><span class="prep-custom-control dropdown-custom-control" data-dropdown-custom-path="basic_info.division" hidden><input class="custom-input" data-path="basic_info.division" aria-label="사업부 직접 입력" /><button type="button" data-dropdown-restore-path="basic_info.division" title="사업부 드롭다운으로 돌아가기" aria-label="사업부 드롭다운으로 돌아가기">↩</button></span></label>
                <label>부서<input data-path="basic_info.department" placeholder="부서를 입력하세요" /></label>
                <label>요청자<input data-path="basic_info.requester_name" placeholder="성함을 입력하세요" /></label>
                <label>직급<select data-dropdown-path="basic_info.requester_role"></select><span class="prep-custom-control dropdown-custom-control" data-dropdown-custom-path="basic_info.requester_role" hidden><input class="custom-input" data-path="basic_info.requester_role" aria-label="직급 직접 입력" /><button type="button" data-dropdown-restore-path="basic_info.requester_role" title="직급 드롭다운으로 돌아가기" aria-label="직급 드롭다운으로 돌아가기">↩</button></span></label>
              </div>
            </div>
          </section>

          <section class="section open" id="section-request-basic">
            <div class="section-head">
              <div class="section-title"><h3>의뢰 기본 정보</h3></div>
            </div>
            <div class="section-body">
              <div class="grid request-basic-grid">
                <label class="request-type-field">의뢰 유형<select data-dropdown-path="analysis_overview.request_type"></select><span class="prep-custom-control dropdown-custom-control" data-dropdown-custom-path="analysis_overview.request_type" hidden><input class="custom-input" data-path="analysis_overview.request_type" aria-label="의뢰 유형 직접 입력" placeholder="의뢰 유형을 직접 입력해 주세요." /><button type="button" data-dropdown-restore-path="analysis_overview.request_type" title="의뢰 유형 목록으로 돌아가기" aria-label="의뢰 유형 목록으로 돌아가기">↩</button></span></label>
                <div class="undecided-field request-project-field" id="pmsProjectField">
                  <label for="projectNameInput">프로젝트명(PMS)</label>
                  <div class="pms-combobox" data-pms-combobox>
                    <input id="projectNameInput" data-path="analysis_overview.project_name" role="combobox" aria-autocomplete="list" aria-haspopup="listbox" aria-controls="projectNameMenu" aria-expanded="false" autocomplete="off" />
                    <button class="undecided-combobox-toggle" type="button" data-pms-toggle aria-label="PMS 프로젝트 검색" aria-controls="projectNameMenu" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 9 5 5 5-5"></path></svg></button>
                    <div class="pms-combobox-menu" id="projectNameMenu" data-pms-menu role="listbox" aria-label="PMS 프로젝트 검색 결과" hidden></div>
                  </div>
                  <p class="pms-project-helper" id="pmsProjectHelper" hidden></p>
                </div>
                <label class="request-basic-row2-start">개발 등급<select data-dropdown-path="analysis_overview.development_grade"></select><span class="prep-custom-control dropdown-custom-control" data-dropdown-custom-path="analysis_overview.development_grade" hidden><input class="custom-input" data-path="analysis_overview.development_grade" aria-label="개발 등급 직접 입력" /><button type="button" data-dropdown-restore-path="analysis_overview.development_grade" title="개발 등급 드롭다운으로 돌아가기" aria-label="개발 등급 드롭다운으로 돌아가기">↩</button></span></label>
                <label>NPI 단계<select data-dropdown-path="analysis_overview.npi_stage"></select><span class="prep-custom-control dropdown-custom-control" data-dropdown-custom-path="analysis_overview.npi_stage" hidden><input class="custom-input" data-path="analysis_overview.npi_stage" aria-label="NPI 단계 직접 입력" /><button type="button" data-dropdown-restore-path="analysis_overview.npi_stage" title="NPI 단계 드롭다운으로 돌아가기" aria-label="NPI 단계 드롭다운으로 돌아가기">↩</button></span></label>
                <div class="undecided-field request-model-field">
                  <label for="modelSuffixInput">모델명(Model Suffix)</label>
                  <div class="undecided-combobox" data-undecided-combobox>
                    <input id="modelSuffixInput" data-path="analysis_overview.model_suffix" data-undecided-input role="combobox" aria-autocomplete="none" aria-haspopup="listbox" aria-controls="modelSuffixMenu" aria-expanded="false" autocomplete="off" />
                    <button class="undecided-combobox-toggle" type="button" data-undecided-toggle aria-label="모델명 입력 방식 선택" aria-controls="modelSuffixMenu" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 9 5 5 5-5"></path></svg></button>
                    <div class="undecided-combobox-menu" id="modelSuffixMenu" data-undecided-menu role="listbox" aria-label="모델명 입력 방식" hidden>
                      <button class="undecided-combobox-option" type="button" role="option" data-undecided-mode="custom" aria-selected="true">직접 입력</button>
                      <button class="undecided-combobox-option" type="button" role="option" data-undecided-mode="undecided" aria-selected="false">미정</button>
                    </div>
                  </div>
                </div>
                <label>희망 완료일<input data-path="analysis_overview.desired_completion_date" type="date" /></label>
              </div>
            </div>
          </section>

          <div class="gate" id="analysisGate">
            <strong>해석유형을 먼저 선택해 주세요.</strong>
            <p class="subtitle">제품군과 검토 목적을 먼저 선택하면 필요한 입력 항목을 채워 주세요.</p>
          </div>

          <section class="section open" id="section-overview" data-section="analysis_overview">
            <div class="section-head">
              <div class="section-title"><h3>해석 요청 내용</h3></div>
              <div class="section-meta" id="meta-analysis_overview" hidden aria-hidden="true"></div>
            </div>
            <div class="section-body">
              <div class="request-detail-grid">
                <label>해석을 요청하게 된 배경<textarea data-path="analysis_overview.request_description" rows="2" placeholder="해석을 요청하게 된 배경을 작성해 주세요."></textarea></label>
                <label>해석으로 확인하고 싶은 내용<textarea data-path="analysis_overview.additional_result_request" rows="2" placeholder="해석으로 확인하고 싶은 내용을 작성해 주세요."></textarea></label>
              </div>
            </div>
          </section>
          </div>
          <div class="screen-action-bar" aria-label="요청 내용 단계 이동">
            <button class="ghost" type="button" data-screen-action="SCREEN-01">이전: 의뢰 대상·시작</button>
            <button class="primary" type="button" data-screen-action="SCREEN-03">다음: 해석 제품</button>
          </div>
          </section>

          <section class="screen-group geometry-screen" data-screen="SCREEN-03" aria-labelledby="screen03Heading">
          <div class="screen-scroll-content">
          <h2 class="screen-heading" id="screen03Heading"><span>해석 제품</span></h2>
          <p class="screen-description">해석 대상 제품의 도면번호와 비교 제품의 Base 대비 차이를 입력합니다.</p>
          <section class="section open" id="section-geometry" data-section="geometry">
            <div class="section-head">
              <div class="section-title"><h3>총 조립 형상</h3></div>
              <div class="section-meta" id="meta-geometry"></div>
            </div>
            <div class="section-body">
              <div class="geometry-policy-guidance"><span class="prep-info-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"></circle><path d="M12 11v6"></path><path d="M12 7.5h.01"></path></svg></span><div class="geometry-policy-copy"><strong class="geometry-policy-heading">해석은 입력된 총 조립도 CAD 형상을 기준으로 진행합니다.</strong><p class="geometry-policy-body">형상 변경·조립 변경 등은 CAD에 먼저 반영한 뒤, 변경된 도면번호로 의뢰해 주세요.</p></div></div>
              <div class="product-table" aria-label="해석 대상 제품 입력">
                <div class="product-table-row product-table-head" aria-hidden="true"><span class="field-label" aria-hidden="true"></span><span class="field-label">총조립도 도면번호 (NPDM MCAD)</span><span class="field-label">Base 대비 변경점</span><span class="product-action-heading" aria-hidden="true"></span></div>
                <div class="row-list" id="productRows"></div>
              </div>
              <div class="geometry-drawing-warning case-review-message error" id="geometryDrawingDuplicateWarning" aria-live="polite"></div>
              <div class="geometry-cad-warning case-review-message warning" id="geometryCadWarning" aria-live="polite"></div>
            </div>
          </section>
          </div>
          <div class="screen-action-bar" aria-label="해석 제품 단계 이동">
            <button class="ghost" type="button" data-screen-action="SCREEN-02">이전: 요청 내용</button>
            <button class="primary" type="button" data-screen-action="SCREEN-04">다음: 해석 조건</button>
          </div>
          </section>

          <section class="screen-group stage-static-screen condition-input-screen" data-screen="SCREEN-04" aria-labelledby="screen04Heading">
          <div class="screen-scroll-content">
          <h2 class="screen-heading" id="screen04Heading"><span>해석 조건</span></h2>
          <p class="screen-description">각 해석 조건의 첫 번째 조건은 <strong>Base 조건</strong>이며, 우측의 <strong>추가(+)</strong> 버튼으로 추가한 조건은 <strong>비교 조건</strong>으로 사용됩니다.</p>
          <section class="section open" id="section-conditions" data-section="conditions">
            <div class="section-body"><div id="conditionScopeTabs"></div><div id="conditionFields"></div><div class="condition-duplicate-warning case-review-message error" id="conditionDuplicateWarning" aria-live="polite"></div></div>
          </section>
          </div>
          <div class="screen-action-bar" aria-label="해석 조건 단계 이동">
            <button class="ghost" type="button" data-screen-action="SCREEN-03">이전: 해석 제품</button>
            <button class="primary" type="button" data-screen-action="SCREEN-05">다음: Case Matrix</button>
          </div>
          </section>

          <section class="screen-group stage-static-screen" data-screen="SCREEN-05" aria-labelledby="screen05Heading">
          <div class="screen-scroll-content">
          <h2 class="screen-heading" id="screen05Heading"><span>Case Matrix</span></h2>
          <p class="screen-description">해석 제품과 해석 조건의 조합을 Case별로 확인하고 구성합니다.</p>
          <section class="section open" id="section-case" data-section="case_matrix">
            <div class="section-head">
              <div class="section-title"><h3>Case 구성</h3></div>
            </div>
            <div class="section-body">
              <div id="caseScopeTabs"></div>
              <div id="caseCommon"></div>
              <div id="caseMatrix"></div>
              <div class="case-duplicate-warning case-review-message error" id="caseDuplicateWarning" aria-live="polite"></div>
              <div class="case-coverage-status case-review-message error" id="caseCoverageStatus" aria-live="polite"></div>
            </div>
          </section>
          </div>
          <div class="screen-action-bar" aria-label="Case Matrix 단계 이동">
            <button class="ghost" type="button" data-screen-action="SCREEN-04">이전: 해석 조건</button>
            <button class="primary" id="caseConfirmNextBtn" type="button" data-action="confirm-case-configuration">다음: 최종 검토</button>
          </div>
          </section>

          </div>
        </div>
        <div class="workspace-tab" id="tab-preview" hidden aria-hidden="true">
          <div class="workspace-form">
            <div class="screen-group" data-screen="SCREEN-06" aria-labelledby="screen06Heading">
              <div class="screen-scroll-content">
              <h2 class="screen-heading" id="screen06Heading"><span>최종 검토</span></h2>
              <p class="screen-description">제출하기 전에 작성한 해석 의뢰 내용을 최종 확인합니다.</p>
              <section class="section open" id="section-preview" data-section="preview">
                <div class="section-head">
                  <div class="section-title"><h3>의뢰서 미리보기</h3></div>
                  <div class="section-meta" id="meta-preview"></div>
                </div>
                <div class="section-body">
                  <div id="documentPreviewPanel"></div>
                  <div id="previewCoverageWarning"></div>
                  <div class="preview-actions">
                    <span class="word-export-required-warning" id="wordExportRequiredWarning" role="status" hidden><span class="preview-missing-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3 2.8 20h18.4L12 3Z"></path><path d="M12 9v5"></path><circle cx="12" cy="17" r=".7"></circle></svg></span><span>필수 입력 누락</span></span>
                    <button class="primary workflow-action-button" id="wordExportSlotBtn" type="button">의뢰서 생성(Word)</button>
                  </div>
                </div>
              </section>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
      </div>
    </div>

    <div class="panel-resizer" id="panelResizer" role="separator" aria-label="입력 폼과 Agent 패널 너비 조절" aria-orientation="vertical" aria-valuemin="1" aria-valuenow="2.29" aria-valuemax="3"></div>
    <aside class="panel chat agent-dock" id="agentDock" data-shell="AgentDock" aria-labelledby="agentDockHeading">
      <div class="chat-head">
        <div id="agentDockHeading" class="title-with-icon" tabindex="-1"><span class="title-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 19a7 7 0 0 1 14 0"></path><circle cx="12" cy="8" r="4"></circle><path d="M4 12v3M20 12v3"></path></svg></span><strong class="stage-assist-title">Agent</strong></div>
        <div class="chat-head-actions">
          <button class="ghost" id="agentClearBtn" type="button" aria-controls="chatLog" aria-label="대화창 비우기" title="대화창 비우기"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6v5h-5"></path><path d="M19 11a7.5 7.5 0 1 0 .2 4"></path></svg></button>
          <button class="ghost" id="agentHideBtn" type="button" aria-controls="agentDock" aria-expanded="true" aria-label="Agent 숨기기" title="Agent 숨기기"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"></rect><path d="M15 4v16"></path><path d="m11 9-3 3 3 3"></path></svg></button>
        </div>
      </div>
      <div class="chat-log" id="chatLog">
        <div class="msg assistant">먼저 해석 대상 제품을 정해 주세요. 이 의뢰 대상·시작에서 사업부 → 제품 분류 → 해석유형을 선택한 다음, 의뢰서 작성 시작 버튼을 누르면 작성을 시작할 수 있습니다. 해석유형을 모르겠다면 해석유형 선택 가이드를 확인하고 Agent에게 물어봐 주세요.</div>
      </div>
      <div class="chat-input">
        <div class="chat-row">
          <textarea id="chatInput" placeholder="예: 에어컨에서 소음이 발생하는 원인을 확인하고 싶어요."></textarea>
          <button class="primary" id="sendBtn" type="button">전송</button>
        </div>
      </div>
    </aside>
  </main>


  <div class="submit-modal" id="contextChangeModal" hidden role="dialog" aria-modal="true" aria-labelledby="contextChangeTitle">
    <div class="submit-dialog">
      <strong id="contextChangeTitle">조합을 변경할까요?</strong>
      <p class="subtitle">제품군, platform, 해석유형을 변경하면 현재 입력한 해석조건 값이 새 입력항목과 맞지 않을 수 있습니다.<br>변경하시겠습니까?</p>
      <div class="context-change-actions">
        <button class="primary" id="contextChangeContinue" type="button">변경 계속</button>
        <button class="ghost" id="contextChangeCancel" type="button">취소</button>
      </div>
    </div>
  </div>

  <div class="submit-modal" id="fanLimitModal" hidden role="dialog" aria-modal="true" aria-labelledby="fanLimitTitle">
    <div class="submit-dialog">
      <strong id="fanLimitTitle">Fan 개수를 확인해 주세요.</strong>
      <p class="subtitle">한 운전 조건에는 Fan을 최대 10개까지 설정할 수 있습니다.<br>10개를 초과하는 조건이 필요한 경우 관리자에게 문의해 주세요.<br><br>홍승도 책임연구원<br><a href="mailto:sedo.hong@lge.com">sedo.hong@lge.com</a></p>
      <div class="context-change-actions">
        <button class="primary" id="fanLimitConfirm" type="button">확인</button>
      </div>
    </div>
  </div>

  <div class="submit-modal request-preview-modal" id="requestPreviewModal" hidden role="dialog" aria-modal="true" aria-labelledby="requestPreviewTitle">
    <div class="submit-dialog request-preview-dialog">
      <div class="request-preview-dialog-head">
        <strong id="requestPreviewTitle">의뢰서 미리보기</strong>
        <button class="ghost" id="requestPreviewCloseBtn" type="button">닫기</button>
      </div>
      <div class="request-preview-dialog-body">
        <div id="requestPreviewModalPanel"></div>
        <div id="requestPreviewModalCoverageWarning"></div>
      </div>
    </div>
  </div>

  <script>
    const $ = (id) => document.getElementById(id);
    const basicKeys = ["division","department","requester_name","requester_role"];
    const overviewInputKeys = ["request_type","project_name","development_grade","npi_stage","model_suffix","desired_completion_date","request_description","additional_result_request"];
    const decisionUseCatalog = {
      problem_analysis:"문제·현상 분석",
      design_review:"설계·변경 검토",
      performance_validation:"성능·시험 검증",
      other:"기타",
      undecided:"아직 결정하지 못함",
    };
    const decisionUseLegacyCodes = {
      design_selection:"design_review", change_applicability:"design_review", root_cause:"problem_analysis",
      improvement_direction:"problem_analysis", phenomenon_review:"problem_analysis",
      performance_requirement:"performance_validation", other:"other", undecided:"undecided",
    };
    const prepAnalysisTypes = ["풍량","기류 패턴","이슬맺힘","열교환기 유속 프로파일","기류도달거리","PDB","실사용 해석","집진해석(먼지거동)","PCB발열","다상유동"];
    const disabledAnalysisTypes = ["기류도달거리","PDB","실사용 해석","집진해석(먼지거동)","PCB발열","다상유동"];
    const disabledAnalysisTypeLockPrefix = "\u{1F512}\uFE0E ";
    const analysisTypeDetails = {
      "풍량": {
        description:"제품의 흡입·토출 또는 관심 위치에서의 풍량을 확인하는 해석입니다.\n형상 또는 운전조건 변경에 따른 풍량 변화와 제품 간 차이를 비교할 수 있습니다.",
        suitable:["제품의 풍량이 충분한지 확인하려는 경우","설계 변경 전후의 풍량 차이를 비교하려는 경우","풍량 부족 원인을 검토하려는 경우"],
      },
      "기류 패턴": {
        description:"제품 내부 또는 외부에서 공기가 어떤 방향과 형태로 흐르는지 확인하는 해석입니다.",
        suitable:["바람이 어느 방향으로 흐르는지 확인하려는 경우","특정 방향으로 기류가 편중되는 원인을 확인하려는 경우","형상 변경 전후의 유동 분포를 비교하려는 경우"],
      },
      "이슬맺힘": {
        description:"제품에서 이슬맺힘이 발생할 가능성이 있는 위치와 관련 원인을 검토하는 해석입니다.",
        suitable:["제품 표면이나 특정 부위에 이슬맺힘이 발생하는 경우","이슬맺힘 발생 원인을 검토하려는 경우","개선안 적용 시 이슬맺힘이 줄어드는지 비교하려는 경우"],
      },
      "열교환기 유속 프로파일": {
        description:"열교환기를 통과하는 공기의 유속 분포를 확인하는 해석입니다.",
        suitable:["열교환기 전면의 유속이 균일한지 확인하려는 경우","열교환기 특정 영역의 유속이 낮거나 높은지 확인하려는 경우","설계 변경에 따른 열교환기 유속 분포를 비교하려는 경우"],
      },
    };
    const defaultDivisions = ["SAC","RAC","Air Care","Chiller"];
    const emptyProductHierarchy = {
      taxonomy_version: "",
      divisions: defaultDivisions.map(label => ({code:label === "Air Care" ? "AIR_CARE" : label.toUpperCase(), label})),
      hierarchy: {},
      paths: [],
    };
    const dropdownOptions = {
      "basic_info.division": ["SAC","RAC","Aircare","Chiller","연구소","직접 입력"],
      "basic_info.requester_role": ["책임연구원","선임연구원","연구원","직접 입력"],
      "analysis_overview.request_type": ["개발 프로젝트","품질 개선","필드 이슈","선행 검토","기타(직접 입력)"],
      "analysis_overview.development_grade": ["A","B","B_Mi","Ca","Ca_Mi","Ca_SW","Cb","Cc","Csw","D","ECM_A","ECM_Cb","HW","JDM","JDM_Ca","JDM_Cb","JDM_D","JDM_파급","ND_Cb","ND_D","ODM_CSKD","ODM_ND","ODM_OTS","ODM_파급","OTS_파생","T1","T2","T3","선행","미정","직접 입력"],
      "analysis_overview.npi_stage": ["CP","DV","MP","MQ","PV","Pre MP","Pre-MP","미정","직접 입력"],
      "conditions.material_type": ["","Air","직접 입력"],
      "conditions.working_fluid": ["air","water"],
      "conditions.outlet_condition": ["pressure outlet"],
    };
    const sectionOrder = [
      ["analysis_overview","해석 요청 내용","section-overview"],
      ["geometry","제품형상","section-geometry"],
      ["conditions","해석조건","section-conditions"],
      ["case_matrix","Case Matrix","section-case"],
    ];
    const screenOrder = [
      {id:"SCREEN-01", headingId:"screen01Heading", tab:"write", requiresContext:false},
      {id:"SCREEN-02", headingId:"screen02Heading", tab:"write", requiresContext:true},
      {id:"SCREEN-03", headingId:"screen03Heading", tab:"write", requiresContext:true},
      {id:"SCREEN-04", headingId:"screen04Heading", tab:"write", requiresContext:true},
      {id:"SCREEN-05", headingId:"screen05Heading", tab:"write", requiresContext:true},
      {id:"SCREEN-06", headingId:"screen06Heading", tab:"preview", requiresContext:true},
    ];
    const analysisScopeLabels = {indoor:"실내측", outdoor:"실외측", both:"실내·실외 모두"};
    const operationModeOptions = ["실내", "실외", "동시운전"];
    const excludedConditionKeys = new Set(["material_type", "pressure", "vane_or_louver", "filter_state"]);
    let requestState = {};
    let previewStateRevision = 0;
    let previewRefreshTimer = null;
    let schema = {};
    let activeTopTab = "write";
    let activeScreen = "SCREEN-01";
    let wordExportInProgress = false;
    let lastPlannerActiveFieldId = "";
    let agentOpen = true;
    let lastAgentFocus = null;
    let chatFocusRestorePending = false;
    let chatHistory = [];
    let replayingChat = false;
    let productHierarchy = emptyProductHierarchy;
    let heatExchangerCatalog = [];
    const heatExchangerCustomFields = new Set();
    const fanCountCustomCards = new Set();
    let expandedFanCardId = "";
    let requestContextDraft = {};
    let pmsSearchTimer = null;
    let pmsSearchItems = [];
    let pmsActiveIndex = -1;
    let activeConditionScope = "indoor";
    let activeCaseScope = "indoor";
    let outdoorCaseMatrixViewed = false;
    let prepAssistStarted = false;
    const stageAssistConfigs = {
      start: {
        title: "의뢰 시작 도움",
        description: "제품과 확인 목적을 선택하면 필요한 입력항목이 자동으로 준비됩니다.",
        actions: [
          {label:"Division 설명", prompt:"Division이 무엇인지 설명"},
          {label:"제품명으로 Division 확인", prompt:"제품명으로 Division 확인"},
          {label:"처음 사용하는 방법 보기", prompt:"처음 사용하는 방법 보기"},
        ],
      },
      division: {
        title: "Division 선택 도움",
        description: "현재는 해석 대상 제품의 Division을 선택하는 단계입니다.",
        actions: [
          {label:"Division 설명", prompt:"Division이 무엇인지 설명"},
          {label:"제품명으로 Division 확인", prompt:"제품명으로 Division 확인"},
          {label:"잘 모르겠어요", prompt:"Division을 잘 모르겠어요"},
        ],
      },
      product_lineup: {
        title: "Product Line-up 선택 도움",
        description: "선택한 Division에 해당하는 Product Line-up만 표시됩니다.",
        actions: [
          {label:"Product Line-up 설명", prompt:"제품 Product Line-up이 무엇인지 설명"},
          {label:"제품명으로 Product Line-up 확인", prompt:"제품명으로 Product Line-up 확인"},
          {label:"기존 의뢰와 비슷하게 시작", prompt:"기존 의뢰와 비슷하게 시작"},
        ],
      },
      platform: {
        title: "Platform 선택 도움",
        description: "선택한 Product Line-up에 해당하는 Platform만 표시됩니다. RAC와 Air Care는 자동 설정됩니다.",
        actions: [
          {label:"Platform 설명", prompt:"제품 Platform이 무엇인지 설명"},
          {label:"제품명으로 Platform 확인", prompt:"제품명으로 Platform 확인"},
        ],
      },
      chassis: {
        title: "Chassis 선택 도움",
        description: "등록된 Chassis만 선택할 수 있으며 Chassis가 없는 경로는 null로 자동 설정됩니다.",
        actions: [
          {label:"Chassis 설명", prompt:"제품 Chassis가 무엇인지 설명"},
          {label:"제품명으로 Chassis 확인", prompt:"제품명으로 Chassis 확인"},
        ],
      },
      analysis_type: {
        title: "해석유형 선택 도움",
        description: "확인하고 싶은 현상을 기준으로 해석유형을 선택합니다.",
        actions: [
          {label:"현상 설명하고 추천받기", prompt:"현상 설명하고 추천받기"},
          {label:"이슬맺힘이 맞는지 확인", prompt:"이슬맺힘이 맞는지 확인"},
          {label:"풍량 해석과 차이 보기", prompt:"풍량 해석과 차이 보기"},
        ],
      },
      conditions: {
        title: "해석조건 입력 도움",
        description: "현재 조합에 맞는 입력항목만 표시됩니다.",
        actions: [
          {label:"누락 조건 확인", prompt:"누락 조건 확인"},
          {label:"조건 의미 설명", prompt:"조건 의미 설명"},
          {label:"Case Matrix 미리보기", prompt:"Case Matrix 미리보기"},
          {label:"AI가 입력값 점검", prompt:"AI가 입력값을 점검해줘"},
        ],
      },
    };
    const touchedFields = new Set();
    const orchestratorPanelState = {conversationId:"", requestId:"", requestVersion:null, dirty:true, loading:false, caseMatrixActionLoading:false, validationActionLoading:false, previewActionLoading:false, wordExportActionLoading:false, ragGuidanceActionLoading:false, caseMatrixSyncedRequestId:"", caseMatrixSyncedRequestVersion:null, previewRenderedRequestId:"", previewRenderedRequestVersion:null, decisionIds:new Set(), refreshedProposalIds:new Set(), latestApprovedState:null};

    function esc(text){
      return String(text ?? "").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");
    }
    function asObj(value){ return value && typeof value === "object" && !Array.isArray(value) ? value : {}; }
    function asArray(value){ return Array.isArray(value) ? value : []; }
    function fieldValue(field, fallback=""){
      const src = asObj(field);
      if (src.status && src.status !== "provided") return fallback;
      const value = Object.prototype.hasOwnProperty.call(src, "value") ? src.value : fallback;
      return value === null || value === undefined ? fallback : value;
    }
    function statusDisplay(field){
      const src = asObj(field);
      return src.display_value || ({unknown:"모름", none:"없음", skipped:"skip"}[src.status] || "");
    }
    function fieldDisplayValue(field, fallback=""){
      if (field !== null && field !== undefined && typeof field !== "object") {
        const value = String(field);
        return value.trim() ? value : fallback;
      }
      if (asObj(asObj(field).value).primary_code) return decisionUseDisplay(field) || fallback;
      const value = fieldValue(field, "");
      if (String(value ?? "").trim()) return value;
      const display = statusDisplay(field);
      return display || fallback;
    }
    function rowValue(row){
      if (row && typeof row === "object") return asObj(row).status === "provided" ? fieldValue(row) : statusDisplay(row);
      return row ?? "";
    }
    function productField(product, key){ return asObj(product)[key]; }
    function productText(product, key){ return fieldDisplayValue(productField(product, key)); }
    function isProvided(field){ return asObj(field).status === "provided" && String(fieldValue(field,"")).trim() !== ""; }
    function pathInput(section, key){ return document.querySelector(`[data-path="${section}.${key}"]`); }
    function setStatus(text){ $("saveStatus") ? $("saveStatus").textContent = text : null; }
    function notify(text){ pushMessage("assistant", text); }

    function localDateValue(date){
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    }

    function configureDesiredCompletionDateMinimum(){
      const input = pathInput("analysis_overview", "desired_completion_date");
      if (!input) return;
      const now = new Date();
      input.min = localDateValue(new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1));
      input.title = "희망 완료일은 내일부터 선택할 수 있습니다.";
    }

    function serializedDecisionUseValue(rawValue){
      if (typeof rawValue !== "string") return null;
      const legacy = rawValue.trim();
      if (!/^\{[\s\S]*\}$/.test(legacy) || !/(?:['"]?primary_code['"]?|['"]?custom_text['"]?)/.test(legacy)) return null;
      const read = (key) => {
        const match = legacy.match(new RegExp(`['"]?${key}['"]?\\s*:\\s*(?:['"]([^'"]*)['"]|(null|none|undefined))`, "i"));
        return match ? String(match[1] || "").trim() : "";
      };
      return {primary_code:read("primary_code"), custom_text:read("custom_text")};
    }

    function normalizeDecisionUse(field){
      const raw = asObj(field);
      const rawValue = Object.prototype.hasOwnProperty.call(raw, "value") ? raw.value : field;
      const serialized = serializedDecisionUseValue(rawValue);
      const value = serialized || asObj(rawValue);
      let primaryCode = String(value.primary_code || "").trim();
      let customText = String(value.custom_text || "").trim();
      if (!primaryCode && !serialized) {
        const legacy = typeof rawValue === "string" ? rawValue.trim() : "";
        primaryCode = decisionUseLegacyCodes[legacy] || (Object.prototype.hasOwnProperty.call(decisionUseCatalog, legacy) ? legacy : (legacy ? "other" : ""));
        if (primaryCode === "other" && legacy && !decisionUseLegacyCodes[legacy]) customText = legacy;
      }
      if (!Object.prototype.hasOwnProperty.call(decisionUseCatalog, primaryCode)) {
        customText = customText || primaryCode;
        primaryCode = customText ? "other" : "";
      }
      return {primary_code:primaryCode, custom_text:primaryCode === "other" ? customText : ""};
    }

    function decisionUseDisplay(field){
      const value = normalizeDecisionUse(field);
      return value.primary_code === "other" && value.custom_text ? `${decisionUseCatalog.other}: ${value.custom_text}` : (decisionUseCatalog[value.primary_code] || "");
    }

    function selectedDecisionUseCode(){ return $("decisionUseSelect")?.value || ""; }

    function renderDecisionUseAuxiliary(code=selectedDecisionUseCode()){
      const customWrap = $("decisionUseCustomWrap");
      const customInput = $("decisionUseCustom");
      const serializedCustom = code === "other" ? serializedDecisionUseValue(customInput?.value) : null;
      if (customInput && serializedCustom) customInput.value = serializedCustom.custom_text;
      if (customWrap) customWrap.hidden = code !== "other";
    }

    function syncDecisionUseEditor(field){
      const value = normalizeDecisionUse(field);
      if ($("decisionUseSelect")) $("decisionUseSelect").value = value.primary_code;
      if ($("decisionUseCustom")) $("decisionUseCustom").value = value.custom_text;
      renderDecisionUseAuxiliary(value.primary_code);
    }

    function collectDecisionUseField(){
      const previous = asObj(asObj(requestState.analysis_overview).decision_use);
      const primaryCode = selectedDecisionUseCode();
      const customText = $("decisionUseCustom")?.value.trim() || "";
      const validity = !primaryCode || (primaryCode === "other" && !customText) ? "invalid" : (primaryCode === "undecided" ? "unverified" : "valid");
      return {
        value:{primary_code:primaryCode, custom_text:primaryCode === "other" ? customText || null : null},
        display_value:primaryCode === "other" && customText ? `${decisionUseCatalog.other}: ${customText}` : (decisionUseCatalog[primaryCode] || ""),
        status:primaryCode ? "provided" : "missing",
        source:"user",
        validity,
        confirmation_status:previous.confirmation_status || "not_required",
        note:previous.note || "",
      };
    }

    function optionsForPath(path){
      const fromSchema = asArray(asObj(schema.ui_options)[path]);
      return fromSchema.length ? fromSchema : asArray(dropdownOptions[path]);
    }

    function dropdownOptionHtml(options){
      return [`<option value="" disabled hidden>선택</option>`, ...asArray(options).filter(option => option !== "").map(option => {
        if (option === "직접 입력" || String(option).includes("(직접 입력)")) return `<option value="__custom__">${esc(option)}</option>`;
        return `<option value="${esc(option)}">${esc(option)}</option>`;
      })].join("");
    }

    function dropdownOptionHtmlWithSelected(options, selected){
      return [`<option value="" disabled hidden ${selected === "" ? "selected" : ""}>선택</option>`, ...asArray(options).filter(option => option !== "").map(option => {
        const value = option === "직접 입력" || String(option).includes("(직접 입력)") ? "__custom__" : option;
        const label = option;
        return `<option value="${esc(value)}" ${String(value) === String(selected) ? "selected" : ""}>${esc(label)}</option>`;
      })].join("");
    }

    function setupDropdowns(){
      document.querySelectorAll("select[data-dropdown-path]").forEach(select => {
        const path = select.dataset.dropdownPath || "";
        select.innerHTML = dropdownOptionHtml(optionsForPath(path));
      });
    }

    function syncDropdownForPath(path, value){
      const select = document.querySelector(`select[data-dropdown-path="${CSS.escape(path)}"]`);
      const input = document.querySelector(`input[data-path="${CSS.escape(path)}"]`);
      const customControl = document.querySelector(`[data-dropdown-custom-path="${CSS.escape(path)}"]`);
      if (!select || !input) return;
      const text = String(value || "");
      const values = Array.from(select.options).map(option => option.value);
      select.value = values.includes(text) ? text : (text ? "__custom__" : "");
      const customMode = select.value === "__custom__";
      select.hidden = customMode;
      if (customControl) customControl.hidden = !customMode;
      else input.hidden = !customMode;
      input.value = text;
    }

    let activeSelectPicker = null;

    function closeSelectPicker({focusSelect=false}={}){
      const active = activeSelectPicker;
      activeSelectPicker = null;
      active?.menu.remove();
      if (focusSelect) active?.select.focus({preventScroll:true});
    }

    function selectPickerButtons(menu){
      return Array.from(menu.querySelectorAll("button:not(:disabled)"));
    }

    function openSelectPicker(select){
      if (select.disabled || select.multiple) return;
      if (activeSelectPicker?.select === select) { closeSelectPicker({focusSelect:true}); return; }
      closeSelectPicker();
      const menu = document.createElement("div");
      menu.className = "select-picker-menu";
      menu.setAttribute("role", "listbox");
      menu.setAttribute("aria-label", select.getAttribute("aria-label") || select.closest("label")?.childNodes[0]?.textContent?.trim() || "선택");
      Array.from(select.options).forEach(option => {
        if (option.hidden) return;
        const button = document.createElement("button");
        button.type = "button";
        button.className = "select-picker-option";
        button.textContent = option.textContent;
        button.disabled = option.disabled;
        button.setAttribute("role", "option");
        button.setAttribute("aria-selected", String(option.selected));
        button.addEventListener("click", () => {
          select.value = option.value;
          select.dispatchEvent(new Event("input", {bubbles:true}));
          select.dispatchEvent(new Event("change", {bubbles:true}));
          closeSelectPicker({focusSelect:true});
        });
        menu.append(button);
      });
      document.body.append(menu);
      const rect = select.getBoundingClientRect();
      const height = Math.min(menu.scrollHeight, 320);
      const below = window.innerHeight - rect.bottom - 4;
      menu.style.width = `${rect.width}px`;
      menu.style.left = `${Math.max(4, Math.min(rect.left, window.innerWidth - rect.width - 4))}px`;
      menu.style.top = `${below >= height ? rect.bottom + 4 : Math.max(4, rect.top - height - 4)}px`;
      activeSelectPicker = {select, menu};
      const selected = menu.querySelector('[aria-selected="true"]:not(:disabled)');
      window.requestAnimationFrame(() => (selected || selectPickerButtons(menu)[0])?.focus({preventScroll:true}));
      menu.addEventListener("keydown", event => {
        const buttons = selectPickerButtons(menu);
        const index = buttons.indexOf(document.activeElement);
        if (event.key === "Escape") {
          event.preventDefault();
          closeSelectPicker({focusSelect:true});
        } else if (event.key === "ArrowDown" || event.key === "ArrowUp") {
          event.preventDefault();
          const direction = event.key === "ArrowDown" ? 1 : -1;
          buttons[(index + direction + buttons.length) % buttons.length]?.focus({preventScroll:true});
        }
      });
    }

    function handleSelectPickerPointerDown(event){
      const select = event.target.closest?.("select");
      if (select) {
        event.preventDefault();
        openSelectPicker(select);
      } else if (!activeSelectPicker?.menu.contains(event.target)) {
        closeSelectPicker();
      }
    }

    function handleSelectPickerKeyDown(event){
      if (!event.target.matches?.("select") || ![" ", "Enter", "ArrowDown", "ArrowUp"].includes(event.key)) return;
      event.preventDefault();
      openSelectPicker(event.target);
    }

    function handleSelectPickerScroll(event){
      if (event.target !== activeSelectPicker?.menu) closeSelectPicker();
    }

    function contextText(value){
      return String(value ?? "").trim();
    }

    function undecidedComboboxSpecialValue(combobox){
      return contextText(combobox?.dataset.undecidedValue) || "미정";
    }

    function undecidedComboboxMode(combobox){
      return combobox?.querySelector("[data-undecided-input]")?.dataset.undecidedMode === "undecided" ? "undecided" : "custom";
    }

    function setUndecidedActiveOption(combobox, activeOption, {focus=false}={}){
      combobox?.querySelectorAll("[data-undecided-mode]").forEach(option => {
        option.dataset.undecidedActive = String(option === activeOption);
      });
      if (focus) activeOption?.focus({preventScroll:true});
    }

    function setUndecidedComboboxOpen(combobox, open, {focusOption=false}={}){
      const input = combobox?.querySelector("[data-undecided-input]");
      const toggle = combobox?.querySelector("[data-undecided-toggle]");
      const menu = combobox?.querySelector("[data-undecided-menu]");
      if (!input || !toggle || !menu) return;
      if (open) {
        document.querySelectorAll("[data-undecided-combobox]").forEach(other => {
          if (other !== combobox) setUndecidedComboboxOpen(other, false);
        });
      }
      menu.hidden = !open;
      input.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-expanded", String(open));
      if (open && focusOption) {
        const selectedOption = menu.querySelector(`[data-undecided-mode="${undecidedComboboxMode(combobox)}"]`);
        setUndecidedActiveOption(combobox, selectedOption, {focus:true});
      } else if (!open) {
        setUndecidedActiveOption(combobox, null);
      }
    }

    function renderUndecidedComboboxMode(combobox, mode){
      const input = combobox?.querySelector("[data-undecided-input]");
      const selectedMode = mode === "undecided" ? "undecided" : "custom";
      if (!input) return;
      input.dataset.undecidedMode = selectedMode;
      input.readOnly = selectedMode === "undecided";
      const fieldLabel = input.dataset.customPlaceholder || (input.id === "modelSuffixInput" ? "모델명을 입력하세요" : "프로젝트명을 입력하세요");
      input.placeholder = selectedMode === "custom" ? fieldLabel : "";
      combobox.querySelectorAll("[data-undecided-mode]").forEach(option => {
        option.setAttribute("aria-selected", String(option.dataset.undecidedMode === selectedMode));
      });
    }

    function syncUndecidedCombobox(path, value){
      const input = document.querySelector(`[data-undecided-input][data-path="${CSS.escape(path)}"]`);
      const combobox = input?.closest("[data-undecided-combobox]");
      if (!combobox) return;
      renderUndecidedComboboxMode(combobox, contextText(value) === undecidedComboboxSpecialValue(combobox) ? "undecided" : "custom");
      setUndecidedComboboxOpen(combobox, false);
    }

    function isDevelopmentProject(){
      return contextText(fieldDisplayValue(asObj(requestState.analysis_overview).request_type)) === "개발 프로젝트";
    }

    function clearPmsProjectDraft(){
      const overview = {...asObj(requestState.analysis_overview)};
      ["selected_pms_project_id","project_name","pms_project_code","region","development_grade","npi_stage","model_suffix"].forEach(key => { overview[key] = ""; });
      requestState = {...requestState, analysis_overview:overview};
    }

    function setRequestControlDisabled(path, disabled){
      const select = document.querySelector(`select[data-dropdown-path="${CSS.escape(path)}"]`);
      const input = document.querySelector(`input[data-path="${CSS.escape(path)}"]`);
      const customControl = document.querySelector(`[data-dropdown-custom-path="${CSS.escape(path)}"]`);
      if (select) select.disabled = disabled;
      if (input) input.disabled = disabled;
      customControl?.querySelectorAll?.("input, button").forEach(control => { control.disabled = disabled; });
    }

    function syncPmsProjectControl(){
      const field = $("pmsProjectField");
      const input = $("projectNameInput");
      const helper = $("pmsProjectHelper");
      const toggle = document.querySelector("[data-pms-toggle]");
      const combobox = document.querySelector("[data-pms-combobox]");
      const overview = asObj(requestState.analysis_overview);
      const enabled = isDevelopmentProject();
      if (!input || !field) return;
      input.disabled = !enabled;
      input.setAttribute?.("aria-disabled", String(!enabled));
      if (toggle) toggle.disabled = !enabled;
      if (field.dataset) field.dataset.disabled = String(!enabled);
      field.setAttribute?.("aria-disabled", String(!enabled));
      if (combobox) combobox.dataset.disabled = String(!enabled);
      ["development_grade", "npi_stage"].forEach(key => {
        const path = `analysis_overview.${key}`;
        syncDropdownForPath(path, fieldDisplayValue(overview[key]));
        setRequestControlDisabled(path, !enabled);
      });
      const modelInput = pathInput("analysis_overview", "model_suffix");
      if (modelInput) modelInput.value = fieldDisplayValue(overview.model_suffix);
      syncUndecidedCombobox("analysis_overview.model_suffix", fieldDisplayValue(overview.model_suffix));
      if (!enabled) {
        input.value = "";
        helper.hidden = true;
        helper.textContent = "";
        setPmsMenuOpen(false);
        return;
      }
      input.value = fieldDisplayValue(overview.project_name);
      input.placeholder = "프로젝트명 또는 모델명으로 검색";
      const code = fieldDisplayValue(overview.pms_project_code);
      const region = fieldDisplayValue(overview.region);
      helper.hidden = !(code || region);
      helper.textContent = code || region ? `PMS ${code} · ${region}` : "";
    }

    function setPmsMenuOpen(open){
      const combobox = document.querySelector("[data-pms-combobox]");
      const input = $("projectNameInput");
      const toggle = document.querySelector("[data-pms-toggle]");
      const menu = document.querySelector("[data-pms-menu]");
      if (!combobox || !input || !toggle || !menu) return;
      const isOpen = Boolean(open) && !input.disabled && !toggle.disabled;
      menu.hidden = !isOpen;
      input.setAttribute("aria-expanded", String(isOpen));
      toggle.setAttribute("aria-expanded", String(isOpen));
      if (!isOpen) setPmsActiveResult(-1);
    }

    function setPmsActiveResult(index){
      const options = Array.from(document.querySelectorAll("[data-pms-index]"));
      pmsActiveIndex = options.length ? ((index % options.length) + options.length) % options.length : -1;
      options.forEach((option, optionIndex) => {
        const active = optionIndex === pmsActiveIndex;
        option.dataset.pmsActive = String(active);
        option.setAttribute("aria-selected", String(active));
      });
    }

    function renderPmsSearchResults(){
      const menu = document.querySelector("[data-pms-menu]");
      if (!menu) return;
      menu.innerHTML = pmsSearchItems.length
        ? pmsSearchItems.map((item, index) => `<button type="button" class="pms-combobox-option" role="option" data-pms-index="${index}" data-pms-active="false" aria-selected="false"><span>${esc(item.project)}</span><small>${esc(item.grade || "-")} · ${esc(item.event || "-")} · ${esc(item.rep_model || "-")} · ${esc(item.region || "-")}</small></button>`).join("")
        : `<div class="pms-combobox-option"><small>검색 결과가 없습니다.</small></div>`;
      setPmsActiveResult(-1);
    }

    async function searchPmsProjects(query=""){
      if (!isDevelopmentProject()) return;
      const division = contextText(collectRequestContextDraft().division);
      if (!division) { pmsSearchItems = []; renderPmsSearchResults(); setPmsMenuOpen(true); return; }
      const res = await fetch(`/api/pms-projects?division=${encodeURIComponent(division)}&query=${encodeURIComponent(query)}`);
      const data = await res.json();
      pmsSearchItems = asArray(data.projects);
      renderPmsSearchResults();
      setPmsMenuOpen(true);
    }

    async function selectPmsProject(item){
      const data = await postJson("/api/pms-projects/select", {state:collectState(), internal_id:item.internal_id});
      adoptStateFromResponse(data);
      syncEditorFromState();
      setPmsMenuOpen(false);
      touchedFields.add("analysis_overview.selected_pms_project_id");
      schedulePreviewRefresh();
    }

    function wirePmsProjectCombobox(){
      const input = $("projectNameInput");
      const toggle = document.querySelector("[data-pms-toggle]");
      const menu = document.querySelector("[data-pms-menu]");
      if (!input || input.dataset.pmsWired === "true") return;
      input.dataset.pmsWired = "true";
      input.addEventListener("focus", () => searchPmsProjects().catch(console.error));
      input.addEventListener("input", () => {
        clearPmsProjectDraft();
        touchedFields.add("analysis_overview.project_name");
        window.clearTimeout(pmsSearchTimer);
        pmsSearchTimer = window.setTimeout(() => searchPmsProjects(input.value).catch(console.error), 180);
      });
      input.addEventListener("keydown", async event => {
        if (event.key === "Escape") {
          setPmsMenuOpen(false);
          return;
        }
        if (event.key === "ArrowDown" || event.key === "ArrowUp") {
          event.preventDefault();
          if (menu?.hidden) await searchPmsProjects(input.value);
          if (!pmsSearchItems.length) return;
          const direction = event.key === "ArrowDown" ? 1 : -1;
          setPmsActiveResult(pmsActiveIndex === -1 ? (direction > 0 ? 0 : pmsSearchItems.length - 1) : pmsActiveIndex + direction);
        } else if (event.key === "Enter" && pmsActiveIndex >= 0) {
          event.preventDefault();
          selectPmsProject(pmsSearchItems[pmsActiveIndex]).catch(console.error);
        }
      });
      toggle?.addEventListener("click", () => searchPmsProjects(input.value).catch(console.error));
      menu?.addEventListener("click", event => {
        const option = event.target.closest("[data-pms-index]");
        if (option) selectPmsProject(pmsSearchItems[Number(option.dataset.pmsIndex)]).catch(err => console.error(err));
      });
      menu?.addEventListener("pointermove", event => {
        const option = event.target.closest("[data-pms-index]");
        if (option) setPmsActiveResult(Number(option.dataset.pmsIndex));
      });
    }

    function selectUndecidedComboboxMode(combobox, mode){
      const input = combobox?.querySelector("[data-undecided-input]");
      if (!input) return;
      const previousMode = undecidedComboboxMode(combobox);
      if (mode === "undecided") {
        const specialValue = undecidedComboboxSpecialValue(combobox);
        if (specialValue === "미정") input.value = "미정";
        else input.value = specialValue;
        renderUndecidedComboboxMode(combobox, "undecided");
      } else {
        if (previousMode === "undecided") input.value = "";
        renderUndecidedComboboxMode(combobox, "custom");
      }
      touchedFields.add(input.dataset.path || "");
      setUndecidedComboboxOpen(combobox, false);
      renderScreenNavigation();
      schedulePreviewRefresh();
      window.requestAnimationFrame(() => input.focus());
    }

    function uniqueValues(items){
      const seen = new Set();
      const out = [];
      asArray(items).forEach(item => {
        const value = contextText(item);
        if (!value || seen.has(value)) return;
        seen.add(value);
        out.push(value);
      });
      return out;
    }

    function fallbackRequestContext(){
      return {
        taxonomy_id: "",
        taxonomy_version: "",
        division: "",
        product_lineup: "",
        platform: "",
        chassis: null,
        display_path: "",
        analysis_type: "",
        analysis_scope: "",
        operation_mode: "",
        context_locked: false,
        condition_fieldset_key: "",
        condition_fieldset_snapshot: [],
      };
    }

    function contextFromState(){
      const context = asObj(requestState.request_context);
      let division = contextText(context.division);
      if (division && !divisionOptions().includes(division)) division = "";
      return {
        ...fallbackRequestContext(),
        ...context,
        division,
        taxonomy_id: contextText(context.taxonomy_id),
        taxonomy_version: contextText(context.taxonomy_version),
        product_lineup: contextText(context.product_lineup),
        platform: contextText(context.platform),
        chassis: context.chassis === null ? null : contextText(context.chassis),
        display_path: contextText(context.display_path),
        analysis_type: contextText(context.analysis_type),
        analysis_scope: contextText(context.analysis_scope),
        operation_mode: contextText(context.operation_mode),
        context_locked: context.context_locked === true,
      };
    }

    function isContextLocked(){
      return contextFromState().context_locked === true;
    }

    function isRacWindowContext(context=contextFromState()){
      return contextText(context.division) === "RAC"
        && contextText(context.product_lineup) === "Window"
        && contextText(context.platform) === "Window";
    }

    function requestedAnalysisScopes(context=contextFromState()){
      if (!isRacWindowContext(context)) return [""];
      return contextText(context.analysis_scope) === "both"
        ? ["indoor", "outdoor"]
        : [["indoor", "outdoor"].includes(contextText(context.analysis_scope)) ? contextText(context.analysis_scope) : "indoor"];
    }

    function hasBothAnalysisScopes(context=contextFromState()){
      return isRacWindowContext(context) && contextText(context.analysis_scope) === "both";
    }

    function scopeLabel(scope){ return analysisScopeLabels[contextText(scope)] || ""; }

    function scopeTabsHtml(kind, activeScope){
      if (!hasBothAnalysisScopes()) return "";
      const contextLabel = kind === "conditions" ? `${scopeLabel(activeScope)} 해석 조건` : `${scopeLabel(activeScope)} Case 구성`;
      return `<div class="analysis-scope-tabs" role="tablist" aria-label="${kind === "conditions" ? "해석 조건" : "Case Matrix"} 해석 범위">${["indoor","outdoor"].map(scope => {
        const status = kind === "case" ? caseMatrixScopeStatus(scope) : "";
        return `<button type="button" role="tab" data-scope-tab="${kind}" data-analysis-scope="${scope}" aria-selected="${String(scope === activeScope)}">${scopeLabel(scope)}${status ? ` <span class="analysis-scope-tab-status">· ${status}</span>` : ""}</button>`;
      }).join("")}</div><div class="analysis-scope-context" aria-live="polite">${contextLabel}</div>`;
    }

    function syncRequestContextDraftFromState(){
      requestContextDraft = contextFromState();
    }

    function hasAnyRequestContextValue(context){
      return ["division","product_lineup","platform","chassis","analysis_type"].some(key => contextText(context[key]));
    }

    function currentStageAssistKey(){
      const context = collectRequestContextDraft();
      if (context.context_locked === true) return "conditions";
      if (!prepAssistStarted && !hasAnyRequestContextValue(context)) return "start";
      if (!contextText(context.division)) return "division";
      if (!contextText(context.product_lineup)) return "product_lineup";
      if (!contextText(context.platform)) return "platform";
      if (!contextText(context.chassis) && !contextText(context.taxonomy_id)) return "chassis";
      return "analysis_type";
    }

    function fillStageAssistPrompt(prompt){
      const input = $("chatInput");
      const text = String(prompt || "").trim();
      if (!input || !text) return;
      input.value = text;
      input.focus();
      input.setSelectionRange?.(text.length, text.length);
    }

    function productHierarchyPayload(){
      return {
        ...emptyProductHierarchy,
        ...asObj(productHierarchy),
        hierarchy: {...emptyProductHierarchy.hierarchy, ...asObj(asObj(productHierarchy).hierarchy)},
      };
    }

    function divisionOptions(){
      const payload = productHierarchyPayload();
      const labels = asArray(payload.divisions).map(item => contextText(asObj(item).label));
      return uniqueValues(labels.length ? labels : defaultDivisions);
    }

    function productLineupOptions(division){
      const payload = productHierarchyPayload();
      return uniqueValues(Object.keys(asObj(asObj(payload.hierarchy)[division])).sort((a,b) => a.localeCompare(b, "ko")));
    }

    function platformOptions(division, productLineup){
      const payload = productHierarchyPayload();
      return uniqueValues(Object.keys(asObj(asObj(asObj(payload.hierarchy)[division])[productLineup])).sort((a,b) => a.localeCompare(b, "ko")));
    }

    function chassisLeaves(division, productLineup, platform){
      const payload = productHierarchyPayload();
      return asArray(asObj(asObj(asObj(payload.hierarchy)[division])[productLineup])[platform]);
    }

    const NULL_CHASSIS_VALUE = "__null_chassis__";

    function chassisOptionValue(value){
      return value === null ? NULL_CHASSIS_VALUE : contextText(value);
    }

    function chassisOptions(division, productLineup, platform){
      return uniqueValues(chassisLeaves(division, productLineup, platform).map(item => chassisOptionValue(asObj(item).chassis)));
    }

    function taxonomyLeaf(division, productLineup, platform, chassis){
      const wanted = chassisOptionValue(chassis);
      return chassisLeaves(division, productLineup, platform).find(item => chassisOptionValue(asObj(item).chassis) === wanted) || null;
    }

    function platformSelectionMode(division){
      return contextText(asObj(asObj(productHierarchyPayload().division_rules)[division]).platform_selection_mode) || "catalog";
    }

    function renderPrepSelect(selectId, values, selected, placeholder, disabled=false, disabledValues=[], disabledSuffix="", disabledPrefix=""){
      const select = $(selectId);
      if (!select) return;
      const rows = uniqueValues(values);
      const disabledSet = new Set(uniqueValues(disabledValues));
      const optionHtml = [`<option value="" disabled hidden>${esc(placeholder)}</option>`, ...rows.map(value => {
        const displayValue = value === NULL_CHASSIS_VALUE ? "null" : value;
        const label = disabledSet.has(value) ? `${disabledPrefix}${displayValue}${disabledSuffix}` : displayValue;
        return `<option value="${esc(value)}" ${disabledSet.has(value) ? "disabled" : ""}>${esc(label)}</option>`;
      })].join("");
      select.innerHTML = optionHtml;
      select.disabled = disabled;
      select.value = rows.includes(selected) ? selected : "";
    }

    function renderRequestPrepCard(){
      const card = $("requestPrepCard");
      if (!card) return;
      const context = {...fallbackRequestContext(), ...requestContextDraft};
      const locked = context.context_locked === true;
      card.hidden = false;
      const prepBody = card.querySelector(".prep-body");
      if (prepBody) prepBody.hidden = locked;
      const changeButton = $("contextChangeBtn");
      if (changeButton) changeButton.hidden = !locked;
      const nextButton = $("nextRequestContentBtn");
      if (nextButton) nextButton.hidden = !locked;
      renderContextChip();
      if (locked) return;
      const divisions = divisionOptions();
      const productLineupRows = context.division ? productLineupOptions(context.division) : [];
      const platformRows = context.division && context.product_lineup ? platformOptions(context.division, context.product_lineup) : [];
      const chassisRows = context.division && context.product_lineup && context.platform ? chassisOptions(context.division, context.product_lineup, context.platform) : [];
      const productLineupDisabled = !context.division;
      const platformDerived = platformSelectionMode(context.division) === "derived_from_product_lineup";
      const platformDisabled = !context.product_lineup || platformDerived;
      const nullChassisSelected = context.chassis === null && !!context.taxonomy_id;
      const selectedChassisOption = nullChassisSelected ? NULL_CHASSIS_VALUE : contextText(context.chassis);
      const chassisAutoNull = chassisRows.length === 1 && chassisRows[0] === NULL_CHASSIS_VALUE;
      const chassisDisabled = !context.platform || chassisAutoNull;

      renderPrepSelect("quickDivisionSelect", divisions, context.division, "Division 선택");
      renderPrepSelect("quickProductLineupSelect", productLineupRows, context.product_lineup, productLineupDisabled ? "Division 먼저 선택" : "Product Line-up 선택", productLineupDisabled);
      renderPrepSelect("quickPlatformSelect", platformRows, context.platform, !context.product_lineup ? "Product Line-up 먼저 선택" : "Platform 선택", platformDisabled);
      renderPrepSelect("quickChassisSelect", chassisRows, selectedChassisOption, !context.platform ? "Platform 먼저 선택" : "Chassis 선택", chassisDisabled);
      renderPrepSelect("quickAnalysisTypeSelect", prepAnalysisTypes, context.analysis_type, "해석유형 선택", false, disabledAnalysisTypes, " (예정)", disabledAnalysisTypeLockPrefix);

      const scopeField = $("analysisScopeField");
      if (scopeField) {
        const visible = isRacWindowContext(context);
        scopeField.hidden = !visible;
        const selectedScope = ["indoor","outdoor","both"].includes(contextText(context.analysis_scope)) ? context.analysis_scope : "";
        scopeField.querySelectorAll("button[data-analysis-scope]").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.analysisScope === selectedScope)));
      }

      const detail = $("analysisTypeDetail");
      if (detail) {
        const selectedDetail = analysisTypeDetails[context.analysis_type];
        if (selectedDetail) {
          detail.innerHTML = `<p class="analysis-type-detail-eyebrow">선택한 해석유형</p><h5 class="analysis-type-detail-title">${esc(context.analysis_type)}</h5><p class="analysis-type-detail-description">${esc(selectedDetail.description)}</p><p class="analysis-type-detail-subheading">이런 경우에 적합합니다</p><ul class="analysis-type-detail-list">${selectedDetail.suitable.map(item => `<li>${esc(item)}</li>`).join("")}</ul>`;
        } else {
          detail.innerHTML = `<p class="analysis-type-detail-eyebrow">선택한 해석유형</p><p class="analysis-type-detail-description">해석유형을 선택하면 해당 해석의 목적과 적합한 활용 사례를 확인할 수 있습니다.</p>`;
        }
      }
      renderContextChip();
    }

    function renderContextChip(){
      const bar = $("contextChipBar");
      const list = $("contextChipList");
      if (!bar || !list) return;
      const context = contextFromState();
      const locked = context.context_locked === true;
      bar.hidden = !locked;
      if (!locked) {
        list.innerHTML = "";
        return;
      }
      const chipValues = ["division","product_lineup","platform","chassis","analysis_type"]
        .map(key => key === "chassis" && context.chassis === null ? "null" : (context[key] || "미선택"));
      if (isRacWindowContext(context)) chipValues.push(scopeLabel(context.analysis_scope));
      list.innerHTML = chipValues
        .map(value => `<span class="chip ok">${esc(value)}</span>`)
        .join("");
    }

    function updateRequestContextDraft(field, value){
      prepAssistStarted = true;
      const next = {...fallbackRequestContext(), ...requestContextDraft};
      next[field] = field === "chassis" && value === NULL_CHASSIS_VALUE ? null : contextText(value);
      if (field === "division") {
        next.product_lineup = "";
        next.platform = "";
        next.chassis = null;
        clearPmsProjectDraft();
      }
      if (field === "product_lineup") {
        next.platform = platformSelectionMode(next.division) === "derived_from_product_lineup" ? next.product_lineup : "";
        next.chassis = null;
      }
      if (field === "platform") next.chassis = null;
      if (["division","product_lineup","platform"].includes(field)) {
        next.taxonomy_id = "";
        next.taxonomy_version = "";
        next.display_path = "";
      }
      if ((field === "product_lineup" && next.platform) || field === "platform") {
        const leaves = chassisLeaves(next.division, next.product_lineup, next.platform);
        if (leaves.length === 1) {
          next.chassis = asObj(leaves[0]).chassis === null ? null : contextText(asObj(leaves[0]).chassis);
          next.taxonomy_id = contextText(asObj(leaves[0]).taxonomy_id);
          next.taxonomy_version = contextText(productHierarchyPayload().taxonomy_version);
          next.display_path = contextText(asObj(leaves[0]).display_path);
        }
      }
      if (field === "chassis") {
        const leaf = asObj(taxonomyLeaf(next.division, next.product_lineup, next.platform, next.chassis));
        next.taxonomy_id = contextText(leaf.taxonomy_id);
        next.taxonomy_version = contextText(productHierarchyPayload().taxonomy_version);
        next.display_path = contextText(leaf.display_path);
      }
      next.analysis_scope = isRacWindowContext(next)
        ? (["indoor","outdoor","both"].includes(contextText(next.analysis_scope)) ? next.analysis_scope : "")
        : "";
      requestContextDraft = next;
      requestState.request_context = {...asObj(requestState.request_context), ...requestContextDraft};
      touchedFields.add(`request_context.${field}`);
      renderRequestPrepCard();
      updateTopChrome();
      schedulePreviewRefresh();
    }

    function collectRequestContextDraft(){
      return {
        ...fallbackRequestContext(),
        ...asObj(requestState.request_context),
        ...requestContextDraft,
        context_locked: asObj(requestState.request_context).context_locked === true,
      };
    }

    function syncQuickPrepSelectionsToDraft(){
      const next = {...fallbackRequestContext(), ...asObj(requestState.request_context), ...requestContextDraft};
      [
        ["division", "quickDivisionSelect"],
        ["product_lineup", "quickProductLineupSelect"],
        ["platform", "quickPlatformSelect"],
        ["chassis", "quickChassisSelect"],
        ["analysis_type", "quickAnalysisTypeSelect"],
      ].forEach(([field, id]) => {
        const select = $(id);
        if (!select) return;
        next[field] = field === "chassis" && select.value === NULL_CHASSIS_VALUE ? null : contextText(select.value);
      });
      const leaf = asObj(taxonomyLeaf(next.division, next.product_lineup, next.platform, next.chassis));
      next.taxonomy_id = contextText(leaf.taxonomy_id);
      next.taxonomy_version = contextText(productHierarchyPayload().taxonomy_version);
      next.display_path = contextText(leaf.display_path);
      next.analysis_scope = isRacWindowContext(next)
        ? (["indoor","outdoor","both"].includes(contextText(next.analysis_scope)) ? next.analysis_scope : "")
        : "";
      requestContextDraft = next;
      requestState.request_context = {...asObj(requestState.request_context), ...requestContextDraft};
      return collectRequestContextDraft();
    }

    function collectContextConfirmState(context){
      try {
        const state = collectState();
        return {...state, request_context: {...asObj(state.request_context), ...context}};
      } catch (err) {
        console.warn("context confirm state fallback", err);
        return {...asObj(requestState), request_context: {...fallbackRequestContext(), ...context}};
      }
    }

    async function fetchProductHierarchyOptions(){
      const res = await fetch("/api/product-taxonomy");
      const data = await res.json();
      if (!res.ok || data.ok === false) throw new Error(data.message || "product hierarchy load failed");
      productHierarchy = data;
      renderRequestPrepCard();
    }

    function missingContextFields(context=null){
      context = context || collectRequestContextDraft();
      const missing = ["division","product_lineup","platform","analysis_type"].filter(key => !contextText(context[key]));
      if (isRacWindowContext(context) && !["indoor","outdoor","both"].includes(contextText(context.analysis_scope))) missing.push("analysis_scope");
      if (!contextText(context.taxonomy_id)) missing.push("chassis");
      return missing;
    }

    async function confirmRequestContext(){
      const context = syncQuickPrepSelectionsToDraft();
      const missing = missingContextFields(context);
      if (missing.length) {
        const screen = screenOrder.find(item => item.id === "SCREEN-01") || screenOrder[0];
        const control = missingRequiredControl("SCREEN-01");
        focusRequiredControl(screen, control);
        if (control?.id === "analysisScopeField") control.querySelectorAll("button[data-analysis-scope]").forEach(button => button.classList.add("required-field-highlight"));
        else if (control) control.classList.add("required-field-highlight");
        return;
      }
      const data = await postJson("/api/request-context/confirm", {state:collectContextConfirmState(context), request_context:context});
      invalidatePendingPreviewRefresh();
      adoptStateFromResponse(data);
      syncEditorFromState();
      navigateScreen("SCREEN-02");
    }


    async function updateOperationMode(value){
      const state = collectState();
      const context = {...collectRequestContextDraft(), operation_mode: contextText(value)};
      state.request_context = {...asObj(state.request_context), ...context};
      const data = await postJson("/api/request-context/fieldset", {state, request_context: context});
      adoptStateFromResponse(data);
      syncEditorFromState();
    }
    function showContextChangeWarning(){
      $("contextChangeModal").hidden = false;
      $("contextChangeCancel").focus();
    }

    function hideContextChangeWarning(){
      $("contextChangeModal").hidden = true;
    }

    function continueContextChange(){
      const current = contextFromState();
      requestContextDraft = {
        ...fallbackRequestContext(),
        ...current,
        context_locked: false,
        condition_fieldset_key: "",
        condition_fieldset_snapshot: [],
      };
      requestState.request_context = {...requestContextDraft};
      hideContextChangeWarning();
      prepAssistStarted = true;
      syncEditorFromState();
      pushMessage("assistant", "조합 변경을 다시 진행할 수 있습니다. 기존 조건 입력값은 보존되어 있지만 조합과 맞지 않으면 다음 단계에서 사용되지 않습니다.");
    }

    function applyRequestTypeChange(value){
      requestState = {...requestState, analysis_overview:{...asObj(requestState.analysis_overview), request_type:value}};
      clearPmsProjectDraft();
      syncPmsProjectControl();
      renderScreenNavigation();
    }

    function handleDropdownChange(select){
      const path = select.dataset.dropdownPath || "";
      const input = document.querySelector(`input[data-path="${CSS.escape(path)}"]`);
      const customControl = document.querySelector(`[data-dropdown-custom-path="${CSS.escape(path)}"]`);
      if (!input) return;
      if (select.value === "__custom__") {
        input.value = "";
        select.hidden = true;
        if (customControl) customControl.hidden = false;
        else input.hidden = false;
        input.focus();
      } else {
        select.hidden = false;
        if (customControl) customControl.hidden = true;
        else input.hidden = true;
        input.value = select.value;
      }
      if (path === "analysis_overview.request_type") applyRequestTypeChange(input.value);
      touchedFields.add(path);
      schedulePreviewRefresh();
    }

    function restoreDropdownControl(button){
      const path = button.dataset.dropdownRestorePath || "";
      const select = document.querySelector(`select[data-dropdown-path="${CSS.escape(path)}"]`);
      const input = document.querySelector(`input[data-path="${CSS.escape(path)}"]`);
      const customControl = document.querySelector(`[data-dropdown-custom-path="${CSS.escape(path)}"]`);
      if (!select || !input) return;
      select.hidden = false;
      select.value = "";
      input.value = "";
      if (customControl) customControl.hidden = true;
      else input.hidden = true;
      touchedFields.add(path);
      if (path === "analysis_overview.request_type") applyRequestTypeChange(input.value);
      else renderScreenNavigation();
      schedulePreviewRefresh();
      select.focus();
    }

    function handleConditionSelectChange(select){
      const key = select.dataset.conditionSelect || "";
      const index = select.dataset.index || "0";
      const input = document.querySelector(`input[data-condition-key="${CSS.escape(key)}"][data-index="${CSS.escape(index)}"]`);
      if (!input) return;
      if (select.value === "__custom__") {
        input.hidden = false;
        input.focus();
      } else {
        input.hidden = true;
        input.value = select.value;
      }
      touchedFields.add(key);
      schedulePreviewRefresh();
    }

    function hasAnalysisType(){
      return !!contextText(contextFromState().analysis_type);
    }

    function updateTopChrome(){
      const contextLocked = isContextLocked();
      const context = collectRequestContextDraft();
      const titleValues = [context.division, context.product_lineup, context.platform, context.chassis === null && context.taxonomy_id ? "null" : context.chassis, context.analysis_type].map(contextText);
      const baseRequestTitle = titleValues.every(Boolean) ? titleValues.join(" / ") : "해석 의뢰를 시작해 주세요.";
      const selectedScopeLabel = isRacWindowContext(context) ? scopeLabel(context.analysis_scope) : "";
      const requestTitle = selectedScopeLabel && baseRequestTitle !== "해석 의뢰를 시작해 주세요." ? `${baseRequestTitle} · ${selectedScopeLabel}` : baseRequestTitle;
      const requestNo = contextText(asObj(requestState.metadata).request_no) || fieldDisplayValue(asObj(requestState.basic_info).request_no) || "-";
      if ($("heroTitle")) $("heroTitle").textContent = requestTitle;
      if ($("requestNoDisplay")) $("requestNoDisplay").textContent = requestNo;
      const ragEnabled = false;
      if ($("ragToggle")) $("ragToggle").checked = false;
      document.querySelectorAll(".workspace-tab").forEach(panel => {
        const isActivePanel = panel.id === `tab-${activeTopTab}`;
        panel.classList.toggle("active", isActivePanel);
        if (isActivePanel) {
          panel.hidden = false;
          panel.removeAttribute("aria-hidden");
        } else {
          panel.hidden = true;
          panel.setAttribute("aria-hidden", "true");
        }
      });
      const contextChangeButton = $("contextChangeBtn");
      if (contextChangeButton) contextChangeButton.hidden = !contextLocked;
    }

    function switchTopTab(tab){
      activeTopTab = tab === "preview" ? "preview" : "write";
      updateTopChrome();
      renderDerivedPanels();
    }

    function screenForSection(section){
      return {
        basic_info:"SCREEN-02", analysis_overview:"SCREEN-02", geometry:"SCREEN-03",
        conditions:"SCREEN-04", case_matrix:"SCREEN-05", preview:"SCREEN-06",
      }[section] || "SCREEN-01";
    }

    function setScreenNavigationStatus(message){
      const status = $("screenNavigationStatus");
      if (status) status.textContent = message;
    }

    function userScreenName(screenId){
      const item = document.querySelector(`.screen-map-item[data-screen="${CSS.escape(screenId)}"]`);
      const number = contextText(item?.dataset.stepNumber);
      const label = contextText(item?.querySelector(".screen-map-label")?.textContent);
      return [number, label].filter(Boolean).join(" ") || "현재 단계";
    }

    function finalSubmissionCompleted(){
      const submission = asObj(asObj(requestState.review).submission);
      return submission.status === "OK" && submission.can_submit === true
        && !!contextText(asObj(requestState.metadata).request_no);
    }

    function renderScreenNavigation(){
      const active = screenOrder.find(screen => screen.id === activeScreen) || screenOrder[0];
      const reviewScreen = screenOrder.find(screen => screen.id === "SCREEN-06");
      const firstIncomplete = firstIncompleteScreenBefore(reviewScreen);
      const firstIncompleteIndex = firstIncomplete ? screenOrder.findIndex(screen => screen.id === firstIncomplete.screen.id) : -1;
      document.querySelectorAll(".screen-map-item[data-screen]").forEach(item => {
        const screen = screenOrder.find(candidate => candidate.id === item.dataset.screen);
        const screenIndex = screenOrder.findIndex(candidate => candidate.id === screen?.id);
        const blocked = !!screen?.requiresContext && firstIncompleteIndex >= 0 && screenIndex > firstIncompleteIndex;
        const completed = screen?.id === "SCREEN-06"
          ? finalSubmissionCompleted()
          : screenIndex >= 0 && screenIndex < 5 && screenIndex < screenOrder.findIndex(candidate => candidate.id === active.id)
            && !blocked && !missingRequiredControl(screen.id) && !blockingScreenError(screen.id);
        const numberNode = item.querySelector(".screen-map-number");
        item.setAttribute("role", "button");
        item.tabIndex = blocked ? -1 : 0;
        item.setAttribute("aria-disabled", String(blocked));
        item.setAttribute("aria-current", screen?.id === active.id ? "page" : "false");
        item.dataset.completed = String(completed);
        if (numberNode) numberNode.textContent = completed ? "✓" : contextText(item.dataset.stepNumber);
        if (completed) item.setAttribute("aria-label", `${contextText(item.dataset.stepNumber)} ${contextText(item.querySelector(".screen-map-label")?.textContent)} 완료`);
        else item.removeAttribute("aria-label");
        if (blocked) item.setAttribute("aria-describedby", "screenNavigationStatus"); else item.removeAttribute("aria-describedby");
      });
      document.querySelectorAll(".workspace-tab").forEach(panel => {
        const isActive = panel.id === `tab-${active.tab}`;
        panel.classList.toggle("active", isActive);
        panel.hidden = !isActive;
        panel.setAttribute("aria-hidden", String(!isActive));
      });
      document.querySelectorAll(".screen-group[data-screen]").forEach(group => {
        group.hidden = group.dataset.screen !== active.id;
      });
      const wordButton = $("wordExportSlotBtn");
      const wordRequiredWarning = $("wordExportRequiredWarning");
      const caseMatrixExportBlocked = caseMatrixBlocksWordExport();
      if (wordButton) {
        wordButton.disabled = wordExportInProgress || firstIncompleteIndex >= 0 || caseMatrixExportBlocked;
        if (wordExportInProgress) wordButton.title = "의뢰서 생성 여부를 확인하고 있습니다.";
        else if (firstIncompleteIndex >= 0) wordButton.title = "필수 입력을 완료하면 의뢰서를 생성할 수 있습니다.";
        else if (caseMatrixExportBlocked) wordButton.title = "Case Matrix의 오류 또는 확인 필요 항목을 해소하면 의뢰서를 생성할 수 있습니다.";
        else wordButton.removeAttribute("title");
      }
      if (wordRequiredWarning) wordRequiredWarning.hidden = firstIncompleteIndex < 0;
      setScreenNavigationStatus(firstIncomplete
        ? `현재 화면: ${userScreenName(active.id)}. ${userScreenName(firstIncomplete.screen.id)}의 필수 입력을 완료하면 이후 단계를 열 수 있습니다.`
        : `현재 화면: ${userScreenName(active.id)}`);
    }

    function focusScreenHeading(screen){
      const heading = $(screen.headingId);
      if (!heading) return;
      heading.tabIndex = -1;
      heading.scrollIntoView({behavior:"smooth", block:"start"});
      heading.focus({preventScroll:true});
    }

    function requiredPathControl(path){
      const select = document.querySelector(`select[data-dropdown-path="${CSS.escape(path)}"]`);
      if (select?.value === "__custom__") return document.querySelector(`input[data-path="${CSS.escape(path)}"]`) || select;
      return select || document.querySelector(`[data-path="${CSS.escape(path)}"]`);
    }

    function missingRequiredControl(screenId){
      if (screenId === "SCREEN-01") {
        if (isContextLocked()) return null;
        const context = collectRequestContextDraft();
        const controls = {
          division: $("quickDivisionSelect"),
          product_lineup: $("quickProductLineupSelect"),
          platform: $("quickPlatformSelect"),
          chassis: $("quickChassisSelect"),
          analysis_type: $("quickAnalysisTypeSelect"),
        };
        const missingControl = ["division", "product_lineup", "platform", "chassis", "analysis_type"]
          .map(key => key === "chassis" ? (!contextText(context.taxonomy_id) ? controls[key] : null) : (!contextText(context[key]) ? controls[key] : null))
          .find(Boolean);
        if (missingControl) return missingControl;
        if (isRacWindowContext(context) && !["indoor", "outdoor", "both"].includes(contextText(context.analysis_scope))) {
          return $("analysisScopeField");
        }
        return $("prepStartBtn");
      }
      if (screenId === "SCREEN-02") {
        const paths = [
          "basic_info.division", "basic_info.department", "basic_info.requester_name", "basic_info.requester_role",
          "analysis_overview.request_type", "analysis_overview.project_name", "analysis_overview.development_grade", "analysis_overview.npi_stage",
          "analysis_overview.model_suffix", "analysis_overview.desired_completion_date",
          "analysis_overview.request_description", "analysis_overview.additional_result_request",
        ];
        const desiredCompletionDate = requiredPathControl("analysis_overview.desired_completion_date");
        if (desiredCompletionDate && !desiredCompletionDate.validity.valid) return desiredCompletionDate;
        return paths.map(requiredPathControl).find(control => !contextText(control?.value)) || null;
      }
      if (screenId === "SCREEN-03") {
        return Array.from(document.querySelectorAll('[data-product-field="drawing_no"], [data-product-field="description"]'))
          .find(control => !contextText(control.value)) || null;
      }
      if (screenId === "SCREEN-04") {
        const missingFanMode = Array.from(document.querySelectorAll('#conditionFields .condition-card-type-operating [data-fan-rpm-mode]'))
          .find(control => !contextText(control.value));
        if (missingFanMode) return missingFanMode;
        return Array.from(document.querySelectorAll('#conditionFields [data-card-field]'))
          .find(control => !contextText(control.value)) || null;
      }
      if (screenId === "SCREEN-05") {
        const rows = Array.from(document.querySelectorAll('tr[data-case-row]'));
        if (!rows.length) return document.querySelector('[data-action="add-case"]');
        return rows.flatMap(row => Array.from(row.querySelectorAll('select[data-case-field]')))
          .find(control => !contextText(control.value)) || null;
      }
      return null;
    }

    function conditionValidationIssues(state=requestState){
      return asArray(caseValidatorState(state).blocking)
        .filter(issue => contextText(asObj(issue).section) === "conditions");
    }

    function conditionDuplicateIssues(state=requestState){
      return conditionValidationIssues(state)
        .filter(issue => contextText(asObj(issue).code) === "conditions.duplicate");
    }

    function renderConditionDuplicateWarning(){
      const target = $("conditionDuplicateWarning");
      if (!target) return;
      const issues = conditionDuplicateIssues();
      target.innerHTML = issues.length
        ? `<div class="coverage-warning-head"><span class="coverage-warning-icon" aria-hidden="true">⊗</span><strong class="coverage-warning-title">오류 · 동일한 해석 조건이 있습니다.</strong></div>${issues.map(issue => `<p class="coverage-warning-copy">${esc(contextText(asObj(issue).field_label))} 조건이 중복되었습니다.</p>`).join("")}`
        : "";
    }

    function focusConditionValidationIssue(issue){
      const scope = contextText(asObj(issue).analysis_scope);
      if (hasBothAnalysisScopes() && ["indoor", "outdoor"].includes(scope) && scope !== activeConditionScope) {
        preserveEditorDraftBeforeRerender();
        activeConditionScope = scope;
        renderConditionFields();
      }
      const control = revealMissingFanControl(missingRequiredControl("SCREEN-04")) || $("section-conditions");
      if (control !== $("section-conditions")) control.classList.add("required-field-highlight");
      if (control?.scrollIntoView) control.scrollIntoView({behavior:"smooth", block:"center"});
      if (control?.focus) control.focus();
    }

    async function confirmConditionsBeforeCaseMatrix(){
      await refreshPreview();
      const issues = conditionValidationIssues();
      if (issues.length) {
        focusConditionValidationIssue(issues[0]);
        return;
      }
      navigateScreen("SCREEN-05");
    }

    function revealMissingFanControl(control){
      const detail = control?.closest?.("[data-fan-detail-card]");
      if (!detail?.hidden) return control;
      const cardId = contextText(control.dataset.cardId);
      const fanIndex = contextText(control.dataset.fanIndex);
      const fieldKey = contextText(control.dataset.cardField);
      if (!cardId || !fanIndex || !["fan_location", "fan_rpm"].includes(fieldKey)) return control;
      preserveEditorDraftBeforeRerender();
      expandedFanCardId = cardId;
      renderConditionFields();
      return document.querySelector(`[data-card-id="${CSS.escape(cardId)}"][data-fan-index="${CSS.escape(fanIndex)}"][data-card-field="${CSS.escape(fieldKey)}"]`);
    }

    function blockingScreenError(screenId){
      if (screenId === "SCREEN-03" && geometryDrawingDuplicateIssues().length) return $("geometryDrawingDuplicateWarning");
      if (screenId === "SCREEN-04" && conditionDuplicateIssues().length) return $("conditionDuplicateWarning");
      if (screenId === "SCREEN-05" && caseConfigurationIssues().length) return $("caseDuplicateWarning");
      return null;
    }

    function focusRequiredControl(screen, control){
      activeScreen = screen.id;
      activeTopTab = screen.tab;
      renderScreenNavigation();
      const isError = control?.matches?.(".case-review-message.error");
      setScreenNavigationStatus(isError
        ? `${userScreenName(screen.id)}의 오류를 수정한 뒤 다음 단계로 이동할 수 있습니다.`
        : `${userScreenName(screen.id)}의 필수 입력을 완료한 뒤 다음 단계로 이동할 수 있습니다.`);
      const target = screen.id === "SCREEN-04" ? revealMissingFanControl(control) || $(screen.headingId) : control || $(screen.headingId);
      const focusTarget = target?.id === "analysisScopeField"
        ? target.querySelector("button[data-analysis-scope]") || target
        : target;
      if (isError && target && !target.hasAttribute("tabindex")) target.tabIndex = -1;
      if (!isError && control && target) {
        if (target.id === "analysisScopeField") target.querySelectorAll("button[data-analysis-scope]").forEach(button => button.classList.add("required-field-highlight"));
        else target.classList.add("required-field-highlight");
      }
      target?.scrollIntoView({behavior:"smooth", block:"center"});
      if (target?.id === "analysisScopeField") focusTarget?.focus?.({preventScroll:true});
      else target?.focus?.({preventScroll:true});
      if (target?.validity && !target.validity.valid) target.reportValidity?.();
    }

    function firstIncompleteScreenBefore(targetScreen){
      const targetIndex = screenOrder.findIndex(item => item.id === targetScreen.id);
      if (targetIndex < 1) return null;
      for (let index = 0; index < targetIndex; index += 1) {
        const screen = screenOrder[index];
        const control = missingRequiredControl(screen.id) || blockingScreenError(screen.id);
        if (control) return {screen, control};
      }
      return null;
    }

    function navigateScreen(screenId, options={}){
      const screen = screenOrder.find(item => item.id === screenId) || screenOrder[0];
      if (screen.requiresContext && !isContextLocked()) {
        const first = firstIncompleteScreenBefore(screen) || {screen:screenOrder[0], control:missingRequiredControl("SCREEN-01")};
        focusRequiredControl(first.screen, first.control);
        return false;
      }
      const currentIndex = screenOrder.findIndex(item => item.id === activeScreen);
      const targetIndex = screenOrder.findIndex(item => item.id === screen.id);
      if (!options.bypassRequiredGate && targetIndex > currentIndex) {
        const first = firstIncompleteScreenBefore(screen);
        if (first) {
          focusRequiredControl(first.screen, first.control);
          return false;
        }
      }
      if (typeof completeCaseImpactReviewOnLeave === "function") completeCaseImpactReviewOnLeave(screen.id);
      activeScreen = screen.id;
      activeTopTab = screen.tab;
      renderScreenNavigation();
      if (screen.id === "SCREEN-05" && typeof caseImpactBaseline !== "undefined" && !caseImpactBaseline) {
        resetCaseImpactBaseline();
      }
      if (screen.id === "SCREEN-05" && typeof recordCaseImpactReviewMatrixRender === "function") {
        recordCaseImpactReviewMatrixRender();
      }
      if (options.focus !== false) focusScreenHeading(screen);
      return true;
    }

    function updateGate(){
      const contextLocked = isContextLocked();
      const ready = contextLocked && hasAnalysisType();
      const contextGate = $("contextLockGate");
      if (contextGate) contextGate.hidden = contextLocked;
      $("analysisGate").style.display = ready || !contextLocked ? "none" : "";
      $("formView").style.display = "";
      ["section-overview","section-geometry","section-conditions","section-case"].forEach(id => {
        const section = $(id);
        if (section) section.style.display = contextLocked ? "" : "none";
      });
      if (!contextLocked) $("section-basic")?.classList.add("open");
      if (!contextLocked && screenOrder.find(screen => screen.id === activeScreen)?.requiresContext) activeScreen = "SCREEN-01";
      renderScreenNavigation();
      renderContextChip();
      updateTopChrome();
    }

    function valuesFromRows(selector){
      return Array.from(document.querySelectorAll(selector)).map(input => input.value);
    }

    function productDescription(product, comparison=false){
      if (!comparison) return "Base";
      return productText(product, "difference_from_base") || productText(product, "display_name");
    }
    function productRow(product, index, comparison=false){
      const id = esc(product.geometry_id || `${comparison ? "comparison" : "base"}_${index + 1}`);
      const geometryNumber = comparison ? index + 2 : 1;
      const geometryLabel = comparison ? `비교 ${index + 1}` : "Base";
      const description = productDescription(product, comparison);
      const drawingPlaceholder = comparison ? "변경사항이 반영된 총조립도 도면번호" : "총조립도 도면번호";
      const descriptionField = comparison
        ? `<label><input aria-label="${geometryLabel} 설명" data-product-field="description" value="${esc(description)}" placeholder="CAD에 반영된 변경사항" /></label>`
        : `<div class="base-product-description" aria-label="Base 설명" aria-readonly="true">기존 형상</div>`;
      const action = comparison
        ? `<button class="condition-row-action remove" type="button" data-action="remove-comparison" data-index="${index}" title="해석 대상 제품 행 삭제" aria-label="${geometryLabel} 행 삭제">−</button>`
        : `<button class="primary condition-row-action" type="button" data-action="add-comparison" title="해석 대상 제품 행 추가" aria-label="해석 대상 제품 행 추가">+</button>`;
      return `<div class="product-table-row" data-product-id="${id}" data-product-index="${index}" data-product-role="${comparison ? "comparison" : "base"}">
        <div class="product-geometry-name row-identity" data-geometry-name>${geometryLabel}</div>
        <label><input aria-label="${geometryLabel} 도면번호 (NPDM MCAD)" data-product-field="drawing_no" value="${esc(productText(product, "drawing_no"))}" placeholder="${drawingPlaceholder}" pattern="[A-Za-z0-9-]+" title="영문, 숫자, 하이픈(-)만 입력" /></label>
        ${descriptionField}
        <div class="condition-row-actions">${action}</div>
      </div>`;
    }
    function renderProductCards(baseProduct, comparisons){
      const list = asArray(comparisons);
      $("productRows").innerHTML = productRow(asObj(baseProduct), 0, false) + list.map((product, index) => productRow(asObj(product), index, true)).join("");
    }
    function reindexProductRows(){
      Array.from(document.querySelectorAll('#productRows [data-product-role="comparison"]')).forEach((row, index) => {
        row.dataset.productIndex = String(index);
        const geometryLabel = `비교 ${index + 1}`;
        const geometryName = row.querySelector("[data-geometry-name]");
        if (geometryName) geometryName.textContent = geometryLabel;
        const removeButton = row.querySelector('[data-action="remove-comparison"]');
        if (removeButton) {
          removeButton.dataset.index = String(index);
          removeButton.setAttribute("aria-label", `${geometryLabel} 행 삭제`);
        }
      });
    }
    function collectProductCards(){
      return Array.from(document.querySelectorAll("#productRows [data-product-id]")).map(row => {
        const value = key => row.querySelector(`[data-product-field="${key}"]`)?.value || "";
        const role = row.dataset.productRole || "comparison";
        const description = role === "base" ? "Base" : value("description");
        return {geometry_id:row.dataset.productId, drawing_no:value("drawing_no"), display_name:description, display_name_custom:true, difference_from_base:role === "comparison" ? description : "", role};
      });
    }

    function conditionSnapshotGroups(){
      return asArray(asObj(requestState.request_context).condition_fieldset_snapshot);
    }

    function conditionGroupsForUi(groups){ return asArray(groups); }

    function conditionFieldByKey(){
      const out = {};
      asArray(asObj(requestState.conditions).fields).forEach(field => { if (field && field.key) out[field.key] = field; });
      return out;
    }

    function conditionCardIdentity(state=requestState){
      return asArray(asObj(asObj(state).conditions).condition_sets)
        .map(card => `${contextText(asObj(card).analysis_scope)}:${contextText(asObj(card).type)}:${contextText(asObj(card).id)}`)
        .join("|");
    }

    function newConditionCardId(type){
      const bytes = new Uint8Array(16);
      window.crypto.getRandomValues(bytes);
      const suffix = Array.from(bytes, value => value.toString(16).padStart(2, "0")).join("");
      return `${contextText(type)}_${suffix}`;
    }

    function conditionValuesMap(){
      return {};
    }

    function conditionOptionsMap(){
      return asObj(asObj(requestState.conditions).condition_options);
    }

    function conditionGroupOptionKey(group){
      const key = contextText(asObj(group).key);
      return key ? `${key}_enabled` : "";
    }

    function conditionGroupEnabled(group){
      const row = asObj(group);
      if (row.optional_section !== true) return true;
      const storageKey = conditionGroupOptionKey(row);
      const checkbox = storageKey ? document.querySelector(`input[data-condition-option="${CSS.escape(storageKey)}"]`) : null;
      if (checkbox) return checkbox.checked;
      const options = conditionOptionsMap();
      if (storageKey && Object.prototype.hasOwnProperty.call(options, storageKey)) return options[storageKey] === true;
      const optionKey = contextText(row.option_key);
      if (optionKey && Object.prototype.hasOwnProperty.call(options, optionKey)) return options[optionKey] === true;
      return false;
    }

    function conditionValueRows(key){
      const rawField = conditionFieldByKey()[key];
      const fieldRows = asArray(asObj(rawField).values);
      if (fieldRows.length) return fieldRows;
      const raw = conditionValuesMap()[key];
      const values = Array.isArray(raw) ? raw : (raw === undefined || raw === null || raw === "" ? [] : [raw]);
      return values.map((value, index) => {
        const text = rowValue(value);
        return {id:`${key}_value_${index+1}`, value:text, status:String(text || "").trim() ? "provided" : "missing", source:"user", display_value:String(text || "")};
      });
    }

    function conditionRowsForRender(key){
      const rows = conditionValueRows(key);
      return rows.length ? rows : [{value:""}];
    }

    function conditionRequirementChip(field){
      const level = contextText(asObj(field).required_level);
      if (level === "conditional_required") return `<span class="chip required">조건부 필수</span>`;
      if (level === "required" || asObj(field).required === true) return `<span class="chip required">필수</span>`;
      return "";
    }

    function hasCandidateRows(field){
      return asArray(field.values).some(row => asObj(row).source === "ai_suggested");
    }

    function isIntegratedProductGroup(value){
      const token = contextText(value).replace(/\s+/g, "").toLowerCase();
      return token.includes("통합형") || token.includes("integrated");
    }

    function shouldShowOperationModeControl(){
      return isContextLocked() && isIntegratedProductGroup(contextFromState().product_lineup);
    }

    function operationModeControlHtml(){
      if (!shouldShowOperationModeControl()) return "";
      const selected = contextText(contextFromState().operation_mode) || "실내";
      const options = operationModeOptions.map(value => `<option value="${esc(value)}" ${value === selected ? "selected" : ""}>${esc(value)}</option>`).join("");
      return `<label class="operation-mode-control">운전 구분<select id="operationModeSelect">${options}</select></label>`;
    }

    const heatExchangerTypes = ["Fin&Tube", "Micro-Channel"];
    const heatExchangerCascadeKeys = ["tube_diameter", "fin_type", "row_count", "fpi"];
    const heatExchangerScreenFieldLabels = {tube_diameter:"관 직경(Pi) / 채널 폭(Width)", fin_type:"Fin type", row_count:"열 수", fpi:"FPI / FPDM"};

    function heatExchangerType(cards){
      const explicit = contextText(asObj(asArray(cards)[0]).heat_exchanger_type);
      if (heatExchangerTypes.includes(explicit)) return explicit;
      const tubeDiameter = fieldDisplayValue(asObj(asObj(asArray(cards)[0]).fields).tube_diameter);
      return tubeDiameter.toUpperCase().startsWith("W") ? "Micro-Channel" : "Fin&Tube";
    }

    function heatExchangerFieldLabels(type){
      return type === "Micro-Channel"
        ? {tube_diameter:"채널 폭 (Witdth)", fin_type:"Fin type", row_count:"열 수", fpi:"FPDM"}
        : {tube_diameter:"관 직경(Pi)", fin_type:"Fin type", row_count:"열 수", fpi:"FPI"};
    }

    function heatExchangerCatalogValue(row, key, type){
      if (type === "Micro-Channel" && key === "fin_type") return "Flat";
      return contextText(asObj(row)[key]);
    }

    function heatExchangerCatalogRows(type){
      return heatExchangerCatalog.filter(row => {
        const microChannel = contextText(asObj(row).tube_diameter).toUpperCase().startsWith("W");
        return microChannel === (type === "Micro-Channel");
      });
    }

    function heatExchangerOptions(key, selections, type){
      const keyIndex = heatExchangerCascadeKeys.indexOf(key);
      if (keyIndex < 0) return [];
      const filtered = heatExchangerCatalogRows(type).filter(row => heatExchangerCascadeKeys
        .slice(0, keyIndex)
        .every(parentKey => heatExchangerCatalogValue(row, parentKey, type) === contextText(asObj(selections)[parentKey])));
      return uniqueValues(filtered.map(row => heatExchangerCatalogValue(row, key, type)));
    }

    function heatExchangerCustomFieldId(cardId, key){
      return `${contextText(cardId)}:${contextText(key)}`;
    }

    function clearHeatExchangerCustomFields(cardId, keys){
      asArray(keys).forEach(key => heatExchangerCustomFields.delete(heatExchangerCustomFieldId(cardId, key)));
    }

    function heatExchangerSelectHtml(cardId, key, fields, showLabel, fieldLabels, type){
      const selections = Object.fromEntries(heatExchangerCascadeKeys.map(fieldKey => [fieldKey, fieldDisplayValue(fields[fieldKey])]));
      if (type === "Micro-Channel") selections.fin_type = "Flat";
      const keyIndex = heatExchangerCascadeKeys.indexOf(key);
      const parentKeys = heatExchangerCascadeKeys.slice(0, keyIndex);
      const missingParentKey = parentKeys.find(parentKey => !contextText(selections[parentKey])) || "";
      const disabled = key === "fin_type" && type === "Micro-Channel"
        ? true
        : (keyIndex === 0 ? false : !!missingParentKey);
      const options = key === "fin_type" && type === "Micro-Channel" ? ["Flat"] : (disabled ? [] : heatExchangerOptions(key, selections, type));
      const selected = options.includes(contextText(selections[key])) ? contextText(selections[key]) : "";
      const customFieldId = heatExchangerCustomFieldId(cardId, key);
      const customAllowed = !(key === "fin_type" && type === "Micro-Channel");
      const customMode = !disabled && customAllowed && (heatExchangerCustomFields.has(customFieldId) || (!!contextText(selections[key]) && !options.includes(contextText(selections[key]))));
      if (customMode) {
        heatExchangerCustomFields.add(customFieldId);
        const customInput = `<span class="prep-custom-control heat-exchanger-custom-control"><input data-card-id="${esc(cardId)}" data-card-field="${esc(key)}" data-heat-exchanger-custom-field="${esc(key)}" value="${esc(selections[key])}" aria-label="${esc(fieldLabels[key])} 직접 입력" /><button type="button" data-heat-exchanger-restore="${esc(key)}" data-card-id="${esc(cardId)}" title="${esc(fieldLabels[key])} 드롭다운으로 돌아가기" aria-label="${esc(fieldLabels[key])} 드롭다운으로 돌아가기">↩</button></span>`;
        return showLabel ? `<label>${esc(fieldLabels[key])}${customInput}</label>` : customInput;
      }
      const placeholder = disabled && missingParentKey ? `${fieldLabels[missingParentKey]} 먼저 선택` : `${fieldLabels[key]} 선택`;
      const attributes = `data-card-id="${esc(cardId)}" data-card-field="${esc(key)}" data-heat-exchanger-field="${esc(key)}" aria-label="${esc(fieldLabels[key])}"`;
      const customOption = customAllowed && !disabled ? `<option value="__custom__">직접 입력</option>` : "";
      const optionHtml = [`<option value="" disabled hidden ${selected ? "" : "selected"}>${esc(placeholder)}</option>`, ...options.map(value => `<option value="${esc(value)}" ${value === selected ? "selected" : ""}>${esc(value)}</option>`), customOption].join("");
      const select = `<select ${attributes} ${disabled ? "disabled" : ""}>${optionHtml}</select>`;
      return showLabel ? `<label>${esc(fieldLabels[key])}${select}</label>` : select;
    }

    function handleHeatExchangerCascadeChange(select){
      const changedKey = select.dataset.heatExchangerField || "";
      const changedIndex = heatExchangerCascadeKeys.indexOf(changedKey);
      if (changedIndex < 0) return;
      const cards = collectConditionSets();
      const card = cards.find(item => contextText(asObj(item).id) === select.dataset.cardId);
      if (!card) return;
      const downstreamKeys = heatExchangerCascadeKeys.slice(changedIndex + 1);
      clearHeatExchangerCustomFields(card.id, downstreamKeys);
      if (select.value === "__custom__") {
        heatExchangerCustomFields.add(heatExchangerCustomFieldId(card.id, changedKey));
        card.fields[changedKey] = "";
      } else {
        heatExchangerCustomFields.delete(heatExchangerCustomFieldId(card.id, changedKey));
      }
      downstreamKeys.forEach(key => { card.fields[key] = ""; });
      if (heatExchangerType([card]) === "Micro-Channel") card.fields.fin_type = "Flat";
      requestState.conditions = {...asObj(requestState.conditions), condition_sets:cards};
      renderConditionFields();
      const focusKey = select.value === "__custom__" ? changedKey : heatExchangerCascadeKeys[Math.min(changedIndex + 1, heatExchangerCascadeKeys.length - 1)];
      window.requestAnimationFrame(() => document.querySelector(`[data-card-id="${CSS.escape(contextText(card.id))}"][data-heat-exchanger-custom-field="${CSS.escape(focusKey)}"], [data-card-id="${CSS.escape(contextText(card.id))}"][data-heat-exchanger-field="${CSS.escape(focusKey)}"]`)?.focus());
      schedulePreviewRefresh();
    }

    function handleHeatExchangerCustomInput(input){
      const changedKey = input.dataset.heatExchangerCustomField || "";
      const changedIndex = heatExchangerCascadeKeys.indexOf(changedKey);
      if (changedIndex < 0) return;
      const cards = collectConditionSets();
      const card = cards.find(item => contextText(asObj(item).id) === input.dataset.cardId);
      if (!card) return;
      const downstreamKeys = heatExchangerCascadeKeys.slice(changedIndex + 1);
      clearHeatExchangerCustomFields(card.id, downstreamKeys);
      downstreamKeys.forEach(key => { card.fields[key] = ""; });
      if (heatExchangerType([card]) === "Micro-Channel") card.fields.fin_type = "Flat";
      requestState.conditions = {...asObj(requestState.conditions), condition_sets:cards};
      renderConditionFields();
      const focusKey = heatExchangerCascadeKeys[Math.min(changedIndex + 1, heatExchangerCascadeKeys.length - 1)];
      window.requestAnimationFrame(() => document.querySelector(`[data-card-id="${CSS.escape(contextText(card.id))}"][data-heat-exchanger-custom-field="${CSS.escape(focusKey)}"], [data-card-id="${CSS.escape(contextText(card.id))}"][data-heat-exchanger-field="${CSS.escape(focusKey)}"]`)?.focus());
      schedulePreviewRefresh();
    }

    function restoreHeatExchangerDropdown(button){
      const key = button.dataset.heatExchangerRestore || "";
      const keyIndex = heatExchangerCascadeKeys.indexOf(key);
      if (keyIndex < 0) return;
      const cards = collectConditionSets();
      const card = cards.find(item => contextText(asObj(item).id) === button.dataset.cardId);
      if (!card) return;
      const resetKeys = heatExchangerCascadeKeys.slice(keyIndex);
      clearHeatExchangerCustomFields(card.id, resetKeys);
      resetKeys.forEach(fieldKey => { card.fields[fieldKey] = ""; });
      if (heatExchangerType([card]) === "Micro-Channel") card.fields.fin_type = "Flat";
      requestState.conditions = {...asObj(requestState.conditions), condition_sets:cards};
      renderConditionFields();
      window.requestAnimationFrame(() => document.querySelector(`[data-card-id="${CSS.escape(contextText(card.id))}"][data-heat-exchanger-field="${CSS.escape(key)}"]`)?.focus());
      schedulePreviewRefresh();
    }

    function handleHeatExchangerTypeChange(select){
      const selectedType = heatExchangerTypes.includes(select.value) ? select.value : heatExchangerTypes[0];
      const cards = collectConditionSets();
      const card = cards.find(item => contextText(asObj(item).id) === select.dataset.cardId);
      if (!card || contextText(asObj(card).type) !== "heat_exchanger") return;
      clearHeatExchangerCustomFields(card.id, heatExchangerCascadeKeys);
      card.heat_exchanger_type = selectedType;
      card.fields.tube_diameter = "";
      card.fields.fin_type = selectedType === "Micro-Channel" ? "Flat" : "";
      card.fields.row_count = "";
      card.fields.fpi = "";
      requestState.conditions = {...asObj(requestState.conditions), condition_sets:cards};
      renderConditionFields();
      window.requestAnimationFrame(() => document.querySelector(`[data-card-id="${CSS.escape(contextText(card.id))}"][data-heat-exchanger-field="tube_diameter"]`)?.focus());
      schedulePreviewRefresh();
    }

    function heatExchangerTypeSelectHtml(cardId, card, showLabel){
      const selected = heatExchangerType([card]);
      const options = heatExchangerTypes.map(value => `<option value="${esc(value)}" ${value === selected ? "selected" : ""}>${esc(value)}</option>`).join("");
      const select = `<select data-card-id="${esc(cardId)}" data-heat-exchanger-type aria-label="HEX type">${options}</select>`;
      return showLabel ? `<label>HEX Type${select}</label>` : select;
    }

    function resizeFanRpmInputs(cardId, rawCount){
      preserveEditorDraftBeforeRerender();
      const count = Number(rawCount);
      const cards = collectConditionSets();
      const card = cards.find(item => contextText(asObj(item).id) === cardId && contextText(asObj(item).type) === "operating");
      if (!card) return;
      const current = asArray(card.fans);
      if (!Number.isInteger(count) || count < 1) {
        renderConditionFields();
        return false;
      }
      if (count > 10) {
        renderConditionFields();
        showFanLimitModal(cardId);
        return false;
      }
      card.fans = Array.from({length:count}, (_, index) => {
        const fan = asObj(current[index]);
        return {
          id:contextText(fan.id) || `fan_${index + 1}`,
          name:contextText(fan.name),
          location:contextText(fan.location),
          running:true,
          values:{fan_rpm:contextText(asObj(fan.values).fan_rpm)},
        };
      });
      if (count === 1 || current.length === 1) card.fan_rpm_mode = "";
      if (count === 1 && expandedFanCardId === cardId) expandedFanCardId = "";
      requestState.conditions = {...asObj(requestState.conditions), condition_sets:cards};
      renderConditionFields();
      const focusIndex = Math.min(current.length, count - 1);
      const focusSelector = count === 1
        ? `[data-card-id="${CSS.escape(cardId)}"][data-card-field="fan_rpm"]`
        : `[data-card-id="${CSS.escape(cardId)}"][data-fan-rpm-mode]`;
      window.requestAnimationFrame(() => document.querySelector(focusSelector)?.focus());
      schedulePreviewRefresh();
      return true;
    }

    function showFanLimitModal(cardId){
      const modal = $("fanLimitModal");
      if (!modal) return;
      modal.dataset.returnCardId = cardId;
      modal.hidden = false;
      window.requestAnimationFrame(() => $("fanLimitConfirm")?.focus());
    }

    function hideFanLimitModal(){
      const modal = $("fanLimitModal");
      if (!modal) return;
      const cardId = contextText(modal.dataset.returnCardId);
      modal.hidden = true;
      modal.dataset.returnCardId = "";
      window.requestAnimationFrame(() => document.querySelector(`[data-card-id="${CSS.escape(cardId)}"][data-fan-count-custom], [data-card-id="${CSS.escape(cardId)}"][data-fan-count]`)?.focus());
    }

    function handleFanRpmModeChange(select){
      preserveEditorDraftBeforeRerender();
      const cardId = contextText(select.dataset.cardId);
      const cards = collectConditionSets();
      const card = cards.find(item => contextText(asObj(item).id) === cardId && contextText(asObj(item).type) === "operating");
      if (!card || asArray(card.fans).length < 2) return;
      card.fan_rpm_mode = ["common", "individual"].includes(select.value) ? select.value : "";
      if (card.fan_rpm_mode !== "individual" && expandedFanCardId === cardId) expandedFanCardId = "";
      requestState.conditions = {...asObj(requestState.conditions), condition_sets:cards};
      renderConditionFields();
      const focusSelector = card.fan_rpm_mode === "individual"
        ? `[data-card-id="${CSS.escape(cardId)}"][data-fan-detail-toggle]`
        : card.fan_rpm_mode === "common"
          ? `[data-card-id="${CSS.escape(cardId)}"][data-fan-common-rpm]`
          : `[data-card-id="${CSS.escape(cardId)}"][data-fan-rpm-mode]`;
      window.requestAnimationFrame(() => document.querySelector(focusSelector)?.focus());
      schedulePreviewRefresh();
    }

    function toggleFanDetail(button){
      preserveEditorDraftBeforeRerender();
      const cardId = contextText(button.dataset.cardId);
      expandedFanCardId = expandedFanCardId === cardId ? "" : cardId;
      renderConditionFields();
      const target = expandedFanCardId
        ? document.querySelector(`[data-card-id="${CSS.escape(cardId)}"][data-fan-index="0"][data-card-field="fan_location"]`)
        : document.querySelector(`[data-card-id="${CSS.escape(cardId)}"][data-fan-detail-toggle]`);
      window.requestAnimationFrame(() => target?.focus());
    }

    function handleFanCountChange(select){
      const cardId = contextText(select.dataset.cardId);
      if (select.value === "__custom__") {
        preserveEditorDraftBeforeRerender();
        fanCountCustomCards.add(cardId);
        renderConditionFields();
        window.requestAnimationFrame(() => document.querySelector(`[data-card-id="${CSS.escape(cardId)}"][data-fan-count-custom]`)?.focus());
        return;
      }
      fanCountCustomCards.delete(cardId);
      resizeFanRpmInputs(cardId, select.value);
    }

    function restoreFanCountDropdown(button){
      const cardId = contextText(button.dataset.cardId);
      fanCountCustomCards.delete(cardId);
      resizeFanRpmInputs(cardId, 1);
      window.requestAnimationFrame(() => document.querySelector(`[data-card-id="${CSS.escape(cardId)}"][data-fan-count]`)?.focus());
    }

    function renderConditionFields(){
      const scopeTabs = $("conditionScopeTabs");
      const requestedScopes = requestedAnalysisScopes();
      if (!requestedScopes.includes(activeConditionScope)) activeConditionScope = requestedScopes[0];
      if (scopeTabs) scopeTabs.innerHTML = scopeTabsHtml("conditions", activeConditionScope);
      if (!isContextLocked()) {
        $("conditionFields").innerHTML = `<div class="empty">조합 확정 후 조건 입력항목을 표시합니다.</div>`;
        return;
      }
      const scoped = requestedScopes[0] !== "";
      const cards = asArray(asObj(requestState.conditions).condition_sets)
        .filter(card => !scoped || contextText(asObj(card).analysis_scope) === activeConditionScope);
      const types = uniqueValues(cards.map(card => contextText(asObj(card).type)));
      const fieldsetInputMetadata = new Map(conditionSnapshotGroups().flatMap(group =>
        asArray(asObj(group).fields).map(field => [contextText(asObj(field).key), asObj(field)])
      ));
      const valueOrNoneEnabled = metadata => metadata.allow_custom_input === true && asArray(metadata.allowed_values).map(contextText).includes("없음");
      const typeLabels = {operating:"운전 조건",heat_exchanger:"열교환기 사양",supply_air:"취출 공기 조건",space_environment:"공간 환경 조건"};
      const fieldLabels = {name:"사양",fan:"운전",fan_count:"팬 개수",fan_location:"위치",fan_rpm:"팬 회전수(RPM)",fin_type:"Fin type",tube_diameter:"관 직경(Pi)",row_count:"열 수",fpi:"FPI",heat_exchanger_temp:"취출 온도 (°C)",heat_exchanger_rh:"취출 상대습도 (%)",room_temp:"공간 온도 (°C)",room_rh:"공간 상대습도 (%)"};
      const fieldKeysFor = (type, fields) => {
        const orderedKeys = {
          operating: [],
          heat_exchanger: ["name", "tube_diameter", "fin_type", "row_count", "fpi"],
          supply_air: ["heat_exchanger_temp", "heat_exchanger_rh"],
          space_environment: ["room_temp", "room_rh"],
        };
        return (orderedKeys[type] || Object.keys(fields)).filter(key => Object.prototype.hasOwnProperty.call(fields, key));
      };
      const inputHtml = (cardId, key, value, showLabel, fanIndex) => {
        const attributes = fanIndex === undefined
          ? `data-card-id="${esc(cardId)}" data-card-field="${esc(key)}"`
          : `data-card-id="${esc(cardId)}" data-fan-index="${fanIndex}" data-card-field="${esc(key)}"`;
        if (fanIndex === undefined && valueOrNoneEnabled(asObj(fieldsetInputMetadata.get(key)))) {
          const unavailable = contextText(value) === "없음";
          const menuId = `condition-${cardId}-${key}-mode`;
          const input = `<input ${attributes} value="${esc(value)}" data-undecided-input data-undecided-mode="${unavailable ? "undecided" : "custom"}" data-custom-placeholder="온도를 입력하세요" role="combobox" aria-autocomplete="none" aria-haspopup="listbox" aria-controls="${esc(menuId)}" aria-expanded="false" autocomplete="off" ${unavailable ? "readonly" : ""} aria-label="${esc(fieldLabels[key] || key)}" />`;
          const control = `<div class="undecided-combobox condition-temperature-combobox" data-undecided-combobox data-undecided-value="없음">${input}<button class="undecided-combobox-toggle" type="button" data-undecided-toggle aria-label="${esc(fieldLabels[key] || key)} 입력 방식 선택" aria-controls="${esc(menuId)}" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 9 5 5 5-5"></path></svg></button><div class="undecided-combobox-menu" id="${esc(menuId)}" data-undecided-menu role="listbox" aria-label="${esc(fieldLabels[key] || key)} 입력 방식" hidden><button class="undecided-combobox-option" type="button" role="option" data-undecided-mode="custom" aria-selected="${String(!unavailable)}">직접 입력</button><button class="undecided-combobox-option" type="button" role="option" data-undecided-mode="undecided" aria-selected="${String(unavailable)}">없음</button></div></div>`;
          return showLabel ? `<label>${esc(fieldLabels[key] || key)}${control}</label>` : control;
        }
        const input = `<input ${attributes} value="${esc(value)}" aria-label="${esc(fieldLabels[key] || key)}" />`;
        return showLabel ? `<label>${esc(fieldLabels[key] || key)}${input}</label>` : input;
      };
      const fixedTextHtml = (key, value, showLabel) => {
        const text = `<div class="product-geometry-name condition-spec-name row-identity" data-spec-name aria-label="${esc(fieldLabels[key] || key)}" aria-readonly="true">${esc(value)}</div>`;
        return showLabel ? `<label>${esc(fieldLabels[key] || key)}${text}</label>` : text;
      };
      const fanCountControlHtml = (cardId, fans, showLabel) => {
        const count = Math.max(1, fans.length);
        const customMode = fanCountCustomCards.has(cardId) || count > 4;
        let control = "";
        if (customMode) {
          fanCountCustomCards.add(cardId);
          control = `<span class="prep-custom-control fan-count-custom-control"><input type="number" min="1" max="10" step="1" inputmode="numeric" data-card-id="${esc(cardId)}" data-fan-count-custom value="${count}" aria-label="개수 직접 입력" /><button type="button" data-fan-count-restore data-card-id="${esc(cardId)}" title="개수 목록으로 돌아가기" aria-label="개수 목록으로 돌아가기">↩</button></span>`;
        } else {
          const options = [1,2,3,4].map(value => `<option value="${value}" ${value === count ? "selected" : ""}>${value}</option>`).join("");
          control = `<select data-card-id="${esc(cardId)}" data-fan-count aria-label="개수">${options}<option value="__custom__">직접 입력</option></select>`;
        }
        return showLabel ? `<label>${esc(fieldLabels.fan_count)}${control}</label>` : control;
      };
      const commonFanRpm = fans => {
        const rpms = asArray(fans).map(fan => contextText(asObj(asObj(fan).values).fan_rpm));
        return rpms.length && rpms.every(rpm => rpm && rpm === rpms[0]) ? rpms[0] : "";
      };
      const fanConfigurationInputsHtml = (cardId, card, fans, showLabel) => {
        const multiple = fans.length >= 2;
        const label = showLabel ? `<span>팬 회전 설정</span>` : "";
        if (!multiple) {
          const rpm = contextText(asObj(asObj(fans[0]).values).fan_rpm);
          return `<label class="fan-input-column">${label}<span class="fan-rpm-editor single"><span class="fan-rpm-control"><input data-card-id="${esc(cardId)}" data-fan-index="0" data-card-field="fan_rpm" value="${esc(rpm)}" aria-label="${esc(fieldLabels.fan_rpm)}" /><span class="fan-rpm-unit">RPM</span></span></span></label>`;
        }
        const mode = ["common", "individual"].includes(contextText(card.fan_rpm_mode)) ? contextText(card.fan_rpm_mode) : "";
        const modeOptions = `<option value="" ${mode ? "" : "selected"}>입력 방식 선택</option><option value="common" ${mode === "common" ? "selected" : ""}>모든 팬 동일</option><option value="individual" ${mode === "individual" ? "selected" : ""}>팬별 입력</option>`;
        const modeSelect = `<select data-card-id="${esc(cardId)}" data-fan-rpm-mode aria-label="팬 회전수 입력방식">${modeOptions}</select>`;
        if (mode === "common") {
          const rpm = commonFanRpm(fans);
          return `<label class="fan-input-column">${label}<span class="fan-rpm-editor"><span class="fan-rpm-control"><input data-card-id="${esc(cardId)}" data-card-field="fan_rpm" data-fan-common-rpm value="${esc(rpm)}" aria-label="공통 팬 회전수(RPM)" /><span class="fan-rpm-unit">RPM</span></span>${modeSelect}</span></label>`;
        }
        if (mode !== "individual") return `<label class="fan-input-column">${label}<span class="fan-rpm-editor mode-pending">${modeSelect}</span></label>`;
        const expanded = expandedFanCardId === cardId;
        const detailInputs = fans.map((rawFan, fanIndex) => {
          const fan = asObj(rawFan);
          return `<div class="fan-input-set" data-fan-set="${fanIndex + 1}"><span class="fan-input-order" aria-hidden="true">${fanIndex + 1}</span><label class="fan-input-column"><span>${esc(fieldLabels.fan_location)}</span><input data-card-id="${esc(cardId)}" data-fan-index="${fanIndex}" data-card-field="fan_location" value="${esc(fan.location)}" placeholder="예 : 상/중/하" aria-label="${esc(fieldLabels.fan_location)} ${fanIndex + 1}" /></label><label class="fan-input-column"><span>${esc(fieldLabels.fan_rpm)}</span><input data-card-id="${esc(cardId)}" data-fan-index="${fanIndex}" data-card-field="fan_rpm" value="${esc(asObj(fan.values).fan_rpm)}" aria-label="${esc(fieldLabels.fan_rpm)} ${fanIndex + 1}" /></label></div>`;
        }).join("");
        return `<label class="fan-input-column">${label}<span class="fan-rpm-editor"><button class="ghost fan-detail-toggle" type="button" data-card-id="${esc(cardId)}" data-fan-detail-toggle aria-controls="fan-detail-${esc(cardId)}" aria-expanded="${String(expanded)}"><span>팬별 설정</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 9 5 5 5-5"></path></svg></button>${modeSelect}</span></label><div class="fan-detail" id="fan-detail-${esc(cardId)}" data-fan-detail-card="${esc(cardId)}" ${expanded ? "" : "hidden"}><h4 class="fan-detail-title">팬별 회전수 설정</h4><div class="fan-detail-grid">${detailInputs}</div></div>`;
      };
      const rowHtml = (card, isFirst, rowIndex) => {
        const row = asObj(card), cardId = contextText(row.id), type = contextText(row.type), fields = asObj(row.fields);
        const fieldKeys = fieldKeysFor(type, fields);
        const exchangerType = type === "heat_exchanger" ? heatExchangerType([row]) : "";
        const rowFieldLabels = type === "heat_exchanger" ? {...fieldLabels, ...heatExchangerScreenFieldLabels} : fieldLabels;
        const fans = type === "operating" ? (asArray(row.fans).length ? asArray(row.fans) : [{id:"fan_1",name:"",location:"",running:true,values:{fan_rpm:""}}]) : [];
        const inputs = type === "operating"
          ? `${fixedTextHtml("fan", `운전 ${rowIndex}`, false)}${fanCountControlHtml(cardId, fans, isFirst)}${fanConfigurationInputsHtml(cardId, row, fans, isFirst)}`
          : fieldKeys.map(key => type === "heat_exchanger" && key === "name"
            ? `${fixedTextHtml(key, `사양 ${rowIndex}`, false)}${heatExchangerTypeSelectHtml(cardId, row, isFirst)}`
            : (type === "heat_exchanger" && heatExchangerCascadeKeys.includes(key)
              ? heatExchangerSelectHtml(cardId, key, fields, isFirst, rowFieldLabels, exchangerType)
              : inputHtml(cardId, key, fieldDisplayValue(fields[key]), isFirst))).join("");
        const remove = `<button class="condition-row-action remove" type="button" data-action="remove-condition-card" data-card-id="${esc(cardId)}" title="조건 행 삭제" aria-label="조건 행 삭제">−</button>`;
        const action = isFirst
          ? `<div class="condition-row-actions"><button class="primary condition-row-action" type="button" data-action="add-condition-card" data-card-type="${esc(type)}" title="${esc(typeLabels[type])} 추가" aria-label="${esc(typeLabels[type])} 추가">+</button></div>`
          : `<div class="condition-row-actions">${remove}</div>`;
        return `<div class="condition-card-row" data-condition-card="${esc(cardId)}" style="--field-count:${type === "operating" ? 3 : fieldKeys.length}">${inputs}${action}</div>`;
      };
      const groupHtml = type => {
        const list = cards.filter(card => contextText(asObj(card).type) === type);
        if (!list.length) return "";
        const body = `<div class="condition-card-rows">${list.map((card, index) => rowHtml(card, index === 0, index + 1)).join("")}</div>`;
        return `<article class="condition-group condition-card-type condition-card-type-${esc(type)}"><div class="condition-group-head"><h3>${esc(typeLabels[type])}</h3></div>${body}</article>`;
      };
      const primary = types.filter(type => type !== "supply_air" && type !== "space_environment").map(groupHtml).join("");
      const environment = ["space_environment", "supply_air"].filter(type => types.includes(type)).map(groupHtml).join("");
      const temperatureGuidance = Array.from(fieldsetInputMetadata.values()).some(valueOrNoneEnabled)
        ? `<p class="condition-temperature-guidance">${esc("온도 조건에 따라 해석 결과가 달라질 수 있으므로, 확인된 온도 조건이 있다면 입력해 주세요.")}<br>${esc("별도 온도 조건이 없는 경우에만 ‘없음’을 선택해 주세요.")}</p>`
        : "";
      $("conditionFields").innerHTML = `<div class="condition-card-layout">${primary ? `<div class="condition-primary-grid">${primary}</div>` : ""}${environment ? `<div class="condition-environment-grid">${environment}</div>${temperatureGuidance}` : ""}</div>`;
      wireUndecidedComboboxes($("conditionFields"));
    }

    function syncEditorFromState(){
      syncRequestContextDraftFromState();
      const basic = asObj(requestState.basic_info);
      basicKeys.forEach(key => {
        const input = pathInput("basic_info", key);
        const value = fieldDisplayValue(basic[key]);
        if (input) input.value = value;
        syncDropdownForPath(`basic_info.${key}`, value);
      });
      const overview = asObj(requestState.analysis_overview);
      overviewInputKeys.forEach(key => {
        const input = pathInput("analysis_overview", key);
        const value = fieldDisplayValue(overview[key]);
        if (input) input.value = value;
        syncDropdownForPath(`analysis_overview.${key}`, value);
        syncUndecidedCombobox(`analysis_overview.${key}`, value);
      });
      syncPmsProjectControl();
      const geometry = asObj(requestState.geometry);
      renderProductCards(geometry.base_product, geometry.comparison_products);
      renderConditionFields();
      renderRequestPrepCard();
      refreshAnalysisResultGuidance();
      updateGate();
      renderDerivedPanels();
      updateTopChrome();
    }
    function collectConditionSets(){
      const heatExchangerIndexes = new Map();
      const operatingIndexes = new Map();
      return asArray(asObj(requestState.conditions).condition_sets).map(raw => {
        const card = JSON.parse(JSON.stringify(raw));
        const id = contextText(card.id);
        const scope = contextText(card.analysis_scope);
        if (contextText(card.type) === "heat_exchanger") {
          const typeSelect = document.querySelector(`select[data-card-id="${CSS.escape(id)}"][data-heat-exchanger-type]`);
          card.heat_exchanger_type = heatExchangerTypes.includes(typeSelect?.value) ? typeSelect.value : heatExchangerType([card]);
        }
        asArray(card.fans).forEach((fan, index) => {
          const locationInput = document.querySelector(`[data-card-id="${CSS.escape(id)}"][data-fan-index="${index}"][data-card-field="fan_location"]`);
          const rpmInput = document.querySelector(`[data-card-id="${CSS.escape(id)}"][data-fan-index="${index}"][data-card-field="fan_rpm"]`) || (card.fans.length === 1 ? document.querySelector(`[data-card-id="${CSS.escape(id)}"][data-card-field="fan_rpm"]`) : null);
          if (locationInput) fan.location = locationInput.value.trim();
          if (rpmInput) fan.values = {fan_rpm: rpmInput.value.trim()};
        });
        Object.keys(asObj(card.fields)).forEach(key => { const input = document.querySelector(`[data-card-id="${CSS.escape(id)}"][data-card-field="${key}"]`); if (input) card.fields[key] = input.value.trim(); });
        if (contextText(card.type) === "operating") {
          card.fan_rpm_mode = asArray(card.fans).length >= 2 && ["common", "individual"].includes(contextText(card.fan_rpm_mode)) ? contextText(card.fan_rpm_mode) : "";
          const modeSelect = document.querySelector(`[data-card-id="${CSS.escape(id)}"][data-fan-rpm-mode]`);
          const commonRpmInput = document.querySelector(`[data-card-id="${CSS.escape(id)}"][data-fan-common-rpm]`);
          if (commonRpmInput) {
            asArray(card.fans).forEach(fan => { fan.values = {fan_rpm: commonRpmInput.value.trim()}; });
          }
          if (modeSelect) card.fan_rpm_mode = ["common", "individual"].includes(modeSelect.value) ? modeSelect.value : "";
          const operatingIndex = (operatingIndexes.get(scope) || 0) + 1;
          operatingIndexes.set(scope, operatingIndex);
          card.name = `운전 ${operatingIndex}`;
          card.fan_count = asArray(card.fans).length;
          card.fan_locations = asArray(card.fans).map(fan => contextText(asObj(fan).location));
          card.fan_rpms = asArray(card.fans).map(fan => contextText(asObj(asObj(fan).values).fan_rpm));
        }
        if (contextText(card.type) === "heat_exchanger") {
          const heatExchangerIndex = (heatExchangerIndexes.get(scope) || 0) + 1;
          heatExchangerIndexes.set(scope, heatExchangerIndex);
          card.fields.name = `사양 ${heatExchangerIndex}`;
        }
        return card;
      });
    }

    async function refreshAnalysisResultGuidance(){
      const root = $("analysisResultGuidance");
      if (!root) return;
      const analysisType = contextText(contextFromState().analysis_type);
      const label = $("analysisResultGuidanceLabel");
      if (label) label.textContent = `해석 결과 안내${analysisType ? ` - ${analysisType}` : ""}`;
      const panel = message => `<span class="analysis-result-guidance-icon" aria-hidden="true">i</span><p>${message}</p>`;
      if (!analysisType) {
        root.innerHTML = panel("해석유형을 선택하면 결과 안내를 표시합니다.");
        return;
      }
      root.innerHTML = panel("해석 결과 안내를 불러오는 중입니다.");
      try {
        const response = await fetch(`/api/analysis-type-guidance?analysis_type=${encodeURIComponent(analysisType)}`);
        const data = await response.json();
        if (!response.ok || data.ok === false) throw new Error(data.message || "결과 안내를 조회하지 못했습니다.");
        root.innerHTML = panel(esc(data.guidance || ""));
      } catch (err) {
        root.innerHTML = `<span class="analysis-result-guidance-icon" aria-hidden="true">i</span><div><p>해석 결과 안내를 불러오지 못했습니다.</p><button class="ghost" type="button" id="retryAnalysisResultGuidance">다시 시도</button></div>`;
      }
    }


    function collectCaseRows(){
      return asArray(asObj(requestState.case_matrix).rows).map(raw => {
        const row = JSON.parse(JSON.stringify(raw));
        const id = contextText(row.case_id);
        const geometry = document.querySelector(`select[data-case-row-id="${CSS.escape(id)}"][data-case-field="geometry_id"]`);
        const visibleCells = {...asObj(row.visible_cells)};
        if (geometry) {
          row.geometry_id = geometry.value;
          visibleCells.geometry_id = contextText(geometry.selectedOptions?.[0]?.textContent);
        }
        const values = {...asObj(row.condition_values)};
        document.querySelectorAll(`select[data-case-row-id="${CSS.escape(id)}"][data-case-field]`).forEach(select => {
          const key = select.dataset.caseField;
          if (key && key !== "geometry_id") {
            values[key] = select.value;
            visibleCells[key] = contextText(select.selectedOptions?.[0]?.textContent);
          }
        });
        row.condition_values = values;
        row.visible_cells = visibleCells;
        return row;
      });
    }

    function preserveCaseSelections(changedSelect=null){
      const matrix = asObj(requestState.case_matrix);
      requestState = {...requestState, case_matrix:{...matrix, rows:collectCaseRows()}};
      if (typeof resolveCaseImpactSelections === "function") resolveCaseImpactSelections();
      clearCaseConfigurationWarning();
      if (changedSelect) updateCaseSelectSummary(changedSelect);
      caseValidationPending = true;
      renderCaseValidationStatus();
      lastCaseDeleteNoticeVisible = false;
      document.querySelector("[data-last-case-delete-notice]")?.remove();
      schedulePreviewRefresh();
    }

    function collectState(){
      const products = collectProductCards();
      const next = {
        metadata: {
          ...asObj(requestState.metadata),
          rag_enabled: false,
          rag_scope: "LG CFD Reports 2025 해석보고서",
          rag_ranking: "product_first",
          active_top_tab: "write",
          touched_fields: Array.from(touchedFields),
          chat_history: chatHistory,
        },
        request_context: collectRequestContextDraft(),
        basic_info: {},
        analysis_overview: {},
        geometry: {
          base_product: products[0] || asObj(requestState.geometry).base_product,
          comparison_products: products.slice(1),
        },
        conditions: {
          mode: asObj(requestState.conditions).mode || "standard",
          condition_sets: collectConditionSets(),
        },
        case_matrix: { ...asObj(requestState.case_matrix), rows: collectCaseRows() },
        review: asObj(requestState.review),
      };
      basicKeys.forEach(key => { const input = pathInput("basic_info", key); next.basic_info[key] = input ? input.value : ""; });
      overviewInputKeys.forEach(key => { const input = pathInput("analysis_overview", key); next.analysis_overview[key] = input ? input.value : ""; });
      ["selected_pms_project_id", "pms_project_code", "region"].forEach(key => { next.analysis_overview[key] = fieldValue(asObj(requestState.analysis_overview)[key], ""); });
      return next;
    }

    function preserveEditorDraftBeforeRerender(){
      // Condition row actions rebuild the whole editor. Capture every visible
      // screen first so geometry and overview edits are not replaced by an
      // older asynchronous preview response still stored in requestState.
      requestState = collectState();
    }

    async function postJson(url, payload){
      const res = await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload || {})});
      const text = await res.text();
      let data = {};
      try {
        data = text ? JSON.parse(text) : {};
      } catch (err) {
        throw new Error(`서버 응답을 읽지 못했습니다 (${res.status}). ${text.slice(0, 120)}`);
      }
      if (!res.ok || data.ok === false) {
        const missing = asArray(data.missing_fields).length ? ` 누락: ${asArray(data.missing_fields).join(", ")}` : "";
        throw new Error((data.assistant || data.message || `Request failed: ${res.status}`) + missing);
      }
      return data;
    }

    async function postState(url, extra={}){
      return postJson(url, {state:collectState(), ...extra});
    }

    async function startNewRequest(){
      const data = await postJson("/api/request/new", {});
      Object.assign(orchestratorPanelState, {conversationId:"", requestId:"", requestVersion:null, dirty:true, loading:false, caseMatrixSyncedRequestId:"", caseMatrixSyncedRequestVersion:null, previewRenderedRequestId:"", previewRenderedRequestVersion:null, latestApprovedState:null});
      orchestratorPanelState.decisionIds.clear();
      orchestratorPanelState.refreshedProposalIds.clear();
      touchedFields.clear();
      heatExchangerCustomFields.clear();
      fanCountCustomCards.clear();
      chatHistory = [];
      requestContextDraft = fallbackRequestContext();
      activeTopTab = "write";
      prepAssistStarted = false;
      lastPlannerActiveFieldId = "";
      lastCaseDeleteNoticeVisible = false;
      caseSourceSummaryExpanded = true;
      outdoorCaseMatrixViewed = false;
      adoptStateFromResponse(data);
      resetCaseImpactBaseline({deferUntilMatrixRender:true});
      restoreChatHistoryFromState();
      syncEditorFromState();
    }

    function adoptStateFromResponse(data){
      requestState = asObj(data).state || requestState;
      if (Object.prototype.hasOwnProperty.call(asObj(data), "candidate_conditions")) {
        requestState.candidate_conditions = data.candidate_conditions || {};
      }
    }

    function invalidatePendingPreviewRefresh(){
      previewStateRevision += 1;
      if (previewRefreshTimer !== null) {
        window.clearTimeout(previewRefreshTimer);
        previewRefreshTimer = null;
      }
    }

    function schedulePreviewRefresh(){
      clearCaseConfigurationWarning();
      renderScreenNavigation();
      orchestratorPanelState.dirty = true;
      invalidatePendingPreviewRefresh();
      const scheduledRevision = previewStateRevision;
      previewRefreshTimer = window.setTimeout(() => {
        previewRefreshTimer = null;
        refreshPreview(scheduledRevision);
      }, 650);
    }

    async function refreshPreview(requestedRevision=previewStateRevision){
      try {
        const data = await postState("/api/preview");
        if (requestedRevision !== previewStateRevision) return false;
        const previousConditionIdentity = conditionCardIdentity();
        adoptStateFromResponse(data);
        classifyCaseImpact(requestState);
        if (previousConditionIdentity !== conditionCardIdentity()) renderConditionFields();
        renderDerivedPanels();
        return true;
      } finally {
        if (requestedRevision === previewStateRevision) {
          caseValidationPending = false;
          renderCaseValidationStatus();
        }
      }
    }

    const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
    const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
    let caseImpactBaseline = null;
    let caseImpactSideState = {status:"", reasons:[]};
    let caseMatrixBlockingScope = "";
    let caseConfigurationWarning = "";
    let caseConfigurationWarningTimer = null;
    let lastCaseDeleteNoticeVisible = false;
    let caseSourceSummaryExpanded = true;
    let caseValidationPending = false;

    function sourceFieldValue(value){
      return contextText(asObj(value).value ?? value);
    }

    function caseImpactSources(state){
      const geometry = new Map();
      const matrix = asObj(asObj(state).case_matrix);
      const optionSets = [asObj(matrix.dropdown_options), ...Object.values(asObj(matrix.dropdown_options_by_scope)).map(asObj)];
      const validValues = key => new Set(optionSets.flatMap(options => asArray(options[key]).map(item => contextText(asObj(item).value))).filter(Boolean));
      const validGeometryIds = validValues("geometry_id");
      const validConditionIds = new Set(asArray(matrix.visible_columns)
        .filter(column => contextText(asObj(column).kind) === "condition")
        .flatMap(column => [...validValues(contextText(asObj(column).key))]));
      const allProducts = [asObj(asObj(state).geometry).base_product, ...asArray(asObj(asObj(state).geometry).comparison_products)];
      allProducts.forEach(product => {
        const row = asObj(product), id = contextText(row.geometry_id);
        if (id && validGeometryIds.has(id)) geometry.set(id, sourceFieldValue(row.drawing_no));
      });
      const conditions = new Map();
      const conditionScopes = new Map();
      asArray(asObj(asObj(state).conditions).condition_sets).forEach(card => {
        const row = asObj(card), cardId = contextText(row.id);
        if (!validConditionIds.has(cardId)) return;
        if (cardId) conditionScopes.set(cardId, contextText(row.analysis_scope));
        Object.entries(asObj(row.fields)).forEach(([key, value]) => conditions.set(`${cardId}:${key}`, sourceFieldValue(value)));
        asArray(row.fans).forEach((fan, index) => conditions.set(`${cardId}:fan_${index + 1}_rpm`, sourceFieldValue(asObj(fan).values?.fan_rpm)));
      });
      return {geometry, conditions, conditionScopes};
    }

    function resetCaseImpactBaseline(options={}){
      caseImpactBaseline = options.deferUntilMatrixRender
        ? null
        : {sources:caseImpactSources(requestState), rows:asArray(asObj(requestState.case_matrix).rows).map(row => JSON.parse(JSON.stringify(row)))};
      caseImpactSideState = {status:"", reasons:[]};
      if (typeof caseMatrixBlockingScope !== "undefined") caseMatrixBlockingScope = "";
      clearCaseConfigurationWarning();
    }

    function clearCaseConfigurationWarning(){
      caseConfigurationWarning = "";
      if (caseConfigurationWarningTimer !== null) {
        window.clearTimeout(caseConfigurationWarningTimer);
        caseConfigurationWarningTimer = null;
      }
    }

    function showCaseConfigurationInfo(){
      clearCaseConfigurationWarning();
      caseConfigurationWarning = "현재 입력된 해석 제품과 조건으로 구성할 수 있는 모든 Case 조합이 이미 추가되어 있습니다.";
      caseConfigurationWarningTimer = window.setTimeout(() => {
        caseConfigurationWarning = "";
        caseConfigurationWarningTimer = null;
        renderCasePreview();
      }, 4000);
    }

    function hasConditionReference(rows, value){
      return rows.some(row => Object.values(asObj(row).condition_values).some(item => contextText(item) === value));
    }

    function conditionImpactScope(sources, key){
      const cardId = contextText(key).split(":", 1)[0];
      const scopes = sources?.conditionScopes;
      const scope = scopes instanceof Map ? contextText(scopes.get(cardId)) : "";
      return ["indoor","outdoor"].includes(scope) ? scope : "";
    }

    function classifyCaseImpact(state){
      if (!caseImpactBaseline) return false;
      const current = caseImpactSources(state), baseline = caseImpactBaseline.sources;
      const rows = asArray(asObj(state.case_matrix).rows).length ? asArray(asObj(state.case_matrix).rows) : caseImpactBaseline.rows;
      const rebuildReasons = [], reviewReasons = [];
      const changedConditionScopes = new Set();
      let commonSourceChanged = false;
      const impactedCaseIds = new Set();
      const reviewImpactedCaseIds = new Set();
      const invalidSelections = new Map();
      const invalidSelectionValue = (row, key) => {
        const invalid = asObj(asObj(row).invalid_selection_values)[key];
        return contextText(invalid.value ?? invalid);
      };
      const selectionValue = (row, key) => {
        const item = asObj(row);
        const selected = key === "geometry_id" ? item.geometry_id : asObj(item.condition_values)[key];
        return contextText(selected) || invalidSelectionValue(item, key);
      };
      const conditionSelectionValues = row => {
        const item = asObj(row), values = Object.values(asObj(item.condition_values)).map(contextText);
        Object.entries(asObj(item.invalid_selection_values)).forEach(([key, value]) => {
          if (key !== "geometry_id") values.push(contextText(asObj(value).value ?? value));
        });
        return values;
      };
      const impactedRows = predicate => rows.filter(row => predicate(asObj(row)));
      const markImpacted = impacted => impacted.forEach(row => {
        const caseId = contextText(asObj(row).case_id);
        if (caseId) impactedCaseIds.add(caseId);
      });
      const markReviewImpacted = impacted => impacted.forEach(row => {
        const caseId = contextText(asObj(row).case_id);
        if (caseId) reviewImpactedCaseIds.add(caseId);
      });
      const markInvalid = (impacted, key) => impacted.forEach(row => {
        const item = asObj(row), caseId = contextText(item.case_id);
        const value = selectionValue(item, key);
        if (!caseId || !value) return;
        const label = contextText(asObj(item.visible_cells)[key]) || contextText(asObj(asObj(item.invalid_selection_values)[key]).label);
        invalidSelections.set(`${caseId}:${key}`, {caseId, key, value, label});
      });
      const markInvalidCondition = (impacted, cardId) => impacted.forEach(row => {
        const item = asObj(row);
        const keys = new Set([...Object.keys(asObj(item.condition_values)), ...Object.keys(asObj(item.invalid_selection_values))]);
        keys.forEach(key => {
          if (key !== "geometry_id" && selectionValue(item, key) === cardId) markInvalid([item], key);
        });
      });
      baseline.geometry.forEach((drawingNo, id) => {
        const impacted = impactedRows(row => selectionValue(row, "geometry_id") === id);
        const referenced = impacted.length > 0;
        if (!current.geometry.has(id)) {
          if (referenced) {
            rebuildReasons.push(`geometry:${id}:deleted`);
            markImpacted(impacted);
            markInvalid(impacted, "geometry_id");
          }
          commonSourceChanged = true;
        } else if (current.geometry.get(id) !== drawingNo) {
          if (referenced) markImpacted(impacted);
          if (!current.geometry.get(id) && referenced) {
            rebuildReasons.push(`geometry:${id}:identifier_changed`);
            rebuildReasons.push(`geometry:${id}:required_value_invalid`);
            markInvalid(impacted, "geometry_id");
          } else if (referenced) {
            reviewReasons.push(`geometry:${id}:identifier_changed`);
            markReviewImpacted(impacted);
          }
          commonSourceChanged = true;
        }
      });
      baseline.conditions.forEach((value, key) => {
        const cardId = contextText(key).split(":", 1)[0];
        const impacted = impactedRows(row => conditionSelectionValues(row).some(item => item === value || item === cardId));
        const referenced = impacted.length > 0;
        if (!current.conditions.has(key)) {
          if (referenced) {
            rebuildReasons.push(`condition:${key}:deleted`);
            markImpacted(impacted);
            markInvalidCondition(impacted, cardId);
          }
          const scope = conditionImpactScope(baseline, key);
          if (scope) changedConditionScopes.add(scope);
        } else if (current.conditions.get(key) !== value) {
          if (referenced) markImpacted(impacted);
          if (!current.conditions.get(key) && referenced) {
            rebuildReasons.push(`condition:${key}:identifier_changed`);
            rebuildReasons.push(`condition:${key}:required_value_invalid`);
            markInvalidCondition(impacted, cardId);
          } else if (referenced) {
            reviewReasons.push(`condition:${key}:identifier_changed`);
            markReviewImpacted(impacted);
          }
          const scope = conditionImpactScope(current, key) || conditionImpactScope(baseline, key);
          if (scope) changedConditionScopes.add(scope);
        }
      });
      const reviewKey = JSON.stringify({
        reasons:reviewReasons,
        impactedCaseIds:[...impactedCaseIds],
        geometry:[...current.geometry],
        conditions:[...current.conditions],
      });
      const previousImpact = asObj(caseImpactSideState);
      const sameReview = contextText(previousImpact.status) === CASE_REVIEW_REQUIRED
        && contextText(previousImpact.reviewKey) === reviewKey;
      const renderedReviewScopes = sameReview ? asArray(previousImpact.renderedScopes) : [];
      caseImpactSideState = rebuildReasons.length
        ? {status:CASE_REBUILD_REQUIRED, reasons:rebuildReasons, impactedCaseIds:[...impactedCaseIds], reviewImpactedCaseIds:[...reviewImpactedCaseIds], invalidSelections:[...invalidSelections.values()]}
        : reviewReasons.length ? {status:CASE_REVIEW_REQUIRED, reasons:reviewReasons, impactedCaseIds:[...impactedCaseIds], reviewImpactedCaseIds:[...reviewImpactedCaseIds], invalidSelections:[], reviewKey, renderedScopes:renderedReviewScopes} : {status:"", reasons:[]};
      const caseImpactDetected = Boolean(caseImpactSideState.status);
      const blockingScope = typeof caseMatrixBlockingErrorScope === "function" ? caseMatrixBlockingErrorScope(state) : "";
      const previousBlockingScope = typeof caseMatrixBlockingScope === "string" ? caseMatrixBlockingScope : "";
      if (typeof caseMatrixBlockingScope !== "undefined") caseMatrixBlockingScope = blockingScope;
      const preferredImpactScope = !commonSourceChanged && changedConditionScopes.size === 1
        ? Array.from(changedConditionScopes)[0]
        : "indoor";
      if (blockingScope) {
        activeCaseScope = blockingScope;
      } else if (previousBlockingScope && contextText(caseImpactSideState.status) === CASE_REVIEW_REQUIRED && hasBothAnalysisScopes()) {
        activeCaseScope = preferredImpactScope;
      } else if (caseImpactDetected && !sameReview) {
        outdoorCaseMatrixViewed = false;
        if (hasBothAnalysisScopes()) {
          activeCaseScope = preferredImpactScope;
        }
      }
      return caseImpactDetected;
    }

    function caseImpactNoticeHtml(){
      return "";
    }

    function unresolvedCaseImpactSelections(rows=asArray(asObj(requestState.case_matrix).rows)){
      return asArray(caseImpactSideState.invalidSelections).filter(raw => {
        const item = asObj(raw), row = rows.find(candidate => contextText(asObj(candidate).case_id) === contextText(item.caseId));
        if (!row) return false;
        const value = contextText(item.key) === "geometry_id"
          ? contextText(asObj(row).geometry_id)
          : contextText(asObj(asObj(row).condition_values)[contextText(item.key)]);
        return !value;
      });
    }

    function resolveCaseImpactSelections(){
      if (caseImpactSideState.status !== CASE_REBUILD_REQUIRED) return;
      const remaining = unresolvedCaseImpactSelections();
      if (remaining.length) {
        caseImpactSideState = {...caseImpactSideState, invalidSelections:remaining};
        return;
      }
    }

    function caseImpactPreviousSelection(rowId, key, selected){
      if (contextText(selected)) return "";
      const entry = caseImpactSideState.status === CASE_REBUILD_REQUIRED && asArray(caseImpactSideState.invalidSelections).find(item => {
        const source = asObj(item);
        return contextText(source.caseId) === contextText(rowId) && contextText(source.key) === contextText(key);
      });
      if (entry) {
        const label = contextText(asObj(entry).label);
        if (label) return label;
      }
      const row = asArray(asObj(requestState.case_matrix).rows).find(item => contextText(asObj(item).case_id) === contextText(rowId));
      return contextText(asObj(asObj(asObj(row).invalid_selection_values)[key]).label);
    }

    function caseConfigurationInfoHtml(){
      if (!caseConfigurationWarning) return "";
      return `<div class="geometry-policy-guidance case-configuration-info" data-case-configuration-warning role="status"><span class="prep-info-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"></circle><path d="M12 11v6"></path><path d="M12 7.5h.01"></path></svg></span><div class="geometry-policy-copy"><strong class="geometry-policy-heading">추가 가능한 Case가 없습니다.</strong><p class="geometry-policy-body">${esc(caseConfigurationWarning)}</p></div></div>`;
    }

    function conditionUnitFields(type){
      return {
        space_environment:[["room_temp","공간 온도","°C"],["room_rh","공간 상대습도","%"]],
        supply_air:[["heat_exchanger_temp","취출 온도","°C"],["heat_exchanger_rh","취출 상대습도","%"]],
      }[type] || [];
    }

    function conditionFieldDisplayWithUnit(type, key, field){
      const value = contextText(fieldDisplayValue(field));
      if (!value) return "";
      const unit = contextText(asArray(conditionUnitFields(type)).find(item => item[0] === key)?.[2]);
      if (!unit) return value;
      const compact = value.replace(/\s+/g, "").toLowerCase();
      const hasUnit = unit === "°C"
        ? compact.endsWith("°c") || compact.endsWith("℃")
        : unit === "%" ? compact.endsWith("%") : true;
      return hasUnit ? value : `${value}${unit}`;
    }

    function caseGroupedConditionLabel(type, fields){
      const parts = [];
      for (const [key] of conditionUnitFields(type)) {
        if (!Object.prototype.hasOwnProperty.call(fields, key)) continue;
        const value = conditionFieldDisplayWithUnit(type, key, fields[key]);
        if (!value) return "";
        parts.push(value);
      }
      return parts.join(" / ");
    }

    function liveCaseDropdownOptions(){
      const matrix = asObj(requestState.case_matrix);
      const requestedScopes = requestedAnalysisScopes();
      if (!requestedScopes.includes(activeCaseScope)) activeCaseScope = requestedScopes[0];
      return asObj(asObj(matrix.dropdown_options_by_scope)[activeCaseScope] || matrix.dropdown_options);
    }

    function operatingFanDisplay(rawCard){
      const card = asObj(rawCard), fans = asArray(card.fans), count = Math.max(1, fans.length);
      const rpms = fans.map(fan => contextText(asObj(asObj(fan).values).fan_rpm));
      if (count === 1) return {count, text:rpms[0] || "-", missing:!rpms[0]};
      const mode = contextText(card.fan_rpm_mode);
      if (mode === "common") {
        const rpm = rpms.length === count && rpms.every(value => value && value === rpms[0]) ? rpms[0] : "";
        return {count, text:`모든 팬 ${rpm || "-"}`, missing:!rpm};
      }
      const values = fans.map(rawFan => {
        const fan = asObj(rawFan), location = contextText(fan.location), rpm = contextText(asObj(fan.values).fan_rpm);
        return `${location ? `${location} ` : ""}${rpm || "-"}`;
      });
      return {count, text:values.join(" / ") || "-", missing:mode !== "individual" || fans.some((fan, index) => !contextText(asObj(fan).location) || !rpms[index])};
    }

    function caseSelectionSources(sourceState=requestState, analysisScope=""){
      const state = asObj(sourceState);
      const geometry = asObj(state.geometry);
      const products = [asObj(geometry.base_product), ...asArray(geometry.comparison_products)];
      const context = asObj(state.request_context);
      const scoped = contextText(context.analysis_scope) === "both" || ["indoor","outdoor"].includes(contextText(context.analysis_scope));
      const conditionSets = asArray(asObj(state.conditions).condition_sets).map(asObj)
        .filter(card => !scoped || !analysisScope || contextText(card.analysis_scope) === analysisScope);
      return {
        products,
        productsById:new Map(products.map((product, index) => [contextText(product.geometry_id), {product, index}])),
        operatingById:new Map(conditionSets
          .filter(card => contextText(card.type) === "operating")
          .map(card => [contextText(card.id), card])),
        specificationById:new Map(conditionSets
          .filter(card => contextText(card.type) === "heat_exchanger")
          .map(card => [contextText(card.id), card])),
      };
    }

    function caseOperatingSelectionPresentation(rawCard, rawLabel){
      const card = asObj(rawCard), fans = asArray(card.fans).map(asObj);
      const display = operatingFanDisplay(card), count = display.count;
      const label = contextText(rawLabel);
      const rpms = fans.map(fan => contextText(asObj(fan.values).fan_rpm));
      if (count === 1) return {label, summary:rpms[0] ? `${rpms[0]} RPM` : ""};
      const mode = contextText(card.fan_rpm_mode);
      if (mode === "individual") return {label, summary:`팬 ${count}개 · 팬별 입력`};
      const commonRpm = rpms.find(Boolean) || "";
      return {label, summary:commonRpm ? `팬 ${count}개 · ${commonRpm} RPM` : `팬 ${count}개`};
    }

    function caseSourceOperatingPresentation(rawCard, rawLabel){
      const card = asObj(rawCard), display = operatingFanDisplay(card), count = display.count;
      const label = contextText(rawLabel);
      if (count === 1) return {label, summary:display.text && display.text !== "-" ? `${display.text} RPM` : ""};
      if (contextText(card.fan_rpm_mode) === "individual") {
        const details = display.text.split(" / ").map(value => `${value} RPM`).join(" / ");
        return {label, summary:`팬 ${count}개 · ${details}`};
      }
      const rpm = asArray(card.fans).map(asObj).map(fan => contextText(asObj(fan.values).fan_rpm)).find(Boolean) || "";
      return {label, summary:rpm ? `팬 ${count}개 · ${rpm} RPM` : `팬 ${count}개`};
    }

    function caseProductSelectionPresentation(rawProduct, rawLabel){
      const product = asObj(rawProduct);
      const drawingNo = productText(product, "drawing_no");
      return {label:drawingNo || contextText(rawLabel), summary:""};
    }

    function caseSourceProductPresentation(rawProduct, rawLabel){
      const product = asObj(rawProduct), drawingNo = productText(product, "drawing_no");
      const base = contextText(product.role) === "base";
      const difference = base ? "기존 형상" : (productText(product, "difference_from_base") || productText(product, "display_name"));
      return {label:drawingNo || contextText(rawLabel), summary:difference};
    }

    function caseSpecificationSelectionPresentation(rawCard, rawLabel){
      const card = asObj(rawCard), fields = asObj(card.fields), type = heatExchangerType([card]);
      const tubeDiameter = fieldDisplayValue(fields.tube_diameter);
      const finType = fieldDisplayValue(fields.fin_type);
      const rowCount = fieldDisplayValue(fields.row_count);
      const fpi = fieldDisplayValue(fields.fpi);
      const suffix = (value, unit) => value && value.toLowerCase().endsWith(unit.toLowerCase()) ? value : (value ? `${value}${unit}` : "");
      const fpiLabel = contextText(heatExchangerFieldLabels(type).fpi) || "FPI";
      const details = [
        type === "Fin&Tube" ? suffix(tubeDiameter, "Pi") : tubeDiameter,
        finType,
        suffix(rowCount, "열"),
        fpi ? `${fpiLabel} ${fpi}` : "",
      ].filter(Boolean);
      const compactType = type === "Fin&Tube" ? "F&T" : type === "Micro-Channel" ? "MC" : type;
      return {label:[contextText(rawLabel), compactType].filter(Boolean).join(" · "), summary:details.join(" · ")};
    }

    function caseSourceSpecificationPresentation(rawCard, rawLabel){
      const matrixPresentation = caseSpecificationSelectionPresentation(rawCard, rawLabel);
      const type = heatExchangerType([asObj(rawCard)]);
      return {label:contextText(rawLabel), summary:[type, matrixPresentation.summary].filter(Boolean).join(" · ")};
    }

    function caseSelectionPresentation(key, rawValue, rawLabel="", sources=caseSelectionSources()){
      const value = contextText(rawValue), fallbackLabel = contextText(rawLabel) || value;
      if (!value) return {label:fallbackLabel, summary:""};
      const productSource = asObj(sources.productsById.get(value));
      if (productSource.product) return caseProductSelectionPresentation(productSource.product, fallbackLabel);
      if (sources.operatingById.has(value)) return caseOperatingSelectionPresentation(sources.operatingById.get(value), fallbackLabel);
      if (sources.specificationById.has(value)) return caseSpecificationSelectionPresentation(sources.specificationById.get(value), fallbackLabel);
      return {label:fallbackLabel, summary:""};
    }

    function caseSelectFieldHtml(rowId, key, selected, options, sources){
      const selectedValue = contextText(selected);
      const previousSelection = caseImpactPreviousSelection(rowId, key, selectedValue);
      let selectedPresentation = {label:"선택", summary:""};
      const optionHtml = [`<option value="" disabled hidden ${selectedValue ? "" : "selected"}>[선택 필요]</option>`, ...asArray(options).map(option => {
        const item = asObj(option), value = contextText(item.value);
        const presentation = caseSelectionPresentation(key, value, item.label || value, sources);
        if (value === selectedValue) selectedPresentation = presentation;
        return `<option value="${esc(value)}" ${value === selectedValue ? "selected" : ""}>${esc(presentation.label)}</option>`;
      })].join("");
      const supportsSummary = key !== "geometry_id";
      const summaryHtml = supportsSummary ? caseSelectionSummaryHtml(previousSelection ? `기존 값: ${previousSelection}` : selectedPresentation.summary)
        : previousSelection ? caseSelectionSummaryHtml(`기존 값: ${previousSelection}`) : "";
      return `<div class="case-select-field"><select data-case-row-id="${esc(rowId)}" data-case-field="${esc(key)}">${optionHtml}</select>${summaryHtml}</div>`;
    }

    function caseSelectionSummaryHtml(summary){
      const text = contextText(summary);
      return `<div class="case-select-summary" ${text ? "" : "hidden"}>${esc(text)}</div>`;
    }

    function caseReadonlyFieldHtml(key, selected, rawLabel, sources){
      const presentation = caseSelectionPresentation(key, selected, rawLabel, sources);
      return `<div class="case-select-field case-select-readonly"><div class="case-readonly-value">${esc(presentation.label || "-")}</div>${caseSelectionSummaryHtml(presentation.summary)}</div>`;
    }

    function updateCaseSelectSummary(select){
      const field = select?.closest?.(".case-select-field"), summary = field?.querySelector?.(".case-select-summary");
      if (!field || !summary) return;
      const selectedOption = select.selectedOptions?.[0];
      const presentation = caseSelectionPresentation(select.dataset.caseField, select.value, selectedOption?.textContent || "");
      summary.textContent = presentation.summary;
      summary.hidden = !presentation.summary;
    }

    function caseSourceReferenceHtml(){
      const options = liveCaseDropdownOptions();
      const sources = caseSelectionSources();
      const productsById = new Map(sources.products.map(product => [contextText(product.geometry_id), product]));
      const operatingById = sources.operatingById;
      const specificationById = sources.specificationById;
      const listHtml = (items, presentationFor) => {
        const rows = asArray(items).map(raw => {
          const item = asObj(raw), value = contextText(item.value), fallbackLabel = contextText(item.label) || value;
          const presentation = presentationFor(value, fallbackLabel);
          return `<li><strong class="case-source-name">${esc(presentation.label || fallbackLabel)}</strong><span class="case-source-details">${esc(presentation.summary || "-")}</span></li>`;
        }).join("");
        return rows || `<li><strong class="case-source-name">입력값 없음</strong><span class="case-source-details">-</span></li>`;
      };
      const geometryList = listHtml(options.geometry_id, (value, label) => caseSourceProductPresentation(productsById.get(value), label));
      const operatingList = listHtml(options.fan, (value, label) => caseSourceOperatingPresentation(operatingById.get(value), label));
      const specificationList = listHtml(options.heat_exchanger, (value, label) => caseSourceSpecificationPresentation(specificationById.get(value), label));
      const geometryCount = asArray(options.geometry_id).length;
      const operatingCount = asArray(options.fan).length;
      const specificationCount = asArray(options.heat_exchanger).length;
      const sourceColumn = (title, list) => `<section class="case-source-column"><h5>${esc(title)}</h5><ul class="case-source-list">${list}</ul></section>`;
      return `<section class="case-source-reference" aria-labelledby="caseSourceTitle"><div class="case-source-head"><h4 id="caseSourceTitle">입력값 요약</h4><div class="case-source-counts" aria-label="입력값 개수"><span><b>해석 제품</b> ${geometryCount}개</span><span><b>운전 조건</b> ${operatingCount}개</span><span><b>열교환기 사양</b> ${specificationCount}개</span></div><button class="case-source-toggle" type="button" data-action="toggle-case-source" aria-controls="caseSourceDetails" aria-expanded="${String(caseSourceSummaryExpanded)}">${caseSourceSummaryExpanded ? "상세 닫기" : "상세 보기"}</button></div><div class="case-source-content" id="caseSourceDetails" ${caseSourceSummaryExpanded ? "" : "hidden"}>${sourceColumn("해석 제품", geometryList)}${sourceColumn("운전 조건", operatingList)}${sourceColumn("열교환기 사양", specificationList)}</div></section>`;
    }

    function caseTableValidationPresentation(){
      if (caseValidationPending) return {text:"확인 중…", tone:"pending"};
      const missingCount = caseSelectionMissingIssues().length;
      const duplicateCount = caseDuplicateIssues().length;
      const scopeBlockCount = caseConfigurationIssues().filter(issue => contextText(asObj(issue).code) === "case_matrix.scope_geometry_missing").length;
      const coverage = caseCoverageState();
      const parts = [];
      if (missingCount) parts.push(`미선택 항목 ${missingCount}건`);
      if (duplicateCount) parts.push(`중복 Case ${duplicateCount}건`);
      if (scopeBlockCount) parts.push(`scope Case 누락 ${scopeBlockCount}건`);
      if (coverage.complete === false) parts.push("미사용 입력값 있음");
      const hasError = missingCount || duplicateCount || scopeBlockCount || coverage.complete === false;
      if (!hasError && caseImpactReviewRequiredForScope()) parts.push("⚠ 확인 필요");
      else if (!hasError && coverage.complete === true) parts.push("검증 완료");
      return {text:parts.join(" · "), tone:hasError ? "error" : caseImpactReviewRequiredForScope() ? "warning" : coverage.complete === true ? "ok" : ""};
    }

    function renderCaseValidationStatus(){
      const target = $("caseMatrix")?.querySelector(".case-validation-status");
      if (!target) return;
      const validation = caseTableValidationPresentation();
      target.textContent = validation.text;
      target.className = `case-validation-status ${validation.tone}`;
    }

    function caseColumnDisplayLabel(column){
      const item = asObj(column), key = contextText(item.key);
      if (key === "case_no") return "Case";
      if (key === "geometry_id") return "해석 제품";
      if (key === "remove") return "삭제";
      return contextText(item.label) || key;
    }

    function caseColumnClass(key){
      return `case-col-${contextText(key).replace(/[^A-Za-z0-9_-]/g, "-")}`;
    }

    function caseTableHtml(){
      const matrix = asObj(requestState.case_matrix);
      const columns = asArray(matrix.visible_columns);
      const requestedScopes = requestedAnalysisScopes();
      const rows = asArray(matrix.rows).filter(row => requestedScopes[0] === "" || contextText(asObj(row).analysis_scope) === activeCaseScope);
      const optionMap = liveCaseDropdownOptions();
      const sources = caseSelectionSources();
      const validation = caseTableValidationPresentation();
      const toolbar = `<div class="case-matrix-toolbar"><div class="case-matrix-title"><h4>Case 조합표</h4><span class="case-count">Case ${rows.length}개</span>${validation.text ? `<span class="case-validation-status ${esc(validation.tone)}">${esc(validation.text)}</span>` : ""}</div><button class="primary" type="button" data-action="add-case">Case 추가</button></div>`;
      if (!columns.length || !rows.length) return `${toolbar}<div class="empty">형상 또는 Case 추가 후 직접 매핑해 주세요.</div>`;
      const head = columns.map(column => {
        const item = asObj(column), key = contextText(item.key);
        return `<th class="${caseColumnClass(key)}">${esc(caseColumnDisplayLabel(item))}</th>`;
      }).join("");
      const body = rows.map((raw, index) => {
        const row = asObj(raw), id = contextText(row.case_id), values = asObj(row.condition_values);
        return `<tr data-case-row="${esc(id)}">${columns.map(column => {
          const item = asObj(column), key = contextText(item.key);
          if (key === "case_no") return `<td class="case-number ${caseColumnClass(key)}">${index + 1}${caseImpactReviewRequiredForCase(row) ? `<span class="case-validation-status warning">⚠ 확인 필요</span>` : ""}</td>`;
          if (key === "remove") return `<td class="case-remove-cell ${caseColumnClass(key)}"><button class="condition-row-action remove" type="button" data-action="remove-case" data-case-id="${esc(id)}" title="Case ${index + 1} 삭제" aria-label="Case ${index + 1} 삭제">−</button></td>`;
          const selected = key === "geometry_id" ? row.geometry_id : values[key];
          return `<td class="${caseColumnClass(key)}">${caseSelectFieldHtml(id, key, selected, optionMap[key], sources)}</td>`;
        }).join("")}</tr>`;
      }).join("");
      const deleteNotice = lastCaseDeleteNoticeVisible
        ? `<div class="case-action-notice" data-last-case-delete-notice role="status"><strong>마지막 Case는 삭제할 수 없습니다.</strong><span>해석을 위해 최소 1개의 Case가 필요합니다.</span></div>`
        : "";
      return `${toolbar}<div class="matrix-wrap case-matrix-wrap"><table class="case-matrix-grid"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>${deleteNotice}`;
    }

    function caseValidatorState(state=requestState){
      return asObj(asObj(asObj(state).review).validator);
    }

    function hasBothCaseScopes(state=requestState){
      return contextText(asObj(asObj(state).request_context).analysis_scope) === "both";
    }

    function currentCaseScope(state=requestState){
      return hasBothCaseScopes(state) && typeof activeCaseScope === "string" ? activeCaseScope : "";
    }

    function caseScopeKeys(state=requestState){
      return hasBothCaseScopes(state) ? ["indoor","outdoor"] : [""];
    }

    function caseScopeLabel(scope){ return {indoor:"실내측",outdoor:"실외측"}[contextText(scope)] || ""; }

    function caseImpactReviewRequiredForCase(row){
      const impact = typeof caseImpactSideState === "undefined" ? {} : asObj(caseImpactSideState);
      return contextText(impact.status) === "CASE_REVIEW_REQUIRED"
        && asArray(impact.impactedCaseIds).includes(contextText(asObj(row).case_id));
    }

    function caseImpactReviewRequiredForScope(scope=currentCaseScope()){
      const impact = typeof caseImpactSideState === "undefined" ? {} : asObj(caseImpactSideState);
      if (contextText(impact.status) !== "CASE_REVIEW_REQUIRED") return false;
      return asArray(asObj(requestState.case_matrix).rows).some(row => {
        const item = asObj(row);
        return (!scope || contextText(item.analysis_scope) === scope) && caseImpactReviewRequiredForCase(item);
      });
    }

    function caseImpactReviewPendingForScope(scope, state=requestState){
      const impact = typeof caseImpactSideState === "undefined" ? {} : asObj(caseImpactSideState);
      const reviewIds = asArray(impact.reviewImpactedCaseIds);
      const impactedIds = reviewIds.length || contextText(impact.status) !== CASE_REVIEW_REQUIRED
        ? reviewIds
        : asArray(impact.impactedCaseIds);
      if (!impactedIds.length) return false;
      return asArray(asObj(state.case_matrix).rows).some(row => {
        const item = asObj(row);
        return contextText(item.analysis_scope) === scope && impactedIds.includes(contextText(item.case_id));
      });
    }

    function caseMatrixBlockingIssuesForScope(scope, state=requestState){
      if (!hasBothCaseScopes(state) || !["indoor","outdoor"].includes(scope)) return [];
      return asArray(caseValidatorState(state).blocking).filter(rawIssue => {
        const issue = asObj(rawIssue);
        return contextText(issue.section) === "case_matrix" && contextText(issue.analysis_scope) === scope;
      });
    }

    function caseMatrixBlockingErrorScope(state=requestState){
      if (!hasBothCaseScopes(state)) return "";
      const issue = asArray(caseValidatorState(state).blocking).map(asObj).find(item =>
        contextText(item.section) === "case_matrix" && ["indoor","outdoor"].includes(contextText(item.analysis_scope))
      );
      return issue ? contextText(issue.analysis_scope) : "";
    }

    function caseMatrixScopeStatus(scope, state=requestState){
      if (caseMatrixBlockingIssuesForScope(scope, state).length) return "오류";
      return caseImpactReviewPendingForScope(scope, state) ? "확인 필요" : "";
    }

    function geometryDrawingDuplicateIssues(state=requestState){
      return asArray(caseValidatorState(state).blocking)
        .filter(issue => contextText(asObj(issue).code) === "geometry.product.drawing_no.duplicate");
    }

    function renderGeometryDrawingDuplicateWarning(){
      const target = $("geometryDrawingDuplicateWarning");
      if (!target) return;
      target.innerHTML = geometryDrawingDuplicateIssues().length
        ? `<div class="coverage-warning-head"><span class="coverage-warning-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"></circle><path d="m9 9 6 6M15 9l-6 6"></path></svg></span><strong class="coverage-warning-title">오류 · 해석 제품을 확인해 주세요.</strong></div><p class="coverage-warning-copy">이미 입력된 도면번호입니다.<br>형상이나 조립 상태가 다른 경우에는 다른 도면번호를 입력해 주세요.<br>필요 시 임시 도면번호를 사용할 수 있습니다.</p>`
        : "";
    }

    function renderGeometryCadWarning(){
      const target = $("geometryCadWarning");
      if (!target) return;
      const comparisons = asArray(asObj(requestState.geometry).comparison_products);
      target.innerHTML = comparisons.length
        ? `<div class="coverage-warning-head"><span class="coverage-warning-icon" aria-hidden="true">⚠</span><strong class="coverage-warning-title">CAD 반영 상태를 다시 확인해 주세요.</strong></div><p class="coverage-warning-copy">베인 각도, 부품 위치, 조립 상태, 형상 변경 등 해석에 필요한 사항이 입력한 총조립도 CAD에 반영되어 있어야 합니다.</p>`
        : "";
    }

    function caseDuplicateIssues(state=requestState){
      return caseDuplicateIssuesForScope(state, currentCaseScope(state));
    }

    function caseDuplicateIssuesForScope(state=requestState, scope=""){
      const both = hasBothCaseScopes(state);
      return asArray(caseValidatorState(state).blocking)
        .filter(issue => contextText(asObj(issue).code) === "case_matrix.duplicate" && (!both || !scope || contextText(asObj(issue).analysis_scope) === scope));
    }

    function caseSelectionMissingIssues(state=requestState, scope=currentCaseScope(state)){
      const missingCodes = new Set(["case_matrix.rows_missing", "case_matrix.geometry_missing"]);
      asArray(asObj(asObj(state).case_matrix).visible_columns)
        .filter(column => contextText(asObj(column).kind) === "condition")
        .map(column => contextText(asObj(column).key))
        .filter(Boolean)
        .forEach(key => missingCodes.add(`case_matrix.${key}.missing`));
      const both = hasBothCaseScopes(state);
      return asArray(caseValidatorState(state).blocking)
        .filter(issue => missingCodes.has(contextText(asObj(issue).code)) && (!both || !scope || contextText(asObj(issue).analysis_scope) === scope));
    }

    function caseConfigurationIssues(state=requestState, scope=""){
      const missing = new Set(caseSelectionMissingIssues(state, scope));
      const both = hasBothCaseScopes(state);
      return asArray(caseValidatorState(state).blocking).filter(rawIssue => {
        const issue = asObj(rawIssue);
        if (both && scope && contextText(issue.analysis_scope) !== scope) return false;
        return missing.has(rawIssue)
          || ["case_matrix.duplicate", "case_matrix.scope_geometry_missing"].includes(contextText(issue.code));
      });
    }

    function caseCoverageState(state=requestState, scope=currentCaseScope(state)){
      const coverage = asObj(caseValidatorState(state).coverage);
      if (!hasBothCaseScopes(state) || !scope) return coverage;
      return asObj(asObj(coverage.by_scope)[scope]);
    }

    function caseMatrixBlocksWordExport(state=requestState){
      return caseDuplicateIssuesForScope(state, "").length > 0 || caseCoverageState(state, "").complete === false;
    }

    function coverageUnusedGroups(coverage){
      const groups = new Map();
      asArray(asObj(coverage).unused_items).forEach(rawItem => {
        const item = asObj(rawItem);
        const key = contextText(item.column_key);
        const label = contextText(item.column_label);
        const option = contextText(item.option_label);
        if (!key || !label || !option) return;
        if (!groups.has(key)) groups.set(key, {label, options:[]});
        const group = groups.get(key);
        if (!group.options.includes(option)) group.options.push(option);
      });
      return Array.from(groups.values());
    }

    function coverageUnusedItemsHtml(coverage){
      const labels = coverageUnusedGroups(coverage).flatMap(group => group.options);
      return `<p class="coverage-warning-copy">${esc(labels.join(", "))}가 어떤 Case에도 선택되지 않았습니다.</p>`;
    }

    function caseConfigurationMessageHtml(issues, state=requestState, includeReviewAction=false){
      const columns = asArray(asObj(asObj(state).case_matrix).visible_columns).map(asObj);
      const columnLabels = new Map(columns.map(column => [contextText(column.key), contextText(column.label)]));
      const columnOrder = new Map(columns.map((column, index) => [contextText(column.key), index]));
      const missingByCase = new Map();
      const rows = [];
      asArray(issues).forEach(rawIssue => {
        const issue = asObj(rawIssue);
        const code = contextText(issue.code);
        if (code === "case_matrix.rows_missing") {
          rows.push(`<p class="coverage-warning-copy">Case를 1개 이상 추가해 주세요.</p>`);
          return;
        }
        if (code === "case_matrix.unused_option") {
          rows.push(`<p class="coverage-warning-copy">${esc(contextText(issue.field_label) || contextText(issue.option_label))}이(가) 어떤 Case에도 선택되지 않았습니다.</p>`);
          return;
        }
        if (code === "case_matrix.scope_geometry_missing") {
          rows.push(`<p class="coverage-warning-copy">${esc(contextText(issue.message))}</p>`);
          return;
        }
        if (code !== "case_matrix.duplicate") {
          const path = contextText(issue.path);
          const rowIndex = Number.parseInt((path.match(/case_matrix\.rows\[(\d+)\]/) || [])[1] || "-1", 10);
          const fieldKey = contextText(issue.field_key);
          const label = columnLabels.get(fieldKey);
          if (rowIndex < 0 || !label) return;
          const caseNo = Number.parseInt(contextText(issue.case_no), 10) || rowIndex + 1;
          if (!missingByCase.has(caseNo)) missingByCase.set(caseNo, []);
          const fields = missingByCase.get(caseNo);
          if (!fields.some(item => item.key === fieldKey)) fields.push({key:fieldKey, label});
          return;
        }
        const caseNo = Number.parseInt(contextText(issue.case_no), 10);
        const duplicateOfCaseNo = Number.parseInt(contextText(issue.duplicate_of_case_no), 10);
        if (caseNo > 0 && duplicateOfCaseNo > 0) rows.push(`<p class="coverage-warning-copy">Case ${caseNo}: Case ${duplicateOfCaseNo}과 동일합니다.</p>`);
      });
      const missingRows = Array.from(missingByCase.entries()).sort(([left], [right]) => left - right).map(([caseNo, fields]) => {
        fields.sort((left, right) => (columnOrder.get(left.key) ?? 0) - (columnOrder.get(right.key) ?? 0));
        return `<p class="coverage-warning-copy">Case ${caseNo}: ${esc(fields.map(item => item.label).join(", "))}을 선택해 주세요.</p>`;
      });
      rows.unshift(...missingRows);
      if (!rows.length) return "";
      const action = includeReviewAction ? `<button class="ghost" type="button" data-action="review-case-coverage">05 Case Matrix에서 확인</button>` : "";
      return `<div class="coverage-warning-head"><span class="coverage-warning-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"></circle><path d="m9 9 6 6M15 9l-6 6"></path></svg></span><strong class="coverage-warning-title">오류 · Case 구성을 확인해 주세요.</strong></div>${rows.join("")}${action}`;
    }

    function renderCaseDuplicateWarning(){
      const target = $("caseDuplicateWarning");
      if (!target) return;
      const issues = caseConfigurationIssues(requestState, currentCaseScope());
      const coverageBlocked = caseCoverageState(requestState, currentCaseScope()).complete === false;
      const reviewRequired = !issues.length && !coverageBlocked && caseImpactReviewRequiredForScope();
      target.className = `case-duplicate-warning case-review-message ${reviewRequired ? "warning" : "error"}`;
      target.innerHTML = issues.length
        ? caseConfigurationMessageHtml(issues)
        : reviewRequired
          ? `<div class="coverage-warning-head"><span class="coverage-warning-icon" aria-hidden="true">⚠</span><strong class="coverage-warning-title">확인 필요</strong></div><p class="coverage-warning-copy">입력값 변경으로 영향을 받은 Case가 있습니다.<br>표시된 Case 구성을 다시 확인해 주세요.</p>`
          : "";
    }

    function renderCaseCoverageStatus(){
      const target = $("caseCoverageStatus");
      if (!target) return;
      const coverage = caseCoverageState(requestState, currentCaseScope());
      const incomplete = coverage.complete === false;
      target.dataset.coverageComplete = String(coverage.complete);
      target.innerHTML = incomplete
        ? `<div class="coverage-warning-head"><span class="coverage-warning-icon" aria-hidden="true">⚠</span><strong class="coverage-warning-title">오류 · Case에 사용되지 않은 항목이 있습니다.</strong></div>${coverageUnusedItemsHtml(coverage)}<p class="coverage-warning-copy">사용할 항목은 Case에서 선택하고, 필요하지 않은 항목은 입력 화면에서 삭제해 주세요.</p>`
        : "";
    }

    function toggleCaseSourceSummary(){
      caseSourceSummaryExpanded = !caseSourceSummaryExpanded;
      renderCasePreview();
      window.requestAnimationFrame(() => document.querySelector('[data-action="toggle-case-source"]')?.focus());
    }

    function switchAnalysisScopeTab(kind, scope){
      if (!["indoor","outdoor"].includes(scope)) return;
      if (kind === "conditions") {
        preserveEditorDraftBeforeRerender();
        activeConditionScope = scope;
        renderConditionFields();
        return;
      }
      if (kind === "case") {
        preserveCaseSelections();
        activeCaseScope = scope;
        renderCasePreview();
      }
    }

    function requiresOutdoorCaseMatrixView(){
      return hasBothAnalysisScopes();
    }

    function recordOutdoorCaseMatrixView(){
      if (activeScreen === "SCREEN-05" && requiresOutdoorCaseMatrixView() && activeCaseScope === "outdoor") {
        outdoorCaseMatrixViewed = true;
      }
    }

    function caseImpactReviewScopes(){
      const impact = asObj(caseImpactSideState);
      if (contextText(impact.status) !== CASE_REVIEW_REQUIRED) return [];
      const impactedIds = new Set(asArray(impact.impactedCaseIds).map(contextText));
      return [...new Set(asArray(asObj(requestState.case_matrix).rows)
        .filter(row => impactedIds.has(contextText(asObj(row).case_id)))
        .map(row => contextText(asObj(row).analysis_scope))
        .filter(scope => scope === "" || ["indoor", "outdoor"].includes(scope)))];
    }

    function recordCaseImpactReviewMatrixRender(){
      if (activeScreen !== "SCREEN-05" || typeof caseImpactSideState === "undefined") return;
      const scope = (typeof currentCaseScope === "function" ? currentCaseScope() : "") || requestedAnalysisScopes()[0] || "";
      if (typeof caseImpactReviewRequiredForScope !== "function" || !caseImpactReviewRequiredForScope(scope)) return;
      const impact = asObj(caseImpactSideState);
      const renderedScopes = new Set(asArray(impact.renderedScopes));
      renderedScopes.add(scope);
      caseImpactSideState = {...impact, renderedScopes:[...renderedScopes]};
    }

    function completeCaseImpactReviewOnLeave(screenId){
      if (activeScreen !== "SCREEN-05" || !["SCREEN-01", "SCREEN-02", "SCREEN-03", "SCREEN-04", "SCREEN-06"].includes(screenId)) return;
      const impact = asObj(caseImpactSideState);
      const requiredScopes = caseImpactReviewScopes();
      if (contextText(impact.status) !== CASE_REVIEW_REQUIRED || !requiredScopes.length) return;
      const renderedScopes = new Set(asArray(impact.renderedScopes));
      if (requiredScopes.every(scope => renderedScopes.has(scope))) resetCaseImpactBaseline();
    }

    function renderPreviewCaseMatrixStatus(state=requestState, options={}){
      const settings = asObj(options);
      const target = settings.target || $("previewCoverageWarning");
      if (!target) return;
      const messages = [];
      const scopes = caseScopeKeys(state);
      scopes.forEach(scope => {
        const configurationIssues = Object.prototype.hasOwnProperty.call(settings, "configurationIssues")
          ? asArray(settings.configurationIssues).filter(issue => !scope || contextText(asObj(issue).analysis_scope) === scope)
          : caseConfigurationIssues(state, scope);
        const suppliedCoverage = Object.keys(asObj(settings.coverage)).length ? asObj(settings.coverage) : null;
        const coverage = suppliedCoverage ? (scope ? asObj(asObj(suppliedCoverage.by_scope)[scope]) : suppliedCoverage) : caseCoverageState(state, scope);
        const scopeHeading = scope ? `<h5 class="preview-scope-heading">${caseScopeLabel(scope)}</h5>` : "";
        const configurationMessage = caseConfigurationMessageHtml(configurationIssues, state);
        if (configurationMessage) messages.push(`<div class="case-review-message error">${scopeHeading}${configurationMessage}</div>`);
        if (coverage.complete === false) messages.push(`<div class="case-review-message error">${scopeHeading}<div class="coverage-warning-head"><span class="coverage-warning-icon" aria-hidden="true">⚠</span><strong class="coverage-warning-title">오류 · Case에 사용되지 않은 항목이 있습니다.</strong></div>${coverageUnusedItemsHtml(coverage)}<p class="coverage-warning-copy">사용할 항목은 05 Case Matrix에서 선택하고, 필요하지 않은 항목은 입력 화면에서 삭제해 주세요.</p></div>`);
      });
      target.innerHTML = messages.join("");
    }

    function renderCompactPreviewCaseMatrixStatus(state=requestState, target){
      if (!target) return;
      const groups = [];
      caseScopeKeys(state).forEach(scope => {
        const configurationMessage = caseConfigurationMessageHtml(caseConfigurationIssues(state, scope), state);
        const coverage = caseCoverageState(state, scope);
        const coverageMessage = coverage.complete === false
          ? `${coverageUnusedItemsHtml(coverage)}<p class="coverage-warning-copy">사용할 항목은 05 Case Matrix에서 선택하고, 필요하지 않은 항목은 입력 화면에서 삭제해 주세요.</p>`
          : "";
        if (!configurationMessage && !coverageMessage) return;
        const scopeHeading = scope ? `<h5 class="preview-scope-heading">${caseScopeLabel(scope)}</h5>` : "";
        groups.push(`<section class="request-preview-case-error-scope">${scopeHeading}${configurationMessage}${coverageMessage}</section>`);
      });
      target.innerHTML = groups.length
        ? `<div class="case-review-message error request-preview-case-errors"><div class="coverage-warning-head"><span class="coverage-warning-icon" aria-hidden="true">⊗</span><strong class="coverage-warning-title">오류 · Case 구성을 확인해 주세요.</strong></div>${groups.join("")}</div>`
        : "";
    }

    function renderCasePreview(){
      const requestedScopes = requestedAnalysisScopes();
      if (!requestedScopes.includes(activeCaseScope)) activeCaseScope = requestedScopes[0];
      const scopeTabs = $("caseScopeTabs");
      if (scopeTabs) scopeTabs.innerHTML = scopeTabsHtml("case", activeCaseScope);
      $("caseCommon").innerHTML = caseImpactNoticeHtml();
      const caseMatrix = $("caseMatrix");
      const activeCaseSelect = document.activeElement?.matches?.("select[data-case-field]");
      const matrixScopeMatchesActiveScope = caseMatrix?.dataset?.caseMatrixScope === activeCaseScope;
      const renderCaseMatrix = !activeCaseSelect || !matrixScopeMatchesActiveScope;
      if (renderCaseMatrix) {
        caseMatrix.innerHTML = `${caseSourceReferenceHtml()}${caseTableHtml()}${caseConfigurationInfoHtml()}`;
        caseMatrix.dataset.caseMatrixScope = activeCaseScope;
      }
      if (renderCaseMatrix) {
        if (activeScreen === "SCREEN-05" && typeof caseImpactBaseline !== "undefined" && !caseImpactBaseline) resetCaseImpactBaseline();
        recordCaseImpactReviewMatrixRender();
        recordOutdoorCaseMatrixView();
      }
      renderCaseDuplicateWarning();
      renderCaseCoverageStatus();
    }

    function focusCaseValidationIssue(issue){
      const issueScope = contextText(asObj(issue).analysis_scope);
      if (hasBothAnalysisScopes() && ["indoor","outdoor"].includes(issueScope) && issueScope !== activeCaseScope) {
        switchAnalysisScopeTab("case", issueScope);
      }
      const path = contextText(asObj(issue).path);
      const rowIndex = Number.parseInt((path.match(/case_matrix\.rows\[(\d+)\]/) || [])[1] || "-1", 10);
      const row = asArray(asObj(requestState.case_matrix).rows)[rowIndex];
      const fieldKey = contextText(asObj(issue).field_key) || (path.endsWith(".geometry_id") ? "geometry_id" : "");
      const target = row && fieldKey
        ? document.querySelector(`select[data-case-row-id="${CSS.escape(contextText(asObj(row).case_id))}"][data-case-field="${CSS.escape(fieldKey)}"]`)
        : row ? document.querySelector(`tr[data-case-row="${CSS.escape(contextText(asObj(row).case_id))}"]`)
        : $("caseDuplicateWarning");
      (target || $("section-case"))?.scrollIntoView({behavior:"smooth", block:"center"});
      if (target) {
        if (row && fieldKey) {
          target.classList.add("required-field-highlight");
          target.focus();
        }
      }
    }

    function focusCaseCoverageIssue(){
      const coverage = asObj(caseValidatorState().coverage);
      const scope = hasBothAnalysisScopes()
        ? ["indoor","outdoor"].find(item => asObj(asObj(coverage.by_scope)[item]).complete === false) || ""
        : "";
      if (scope && scope !== activeCaseScope) switchAnalysisScopeTab("case", scope);
      $("caseCoverageStatus")?.scrollIntoView({behavior:"smooth", block:"center"});
    }

    async function confirmCaseConfiguration(){
      const action = $("caseConfirmNextBtn");
      if (action?.disabled) return;
      if (action) action.disabled = true;
      try {
        await refreshPreview();
        const unresolvedSelections = typeof unresolvedCaseImpactSelections === "function" && unresolvedCaseImpactSelections().length;
        const reviewPending = typeof caseImpactSideState !== "undefined"
          && contextText(asObj(caseImpactSideState).status) === "CASE_REVIEW_REQUIRED";
        renderCasePreview();
        const blockingIssues = caseConfigurationIssues();
        const coverageBlocked = asObj(asObj(asObj(requestState).review).validator).coverage?.complete === false;
        if (blockingIssues.length || coverageBlocked) {
          if (blockingIssues.length) focusCaseValidationIssue(blockingIssues[0]);
          else focusCaseCoverageIssue();
          return;
        }
        if (requiresOutdoorCaseMatrixView() && !outdoorCaseMatrixViewed) {
          switchAnalysisScopeTab("case", "outdoor");
          return;
        }
        if (!unresolvedSelections && !reviewPending) resetCaseImpactBaseline();
        navigateScreen("SCREEN-06");
      } finally {
        if (action) action.disabled = false;
      }
    }

    function renderDerivedPanels(){
      renderGeometryDrawingDuplicateWarning();
      renderGeometryCadWarning();
      renderConditionDuplicateWarning();
      renderCasePreview();
      renderDocumentPreviewPanel();
    }

    function renderDocumentPreviewPanel(sourceState, previewReceipt, targetPanel){
      const panel = targetPanel || $("documentPreviewPanel");
      if (!panel) return;
      const state = asObj(sourceState === undefined ? requestState : sourceState);
      const compactMissingPresentation = panel === $("requestPreviewModalPanel");
      const rawValue = field => field && typeof field === "object" ? fieldDisplayValue(field, "") : String(field ?? "").trim();
      const value = field => contextText(rawValue(field)) || "-";
      const isMissing = field => !contextText(rawValue(field));
      const missingIcon = () => `<span class="preview-missing-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3 2.8 20h18.4L12 3Z"></path><path d="M12 9v5"></path><circle cx="12" cy="17" r=".7"></circle></svg></span>`;
      const previewFieldLabel = (label, missing, attributes="") => `<span class="preview-field-label${missing ? " preview-field-missing" : ""}" ${attributes}>${missing ? missingIcon() : ""}<span>${esc(label)}</span></span>`;
      const previewTableValue = (label, displayValue, missing=false) => {
        const text = contextText(displayValue) || "-";
        const presentation = missing && compactMissingPresentation ? "미입력" : text;
        return `<span class="preview-table-value${missing ? " preview-field-missing" : ""}" data-preview-missing="${missing}" aria-label="${esc(`${label}: ${presentation}`)}">${missing ? missingIcon() : ""}<span>${esc(presentation)}</span></span>`;
      };
      const kv = (label, field) => {
        const missing = isMissing(field);
        const presentation = missing && compactMissingPresentation ? "미입력" : value(field);
        return `<div class="preview-kv" data-preview-field="${esc(label)}" data-preview-missing="${missing}">${previewFieldLabel(label, missing, "data-preview-label")}<span data-preview-value>${esc(presentation)}</span></div>`;
      };
      const kvGrid = items => `<div class="preview-kv-grid">${items.join("")}</div>`;
      const tableWrap = (table, className="") => `<div class="preview-table-wrap${className ? ` ${className}` : ""}">${table}</div>`;
      const section = (key, title, body) => `<section class="preview-section" data-preview-section="${esc(key)}"><h4 data-preview-section-title>${esc(title)}</h4>${body}</section>`;
      const basic = asObj(state.basic_info);
      const overview = asObj(state.analysis_overview);
      const context = asObj(state.request_context);
      const products = [asObj(asObj(state.geometry).base_product), ...asArray(asObj(state.geometry).comparison_products)].filter(product => Object.keys(product).length);
      const productDrawingMissing = !products.length || products.some(product => !contextText(productText(product, "drawing_no")));
      const productDescriptionMissing = products.some((product, index) => index > 0 && !contextText(productDescription(product, true)));
      const productRows = products.length ? products.map((product, index) => `<tr data-preview-product="${esc(product.role || (index ? "comparison" : "base"))}"><td>${esc(index ? `비교 ${index}` : "Base")}</td><td>${esc(productText(product, "drawing_no") || "-")}</td><td>${esc(index ? productDescription(product, true) || "-" : "기존 형상")}</td></tr>`).join("") : `<tr><td colspan="3">등록된 제품이 없습니다.</td></tr>`;
      const previewScopes = requestedAnalysisScopes(context);
      const allConditionSets = asArray(asObj(state.conditions).condition_sets).map(asObj);
      const conditionsBodyForScope = scope => {
        const conditionSets = allConditionSets.filter(row => previewScopes[0] === "" || contextText(row.analysis_scope) === scope);
        const conditionByType = type => conditionSets.filter(row => contextText(row.type) === type);
        const operatingRows = conditionByType("operating").map((row, index) => {
          const display = operatingFanDisplay(row), count = display.count;
          const mode = contextText(row.fan_rpm_mode);
          const setting = count === 1 ? `${display.text} RPM` : mode === "common" ? `${display.text.replace(/^모든 팬\s*/, "모든 팬 동일 · ")} RPM` : `${display.text} RPM`;
          return `<tr data-preview-condition-card="${esc(row.id || "")}"><td>${esc(contextText(row.name) || `운전 ${index + 1}`)}</td><td>${esc(count || "-")}</td><td>${previewTableValue("팬 회전 설정", setting, display.missing)}</td></tr>`;
        }).join("") || `<tr><td colspan="3">운전 조건이 없습니다.</td></tr>`;
        const specificationRows = conditionByType("heat_exchanger").map((row, index) => {
          const fields = asObj(row.fields), type = heatExchangerType([row]);
          const labels = heatExchangerFieldLabels(type);
          const name = contextText(fieldDisplayValue(fields.name)) || `사양 ${index + 1}`;
          const keys = ["tube_diameter", "fin_type", "row_count", "fpi"];
          const cells = keys.map(key => `<td>${previewTableValue(labels[key] || key, value(fields[key]), isMissing(fields[key]))}</td>`).join("");
          return `<tr data-preview-condition-card="${esc(row.id || "")}"><td>${esc(name)}</td><td>${esc(type || "-")}</td>${cells}</tr>`;
        }).join("") || `<tr><td colspan="6">열교환기 사양이 없습니다.</td></tr>`;
        const groupedConditionBody = type => {
          const fields = asObj(asObj(conditionByType(type)[0]).fields);
          const items = conditionUnitFields(type).filter(([key]) => Object.prototype.hasOwnProperty.call(fields, key)).map(([key, label]) => kv(label, conditionFieldDisplayWithUnit(type, key, fields[key])));
          return items.length ? kvGrid(items) : "";
        };
        const environmentBody = groupedConditionBody("space_environment");
        const supplyBody = groupedConditionBody("supply_air");
        const suffix = scope ? `_${scope}` : "";
        const operatingTable = tableWrap(`<table class="preview-table" data-preview-table="operating_conditions${suffix}"><thead><tr><th></th><th>팬 개수</th><th>팬 회전 설정</th></tr></thead><tbody>${operatingRows}</tbody></table>`);
        const specificationTable = tableWrap(`<table class="preview-table preview-specification-table" data-preview-table="heat_exchanger_conditions${suffix}"><colgroup><col class="preview-spec-name"><col class="preview-spec-type"><col class="preview-spec-dimension"><col class="preview-spec-fin"><col class="preview-spec-rows"><col class="preview-spec-pitch"></colgroup><thead><tr><th></th><th>HEX Type</th><th>관 직경(Pi) / 채널 폭(Width)</th><th>Fin type</th><th>열 수</th><th>FPI / FPDM</th></tr></thead><tbody>${specificationRows}</tbody></table>`);
        const environmentSections = [environmentBody ? `<div><h5 data-preview-group-title>공간 환경 조건</h5>${environmentBody}</div>` : "", supplyBody ? `<div><h5 data-preview-group-title>취출 공기 조건</h5>${supplyBody}</div>` : ""].filter(Boolean).join("");
        return `<div class="preview-condition-block"><h5 data-preview-group-title>운전 조건</h5>${operatingTable}</div><div class="preview-condition-block"><h5 data-preview-group-title>열교환기 사양</h5>${specificationTable}</div>${environmentSections ? `<div class="preview-condition-pair">${environmentSections}</div>` : ""}`;
      };
      const conditionsBody = previewScopes.length > 1
        ? previewScopes.map(scope => `<div class="preview-scope-group"><h5 class="preview-scope-heading" data-preview-group-title>${scopeLabel(scope)}</h5>${conditionsBodyForScope(scope)}</div>`).join("")
        : conditionsBodyForScope(previewScopes[0]);
      const matrix = asObj(state.case_matrix);
      const matrixColumns = asArray(matrix.visible_columns).filter(column => asObj(column).key !== "remove");
      const matrixTableForScope = scope => {
        const rawMatrixRows = asArray(matrix.rows).filter(row => previewScopes[0] === "" || contextText(asObj(row).analysis_scope) === scope);
        const matrixSources = caseSelectionSources(state);
        if (scope) {
          const scopedSources = caseSelectionSources(state, scope);
          matrixSources.operatingById = scopedSources.operatingById;
          matrixSources.specificationById = scopedSources.specificationById;
        }
        const matrixRows = rawMatrixRows.map(item => { const row = asObj(item), cells = asObj(row.visible_cells), selections = asObj(row.condition_values); return `<tr data-preview-case="${esc(row.case_id || "")}">${matrixColumns.map(column => { const key = contextText(asObj(column).key); if (key === "case_no") return `<td class="case-number ${caseColumnClass(key)}">${esc(cells[key] || "-")}</td>`; const selected = key === "geometry_id" ? row.geometry_id : selections[key]; return `<td class="${caseColumnClass(key)}">${caseReadonlyFieldHtml(key, selected, cells[key], matrixSources)}</td>`; }).join("")}</tr>`; }).join("");
        const tableOpen = scope
          ? `<table class="preview-table case-matrix-grid" data-preview-table="case_matrix_${scope}">`
          : `<table class="preview-table case-matrix-grid" data-preview-table="case_matrix">`;
        return matrixColumns.length && matrixRows ? tableWrap(`${tableOpen}<thead><tr>${matrixColumns.map(column => { const row = asObj(column), key = contextText(row.key), missing = rawMatrixRows.some(item => !contextText(asObj(asObj(item).visible_cells)[key])); return `<th class="${caseColumnClass(key)}">${previewFieldLabel(caseColumnDisplayLabel(row), missing)}</th>`; }).join("")}</tr></thead><tbody>${matrixRows}</tbody></table>`, "case-matrix-wrap") : `<div class="empty" data-preview-matrix-empty>${missingIcon()}<span>Case: 생성된 Case가 없습니다.</span></div>`;
      };
      const matrixTable = previewScopes.length > 1
        ? previewScopes.map(scope => `<div class="preview-scope-group"><h5 class="preview-scope-heading" data-preview-group-title>${scopeLabel(scope)}</h5>${matrixTableForScope(scope)}</div>`).join("")
        : matrixTableForScope(previewScopes[0]);
      const requestFields = [kv("의뢰 유형", overview.request_type), kv("프로젝트명(PMS)", overview.project_name), kv("개발 등급", overview.development_grade), kv("NPI 단계", overview.npi_stage), kv("모델명(Model Suffix)", overview.model_suffix), kv("희망 완료일", overview.desired_completion_date), kv("해석유형", context.analysis_type)];
      if (isRacWindowContext(context)) requestFields.push(kv("해석 범위", scopeLabel(context.analysis_scope)));
      const narrative = `<div class="preview-review-narrative">${kv("해석을 요청하게 된 배경", overview.request_description)}${kv("해석으로 확인하고 싶은 내용", overview.additional_result_request)}</div>`;
      panel.innerHTML = `<div class="preview-doc" data-preview-document="current-state">
        ${section("requester", "의뢰자 정보", kvGrid([kv("사업부", basic.division), kv("부서", basic.department), kv("요청자", basic.requester_name), kv("직급", basic.requester_role)]))}
        ${section("overview", "요청 내용", `${kvGrid(requestFields)}${narrative}`)}
        ${section("geometry", "해석 제품", tableWrap(`<table class="preview-table preview-product-table" data-preview-table="geometry"><colgroup><col class="preview-product-role"><col class="preview-product-drawing"><col class="preview-product-change"></colgroup><thead><tr><th>구분</th><th>${previewFieldLabel("총조립도 도면번호 (NPDM MCAD)", productDrawingMissing)}</th><th>${previewFieldLabel("Base 대비 변경점", productDescriptionMissing)}</th></tr></thead><tbody>${productRows}</tbody></table>`))}
        ${section("conditions", "해석 조건", conditionsBody)}
        ${section("case-matrix", "Case Matrix", matrixTable)}
      </div>`;
      if (compactMissingPresentation) renderCompactPreviewCaseMatrixStatus(state, $("requestPreviewModalCoverageWarning"));
      else renderPreviewCaseMatrixStatus(state, {target: $("previewCoverageWarning")});
      const renderedDocument = panel.querySelector('[data-preview-document="current-state"]');
      const receipt = asObj(previewReceipt);
      if (renderedDocument && receipt.requestId && Number.isFinite(receipt.requestVersion)) {
        renderedDocument.dataset.orchestratorPreviewRequestId = receipt.requestId;
        renderedDocument.dataset.orchestratorPreviewRequestVersion = String(receipt.requestVersion);
      } else {
        orchestratorPanelState.previewRenderedRequestId = "";
        orchestratorPanelState.previewRenderedRequestVersion = null;
      }
    }

    function openRequestPreview(){
      const modal = $("requestPreviewModal");
      const panel = $("requestPreviewModalPanel");
      if (!modal || !panel) return;
      requestState = collectState();
      renderDocumentPreviewPanel(requestState, undefined, panel);
      modal.hidden = false;
      $("requestPreviewCloseBtn")?.focus();
    }

    function closeRequestPreview(){
      const modal = $("requestPreviewModal");
      if (!modal || modal.hidden) return;
      modal.hidden = true;
      $("requestPreviewBtn")?.focus();
    }

    function defaultChatHistory(){
      return [{role:"assistant", content:"먼저 해석 대상 제품을 정해 주세요. 이 의뢰 대상·시작에서 사업부 → 제품 분류 → 해석유형을 선택한 다음, 의뢰서 작성 시작 버튼을 누르면 작성을 시작할 수 있습니다. 해석유형을 모르겠다면 해석유형 선택 가이드를 확인하고 Agent에게 물어봐 주세요.", html:""}];
    }

    function normalizeChatHistory(items){
      const normalized = asArray(items)
        .map(item => {
          const row = asObj(item);
          const role = row.role === "user" ? "user" : "assistant";
          const content = String(row.content ?? "");
          const html = String(row.html ?? "");
          if (!content.trim() && !html.trim()) return null;
          return {role, content, html};
        })
        .filter(Boolean)
        .slice(-200);
      return normalized.length ? normalized : defaultChatHistory();
    }

    function isAgentOverlay(){
      return window.matchMedia("(max-width: 1039px)").matches;
    }

    function setPanelRatio(ratio){
      const layout = document.querySelector(".layout");
      const resizer = $("panelResizer");
      if (!layout || !resizer) return;
      const clamped = Math.min(3, Math.max(1, Number(ratio) || 2));
      layout.style.gridTemplateColumns = `minmax(0,${clamped}fr) 14px minmax(0,1fr)`;
      resizer.setAttribute("aria-valuenow", String(Math.round(clamped * 100) / 100));
    }

    function resetPanelRatio(){
      document.querySelector(".layout")?.style.removeProperty("grid-template-columns");
      $("panelResizer")?.setAttribute("aria-valuenow", "2.29");
    }

    function initPanelResizer(){
      const resizer = $("panelResizer");
      const workspace = document.querySelector(".workspace-content");
      const dock = $("agentDock");
      if (!resizer || !workspace || !dock) return;
      let drag = null;
      const finishDrag = event => {
        if (!drag) return;
        if (event?.pointerId === drag.pointerId && resizer.hasPointerCapture?.(event.pointerId)) resizer.releasePointerCapture(event.pointerId);
        drag = null;
        resizer.classList.remove("is-dragging");
        document.body.classList.remove("panel-resizing");
      };
      resizer.addEventListener("pointerdown", event => {
        if (event.button !== 0 || isAgentOverlay() || !agentOpen) return;
        const leftWidth = workspace.getBoundingClientRect().width;
        const rightWidth = dock.getBoundingClientRect().width;
        const totalWidth = leftWidth + rightWidth;
        if (totalWidth <= 0) return;
        drag = {pointerId:event.pointerId, startX:event.clientX, startLeft:leftWidth, totalWidth};
        resizer.setPointerCapture?.(event.pointerId);
        resizer.classList.add("is-dragging");
        document.body.classList.add("panel-resizing");
        event.preventDefault();
      });
      resizer.addEventListener("pointermove", event => {
        if (!drag || event.pointerId !== drag.pointerId) return;
        const nextLeft = Math.min(drag.totalWidth * .75, Math.max(drag.totalWidth * .5, drag.startLeft + event.clientX - drag.startX));
        setPanelRatio(nextLeft / (drag.totalWidth - nextLeft));
      });
      resizer.addEventListener("pointerup", finishDrag);
      resizer.addEventListener("pointercancel", finishDrag);
    }

    function beginChatFocusRestore(){
      chatFocusRestorePending = true;
    }

    function cancelChatFocusRestore(){
      chatFocusRestorePending = false;
    }

    function handlePendingChatFocusPointerDown(event){
      if (chatFocusRestorePending && event.target !== $("chatInput")) cancelChatFocusRestore();
    }

    function handlePendingChatFocusKeyDown(event){
      if (chatFocusRestorePending && event.key === "Tab") cancelChatFocusRestore();
    }

    function restoreChatInputFocusAfterReply(){
      if (!chatFocusRestorePending) return;
      window.requestAnimationFrame(() => {
        if (!chatFocusRestorePending) return;
        chatFocusRestorePending = false;
        const input = $("chatInput");
        if (!agentOpen || document.hidden || !input || input.disabled || !document.contains(input)) return;
        input.focus({preventScroll:true});
        const cursor = input.value.length;
        input.setSelectionRange?.(cursor, cursor);
      });
    }

    function agentRestoreFocusTarget(){
      if (lastAgentFocus && document.contains(lastAgentFocus) && !lastAgentFocus.disabled) return lastAgentFocus;
      if ($("chatInput")?.value.trim()) return $("chatInput");
      return $("agentDockHeading");
    }

    function renderAgentDock(){
      const layout = document.querySelector(".layout");
      const dock = $("agentDock");
      const openButton = $("agentOpenBtn");
      const hideButton = $("agentHideBtn");
      if (!layout || !dock || !openButton || !hideButton) return;
      layout.classList.toggle("agent-hidden", !agentOpen);
      dock.setAttribute("aria-hidden", String(!agentOpen));
      openButton.hidden = agentOpen;
      openButton.setAttribute("aria-expanded", String(agentOpen));
      hideButton.setAttribute("aria-expanded", String(agentOpen));
    }

    function setAgentOpen(open, options={}){
      const nextOpen = Boolean(open);
      if (!nextOpen) cancelChatFocusRestore();
      if (nextOpen === agentOpen) return;
      const dock = $("agentDock");
      if (!nextOpen && dock?.contains(document.activeElement)) lastAgentFocus = document.activeElement;
      agentOpen = nextOpen;
      resetPanelRatio();
      renderAgentDock();
      if (!nextOpen) {
        $("agentOpenBtn")?.focus();
        return;
      }
      if (options.restoreFocus !== false) window.requestAnimationFrame(() => agentRestoreFocusTarget()?.focus());
    }

    function syncChatMetadata(){
      requestState.metadata = {...asObj(requestState.metadata), chat_history: chatHistory};
    }

    function renderChatHistory(){
      $("chatLog").innerHTML = "";
      replayingChat = true;
      normalizeChatHistory(chatHistory).forEach(item => pushMessage(item.role, item.content, item.html));
      replayingChat = false;
      $("chatLog").scrollTop = $("chatLog").scrollHeight;
    }

    function restoreChatHistoryFromState(){
      chatHistory = normalizeChatHistory(asObj(requestState.metadata).chat_history);
      syncChatMetadata();
      renderChatHistory();
    }

    function resetChatHistory(){
      chatHistory = defaultChatHistory();
      syncChatMetadata();
      renderChatHistory();
    }

    async function clearAgentConversation(){
      if (orchestratorPanelState.loading) return;
      const conversationId = orchestratorPanelState.conversationId;
      orchestratorPanelState.conversationId = "";
      orchestratorPanelState.dirty = true;
      lastPlannerActiveFieldId = "";
      chatHistory = [];
      syncChatMetadata();
      $("chatLog").replaceChildren();
      $("chatInput").value = "";
      if (!conversationId) {
        $("chatInput").focus();
        return;
      }
      setOrchestratorLoading(true);
      try {
        await fetch(`/api/conversations/${encodeURIComponent(conversationId)}/close`, {
          method:"POST", headers:{"Content-Type":"application/json"}, body:"{}",
        });
      } catch (_err) {
        // The local chat remains cleared and the next message starts a new conversation.
      } finally {
        setOrchestratorLoading(false);
        $("chatInput").focus();
      }
    }

    function pushMessage(role, content, html=""){
      const msg = document.createElement("div");
      msg.className = `msg ${role}`;
      if (html) msg.innerHTML = html; else msg.textContent = content;
      $("chatLog").appendChild(msg);
      $("chatLog").scrollTop = $("chatLog").scrollHeight;
      if (!replayingChat) {
        chatHistory = normalizeChatHistory([...chatHistory, {role, content:String(content ?? ""), html:String(html ?? "")}]);
        syncChatMetadata();
      }
      return msg;
    }

    function pushTransientMessage(role, content, html=""){
      const msg = document.createElement("div");
      msg.className = `msg ${role}`;
      if (html) msg.innerHTML = html; else msg.textContent = content;
      $("chatLog").appendChild(msg);
      $("chatLog").scrollTop = $("chatLog").scrollHeight;
      return msg;
    }

    function loadingHtml(text){
      return `<div class="loading-message"><span class="spinner" aria-hidden="true"></span><span>${esc(text)}</span></div>`;
    }

    function startLoadingMessage(text){
      const node = pushTransientMessage("assistant", text, loadingHtml(text));
      return () => node.remove();
    }

    function delay(ms){
      return new Promise(resolve => window.setTimeout(resolve, ms));
    }

    function showLoadingFor(text, ms=2000){
      const stopLoading = startLoadingMessage(text);
      return new Promise(resolve => {
        window.setTimeout(() => {
          stopLoading();
          resolve();
        }, ms);
      });
    }

    function renderCandidateMessage(candidateConditions){
      const items = asArray(asObj(candidateConditions).items);
      if (!items.length) return;
      const html = `<div><strong>AI 추천 ${esc(items.length)}개</strong></div><div class="rec-list">${
        items.map(item => `<div class="issue info"><span class="chip candidate">AI 異붿쿇</span> ${esc(item.field_label || item.field_key)}: ${esc(item.value)}</div>`).join("")
      }</div>`;
      pushMessage("assistant", "", html);
    }

    function renderQuickActionMessage(message, actions){
      const buttons = asArray(actions).map(action => {
        const row = asObj(action);
        const id = String(row.id || "");
        const label = String(row.label || id || "?ㅽ뻾");
        if (!id) return "";
        return `<button class="ghost" data-chat-quick-action="${esc(id)}">${esc(label)}</button>`;
      }).filter(Boolean).join("");
      if (!buttons) {
        if (message) pushMessage("assistant", message);
        return;
      }
      const html = `<div class="proposal-card quick-action-card">
        <strong class="quick-action-title">빠른 실행</strong>
        <div class="quick-action-copy">${esc(message || "필요한 작업을 선택할 수 있습니다.").replaceAll("\n","<br>")}</div>
        <div class="proposal-actions quick-actions">${buttons}</div>
      </div>`;
      pushMessage("assistant", "", html);
    }

    function proposalValueText(operation){
      const op = asObj(operation);
      if (["list_values","condition_values","append_unique","remove_list_values"].includes(op.op)) {
        return asArray(op.values).map(item => String(item ?? "").trim()).filter(Boolean).join(", ");
      }
      if (typeof op.value === "boolean") return op.value ? "예" : "아니오";
      return String(op.value ?? "").trim();
    }

    function proposalValueNote(operation){
      const op = asObj(operation);
      if (op.interpretation_note) return String(op.interpretation_note);
      const count = asArray(op.values).map(item => String(item ?? "").trim()).filter(Boolean).length;
      return count > 1 ? `${count}개 값으로 해석했습니다` : "";
    }

    function renderProposalMessage(proposal, assistantText=""){
      const row = asObj(proposal);
      pushMessage("assistant", assistantText || row.summary || "이 기능의 변경 제안은 Agent 대화에서 다시 요청해 주세요.");
    }

    async function requestConditionRecommendation(){
      pushMessage("assistant", "AI 조건 추천은 h3_v0에서 비활성화되어 있습니다.");
      return;
      const loading = showLoadingFor("AI가 현재 의뢰서에 맞는 조건 후보를 찾고 있습니다.");
      const data = await postState("/api/conditions/recommend");
      await loading;
      if (asObj(data.proposal).status === "pending") renderProposalMessage(data.proposal, data.assistant || "");
      else if (data.assistant) pushMessage("assistant", data.assistant);
    }

    async function runChatQuickAction(actionId){
      const action = String(actionId || "");
      if (action === "condition_recommend") {
        await requestConditionRecommendation();
        return;
      }
      const text = action === "condition_example"
        ? "조건 입력 예시 알려줘"
        : action === "missing_items"
          ? "누락된 정보가 뭐야?"
          : "";
      if (!text) return;
      $("chatInput").value = text;
      await sendChatMessage();
    }

    function orchestratorMessage(role, content, detail=""){
      const node = pushMessage(role, content);
      if (detail) {
        const readOnly = document.createElement("div");
        readOnly.className = "orchestrator-readonly";
        readOnly.textContent = detail;
        node.appendChild(readOnly);
      }
      return node;
    }

    function renderNextQuestion(data){
      const nextQuestion = asObj(asObj(data).next_question);
      const responseAction = String(asObj(data).action || "");
      const nextActiveFieldId = String(nextQuestion.active_field_id || "").trim();
      let displayedMessage = String(nextQuestion.message || "");
      if (nextQuestion.kind === "field_question" && nextActiveFieldId) {
        const activeFieldChanged = nextActiveFieldId !== lastPlannerActiveFieldId;
        lastPlannerActiveFieldId = nextActiveFieldId;
        if (activeFieldChanged && responseAction !== "answer" && responseAction !== "clarify") {
          const targetScreen = screenForSection(nextActiveFieldId.split(".", 1)[0]);
          if (targetScreen !== activeScreen && navigateScreen(targetScreen, {focus:false})) {
            const proposalPending = asObj(asObj(data).proposal).status === "pending"
              || asObj(asObj(data).action_proposal).status === "pending";
            const screenName = document.querySelector(`.screen-map-item[data-screen="${targetScreen}"] .screen-map-label > span:last-child`)?.textContent.trim();
            if (!proposalPending && screenName && displayedMessage) {
              const guidanceName = screenName === "해석 제품" ? `${screenName} 정보` : screenName;
              displayedMessage = `다음은 ${guidanceName}입니다.\n${displayedMessage}`;
            }
          }
        }
      }
      if (nextQuestion.message) pushMessage("assistant", displayedMessage);
    }

    function setOrchestratorLoading(loading){
      orchestratorPanelState.loading = loading;
      $("chatInput").disabled = loading;
      $("sendBtn").disabled = loading;
      $("agentClearBtn").disabled = loading;
    }

    function hasSyncedCaseMatrixRequest(){
      return !!orchestratorPanelState.requestId
        && !!orchestratorPanelState.latestApprovedState
        && orchestratorPanelState.caseMatrixSyncedRequestId === orchestratorPanelState.requestId
        && Number.isFinite(orchestratorPanelState.caseMatrixSyncedRequestVersion)
        && orchestratorPanelState.caseMatrixSyncedRequestVersion === orchestratorPanelState.requestVersion;
    }

    function invalidateCaseMatrixSync(){
      // A newer approved Request write is not eligible until H5-020 adopts its GET.
      orchestratorPanelState.caseMatrixSyncedRequestId = "";
      orchestratorPanelState.caseMatrixSyncedRequestVersion = null;
      // A Preview DOM rendered for an older server snapshot is not a Word source.
      orchestratorPanelState.previewRenderedRequestId = "";
      orchestratorPanelState.previewRenderedRequestVersion = null;
    }

    function hasPreviewDomForWord(){
      const documentNode = document.querySelector('[data-preview-document="current-state"]');
      return hasSyncedCaseMatrixRequest()
        && orchestratorPanelState.previewRenderedRequestId === orchestratorPanelState.requestId
        && orchestratorPanelState.previewRenderedRequestVersion === orchestratorPanelState.requestVersion
        && documentNode?.dataset.orchestratorPreviewRequestId === orchestratorPanelState.requestId
        && Number(documentNode?.dataset.orchestratorPreviewRequestVersion) === orchestratorPanelState.requestVersion;
    }

    async function runOrchestratorCaseMatrixAction(){
      if (orchestratorPanelState.loading || orchestratorPanelState.caseMatrixActionLoading) return;
      const action = $("orchestratorCaseMatrixAction");
      orchestratorPanelState.caseMatrixActionLoading = true;
      action.disabled = true;
      try {
        await createOrchestratorConversation();
        if (!hasSyncedCaseMatrixRequest()) throw new Error("request_not_synced");
        const response = await fetch("/api/orchestrator/case-matrix/action", {
          method:"POST", headers:{"Content-Type":"application/json"},
          body:JSON.stringify({request_id:orchestratorPanelState.requestId}),
        });
        const data = await response.json();
        if (data.kind === "case_matrix_blocked") {
          orchestratorMessage("assistant", "Case Matrix 준비 차단", asArray(data.blocking_reasons).join("\n") || "기존 Validator 준비 조건이 충족되지 않았습니다.");
        } else if (!(response.ok && data.kind === "case_matrix_ready" && data.request_id === orchestratorPanelState.requestId)) {
          orchestratorMessage("assistant", "Case Matrix 확인 불가", "서버 최신 의뢰서를 변경하지 않았습니다.");
        }
      } catch (_err) {
        orchestratorMessage("assistant", "Case Matrix 확인 오류", "폼과 기존 Matrix는 변경되지 않았습니다.");
      } finally {
        orchestratorPanelState.caseMatrixActionLoading = false;
        action.disabled = false;
      }
    }

    async function runOrchestratorValidationAction(){
      if (orchestratorPanelState.loading || orchestratorPanelState.validationActionLoading) return;
      const action = $("orchestratorValidationAction");
      orchestratorPanelState.validationActionLoading = true;
      action.disabled = true;
      try {
        await createOrchestratorConversation();
        if (!hasSyncedCaseMatrixRequest()) throw new Error("request_not_synced");
        const response = await fetch("/api/orchestrator/validation/action", {
          method:"POST", headers:{"Content-Type":"application/json"},
          body:JSON.stringify({request_id:orchestratorPanelState.requestId}),
        });
        const data = await response.json();
        if (response.ok && ["validation_ready", "validation_blocked"].includes(data.kind) && data.request_id === orchestratorPanelState.requestId) {
          const validation = asObj(data.validation);
          const issues = [...asArray(validation.blocking), ...asArray(validation.warning)];
          const lines = issues.map(issue => {
            const row = asObj(issue);
            return String(row.message || row.label || row.code || "확인이 필요한 입력 항목이 있습니다.");
          });
          orchestratorMessage("assistant", "오류·누락 확인 결과", lines.length ? lines.join("\n") : "오류 또는 누락 항목이 없습니다.");
        } else {
          orchestratorMessage("assistant", "Validation 확인 불가", "서버 최신 의뢰서를 변경하지 않았습니다.");
        }
      } catch (_err) {
        orchestratorMessage("assistant", "Validation 확인 오류", "기존 의뢰서와 검증 화면은 변경되지 않았습니다.");
      } finally {
        orchestratorPanelState.validationActionLoading = false;
        action.disabled = false;
      }
    }

    async function runOrchestratorPreviewAction(){
      if (orchestratorPanelState.loading || orchestratorPanelState.previewActionLoading) return;
      const action = $("orchestratorPreviewAction");
      orchestratorPanelState.previewActionLoading = true;
      action.disabled = true;
      try {
        await createOrchestratorConversation();
        if (!hasSyncedCaseMatrixRequest()) throw new Error("request_not_synced");
        const response = await fetch("/api/orchestrator/preview/action", {
          method:"POST", headers:{"Content-Type":"application/json"},
          body:JSON.stringify({request_id:orchestratorPanelState.requestId}),
        });
        const data = await response.json();
        if (response.ok && data.kind === "preview_ready"
          && data.request_id === orchestratorPanelState.requestId
          && data.request_version === orchestratorPanelState.requestVersion
          && hasApprovedLatestStateShape(data)) {
          // The one existing Preview entry receives only this fenced server
          // snapshot.  It does not adopt, normalize, validate, or persist it.
          renderDocumentPreviewPanel(data.state, {requestId:data.request_id, requestVersion:data.request_version});
          orchestratorPanelState.previewRenderedRequestId = data.request_id;
          orchestratorPanelState.previewRenderedRequestVersion = data.request_version;
        } else {
          orchestratorMessage("assistant", "Preview 확인 불가", "서버 최신 의뢰서와 기존 Preview는 변경하지 않았습니다.");
        }
      } catch (_err) {
        orchestratorMessage("assistant", "Preview 확인 오류", "서버 최신 의뢰서와 기존 Preview는 변경하지 않았습니다.");
      } finally {
        orchestratorPanelState.previewActionLoading = false;
        action.disabled = false;
      }
    }

    async function runOrchestratorWordExportAction(){
      if (orchestratorPanelState.loading || orchestratorPanelState.wordExportActionLoading) return;
      if (orchestratorPanelState.dirty) {
        orchestratorMessage("assistant", "Word 출력 불가", "최신 입력으로 의뢰서 미리보기를 먼저 확인해 주세요.");
        return;
      }
      if (!hasPreviewDomForWord()) {
        orchestratorMessage("assistant", "Word 출력 불가", "같은 최신 의뢰서의 Preview 확인이 먼저 필요합니다.");
        return;
      }
      const action = $("orchestratorWordExportAction");
      orchestratorPanelState.wordExportActionLoading = true;
      action.disabled = true;
      try {
        // H5-028 may only serialize the DOM produced by the fenced H5-027
        // Preview action; it must not collect or render client state.
        await exportWordFromPreview({useExistingPreviewDom:true});
      } catch (_err) {
        orchestratorMessage("assistant", "Word 출력 불가", "기존 Preview와 서버 의뢰서는 변경하지 않았습니다.");
      } finally {
        orchestratorPanelState.wordExportActionLoading = false;
        action.disabled = false;
      }
    }

    async function runOrchestratorRagGuidanceAction(){
      if (orchestratorPanelState.loading || orchestratorPanelState.ragGuidanceActionLoading) return;
      const question = $("chatInput").value.trim();
      if (!question) {
        orchestratorMessage("assistant", "RAG 근거 확인 불가", "Agent 입력창에 문서 검색 질문을 입력해 주세요.");
        return;
      }
      const action = $("orchestratorRagGuidanceAction");
      orchestratorPanelState.ragGuidanceActionLoading = true;
      action.disabled = true;
      try {
        await createOrchestratorConversation();
        const response = await fetch("/api/orchestrator/rag-guidance/action", {
          method:"POST", headers:{"Content-Type":"application/json"},
          body:JSON.stringify({request_id:orchestratorPanelState.requestId, question}),
        });
        const data = await response.json();
        const qa = asObj(data.qa);
        if (data.request_id !== orchestratorPanelState.requestId || !["rag_guidance_ready", "rag_guidance_no_result", "rag_guidance_disabled", "rag_guidance_error"].includes(data.kind)) {
          orchestratorMessage("assistant", "RAG 근거 안내 불가", "서버 문서 검색 결과를 표시하지 않았습니다. 폼과 기존 UI는 변경되지 않았습니다.");
          return;
        }
        const title = data.kind === "rag_guidance_ready" ? "RAG 근거 확인" : data.kind === "rag_guidance_no_result" ? "RAG 검색 결과 없음" : data.kind === "rag_guidance_disabled" ? "RAG Off" : "RAG 검색 오류";
        orchestratorMessage("assistant", title, String(qa.answer_text || ""));
        const sources = asArray(qa.sources).map(source => String(asObj(source).source_name || asObj(source).title || "근거 문서")).filter(Boolean);
        const limitations = asArray(qa.limitations).map(String).filter(Boolean);
        orchestratorMessage("assistant", "근거 요약", `${sources.length ? sources.join("\n") : "표시할 근거 문서가 없습니다."}${limitations.length ? `\n제한사항: ${limitations.join(" · ")}` : ""}`);
      } catch (_err) {
        orchestratorMessage("assistant", "RAG 근거 안내 오류", "폼, Request, Fieldset, Matrix, Proposal, Preview, Word 및 기존 채팅은 변경되지 않았습니다.");
      } finally {
        orchestratorPanelState.ragGuidanceActionLoading = false;
        action.disabled = false;
      }
    }

    async function createOrchestratorConversation(){
      const draft = collectState();
      const hasRequest = !!orchestratorPanelState.requestId;
      let requestBody = {request_id:orchestratorPanelState.requestId, request_version:orchestratorPanelState.requestVersion, state:orchestratorPanelState.latestApprovedState};
      if (!hasRequest || orchestratorPanelState.dirty) {
        const requestResponse = await fetch(hasRequest
          ? `/api/request/versioned/${encodeURIComponent(orchestratorPanelState.requestId)}`
          : "/api/request/versioned", {
          method:hasRequest ? "PUT" : "POST", headers:{"Content-Type":"application/json"},
          body:JSON.stringify(hasRequest
            ? {expected_version:orchestratorPanelState.requestVersion, state:draft}
            : {state:draft}),
        });
        requestBody = await requestResponse.json();
        if (!requestResponse.ok || !requestBody.request_id) throw new Error(requestBody.error || "request_sync_failed");
        if (hasRequest && requestBody.request_id !== orchestratorPanelState.requestId) throw new Error("request_identity_mismatch");
        orchestratorPanelState.requestId = requestBody.request_id;
        orchestratorPanelState.requestVersion = requestBody.request_version;
        orchestratorPanelState.latestApprovedState = snapshotApprovedLatestState(requestBody.state);
        orchestratorPanelState.caseMatrixSyncedRequestId = requestBody.request_id;
        orchestratorPanelState.caseMatrixSyncedRequestVersion = requestBody.request_version;
        orchestratorPanelState.previewRenderedRequestId = "";
        orchestratorPanelState.previewRenderedRequestVersion = null;
        orchestratorPanelState.dirty = false;
      }
      if (orchestratorPanelState.conversationId) return orchestratorPanelState.conversationId;
      const conversationResponse = await fetch("/api/conversations", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body:JSON.stringify({request_id:requestBody.request_id}),
      });
      const conversationBody = await conversationResponse.json();
      if (!conversationResponse.ok || !conversationBody.conversation_id) throw new Error(conversationBody.error || "conversation_bootstrap_failed");
      orchestratorPanelState.conversationId = conversationBody.conversation_id;
      return orchestratorPanelState.conversationId;
    }

    function orchestratorResponseDetail(data){
      const reasons = asArray(data.reasons).map(String).filter(Boolean);
      const parts = [];
      if (data.route_category) parts.push(`경로: ${data.route_category}`);
      if (reasons.length) parts.push(`사유: ${reasons.join(" · ")}`);
      const planner = asObj(data.planner_decision);
      if (Object.keys(planner).length) parts.push(`다음 입력 안내: ${planner.kind || "read-only"}`);
      return parts.join("\n");
    }

    function proposalStatusText(status){
      const labels = {pending:"대기", approved:"승인됨", rejected:"거절됨", conflicted:"충돌", failed:"실패", expired:"만료", unknown:"알 수 없음", error:"오류"};
      return labels[String(status || "unknown")] || String(status || "unknown");
    }

    function setOrchestratorProposalControls(card, disabled){
      asArray(card?.children).forEach(node => {
        if (node?.dataset?.orchestratorProposalControl) node.disabled = disabled;
        asArray(node?.children).forEach(child => { if (child?.dataset?.orchestratorProposalControl) child.disabled = disabled; });
      });
    }

    // H5-ORCH-021 deliberately consumes the server-produced Fieldset snapshot.
    // It only reads its active/required flags; it does not reproduce Fieldset,
    // Registry, validation, or condition-normalization rules in the client.
    function approvedConditionFieldset(state){
      const source = asObj(state);
      const groups = asArray(asObj(source.request_context).condition_fieldset_snapshot);
      const cards = asArray(asObj(source.conditions).condition_sets);
      const fields = new Map();
      const valuesFor = (groupKey, fieldKey) => cards.filter(card => String(asObj(card).type || "") === groupKey).flatMap(card => {
        const row = asObj(card);
        if (groupKey === "operating") {
          return asArray(row.fans).filter(fan => asObj(fan).running !== false).map(fan => asObj(asObj(fan).values)[fieldKey]);
        }
        const field = asObj(asObj(row.fields)[fieldKey]);
        return [field.value ?? asObj(row.fields)[fieldKey]];
      }).map(value => String(value ?? "").trim()).filter(Boolean);
      groups.forEach(group => {
        const groupRow = asObj(group);
        const groupKey = String(groupRow.key || "").trim();
        if (!groupKey) return;
        asArray(groupRow.fields).forEach(field => {
          const fieldRow = asObj(field);
          const fieldKey = String(fieldRow.key || "").trim();
          if (!fieldKey) return;
          const id = `${groupKey}.${fieldKey}`;
          fields.set(id, {
            id,
            label:String(fieldRow.label || fieldKey),
            active:groupRow.active === true && fieldRow.active !== false,
            required:fieldRow.required === true,
            values:valuesFor(groupKey, fieldKey),
          });
        });
      });
      return fields;
    }

    function renderApprovedConditionalImpact(beforeState, latestState){
      if (!beforeState) return;
      const before = approvedConditionFieldset(beforeState);
      const after = approvedConditionFieldset(latestState);
      const ids = new Set([...before.keys(), ...after.keys()]);
      const lines = [];
      ids.forEach(id => {
        const previous = before.get(id) || {active:false, required:false, values:[]};
        const current = after.get(id) || {active:false, required:false, values:[], label:id};
        const label = current.label || previous.label || id;
        if (!previous.active && current.active) lines.push(`활성화: ${label}`);
        if (current.active && current.required && (!previous.active || !previous.required)) lines.push(`새 필수 입력: ${label}`);
        if (previous.active && !current.active) {
          lines.push(`비활성화: ${label}`);
          if (previous.values.length) lines.push(`값 보존 안내: ${label} — 기존 값 ${previous.values.join(", ")}은 자동으로 삭제하거나 정리하지 않습니다.`);
        }
      });
      if (lines.length) orchestratorMessage("assistant", "조건부 필드 영향 안내", lines.join("\n"));
    }

    function snapshotApprovedLatestState(state){
      // Keep an immutable server-read baseline so later client draft edits cannot
      // become impact authority.
      return JSON.parse(JSON.stringify(state));
    }

    function hasApprovedLatestStateShape(latest){
      const response = asObj(latest);
      const state = response.state;
      const requiredSections = ["metadata", "request_context", "basic_info", "analysis_overview", "geometry", "conditions", "case_matrix", "review", "legacy_internal"];
      return response.request_id === orchestratorPanelState.requestId
        && Number.isFinite(response.request_version)
        && state && typeof state === "object" && !Array.isArray(state)
        && requiredSections.every(section => state[section] && typeof state[section] === "object" && !Array.isArray(state[section]));
    }

    async function refreshApprovedOrchestratorRequest(proposalId){
      if (!proposalId || !orchestratorPanelState.requestId || orchestratorPanelState.refreshedProposalIds.has(proposalId)) return false;
      // Consume this server-approved Proposal before the read: a replay or retry must not refresh twice.
      invalidateCaseMatrixSync();
      orchestratorPanelState.refreshedProposalIds.add(proposalId);
      const response = await fetch(`/api/request/versioned/${encodeURIComponent(orchestratorPanelState.requestId)}`);
      const latest = await response.json();
      if (!response.ok || !hasApprovedLatestStateShape(latest)) {
        throw new Error(asObj(latest).error || "request_refresh_failed");
      }
      const previousApprovedState = orchestratorPanelState.latestApprovedState;
      // Only the canonical latest-read is allowed to replace the legacy form state.
      requestState = latest.state;
      orchestratorPanelState.requestVersion = latest.request_version;
      syncEditorFromState();
      renderDerivedPanels();
      renderApprovedConditionalImpact(previousApprovedState, latest.state);
      orchestratorPanelState.latestApprovedState = snapshotApprovedLatestState(latest.state);
      orchestratorPanelState.dirty = false;
      // The Action gate is a display-only receipt of this exact H5-020 latest GET.
      orchestratorPanelState.caseMatrixSyncedRequestId = latest.request_id;
      orchestratorPanelState.caseMatrixSyncedRequestVersion = latest.request_version;
      return true;
    }

    async function decideOrchestratorProposal(proposalId, decision, card, statusNode){
      if (!proposalId || !["approve", "reject"].includes(decision) || orchestratorPanelState.decisionIds.has(proposalId)) return;
      orchestratorPanelState.decisionIds.add(proposalId);
      setOrchestratorProposalControls(card, true);
      statusNode.textContent = "상태: 처리 중";
      try {
        await createOrchestratorConversation();
        const response = await fetch("/api/orchestrator/proposals/decision", {
          method:"POST", headers:{"Content-Type":"application/json"},
          body:JSON.stringify({proposal_id:proposalId, decision}),
        });
        const data = await response.json();
        const status = String(data.status || (data.error === "proposal_not_found" ? "unknown" : "error"));
        statusNode.textContent = `상태: ${proposalStatusText(status)}`;
        if (response.ok && data.ok === true && data.proposal_id === proposalId && status === "approved") {
          try {
            await refreshApprovedOrchestratorRequest(proposalId);
          } catch (_err) {
            statusNode.textContent = "상태: 승인됨 · 최신 의뢰서 동기화 오류";
            orchestratorMessage("assistant", "변경은 승인되었지만 최신 의뢰서를 화면에 동기화하지 못했습니다.");
          }
          if (asObj(data.proposal).status === "pending") {
            renderOrchestratorProposal(asObj(data.proposal), String(data.assistant || ""));
          } else {
            if (String(data.assistant || "").trim()) orchestratorMessage("assistant", String(data.assistant));
            renderNextQuestion(data);
          }
        } else if (response.ok && data.ok === true && data.proposal_id === proposalId && status === "rejected") {
          renderNextQuestion(data);
        }
      } catch (_err) {
        statusNode.textContent = "상태: 오류";
      } finally {
        // Terminal/read-only only: H5-020 owns any later refresh or synchronization.
        orchestratorPanelState.decisionIds.delete(proposalId);
      }
    }

    function renderOrchestratorProposal(proposal, detail){
      const proposalId = String(proposal.proposal_id || "");
      const node = orchestratorMessage("assistant", detail || "다음 변경 내용을 의뢰서에 반영할까요?");
      const card = document.createElement("div");
      card.className = "proposal-card orchestrator-proposal";
      const title = document.createElement("strong");
      title.textContent = "변경 제안";
      card.appendChild(title);
      const changes = asArray(proposal.changes).map(asObj);
      if (changes.length) {
        const diffList = document.createElement("ul");
        diffList.className = "proposal-list";
        changes.forEach(change => {
          const item = document.createElement("li");
          item.textContent = `${change.label || "변경 항목"}: ${change.current_value || "입력 없음"} → ${change.new_value || "입력 없음"}`;
          diffList.appendChild(item);
        });
        card.appendChild(diffList);
      }
      if (proposal.status === "pending") {
        const actions = document.createElement("div");
        actions.className = "proposal-actions";
        const status = document.createElement("span");
        status.textContent = "상태: 대기";
        for (const [decision, label] of [["approve", "반영"], ["reject", "반영하지 않음"]]) {
          const button = document.createElement("button");
          button.type = "button";
          button.textContent = label;
          button.dataset.orchestratorProposalControl = proposalId;
          button.addEventListener("click", () => decideOrchestratorProposal(proposalId, decision, card, status));
          actions.appendChild(button);
        }
        actions.appendChild(status);
        card.appendChild(actions);
      }
      node.appendChild(card);
    }

    function renderOrchestratorResponse(data){
      const proposal = asObj(data.proposal);
      if (proposal.proposal_id) {
        renderOrchestratorProposal(proposal, String(data.assistant || ""));
        return;
      }
      const kind = String(data.kind || "read_only");
      const message = kind === "clarification"
        ? String(data.question || "변경할 항목과 값을 구체적으로 다시 알려주세요.")
        : kind === "next_field"
        ? "다음 입력 항목 안내를 받았습니다."
        : "요청 내용을 확인했습니다.";
      orchestratorMessage("assistant", message);
    }

    async function sendChatMessage(){
      const text = $("chatInput").value.trim();
      if (!text || orchestratorPanelState.loading) return;
      beginChatFocusRestore();
      $("chatInput").value = "";
      pushMessage("user", text);
      let stopLoading = null;
      let minLoading = Promise.resolve();
      try{
        setOrchestratorLoading(true);
        stopLoading = startLoadingMessage("답변 생성 중입니다.");
        minLoading = delay(1000);
        const conversationId = await createOrchestratorConversation();
        const data = await postJson("/api/chat/send", {message:text, conversation_id:conversationId, mode:"auto"});
        await minLoading;
        stopLoading();
        stopLoading = null;
        adoptStateFromResponse(data);
        if (asObj(data).state) {
          syncEditorFromState();
          renderDerivedPanels();
        }
        if (asObj(data.proposal).status === "pending") {
          renderOrchestratorProposal(data.proposal, String(data.assistant || ""));
        } else {
          pushMessage("assistant", data.assistant || "답변을 생성했습니다.");
        }
        renderNextQuestion(data);
      }catch(err){
        await minLoading;
        if (typeof stopLoading === "function") stopLoading();
        const errorMessage = String(err?.message || "");
        pushMessage("assistant", errorMessage === "LLM이 정상 작동하지 않습니다."
          ? errorMessage
          : "처리 중 통신 오류가 발생했습니다. 입력 내용을 복원했습니다.");
        $("chatInput").value = text;
      } finally {
        setOrchestratorLoading(false);
        restoreChatInputFocusAfterReply();
      }
    }

    function triggerDownload(download){
      const info = asObj(download);
      if (!info.auto_download || !info.download_url) return;
      const link = document.createElement("a");
      link.href = info.download_url;
      link.download = info.filename || "";
      link.style.display = "none";
      document.body.appendChild(link);
      link.click();
      window.setTimeout(() => link.remove(), 1000);
    }

    function previewDomForWord(){
      const documentNode = document.querySelector('[data-preview-document="current-state"]');
      const clean = value => String(value || "").trim();
      const requestTitle = clean($("heroTitle")?.textContent);
      const requestNo = clean($("requestNoDisplay")?.textContent).replace(/^해석\s*의뢰\s*번호\s*:\s*/, "");
      if (!documentNode) return {request_title:requestTitle, request_no:requestNo, state:requestState, sections:[]};
      return {
        request_title:requestTitle,
        request_no:requestNo,
        state:requestState,
        sections:Array.from(documentNode.querySelectorAll('[data-preview-section]')).map(section => {
          const blocks = Array.from(section.querySelectorAll('[data-preview-label], [data-preview-group-title], table[data-preview-table]'))
            .filter(node => !node.matches('[data-preview-label]') || !node.closest('table'))
            .map(node => {
              if (node.matches('[data-preview-label]')) {
                const row = node.closest('.preview-kv');
                return {type:"field", label:clean(node.textContent), value:clean(row?.querySelector('[data-preview-value]')?.textContent)};
              }
              if (node.matches('[data-preview-group-title]')) return {type:"group", title:clean(node.textContent)};
              const rows = Array.from(node.querySelectorAll('tbody tr')).map(row => Array.from(row.querySelectorAll('td')).map(cell => clean(cell.textContent)));
              return {type:"table", key:clean(node.dataset.previewTable), caption:clean(node.querySelector('caption')?.textContent), headers:Array.from(node.querySelectorAll('thead th')).map(cell => clean(cell.textContent)), rows};
            });
          return {title:clean(section.querySelector('[data-preview-section-title]')?.textContent), blocks};
        }),
      };
    }

    async function exportWordFromPreview({useExistingPreviewDom=false}={}){
      if (!useExistingPreviewDom) {
        const reviewScreen = screenOrder.find(screen => screen.id === "SCREEN-06");
        const firstIncomplete = firstIncompleteScreenBefore(reviewScreen);
        if (firstIncomplete) {
          focusRequiredControl(firstIncomplete.screen, firstIncomplete.control);
          setScreenNavigationStatus(`${firstIncomplete.screen.id}의 필수 입력을 완료한 뒤 의뢰서를 생성할 수 있습니다.`);
          return false;
        }
        requestState = collectState();
        renderDocumentPreviewPanel();
      }
      const response = await fetch('/api/export/word', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(previewDomForWord())});
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        if (asObj(error).error === "case_matrix_coverage_incomplete") {
          renderPreviewCaseMatrixStatus(requestState, {coverage:asObj(error).coverage});
          return false;
        }
        if (asObj(error).error === "case_matrix_duplicate") {
          renderPreviewCaseMatrixStatus(requestState, {configurationIssues:[asObj(error).duplicate]});
          return false;
        }
        if (asObj(error).error === "case_matrix_selection_missing") {
          renderPreviewCaseMatrixStatus(requestState, {configurationIssues:asArray(error.issues)});
          return false;
        }
        throw new Error('Word export failed');
      }
      const file = await response.blob();
      const link = document.createElement('a');
      link.href = URL.createObjectURL(file);
      link.download = 'analysis_request.docx';
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      window.setTimeout(() => { URL.revokeObjectURL(link.href); link.remove(); }, 1000);
      return true;
    }

    async function runWordExportFromPreview(){
      const action = $("wordExportSlotBtn");
      if (!action || action.disabled || wordExportInProgress) return false;
      wordExportInProgress = true;
      action.disabled = true;
      action.textContent = "확인 중...";
      try {
        return await exportWordFromPreview();
      } finally {
        wordExportInProgress = false;
        action.textContent = "의뢰서 생성(Word)";
        renderScreenNavigation();
      }
    }

    function mutateRows(listName, action, index){
      if (listName !== "comparison_products") return;
      clearCaseConfigurationWarning();
      const products = collectProductCards();
      const baseProduct = products.find(product => product.role === "base") || asObj(requestState.geometry).base_product;
      const state = {...requestState, geometry:{...asObj(requestState.geometry), base_product:baseProduct, comparison_products:products.filter(product => product.role === "comparison")}};
      const values = [...asArray(state.geometry.comparison_products)];
      let focusSelector = "";
      if (action === "add") {
        values.push({geometry_id:`comparison_${Date.now()}_${values.length + 1}`, role:"comparison", drawing_no:"", display_name:"", difference_from_base:""});
        const added = values[values.length - 1];
        $("productRows").insertAdjacentHTML("beforeend", productRow(added, values.length - 1, true));
        focusSelector = `#productRows [data-product-role="comparison"][data-product-index="${values.length - 1}"] [data-product-field="drawing_no"]`;
      }
      if (action === "remove") {
        values.splice(index, 1);
        document.querySelector(`#productRows [data-product-role="comparison"][data-product-index="${index}"]`)?.remove();
        reindexProductRows();
        focusSelector = values.length
          ? `#productRows [data-product-role="comparison"][data-product-index="${Math.min(index, values.length - 1)}"] [data-product-field="drawing_no"]`
          : '[data-action="add-comparison"]';
      }
      requestState = {...state, geometry:{...asObj(state.geometry), comparison_products:values}};
      renderGeometryCadWarning();
      if (focusSelector) window.requestAnimationFrame(() => document.querySelector(focusSelector)?.focus());
      schedulePreviewRefresh();
    }
    function mutateConditionValues(fieldKey, action, index){
      clearCaseConfigurationWarning();
      const state = collectState();
      const field = asArray(state.conditions.fields).find(item => item.key === fieldKey);
      if (!field) return;
      if (!Array.isArray(field.values)) field.values = [{value:""}];
      if (action === "add") field.values.push({value:"", status:"missing", source:"user"});
      if (action === "remove" && field.values.length > 1) field.values.splice(index,1);
      requestState = state;
      renderConditionFields();
      schedulePreviewRefresh();
    }

    function firstAvailableCaseCombination(matrix, rows, targetScope, scoped){
      const optionsByScope = asObj(matrix.dropdown_options_by_scope);
      const options = asObj(scoped ? optionsByScope[targetScope] : matrix.dropdown_options);
      const conditionKeys = asArray(matrix.visible_columns)
        .filter(column => contextText(asObj(column).kind) === "condition")
        .map(column => contextText(asObj(column).key))
        .filter(Boolean);
      const optionValues = key => asArray(options[key]).map(option => contextText(asObj(option).value)).filter(Boolean);
      const fields = ["geometry_id", ...conditionKeys];
      const valuesByField = new Map(fields.map(key => [key, optionValues(key)]));
      if (fields.some(key => !valuesByField.get(key).length)) return null;
      const existing = new Set(
        rows.filter(row => !scoped || contextText(asObj(row).analysis_scope) === targetScope)
          .map(row => {
            const item = asObj(row), values = asObj(item.condition_values);
            return [contextText(item.geometry_id), ...conditionKeys.map(key => contextText(values[key]))].join("\u001f");
          })
      );
      const selected = {};
      const choose = index => {
        if (index === fields.length) {
          const signature = fields.map(key => selected[key]).join("\u001f");
          return existing.has(signature) ? null : {...selected};
        }
        const key = fields[index];
        for (const value of valuesByField.get(key)) {
          selected[key] = value;
          const result = choose(index + 1);
          if (result) return result;
        }
        return null;
      };
      return choose(0);
    }

    function mutateCaseRows(action, caseId=""){
      const state = collectState();
      const matrix = asObj(state.case_matrix);
      const rows = asArray(matrix.rows);
      const analysisScope = typeof activeCaseScope === "string" ? activeCaseScope : "";
      const contextScope = contextText(asObj(state.request_context).analysis_scope);
      const scoped = contextScope === "both" || ["indoor","outdoor"].includes(contextScope);
      const targetScope = scoped ? (analysisScope || (contextScope === "both" ? "indoor" : contextScope)) : "";
      const scopedRows = rows.filter(row => !scoped || contextText(asObj(row).analysis_scope) === targetScope);
      if (action === "add") {
        lastCaseDeleteNoticeVisible = false;
        const combination = firstAvailableCaseCombination(matrix, rows, targetScope, scoped);
        if (!combination) {
          showCaseConfigurationInfo();
          renderCasePreview();
          return;
        }
        clearCaseConfigurationWarning();
        const values = {};
        Object.entries(combination).forEach(([key, value]) => { if (key !== "geometry_id") values[key] = value; });
        rows.push({case_id:`${targetScope ? `${targetScope}_` : ""}case_${Date.now()}`, ...(scoped ? {analysis_scope:targetScope} : {}), geometry_id:combination.geometry_id, auto_geometry_id:"", condition_values:values});
      } else if (action === "remove") {
        if (scopedRows.length <= 1) {
          lastCaseDeleteNoticeVisible = true;
          renderCasePreview();
          return;
        }
        lastCaseDeleteNoticeVisible = false;
        const nextRows = rows.filter(row => contextText(asObj(row).case_id) !== caseId);
        requestState = {...state, case_matrix:{...matrix, rows:nextRows}};
        renderCasePreview();
        schedulePreviewRefresh();
        return;
      }
      requestState = {...state, case_matrix:{...matrix, rows}};
      caseValidationPending = true;
      renderCasePreview();
      schedulePreviewRefresh();
    }

    function jumpToIssue(section, fieldKey){
      const sectionId = {
        basic_info: "section-basic",
        analysis_overview: "section-overview",
        geometry: "section-geometry",
        conditions: "section-conditions",
        case_matrix: "section-case",
      }[section] || "section-basic";
      navigateScreen(screenForSection(section), {focus:false});
      const sectionEl = $(sectionId);
      if (sectionEl) sectionEl.classList.add("open");
      let target = null;
      if (section === "basic_info" || section === "analysis_overview") {
        target = pathInput(section, fieldKey);
      } else if (section === "geometry") {
        const indexMatch = String(fieldKey || "").match(/comparison_products\[(\d+)\]/);
        const productIndex = indexMatch ? Number.parseInt(indexMatch[1], 10) : 0;
        const productRole = indexMatch ? "comparison" : "base";
        const productField = String(fieldKey || "").includes("difference_from_base") ? "description" : "drawing_no";
        target = document.querySelector(`[data-product-role="${productRole}"][data-product-index="${productIndex}"] [data-product-field="${productField}"]`);
      } else if (section === "conditions") {
        target = document.querySelector(`input[data-condition-key="${CSS.escape(fieldKey || "")}"], input[data-condition-checkbox="${CSS.escape(fieldKey || "")}"]`);
      }
      (target || sectionEl)?.scrollIntoView({behavior:"smooth", block:"center"});
      if (target) {
        target.classList.add("field-highlight");
        target.focus?.();
        window.setTimeout(() => target.classList.remove("field-highlight"), 1800);
      }
    }

    function wireUndecidedComboboxes(root=document){
      root.querySelectorAll("[data-undecided-combobox]").forEach(combobox => {
        if (combobox.dataset.undecidedWired === "true") return;
        combobox.dataset.undecidedWired = "true";
        const input = combobox.querySelector("[data-undecided-input]");
        const toggle = combobox.querySelector("[data-undecided-toggle]");
        const menu = combobox.querySelector("[data-undecided-menu]");
        toggle?.addEventListener("click", () => {
          setUndecidedComboboxOpen(combobox, Boolean(menu?.hidden), {focusOption:Boolean(menu?.hidden)});
        });
        menu?.addEventListener("click", event => {
          const option = event.target.closest("[data-undecided-mode]");
          if (option) selectUndecidedComboboxMode(combobox, option.dataset.undecidedMode || "custom");
        });
        menu?.querySelectorAll("[data-undecided-mode]").forEach(option => {
          option.addEventListener("mouseenter", () => setUndecidedActiveOption(combobox, option, {focus:true}));
          option.addEventListener("focus", () => setUndecidedActiveOption(combobox, option));
        });
        input?.addEventListener("keydown", event => {
          if (event.key === "ArrowDown") {
            event.preventDefault();
            setUndecidedComboboxOpen(combobox, true, {focusOption:true});
          } else if (event.key === "Escape") {
            setUndecidedComboboxOpen(combobox, false);
          }
        });
        menu?.addEventListener("keydown", event => {
          const options = Array.from(combobox.querySelectorAll("[data-undecided-mode]"));
          const index = options.indexOf(document.activeElement);
          if (event.key === "Escape") {
            event.preventDefault();
            setUndecidedComboboxOpen(combobox, false);
            toggle?.focus();
          } else if (event.key === "ArrowDown" || event.key === "ArrowUp") {
            event.preventDefault();
            const direction = event.key === "ArrowDown" ? 1 : -1;
            setUndecidedActiveOption(combobox, options[(index + direction + options.length) % options.length], {focus:true});
          }
        });
      });
    }

    function wireEvents(){
      initPanelResizer();
      document.addEventListener("pointerdown", handlePendingChatFocusPointerDown, true);
      document.addEventListener("pointerdown", handleSelectPickerPointerDown, true);
      document.addEventListener("keydown", handlePendingChatFocusKeyDown, true);
      document.addEventListener("keydown", handleSelectPickerKeyDown, true);
      window.addEventListener("blur", cancelChatFocusRestore);
      window.addEventListener("resize", () => closeSelectPicker());
      document.addEventListener("scroll", handleSelectPickerScroll, true);
      document.addEventListener("visibilitychange", () => {
        if (document.hidden) cancelChatFocusRestore();
      });
      configureDesiredCompletionDateMinimum();
      pathInput("analysis_overview", "desired_completion_date")?.addEventListener("focus", configureDesiredCompletionDateMinimum);
      wireUndecidedComboboxes();
      wirePmsProjectCombobox();
      pathInput("analysis_overview", "request_type")?.addEventListener("change", event => {
        applyRequestTypeChange(event.target.value);
        touchedFields.add("analysis_overview.request_type");
        schedulePreviewRefresh();
      });
      document.addEventListener("click", event => {
        document.querySelectorAll("[data-undecided-combobox]").forEach(combobox => {
          if (!combobox.contains(event.target)) setUndecidedComboboxOpen(combobox, false);
        });
        if (!event.target.closest("[data-pms-combobox]")) setPmsMenuOpen(false);
      });
      document.addEventListener("focusin", event => {
        document.querySelectorAll("[data-undecided-combobox]").forEach(combobox => {
          if (!combobox.contains(event.target)) setUndecidedComboboxOpen(combobox, false);
        });
      });
      $("ragToggle").addEventListener("change", () => { requestState = collectState(); renderDerivedPanels(); });
      $("newRequestBtn").addEventListener("click", () => {
        startNewRequest().catch(err => pushMessage("assistant", `새 의뢰 시작 실패: ${err.message}`));
      });
      $("requestPreviewBtn").addEventListener("click", openRequestPreview);
      $("requestPreviewCloseBtn").addEventListener("click", closeRequestPreview);
      $("requestPreviewModal").addEventListener("click", event => {
        if (event.target === event.currentTarget) closeRequestPreview();
      });
      $("agentClearBtn").addEventListener("click", clearAgentConversation);
      $("agentHideBtn").addEventListener("click", () => setAgentOpen(false));
      $("agentOpenBtn").addEventListener("click", () => setAgentOpen(true));
      $("wordExportSlotBtn").addEventListener("click", () => {
        runWordExportFromPreview().catch(err => console.error(err));
      });
      $("sendBtn").addEventListener("click", sendChatMessage);
      $("chatInput").addEventListener("keydown", event => {
        if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
          event.preventDefault();
          sendChatMessage();
        }
      });
      $("contextChangeBtn").addEventListener("click", showContextChangeWarning);
      $("contextChangeContinue").addEventListener("click", continueContextChange);
      $("contextChangeCancel").addEventListener("click", hideContextChangeWarning);
      $("fanLimitConfirm").addEventListener("click", hideFanLimitModal);
      document.addEventListener("focusin", event => {
        if (agentOpen && $("agentDock")?.contains(event.target)) lastAgentFocus = event.target;
      });
      document.body.addEventListener("keydown", event => {
        if (!$("requestPreviewModal")?.hidden && event.key === "Escape") {
          event.preventDefault();
          closeRequestPreview();
          return;
        }
        if (!$("fanLimitModal")?.hidden) {
          if (event.key === "Tab") {
            event.preventDefault();
            $("fanLimitConfirm")?.focus();
          }
          return;
        }
        if (event.key === "Escape" && agentOpen && isAgentOverlay()) {
          event.preventDefault();
          setAgentOpen(false);
          return;
        }
        const screen = event.target.closest(".screen-map-item[data-screen]");
        if (!screen || (event.key !== "Enter" && event.key !== " ")) return;
        event.preventDefault();
        if (screen.getAttribute("aria-disabled") !== "true") {
          const targetScreen = screen.dataset.screen || "SCREEN-01";
          if (targetScreen === "SCREEN-05") confirmConditionsBeforeCaseMatrix().catch(err => pushMessage("assistant", `조건 검증 실패: ${err.message}`));
          else navigateScreen(targetScreen);
        }
      });
      document.body.addEventListener("click", event => {
        const retryGuidance = event.target.closest("#retryAnalysisResultGuidance");
        if (retryGuidance) { refreshAnalysisResultGuidance(); return; }
        const scopeTab = event.target.closest("button[data-scope-tab][data-analysis-scope]");
        if (scopeTab) { switchAnalysisScopeTab(scopeTab.dataset.scopeTab || "", scopeTab.dataset.analysisScope || ""); return; }
        const scopeChoice = event.target.closest("#analysisScopeField button[data-analysis-scope]");
        if (scopeChoice) {
          document.querySelectorAll("#analysisScopeField .required-field-highlight").forEach(control => control.classList.remove("required-field-highlight"));
          $("analysisScopeField")?.classList.remove("required-field-highlight");
          updateRequestContextDraft("analysis_scope", scopeChoice.dataset.analysisScope || "indoor"); return;
        }
        const stageAssist = event.target.closest("button[data-stage-assist-prompt]");
        if (stageAssist) { fillStageAssistPrompt(stageAssist.dataset.stageAssistPrompt || stageAssist.textContent || ""); return; }
        const prepStart = event.target.closest("#prepStartBtn");
        if (prepStart) {
          confirmRequestContext().catch(err => pushMessage("assistant", `조합 확정 실패: ${err.message}`));
          return;
        }
        const dropdownRestore = event.target.closest("button[data-dropdown-restore-path]");
        if (dropdownRestore) { restoreDropdownControl(dropdownRestore); return; }
        const proposalRefresh = event.target.closest("button[data-chat-proposal-refresh]");
        if (proposalRefresh) { fillStageAssistPrompt(proposalRefresh.dataset.chatProposalRefresh || ""); return; }
        const quickAction = event.target.closest("button[data-chat-quick-action]");
        if (quickAction) { runChatQuickAction(quickAction.dataset.chatQuickAction || "").catch(err => pushMessage("assistant", `빠른 실행 실패: ${err.message}`)); return; }
        const screenAction = event.target.closest("button[data-screen-action]");
        if (screenAction) {
          const targetScreen = screenAction.dataset.screenAction || "SCREEN-01";
          if (targetScreen === "SCREEN-05") { confirmConditionsBeforeCaseMatrix().catch(err => pushMessage("assistant", `조건 검증 실패: ${err.message}`)); return; }
          navigateScreen(targetScreen); return;
        }
        const screen = event.target.closest(".screen-map-item[data-screen]");
        if (screen && screen.getAttribute("aria-disabled") !== "true") {
          const targetScreen = screen.dataset.screen || "SCREEN-01";
          if (targetScreen === "SCREEN-05") { confirmConditionsBeforeCaseMatrix().catch(err => pushMessage("assistant", `조건 검증 실패: ${err.message}`)); return; }
          navigateScreen(targetScreen); return;
        }
        const issue = event.target.closest("button[data-issue-jump]");
        if (issue) { jumpToIssue(issue.dataset.section || "", issue.dataset.field || ""); return; }
        const toggle = event.target.closest("[data-toggle-section]");
        if (toggle) { $(toggle.dataset.toggleSection)?.classList.toggle("open"); return; }
        const heatExchangerRestore = event.target.closest("button[data-heat-exchanger-restore]");
        if (heatExchangerRestore) { restoreHeatExchangerDropdown(heatExchangerRestore); return; }
        const fanCountRestore = event.target.closest("button[data-fan-count-restore]");
        if (fanCountRestore) { restoreFanCountDropdown(fanCountRestore); return; }
        const fanDetailToggle = event.target.closest("button[data-fan-detail-toggle]");
        if (fanDetailToggle) { toggleFanDetail(fanDetailToggle); return; }
        const button = event.target.closest("button[data-action]");
        if (!button) return;
        const action = button.dataset.action;
        if (action === "confirm-case-configuration") { confirmCaseConfiguration().catch(err => console.error(err)); return; }
        if (action === "toggle-case-source") { toggleCaseSourceSummary(); return; }
        if (action === "review-case-coverage") { navigateScreen("SCREEN-05"); return; }
        if (action === "add-case") { mutateCaseRows("add"); return; }
        if (action === "remove-case") { mutateCaseRows("remove", button.dataset.caseId || ""); return; }
        if (action === "condition-recommend-request") { requestConditionRecommendation().catch(err => pushMessage("assistant", `조건 추천 실패: ${err.message}`)); return; }
        if (action === "add-comparison") mutateRows("comparison_products", "add", 0);
        if (action === "remove-comparison") mutateRows("comparison_products", "remove", Number.parseInt(button.dataset.index || "0",10));
        if (action === "add-condition-card") {
          preserveEditorDraftBeforeRerender();
          const type = button.dataset.cardType;
          const cards = collectConditionSets();
          const base = cards.find(card => contextText(asObj(card).type) === type && (!hasBothAnalysisScopes() || contextText(asObj(card).analysis_scope) === activeConditionScope));
          if (!base) return;
          const card = JSON.parse(JSON.stringify(base));
          const number = cards.filter(item => contextText(asObj(item).type) === type && contextText(asObj(item).analysis_scope) === contextText(card.analysis_scope)).length + 1;
          do { card.id = newConditionCardId(type); }
          while (cards.some(item => contextText(asObj(item).id) === card.id));
          card.is_default = false;
          Object.keys(asObj(card.fields)).forEach(key => { card.fields[key] = ""; });
          if (type === "operating") {
            card.name = `운전 ${number}`;
            card.fan_rpm_mode = "";
            card.fans = [{id:"fan_1", name:"", location:"", running:true, values:{fan_rpm:""}}];
          }
          if (type === "heat_exchanger") card.fields.name = `사양 ${number}`;
          if (type === "heat_exchanger" && heatExchangerType([card]) === "Micro-Channel") card.fields.fin_type = "Flat";
          requestState.conditions = {...asObj(requestState.conditions), condition_sets:[...cards, card]}; syncEditorFromState();
          window.requestAnimationFrame(() => document.querySelector(`[data-condition-card="${CSS.escape(card.id)}"] input:not([disabled]), [data-condition-card="${CSS.escape(card.id)}"] select:not([disabled])`)?.focus());
          schedulePreviewRefresh(); return;
        }
        if (action === "remove-condition-card") {
          preserveEditorDraftBeforeRerender();
          const cardId = button.dataset.cardId;
          const cards = collectConditionSets();
          const target = cards.find(card => contextText(asObj(card).id) === cardId);
          if (!target) return;
          if (target.is_default === true) {
            clearHeatExchangerCustomFields(target.id, heatExchangerCascadeKeys);
            Object.keys(asObj(target.fields)).forEach(key => { target.fields[key] = ""; });
            if (contextText(target.type) === "heat_exchanger" && heatExchangerType([target]) === "Micro-Channel") target.fields.fin_type = "Flat";
            if (contextText(target.type) === "operating") {
              fanCountCustomCards.delete(contextText(target.id));
              if (expandedFanCardId === contextText(target.id)) expandedFanCardId = "";
              target.fan_rpm_mode = "";
              target.fans = [{id:"fan_1", name:"", location:"", running:true, values:{fan_rpm:""}}];
            }
            requestState.conditions = {...asObj(requestState.conditions), condition_sets:cards}; syncEditorFromState();
            window.requestAnimationFrame(() => document.querySelector(`[data-condition-card="${CSS.escape(cardId)}"] input:not([disabled]), [data-condition-card="${CSS.escape(cardId)}"] select:not([disabled])`)?.focus());
            schedulePreviewRefresh(); return;
          }
          const typeCards = cards.filter(card => contextText(asObj(card).type) === contextText(asObj(target).type) && contextText(asObj(card).analysis_scope) === contextText(asObj(target).analysis_scope));
          const targetIndex = typeCards.indexOf(target);
          clearHeatExchangerCustomFields(target.id, heatExchangerCascadeKeys);
          fanCountCustomCards.delete(contextText(target.id));
          if (expandedFanCardId === contextText(target.id)) expandedFanCardId = "";
          const remaining = cards.filter(card => contextText(asObj(card).id) !== cardId);
          const remainingTypeCards = remaining.filter(card => contextText(asObj(card).type) === contextText(asObj(target).type) && contextText(asObj(card).analysis_scope) === contextText(asObj(target).analysis_scope));
          const focusCard = remainingTypeCards[Math.min(targetIndex, remainingTypeCards.length - 1)];
          requestState.conditions = {...asObj(requestState.conditions), condition_sets:remaining}; syncEditorFromState();
          if (focusCard) window.requestAnimationFrame(() => document.querySelector(`[data-condition-card="${CSS.escape(focusCard.id)}"] input:not([disabled]), [data-condition-card="${CSS.escape(focusCard.id)}"] select:not([disabled])`)?.focus());
          schedulePreviewRefresh(); return;
        }
        if (action === "add-condition-value" || action === "remove-condition-value") mutateConditionValues(button.dataset.fieldKey, action === "add-condition-value" ? "add" : "remove", Number.parseInt(button.dataset.index || "0",10));
      });
      $("formView").addEventListener("input", event => {
        if (event.target.matches("input, textarea, select")) event.target.classList.remove("required-field-highlight");
        if (event.target.matches("input, textarea, select") && !event.target.matches("select[data-case-field]")) {
          const path = event.target.dataset.path || event.target.dataset.conditionKey || event.target.dataset.productField || event.target.dataset.rowList || event.target.dataset.cardField || "";
          if (path) touchedFields.add(path);
          schedulePreviewRefresh();
        }
      });
      $("formView").addEventListener("change", event => {
        if (event.target.matches("input, textarea, select")) event.target.classList.remove("required-field-highlight");
        if (event.target.matches("input, textarea, select")) renderScreenNavigation();
        if (event.target.matches("select[data-case-field]")) preserveCaseSelections(event.target);
        else if (event.target.matches('[data-product-field="drawing_no"]')) schedulePreviewRefresh();
        else if (event.target.matches("select[data-heat-exchanger-type]")) handleHeatExchangerTypeChange(event.target);
        else if (event.target.matches("select[data-heat-exchanger-field]")) handleHeatExchangerCascadeChange(event.target);
        else if (event.target.matches("input[data-heat-exchanger-custom-field]")) handleHeatExchangerCustomInput(event.target);
        else if (event.target.matches("select[data-fan-count]")) handleFanCountChange(event.target);
        else if (event.target.matches("input[data-fan-count-custom]")) resizeFanRpmInputs(contextText(event.target.dataset.cardId), event.target.value);
        else if (event.target.matches("select[data-fan-rpm-mode]")) handleFanRpmModeChange(event.target);
        else if (event.target.matches("#operationModeSelect")) updateOperationMode(event.target.value).catch(err => pushMessage("assistant", `운전 구분 변경 실패: ${err.message}`));
        else if (event.target.matches("input[data-condition-option]")) { requestState = collectState(); renderConditionFields(); schedulePreviewRefresh(); }
        else if (event.target.matches("#quickDivisionSelect")) updateRequestContextDraft("division", event.target.value);
        else if (event.target.matches("#quickProductLineupSelect")) updateRequestContextDraft("product_lineup", event.target.value);
        else if (event.target.matches("#quickPlatformSelect")) updateRequestContextDraft("platform", event.target.value);
        else if (event.target.matches("#quickChassisSelect")) updateRequestContextDraft("chassis", event.target.value);
        else if (event.target.matches("#quickAnalysisTypeSelect")) updateRequestContextDraft("analysis_type", event.target.value);
        else if (event.target.matches("#decisionUseSelect")) { renderDecisionUseAuxiliary(event.target.value); schedulePreviewRefresh(); }
        else if (event.target.matches("select[data-dropdown-path]")) handleDropdownChange(event.target);
        else if (event.target.matches("select[data-condition-select]")) handleConditionSelectChange(event.target);
        else if (event.target.matches("input[type='checkbox']")) schedulePreviewRefresh();
      });
    }

    async function loadBootstrap(){
      const res = await fetch("/api/bootstrap");
      const data = await res.json();
      adoptStateFromResponse(data);
      resetCaseImpactBaseline({deferUntilMatrixRender:true});
      schema = data.schema || {};
      heatExchangerCatalog = asArray(asObj(data.heat_exchanger_catalog).rows);
      activeTopTab = "write";
      requestState.metadata = {...asObj(requestState.metadata), active_top_tab: activeTopTab};
      asArray(asObj(requestState.metadata).touched_fields).forEach(item => touchedFields.add(String(item)));
      renderAgentDock();
      setupDropdowns();
      restoreChatHistoryFromState();
      syncEditorFromState();
      fetchProductHierarchyOptions().catch(err => pushMessage("assistant", `제품군/platform 목록 불러오기 실패: ${err.message}`));
    }

    wireEvents();
    loadBootstrap().catch(err => pushMessage("assistant", `불러오기 실패: ${err.message}`));
  </script>
</body>
</html>
"""
