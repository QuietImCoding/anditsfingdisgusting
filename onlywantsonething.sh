rm tmp/* 2>/dev/null

getpath() {
    echo $1 | rev | cut -d'/' -f1 | rev
}
cp template.png tmp/

profpic="$(python3 onlywantsonething.py $1)"
profloc="$(getpath $profpic)"
wget --directory-prefix tmp $profpic

uhash="$(echo $1 | shasum | cut -d' ' -f1 | tr -d [[:alpha:]])"
wantpic="$(python3 scrapr.py $uhash)"
wantloc="$(getpath $wantpic)"
wget --directory-prefix tmp $wantpic

convert tmp/$profloc -resize 200x200^ tmp/$profloc
convert tmp/template.png tmp/$profloc -geometry +50+50 -composite tmp/int_1.png
convert tmp/$wantloc -resize 650x275 tmp/$wantloc
convert tmp/int_1.png tmp/$wantloc -gravity Center -geometry +0+200 -composite tmp/out.png

open tmp/

