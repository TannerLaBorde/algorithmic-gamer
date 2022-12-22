call conda activate ava310
nbdev_clean
nbdev_test
nbdev_export
git add . 
git commit -m %1
git push