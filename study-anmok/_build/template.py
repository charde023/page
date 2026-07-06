"""
template.py — HTML/CSS/JS templates for study-anmok pages.

Uses plain string.replace() with __TOKEN__ placeholders instead of str.format(),
because CSS is full of literal { } braces that would collide with .format().
"""

CSS = """
:root{
  --bg:#f8f7fc; --surface:#fff; --text:#241f36; --text-soft:#645d7a;
  --border:#e6e1f2; --accent:#5b21b6; --accent-soft:#ede9fe;
  --orange:#ef6c00; --saved:#16a34a; --warn:#b45309; --warn-bg:#fffbeb; --warn-border:#fde68a;
  --shadow:0 1px 2px rgba(36,31,54,.05),0 8px 24px rgba(36,31,54,.07);
}
*{box-sizing:border-box}
body{
  font-family:'Pretendard Variable',-apple-system,BlinkMacSystemFont,'Malgun Gothic',sans-serif;
  line-height:1.7; max-width:820px; margin:0 auto; padding:32px 24px 96px;
  color:var(--text); background:var(--bg); font-size:17px; word-break:keep-all;
}
h1{font-size:1.6rem; margin:0 0 6px}
h2{font-size:1.25rem; margin:34px 0 12px; padding-bottom:.3em; border-bottom:1px solid var(--border)}
a{color:var(--accent)}
a.back{display:inline-block; margin-bottom:18px; font-size:.92rem; color:var(--text-soft); text-decoration:none}
a.back:hover{color:var(--accent)}
.eyebrow{display:inline-block; font-size:.78rem; font-weight:700; color:var(--accent);
  background:var(--surface); padding:4px 10px; border-radius:999px; border:1px solid var(--accent-soft);
  margin-bottom:12px}
.header{margin:-32px -24px 24px; padding:30px 24px 22px;
  background:linear-gradient(160deg,var(--accent-soft) 0%, var(--bg) 100%);
  border-bottom:1px solid var(--border)}
.meta{color:var(--text-soft); font-size:.9rem; margin-top:6px}
.oneliner{margin:18px 0; padding:14px 16px; border-radius:10px; border:1px solid var(--border);
  background:var(--surface); font-size:.98rem; color:var(--text-soft)}
.callout-warn{margin:18px 0; padding:14px 16px; border-radius:10px;
  border:1px solid var(--warn-border); background:var(--warn-bg); font-size:.88rem; color:var(--warn)}
.callout-warn strong{color:var(--warn)}
span.wikiterm{border-bottom:1px dotted var(--accent); color:var(--accent); cursor:help}
a.daylink{color:var(--accent); text-decoration:none; border-bottom:1px solid var(--accent-soft)}
a.daylink:hover{border-bottom-color:var(--accent)}
.field-input-big{min-height:200px}
.checkfield{display:flex; align-items:flex-start; gap:9px; margin:8px 0; font-size:.95rem; cursor:pointer}
.checkfield input{margin-top:4px; width:17px; height:17px; accent-color:var(--accent); flex:none}
table{border-collapse:collapse; width:100%; margin:16px 0; font-size:.93rem}
th,td{border:1px solid var(--border); padding:8px 10px; text-align:left; vertical-align:top}
th{background:var(--accent-soft)}

/* input fields */
.qa-block{margin:22px 0}
.qa-question{font-weight:600; margin-bottom:8px; line-height:1.6}
.field{margin:16px 0}
.field-label{font-weight:600; margin-bottom:6px; font-size:.95rem}
.field-hint{font-size:.82rem; color:var(--text-soft); margin-bottom:6px}
.field-input{
  width:100%; font-family:inherit; font-size:16px; padding:10px 12px;
  border:1px solid var(--border); border-radius:8px; background:#fff; color:var(--text);
  resize:vertical;
}
.field-input:focus{outline:none; border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-soft)}
.field-input-cell{padding:6px 8px; font-size:.9rem}
.inline-group{display:flex; flex-wrap:wrap; gap:10px 14px; margin-top:4px}
.inline-field{display:flex; flex-direction:column; gap:4px; flex:1 1 140px; min-width:120px}
.inline-field-label{font-size:.82rem; color:var(--text-soft)}
.save-status{display:block; font-size:.78rem; color:var(--saved); margin-top:4px; min-height:1.1em}
.save-status.err{color:#dc2626}
input[type=date].field-input{max-width:220px}

/* buttons */
.toolbar{display:flex; gap:10px; flex-wrap:wrap; margin:26px 0 8px}
button.act{
  font-family:inherit; font-size:.88rem; font-weight:600; padding:9px 16px; border-radius:8px;
  border:1px solid var(--accent); background:var(--accent); color:#fff; cursor:pointer;
}
button.act.secondary{background:#fff; color:var(--accent)}
button.act:hover{opacity:.9}
.global-warning{display:none; margin:14px 0; padding:12px 14px; border-radius:8px;
  border:1px solid var(--warn-border); background:var(--warn-bg); color:var(--warn); font-size:.85rem}

.daynav{display:flex; justify-content:space-between; margin-top:36px; padding-top:16px; border-top:1px solid var(--border); font-size:.9rem}
.daynav a{text-decoration:none}

/* index page cards */
.card-list{list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:14px}
.card{display:block; padding:18px 20px; background:var(--surface); border:1px solid var(--border);
  border-radius:12px; box-shadow:var(--shadow); text-decoration:none; color:inherit; transition:transform .15s}
.card:hover{transform:translateY(-2px)}
.card h2{margin:0 0 6px; font-size:1.08rem; border:0; padding:0; color:var(--text)}
.card .cmeta{color:var(--accent); font-size:.82rem; margin-bottom:6px; font-weight:600}
.card .csum{color:var(--text-soft); font-size:.92rem}

@media (max-width:640px){
  body{padding:24px 16px 80px; font-size:16px}
  .header{margin:-24px -16px 20px; padding:24px 16px 18px}
  .inline-group{flex-direction:column}
}
"""

