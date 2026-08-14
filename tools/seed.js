    const ids = Object.keys(CLASS_BY_ID).filter(id=>!(CLASS_BY_ID[id]||{}).bookend);
    const [c1,c2,c3] = ids;
    const today = AZ.today();
    const mkItems = (n, wrong)=>{
      const out=[];
      for(let i=0;i<n;i++){
        const bad = wrong.includes(i);
        out.push({ c: bad?0:1,
          qt: bad ? 'A car travels 240 m in 12 s at constant velocity. What does the slope of its position-time graph represent?'
                  : 'Which quantity is measured in metres per second?',
          ch: bad ? 'the total distance travelled' : '20 m/s',
          ca: bad ? 'the speed of the car' : '' });
      }
      return out;
    };
    const mkQuiz=(id,cls,unit,correct,total,wrong,mins,at,extra={})=>{
      put({id:'unit-'+id,type:'unit',classId:cls,title:unit,status:'approved',cards:[],questions:[]});
      put(Object.assign({id:'log-'+id,type:'log',mode:'quiz',classId:cls,unitId:'unit-'+id,
        date:today, at:at, correct:correct, total:total, seconds:mins*60,
        xp:correct*10, hints:2, items:mkItems(total,wrong)}, extra));
      return 'log-'+id;
    };
    const l1 = mkQuiz('a',c1,'Unit 3: Constant Velocity',4,5,[2],9, Date.now()-5*3600e3);
    const l2 = mkQuiz('b',c2,'Wordly Wise Book 9 · Lesson 4',12,18,[1,4,7,9,12,15],14, Date.now()-4*3600e3);
    const l3 = mkQuiz('c',c3,'Unit 1: Key Terms',2,3,[0],4, Date.now()-2*3600e3,{partial:true});
    put({id:'log-d',type:'log',mode:'quiz',classId:c1,unitId:'__review__',date:today,
         at:Date.now()-3*3600e3,correct:6,total:7,seconds:480,xp:60,hints:0,items:mkItems(7,[3])});
    put({id:'log-e',type:'log',mode:'cards',classId:c2,unitId:'unit-b',date:today,
         at:Date.now()-6*3600e3,correct:0,total:0,seconds:420,xp:20,hints:0});
    put({id:'focus-a',type:'focus',classId:c3,minutes:25,date:today,at:Date.now()-1*3600e3,xp:25});
    put({id:'m1',type:'mood',when:'pre', logId:l1,readiness:5,feeling:4,date:today});
    put({id:'m2',type:'mood',when:'post',logId:l1,feeling:4,date:today});
    put({id:'m3',type:'mood',when:'pre', logId:l2,readiness:5,feeling:2,date:today});
    put({id:'m4',type:'mood',when:'post',logId:l2,feeling:2,date:today});
    put({id:'m5',type:'mood',when:'pre', logId:l3,readiness:3,feeling:3,date:today});
    // a few due misses
    for(let i=0;i<7;i++) put({id:'miss-'+i,type:'miss',classId: i<4?c2:c1, unitId:'unit-b',
      qid:'q'+i, q:'Q'+i, opts:['a','b','c','d'], ans:0, box:0, due:today});
    go('day',{date:today});