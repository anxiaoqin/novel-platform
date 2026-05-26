import{_ as O,R as y,p as d,m as a,s as l,a5 as t,F as b,S as k,T as p,j as E,M as r,r as s,$ as c,n as x,a1 as I,x as D,E as T}from"./index-DKbKOSLG.js";const J={class:"templates-page"},M={class:"page-header-bar"},P={class:"header-actions"},U={class:"templates-grid"},X={class:"template-header"},j={class:"template-icon"},R={class:"template-info"},q={class:"template-desc"},A={class:"template-fields"},G={class:"template-actions"},H={class:"preview-content"},K={class:"preview-placeholder"},Q={__name:"Templates",setup(W){const f=y("all"),g=y(!1),_=y(null),u=y(JSON.parse(localStorage.getItem("template_favorites")||"[]")),w=[{id:"char-basic",name:"角色基础设定",icon:"👤",category:"character",categoryLabel:"角色",desc:"适用于任何类型的角色基础信息记录",fields:["姓名","年龄","性别","外貌描述","性格特征","背景故事","核心动机","口头禅"],content:`## 角色基础设定

**姓名**：
**年龄**：
**性别**：
**外貌描述**：
**性格特征**：
**背景故事**：
**核心动机**：
**口头禅**：`},{id:"char-ability",name:"角色能力值",icon:"⚔️",category:"character",categoryLabel:"角色",desc:"量化角色各项能力，适用于玄幻/科幻/游戏类型",fields:["力量","敏捷","智力","魅力","体质","感知","特殊能力","能力上限"],content:`## 角色能力值

| 属性 | 数值 | 描述 |
|------|------|------|
| 力量 | /10 | |
| 敏捷 | /10 | |
| 智力 | /10 | |
| 魅力 | /10 | |
| 体质 | /10 | |
| 感知 | /10 | |

**特殊能力**：
**能力上限**：`},{id:"char-relation",name:"人物关系图谱",icon:"🕸️",category:"character",categoryLabel:"角色",desc:"梳理角色之间的复杂关系网络",fields:["角色名","关系对象","关系类型","关系描述","关系变化"],content:`## 人物关系图谱

| 角色 | 关系对象 | 关系类型 | 描述 |
|------|----------|----------|------|
| | | 师徒/朋友/敌对/恋人/亲人 | |
| | | | |

**关系变化记录**：`},{id:"world-basic",name:"世界观框架",icon:"🌍",category:"world",categoryLabel:"世界观",desc:"搭建一个完整故事世界的基础框架",fields:["世界名称","时代背景","地理概况","主要势力","核心规则","科技水平","历史大事件"],content:`## 世界观框架

**世界名称**：
**时代背景**：
**地理概况**：
**主要势力**：
**核心规则**：
**科技水平**：
**历史大事件**：`},{id:"world-magic",name:"魔法/修炼体系",icon:"✨",category:"world",categoryLabel:"世界观",desc:"构建玄幻世界的力量体系",fields:["体系名称","能量来源","修炼等级","突破条件","禁忌之术","体系限制"],content:`## 魔法/修炼体系

**体系名称**：
**能量来源**：
**修炼等级**：
1. 
2. 
3. 

**突破条件**：
**禁忌之术**：
**体系限制**：`},{id:"world-faction",name:"势力/组织设定",icon:"🏛️",category:"world",categoryLabel:"世界观",desc:"详细设定故事中的势力组织",fields:["组织名称","首领","成员规模","核心理念","领地范围","与其他势力关系","秘密"],content:`## 势力/组织设定

**组织名称**：
**首领**：
**成员规模**：
**核心理念**：
**领地范围**：
**与其他势力关系**：
**秘密**：`},{id:"plot-3act",name:"三幕式结构",icon:"🎭",category:"plot",categoryLabel:"情节",desc:"经典三幕式故事结构模板",fields:["第一幕：建置","触发事件","第一转折点","第二幕：对抗","中点","第二转折点","第三幕：解决","高潮"],content:`## 三幕式结构

### 第一幕：建置
- 日常世界：
- 触发事件：
- 第一转折点：

### 第二幕：对抗
- 上升行动：
- 中点：
- 下降行动：
- 第二转折点：

### 第三幕：解决
- 高潮：
- 结局：`},{id:"plot-hero",name:"英雄之旅",icon:"🗡️",category:"plot",categoryLabel:"情节",desc:"坎贝尔英雄之旅12阶段模板",fields:["日常世界","冒险召唤","拒绝召唤","遇见导师","跨越第一道门槛","考验/盟友/敌人","接近最深处","严峻考验","获得奖赏","返回之路","复活","携万灵丹归"],content:`## 英雄之旅

1. **日常世界**：
2. **冒险召唤**：
3. **拒绝召唤**：
4. **遇见导师**：
5. **跨越第一道门槛**：
6. **考验、盟友与敌人**：
7. **接近最深处**：
8. **严峻考验**：
9. **获得奖赏**：
10. **返回之路**：
11. **复活**：
12. **携万灵丹归**：`},{id:"plot-twist",name:"悬念与反转",icon:"🔄",category:"plot",categoryLabel:"情节",desc:"规划悬念埋设和反转设计",fields:["悬念线","埋设位置","揭示位置","反转类型","铺垫线索","读者预期","实际走向"],content:`## 悬念与反转

| 悬念线 | 埋设位置 | 揭示位置 | 反转类型 |
|--------|----------|----------|----------|
| | 第X章 | 第X章 | 身份反转/动机反转/结果反转 |

**铺垫线索**：
**读者预期**：
**实际走向**：`},{id:"chapter-outline",name:"章节大纲",icon:"📋",category:"chapter",categoryLabel:"章节",desc:"规划单章内容的大纲模板",fields:["章节标题","POV角色","时间线","场景地点","核心事件","情感曲线","伏笔埋设","章节结尾钩子"],content:`## 章节大纲

**章节标题**：
**POV角色**：
**时间线**：
**场景地点**：

### 核心事件

### 情感曲线
起 → 承 → 转 → 合

### 伏笔埋设

### 章节结尾钩子`},{id:"chapter-batch",name:"批量章节规划",icon:"📚",category:"chapter",categoryLabel:"章节",desc:"一次性规划10章的情节节奏",fields:["卷名","章节列表","每章核心事件","节奏标注","总字数规划"],content:`## 批量章节规划

**卷名**：

| 章节 | 标题 | 核心事件 | 节奏 | 字数 |
|------|------|----------|------|------|
| 第1章 | | | 紧张 | 3000 |
| 第2章 | | | 放松 | 2500 |
| 第3章 | | | 紧张 | 3000 |
| 第4章 | | | 高潮 | 4000 |
| 第5章 | | | 放松 | 2500 |
`}],$=E(()=>f.value==="all"?w:w.filter(o=>o.category===f.value)),h=o=>u.value.includes(o),L=o=>{u.value.includes(o)?u.value=u.value.filter(e=>e!==o):u.value.push(o),localStorage.setItem("template_favorites",JSON.stringify(u.value))},C=o=>{o&&navigator.clipboard.writeText(o.content).then(()=>{T.success("模板已复制到剪贴板，可粘贴到草稿或章节中使用")}).catch(()=>{T.success("模板内容已准备好，请在编辑器中手动复制")})},S=o=>{_.value=o,g.value=!0};return(o,e)=>{var V;const v=p("el-radio-button"),N=p("el-radio-group"),z=p("el-tag"),m=p("el-button"),B=p("el-icon"),F=p("el-dialog");return r(),d("div",J,[a("div",M,[e[9]||(e[9]=a("h2",null,"📦 素材库",-1)),a("div",P,[l(N,{modelValue:f.value,"onUpdate:modelValue":e[0]||(e[0]=n=>f.value=n),size:"default"},{default:t(()=>[l(v,{label:"all"},{default:t(()=>[...e[4]||(e[4]=[s("全部",-1)])]),_:1}),l(v,{label:"character"},{default:t(()=>[...e[5]||(e[5]=[s("角色",-1)])]),_:1}),l(v,{label:"world"},{default:t(()=>[...e[6]||(e[6]=[s("世界观",-1)])]),_:1}),l(v,{label:"plot"},{default:t(()=>[...e[7]||(e[7]=[s("情节",-1)])]),_:1}),l(v,{label:"chapter"},{default:t(()=>[...e[8]||(e[8]=[s("章节",-1)])]),_:1})]),_:1},8,["modelValue"])])]),a("div",U,[(r(!0),d(b,null,k($.value,n=>(r(),d("div",{key:n.id,class:"template-card"},[a("div",X,[a("span",j,c(n.icon),1),a("div",R,[a("h3",null,c(n.name),1),l(z,{size:"small",round:""},{default:t(()=>[s(c(n.categoryLabel),1)]),_:2},1024)]),h(n.id)?(r(),x(m,{key:0,text:"",type:"warning",onClick:i=>L(n.id)},{default:t(()=>[...e[10]||(e[10]=[s("★",-1)])]),_:1},8,["onClick"])):(r(),x(m,{key:1,text:"",onClick:i=>L(n.id)},{default:t(()=>[...e[11]||(e[11]=[s("☆",-1)])]),_:1},8,["onClick"]))]),a("p",q,c(n.desc),1),a("div",A,[(r(!0),d(b,null,k(n.fields,i=>(r(),d("div",{key:i,class:"field-item"},[l(B,null,{default:t(()=>[l(I(D))]),_:1}),a("span",null,c(i),1)]))),128))]),a("div",G,[l(m,{type:"primary",size:"small",round:"",onClick:i=>C(n)},{default:t(()=>[...e[12]||(e[12]=[s("使用模板",-1)])]),_:1},8,["onClick"]),l(m,{size:"small",round:"",onClick:i=>S(n)},{default:t(()=>[...e[13]||(e[13]=[s("预览",-1)])]),_:1},8,["onClick"])])]))),128))]),l(F,{modelValue:g.value,"onUpdate:modelValue":e[3]||(e[3]=n=>g.value=n),title:(V=_.value)==null?void 0:V.name,width:"600px"},{footer:t(()=>[l(m,{onClick:e[1]||(e[1]=n=>g.value=!1)},{default:t(()=>[...e[14]||(e[14]=[s("关闭",-1)])]),_:1}),l(m,{type:"primary",onClick:e[2]||(e[2]=n=>C(_.value))},{default:t(()=>[...e[15]||(e[15]=[s("使用此模板",-1)])]),_:1})]),default:t(()=>{var n;return[a("div",H,[(r(!0),d(b,null,k((n=_.value)==null?void 0:n.fields,i=>(r(),d("div",{key:i,class:"preview-field"},[a("label",null,c(i),1),a("div",K,"在此填写"+c(i)+"...",1)]))),128))])]}),_:1},8,["modelValue","title"])])}}},Z=O(Q,[["__scopeId","data-v-be773305"]]);export{Z as default};