AUTOSAVE_JS = """
(function(){
  var NS = "study-anmok";
  function storageOk(){
    try{
      var t="__t__"+Date.now();
      window.localStorage.setItem(t,"1");
      window.localStorage.removeItem(t);
      return true;
    }catch(e){ return false; }
  }
  var OK = storageOk();
  var warnEl = document.getElementById("global-warning");
  if(!OK && warnEl){ warnEl.style.display = "block"; }

  function key(field){ return NS + ":" + field.dataset.key; }
  function isCheck(field){ return field.type === "checkbox"; }

  var timers = {};
  function debounceSave(field){
    var k = field.dataset.key;
    if(timers[k]) clearTimeout(timers[k]);
    timers[k] = setTimeout(function(){ saveField(field); }, isCheck(field) ? 0 : 500);
  }

  function statusEl(field){
    return document.querySelector('.save-status[data-for="' + field.dataset.key + '"]');
  }

  function saveField(field){
    var st = statusEl(field);
    if(!OK){
      if(st){ st.textContent = "저장 실패 — 아래 내보내기로 백업하세요"; st.className = "save-status err"; }
      return;
    }
    try{
      var v = isCheck(field) ? (field.checked ? "1" : "0") : field.value;
      window.localStorage.setItem(key(field), v);
      if(st){ st.textContent = (isCheck(field) || field.value) ? "저장됨 · 방금" : ""; st.className = "save-status"; }
    }catch(e){
      if(st){ st.textContent = "저장 실패 — 내보내기로 백업하세요"; st.className = "save-status err"; }
    }
  }

  function restoreAll(){
    if(!OK) return;
    document.querySelectorAll("[data-key]").forEach(function(field){
      var v = window.localStorage.getItem(key(field));
      if(v !== null){
        if(isCheck(field)){ field.checked = (v === "1"); }
        else { field.value = v; }
        var st = statusEl(field);
        if(st && (isCheck(field) ? v === "1" : v)){ st.textContent = "저장된 값 불러옴"; }
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function(){
    restoreAll();
    document.querySelectorAll("[data-key]").forEach(function(field){
      var ev = isCheck(field) ? "change" : "input";
      field.addEventListener(ev, function(){ debounceSave(field); });
    });

    var exportBtn = document.getElementById("export-btn");
    if(exportBtn){
      exportBtn.addEventListener("click", function(){
        var lines = [];
        document.querySelectorAll("[data-key]").forEach(function(field){
          var label = field.dataset.label;
          if(!label){
            var wrap = field.closest(".field") || field.closest(".inline-field") || field.closest(".checkfield") || field.closest(".qa-block");
            var labelEl = wrap ? wrap.querySelector(".field-label, .inline-field-label, .qa-question, span") : null;
            label = labelEl ? labelEl.textContent.trim() : field.dataset.key;
          }
          var value = isCheck(field) ? (field.checked ? "[v] 체크함" : "[ ] 안함") : (field.value.trim() || "(비어있음)");
          lines.push(label + "\\n" + value + "\\n");
        });
        var text = lines.join("\\n---\\n");
        if(navigator.clipboard && navigator.clipboard.writeText){
          navigator.clipboard.writeText(text).then(function(){
            exportBtn.textContent = "복사됨 ✓";
            setTimeout(function(){ exportBtn.textContent = "답변 내보내기"; }, 2000);
          }).catch(function(){ downloadText(text); });
        } else {
          downloadText(text);
        }
      });
    }

    var clearBtn = document.getElementById("clear-btn");
    if(clearBtn){
      clearBtn.addEventListener("click", function(){
        if(!window.confirm("이 페이지의 저장된 답변을 전부 지울까요? (다시 되돌릴 수 없어요)")) return;
        document.querySelectorAll("[data-key]").forEach(function(field){
          try{ window.localStorage.removeItem(key(field)); }catch(e){}
          field.value = "";
          var st = statusEl(field);
          if(st){ st.textContent = ""; }
        });
      });
    }
  });

  function downloadText(text){
    var blob = new Blob([text], {type:"text/plain;charset=utf-8"});
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = document.title.replace(/[^\\w가-힣0-9]+/g,"_") + "_answers.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
})();
"""

