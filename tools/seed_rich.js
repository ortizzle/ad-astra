/* Six weeks of realistic history so Stars renders as it will in November,
   not as it does on install day. */
(function(){
  const today = AZ.today();
  const cls = STUDY_CLASSES.map(c=>c.id);
  let n=0;
  for(let d=41; d>=0; d--){
    const ds = AZ.shift(today,-d);
    const wd = AZ.weekday(ds);
    if(wd===0 || (d%7===3)) continue;              // rest days -> imperfect streak
    const cid = cls[d % cls.length];
    const us = units(cid);
    const u = us[d % Math.max(1,us.length)];
    const total = 5, correct = 3 + (d%3);
    put({id:'log_r'+d, type:'log', mode:'quiz', classId:cid, unitId:u?u.id:'u',
         date:ds, at:Date.now()-d*86400000, correct:Math.min(correct,total), total,
         seconds:240+ (d%5)*40, xp:correct*10, hints:d%4===0?1:0,
         ansSeconds:180, ansCount:total});
    if(d%3===0) put({id:'focus_r'+d, type:'focus', classId:cid, minutes:25, date:ds,
         at:Date.now()-d*86400000, xp:25});
    if(d%5===0) put({id:'log_read'+d, type:'log', mode:'read', classId:'__all__',
         date:ds, at:Date.now()-d*86400000, minutes:30, xp:30, correct:0, total:0});
    n++;
  }
  /* per-question history: some strong, some shaky, some cleared for good */
  cls.forEach((cid,ci)=>{
    units(cid).slice(0,3).forEach((u,ui)=>{
      (u.questions||[]).forEach((q,qi)=>{
        const att = 1 + ((qi+ui) % 4);
        const cor = Math.max(0, att - (qi % 3 === 0 ? 1 : 0));
        put({id:'qstat_'+u.id+'_'+q.id, type:'qstat', qid:q.id, unitId:u.id,
             classId:cid, attempts:att, correct:cor, updatedAt:Date.now()-qi*3600000});
        if(qi % 7 === 3) put({id:'cleared_miss_'+u.id+'_'+q.id, type:'cleared',
             unitId:u.id, qid:q.id, q:q.q, on:AZ.shift(today,-(qi%20))});
        if(qi % 9 === 4) put({id:'miss_'+u.id+'_'+q.id, type:'miss', unitId:u.id,
             classId:cid, qid:q.id, q:q.q, opts:q.opts, ans:q.ans,
             right:q.opts[q.ans], box:qi%5, due:AZ.shift(today, (qi%5)-1), on:today});
      });
    });
  });
  checkBadges();
  return n;
})();
