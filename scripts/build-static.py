#!/usr/bin/env python3
"""Build static HTML pages from TOML data files."""

import tomllib, html
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "docs"
OUT = BASE
CSS = (BASE / "assets" / "css" / "style.css").read_text()

TAB_BAR = '<div class="sheet-bar">{tabs}<a class="sheet-add" href="#" onclick="openModal();return false" title="提交漏洞">＋</a></div>'

TOP_BAR = """<div class="doc-topbar">
  <div class="doc-title"><a href="index.html">护网漏洞库</a> <small>by AdySec</small></div>
  <div class="doc-actions">
    <button class="theme-btn" onclick="toggleTheme()" title="切换主题">🌙</button>
    <a class="btn" href="#" onclick="openModal();return false">＋ 提交漏洞</a>
    <a class="btn btn-outline" href="https://github.com/adysec/hwpoc" target="_blank">GitHub</a>
  </div>
</div>"""

FOOTER = '<div class="doc-footer">护网漏洞库 · 原数据维护于腾讯文档，因人数限制迁移至此；社区通过 Issue 提交 · <a href="mailto:admin@adysec.com">AdySec &lt;admin@adysec.com&gt;</a></div>'

SCRIPT = """<script>
(function(){var si=document.getElementById('searchInput'),ss=document.getElementById('searchCol');if(si&&ss){
var cols={'全部':-1};document.querySelectorAll('#vulnTable thead th').forEach(function(th,i){cols[th.textContent.trim().replace(/\\s*↕\\s*/,'')]=i});
function doSearch(){var q=si.value.toLowerCase(),col=parseInt(ss.value);document.querySelectorAll('#vulnTable tbody tr').forEach(function(r){
r.style.display=(col<0?r.textContent.toLowerCase().includes(q):(r.cells[col]||{}).textContent.toLowerCase().includes(q))?'':'none'})}
si.addEventListener('input',doSearch);ss.addEventListener('change',doSearch)}})();
(function(){document.querySelectorAll('#vulnTable thead th').forEach(function(th){th.addEventListener('click',function(){
var tb=document.querySelector('#vulnTable tbody'),rows=Array.from(tb.querySelectorAll('tr')),col=parseInt(th.dataset.col),
asc=!th.classList.contains('sort-asc');document.querySelectorAll('#vulnTable thead th').forEach(function(h){
h.classList.remove('sort-asc','sort-desc')});th.classList.add(asc?'sort-asc':'sort-desc');rows.sort(function(a,b){
var va=(a.cells[col]||{}).textContent||'',vb=(b.cells[col]||{}).textContent||'';
return asc?va.localeCompare(vb,'zh'):vb.localeCompare(va,'zh')});rows.forEach(function(r){tb.appendChild(r)})})})})();
function copyCell(el){el.classList.toggle('expand');var t=el.textContent.trim();if(!t)return;
navigator.clipboard.writeText(t).then(function(){var to=document.getElementById('toast');if(!to){to=document.createElement('div');to.id='toast';document.body.appendChild(to)}to.textContent='✓ 已复制: '+t.substring(0,40)+(t.length>40?'...':'');to.style.opacity='1';clearTimeout(to._t);to._t=setTimeout(function(){to.style.opacity='0'},2000)}).catch(function(){})}
</script>"""

