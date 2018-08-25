ps | grep hadron | awk '{print$1}' | xargs kill
ps | grep anaconda | awk '{print$1}' | xargs kill