PAGE_TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESCRIPTION__">
<meta name="theme-color" content="#5b21b6">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<style>__CSS__</style>
</head>
<body>
<a class="back" href="../">← 오늘의 공부 목록</a>
<div class="header">
  <div class="eyebrow">오늘의공부 · 안목 훈련</div>
  <h1>__H1__</h1>
  <div class="meta">__GENRE__ · __ANMOK__</div>
</div>

<div class="oneliner">__ONELINER__</div>

<div class="field">
  <div class="field-label">학습일 (오늘 공부한 날짜)</div>
  <input type="date" class="field-input" data-key="__DATEKEY__">
  <span class="save-status" data-for="__DATEKEY__"></span>
</div>

<div id="global-warning" class="global-warning">이 브라우저에서는 자동저장(localStorage)이 꺼져 있어요. 사생활 보호 모드를 해제하거나, 아래 <strong>답변 내보내기</strong> 버튼으로 답을 복사해 옵시디언 원본에 직접 옮겨 적어주세요.</div>
<div class="callout-warn"><strong>저장 안내</strong>: 입력값은 이 브라우저(이 기기)에만 저장됩니다. 다른 기기·시크릿 모드·캐시 삭제 시 사라질 수 있어요. 중요한 답은 <strong>답변 내보내기</strong>로 옵시디언 원본에 옮겨 적어두는 걸 권장합니다.</div>

__BODY__

<div class="toolbar">
  <button type="button" id="export-btn" class="act">답변 내보내기</button>
  <button type="button" id="clear-btn" class="act secondary">이 페이지 저장 지우기</button>
</div>

<div class="daynav">
  __PREV_LINK__
  __NEXT_LINK__
</div>

<script>__AUTOSAVE_JS__</script>
</body>
</html>
"""

INDEX_TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>오늘의공부 · 안목 훈련</title>
<meta name="description" content="옵시디언 오늘의공부 시리즈를 직접 채워 넣는 인터랙티브 학습 노트">
<meta name="theme-color" content="#5b21b6">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<style>__CSS__</style>
</head>
<body>
<a class="back" href="../">← page 목록</a>
<div class="header">
  <div class="eyebrow">오늘의공부 · 안목 훈련</div>
  <h1>오늘의 공부 — 1주차</h1>
  <div class="meta">매일 배운 개념을 직접 채워 넣는 인터랙티브 학습 노트 · 총 __COUNT__일</div>
</div>
<ul class="card-list">
__CARDS__
</ul>
</body>
</html>
"""

CARD_TEMPLATE = """<li><a class="card" href="__HREF__/"><h2>__TITLE__</h2><div class="cmeta">__GENRE__ · __ANMOK__</div><div class="csum">__ONELINER__</div></a></li>"""