MODAL = """<div class="modal-overlay" id="submitModal">
  <div class="modal-box">
    <div class="modal-header">
      <h3>提交漏洞</h3>
      <button class="modal-close" onclick="closeModal()">\u2715</button>
    </div>
    <div class="modal-body">
      <div class="form-row">
        <div class="form-group"><label>厂商 <span class="req">*</span></label><input id="f_vendor" placeholder="如 深信服、奇安信、用友"></div>
        <div class="form-group"><label>漏洞名称 <span class="req">*</span></label><input id="f_name" placeholder="如 CVE-2025-XXXX 或 产品名+类型"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>漏洞类型 <span class="req">*</span></label><input id="f_type" placeholder="如 RCE、SQL注入、未授权访问"></div>
        <div class="form-group"><label>涉及版本</label><input id="f_version" placeholder="受影响版本号或范围"></div>
      </div>
      <div class="form-group"><label>利用路径 / URL</label><input id="f_path" placeholder="漏洞触发路径或接口"></div>
      <div class="form-group"><label>漏洞详情 / POC</label><textarea id="f_detail" rows="3" placeholder="请在此粘贴 POC 或漏洞详情"></textarea></div>
      <div class="form-group"><label>处置建议 / 修复方案</label><textarea id="f_fix" rows="2" placeholder="升级版本、补丁链接、临时缓解措施"></textarea></div>
      <div class="form-row">
        <div class="form-group"><label>情报获取时间</label><input id="f_date" placeholder="如 0630、0701"></div>
        <div class="form-group"><label>来源 / 验证人</label><input id="f_source" placeholder="提交者昵称或来源"></div>
      </div>
      <div class="form-group">
        <label>标签 <span class="req">*</span></label>
        <div class="radio-group">
          <label><input type="radio" name="label" value="0day"> 0day</label>
          <label><input type="radio" name="label" value="1day"> 1day</label>
          <label><input type="radio" name="label" value="nday"> nday</label>
        </div>
      </div>
    </div>
    <div class="modal-footer" style="flex-direction:column;align-items:stretch;gap:6px">
      <div style="font-size:12px;color:var(--text-muted);text-align:center">
        提交方式一：填写表单 → 自动创建 Issue（推荐）<br>
        提交方式二：直接 PR 到 <code style="background:var(--tag-bg);padding:1px 4px;border-radius:2px;font-size:11px">docs/{year}/</code> 目录新增 TOML 文件<br>
        提交方式三：发送邮件至 <a href="mailto:admin@adysec.com" style="color:var(--primary)">admin@adysec.com</a>
      </div>
      <div style="display:flex;gap:8px;justify-content:flex-end">
        <button class="btn btn-outline" onclick="closeModal()">取消</button>
        <button class="btn" onclick="submitVuln(MODAL_YEAR)">提交 Issue</button>
      </div>
    </div>
  </div>
</div>"""

MODAL_JS = """<script>
function openModal(){document.getElementById('submitModal').classList.add('active')}
function closeModal(){document.getElementById('submitModal').classList.remove('active')}
document.getElementById('submitModal').addEventListener('click',function(e){if(e.target===this)closeModal()});
window.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal()});
function submitVuln(year){
var v=document.getElementById('f_vendor').value.trim(),n=document.getElementById('f_name').value.trim(),
t=document.getElementById('f_type').value.trim(),ver=document.getElementById('f_version').value.trim(),
p=document.getElementById('f_path').value.trim(),d=document.getElementById('f_detail').value.trim(),
f=document.getElementById('f_fix').value.trim(),dt=document.getElementById('f_date').value.trim(),
s=document.getElementById('f_source').value.trim(),l=(document.querySelector('input[name="label"]:checked')||{}).value||'';
if(!v||!n||!t||!l){alert('请填写厂商、漏洞名称、漏洞类型和标签（必填项）');return}
var b='### 厂商 *\\n'+v+'\\n\\n### 漏洞名称 *\\n'+n+'\\n\\n### 漏洞类型 *\\n'+t;
if(ver)b+='\\n\\n### 涉及版本\\n'+ver;if(p)b+='\\n\\n### 利用路径 / URL\\n'+p;
if(d)b+='\\n\\n### 漏洞详情 / POC\\n```\\n'+d+'\\n```';if(f)b+='\\n\\n### 处置建议 / 修复方案\\n'+f;
if(dt)b+='\\n\\n### 情报获取时间\\n'+dt;b+='\\n\\n### 标签 *\\n- [x] '+l;
if(s)b+='\\n\\n### 来源 / 验证人\\n'+s;
b+='\\n\\n---\\n\\n**提交前请确认：**\\n- [ ] 该漏洞尚未存在于当前漏洞库中\\n- [ ] 信息准确，POC 经过验证或注明来源\\n- [ ] 已去除敏感信息（如内部 IP、密码等）';
var url='https://github.com/adysec/hwpoc/issues/new?labels=漏洞提交&template=submit-vulnerability.md&title='+encodeURIComponent('['+(year||'')+'] '+n)+'&body='+encodeURIComponent(b);
window.open(url,'_blank');closeModal()}
</script>"""

