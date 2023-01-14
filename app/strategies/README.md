////1.  only buy or sell if not a strong trend (<30), set SL to $1000 , set TP to $4000, and BE $1000
// https://www.youtube.com/watch?v=r_HvNiWtwjw&ab_channel=PeakTradingResearch
#NATGAS 180'
#inputs: ADXThreshold(30), LoopBackShort(16), LoopBackLong(20)
#
#if time < 1000 then begin // buy before 10am
#if adx(15) < ADXThreshold then buy next bar at highest(high, LoopBackLong) stop;
#end;
#
#if (close[1] < close[2] and close[2]<close[3]) = false then begin // sellshort avoiding consecutive down closes
#If adx(15) < ADXThreshold then sellshort next bar at lowest(low, LoopBackShort) stop;
#end;
#
#Setstoploss(1000); Setprofittarget(4000); Setbreakeven(1000)