def load_toml_dir(dirpath):
    items = []
    if not dirpath.is_dir():
        return items
    for fp in sorted(dirpath.glob("*.toml")):
        try:
            items.append(tomllib.loads(fp.read_text()))
        except Exception as e:
            print("  [warn] skip %s: %s" % (fp.name, e))
    return items

def page(title, body, current_year=None):
    years = ["2026", "2025", "2024", "2023"]
    tabs = "".join(
        '<a class="sheet-tab%s" href="%s.html">%s</a>'
        % (" active" if y == current_year else "", y, y)
        for y in years
    )
    modal_year = current_year or ""
    html = "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n"
    html += "<meta charset=\"UTF-8\">\n<meta name=\"viewport\" content=\"width=device-width,initial-scale=1.0\">\n"
    html += "<title>%s — 护网漏洞库 by AdySec</title>\n" % title
    html += "<style>%s</style>\n" % CSS
    html += "<script>(function(){var t=localStorage.getItem('theme');if(!t){t=window.matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'}if(t==='dark'){document.documentElement.setAttribute('data-theme','dark')}})();</script>\n"
    html += "</head>\n<body>\n"
    html += TOP_BAR + "\n"
    html += TAB_BAR.replace("{tabs}", tabs) + "\n"
    html += body + "\n"
    html += MODAL.replace("MODAL_YEAR", "'%s'" % modal_year) + "\n"
    html += FOOTER + "\n"
    html += "<script>function toggleTheme(){var h=document.documentElement;var d=h.getAttribute('data-theme')==='dark';if(d){h.removeAttribute('data-theme');localStorage.setItem('theme','light')}else{h.setAttribute('data-theme','dark');localStorage.setItem('theme','dark')}}</script>\n"
    html += MODAL_JS + "\n"
    html += "</body>\n</html>"
    return html

def label_badge(l):
    if l in ("0day", "1day", "nday"):
        return '<span class="label label-%s">%s</span>' % (l, l)
    return l

def build_index():
    counts = {}
    for y in ["2026", "2025", "2024", "2023"]:
        counts[y] = len(list((DATA / y).glob("*.toml"))) if (DATA / y).is_dir() else 0
    cards = "".join(
        '<a class="home-card" href="%s.html"><span class="num">%d</span><span class="lbl">%s 年</span></a>'
        % (y, c, y) for y, c in counts.items()
    )
    body = '<div class="home-page">\n'
    body += '<h2>护网漏洞库 <small style="font-size:14px;color:var(--text-muted);font-weight:400">by AdySec</small></h2>\n'
    body += '<p>护网（HW）期间漏洞情报汇总 · 0day / 1day / nday</p>\n'
    body += '<p style="font-size:13px;color:var(--text-muted);margin-top:12px">提交漏洞：① 创建 Issue ｜ ② PR 到 <code>docs/{year}/</code> ｜ ③ 邮件 <a href="mailto:admin@adysec.com" style="color:var(--primary)">admin@adysec.com</a></p>\n'
    body += '<div class="home-cards">%s</div>\n' % cards
    body += '<div class="home-links">\n'
    body += '<a class="btn" href="#" onclick="openModal();return false">＋ 提交漏洞</a>\n'
    body += '<a class="btn btn-outline" href="https://github.com/adysec/hwpoc">GitHub 仓库</a>\n'
    body += '</div>\n</div>'
    (OUT / "index.html").write_text(page("首页", body))
    print("index.html")

def build_year(year):
    data = load_toml_dir(DATA / year)
    data.sort(key=lambda d: d.get("date", ""), reverse=True)
    count_0day = sum(1 for d in data if d.get("label") == "0day")
    count_1day = sum(1 for d in data if d.get("label") == "1day")
    count_nday = sum(1 for d in data if d.get("label") == "nday")

    if year == "2023":
        headers = ["厂商", "漏洞名称", "类型", "来源", "信息", "日期", "POC", "标签"]
        rows = []
        for d in data:
            rows.append(
                "<tr><td><span class=\"tag\">%s</span></td><td class=\"cell-hover\" onclick=\"copyCell(this)\">%s</td><td><span class=\"tag\">%s</span></td>"
                "<td>%s</td><td class=\"cell-hover\" onclick=\"copyCell(this)\">%s</td>"
                "<td>%s</td><td class=\"cell-hover\" onclick=\"copyCell(this)\">%s</td>"
                "<td>%s</td></tr>"
                % (html.escape(str(d.get("vendor",""))), html.escape(str(d.get("name",""))), html.escape(str(d.get("type",""))),
                   html.escape(str(d.get("source",""))), html.escape(str(d.get("info",""))), html.escape(str(d.get("date",""))),
                   html.escape(str(d.get("poc",""))), label_badge(d.get("label","")))
            )
    else:
        has_verifier = (year in ("2025", "2026"))
        if has_verifier:
            headers = ["厂商", "漏洞名称", "类型", "版本", "路径", "详情", "处置建议", "日期", "标签", "验真人"]
        else:
            headers = ["厂商", "漏洞名称", "类型", "版本", "路径", "详情", "处置建议", "日期", "标签"]
        rows = []
        for d in data:
            verifier_cell = "<td>%s</td>" % html.escape(str(d.get("verifier",""))) if has_verifier else ""
            rows.append(
                "<tr><td><span class=\"tag\">%s</span></td><td class=\"cell-hover\" onclick=\"copyCell(this)\">%s</td><td><span class=\"tag\">%s</span></td>"
                "<td class=\"cell-hover\" onclick=\"copyCell(this)\">%s</td>"
                "<td class=\"cell-hover\" onclick=\"copyCell(this)\">%s</td>"
                "<td class=\"cell-hover\" onclick=\"copyCell(this)\">%s</td>"
                "<td class=\"cell-hover\" onclick=\"copyCell(this)\">%s</td>"
                "<td>%s</td><td>%s</td>%s</tr>"
                % (html.escape(str(d.get("vendor",""))), html.escape(str(d.get("name",""))), html.escape(str(d.get("type",""))),
                   html.escape(str(d.get("version",""))), html.escape(str(d.get("path",""))), html.escape(str(d.get("detail",""))),
                   html.escape(str(d.get("fix",""))), html.escape(str(d.get("date",""))), label_badge(d.get("label","")),
                   verifier_cell)
            )

    date_col = 5 if year == "2023" else (7 if year in ("2026","2025","2024") else -1)
    ths = "".join(
        '<th data-col="%d"%s>%s <span class="sort-icon">↕</span></th>'
        % (i, ' class="sort-desc"' if i == date_col else "", h)
        for i, h in enumerate(headers)
    )
    tbody = "".join(rows)

    body = '<div class="toolbar">\n'
    body += '<div class="search-wrap"><span class="icon">🔍</span>\n'
    body += '<input type="text" id="searchInput" placeholder="搜索...">\n'
    body += '</div>\n'
    body += '<select id="searchCol" style="padding:4px 8px;font-size:12px;border:1px solid var(--btn-outline-border);border-radius:4px;background:var(--surface);color:var(--text);outline:none">\n'
    body += '<option value="-1">全部列</option>\n'
    for i, h in enumerate(headers):
        body += '<option value="%d">%s</option>\n' % (i, h)
    body += '</select>\n'
    body += '<span class="stat-badge total">共 %d 条</span>\n' % len(data)
    body += '<span class="stat-badge zday">0day %d</span>\n' % count_0day
    body += '<span class="stat-badge oney">1day %d</span>\n' % count_1day
    body += '<span class="stat-badge nday">nday %d</span>\n' % count_nday
    body += '</div>\n'
    body += '<div class="table-wrap">\n'
    body += '<table id="vulnTable">\n'
    body += '<thead><tr>%s</tr></thead>\n' % ths
    body += '<tbody>%s</tbody>\n' % tbody
    body += '</table>\n</div>\n'
    body += SCRIPT

    (OUT / ("%s.html" % year)).write_text(page("%s年漏洞" % year, body, current_year=year))
    print("%s.html (%d entries)" % (year, len(data)))

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ".nojekyll").write_text("")
    build_index()
    for y in ["2026", "2025", "2024", "2023"]:
        build_year(y)
    print("\nDone → file://%s/index.html" % OUT.resolve())

if __name__ == "__main__":
    main()
