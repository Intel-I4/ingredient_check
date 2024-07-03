def txt_label_change(change):  
    label = []
    for n in change:
        if n == "김치": 
            label.append("kimchi,")
        elif n == "포도씨유":
            label.append("grape seed oil,")
        elif n == "파":
            label.append("leek,")
        elif n == "고추가루":
            label.append("powdered red pepper,")
        elif n == "마늘":
            label.append("garlic,")
        elif n == "멸치육수":
            label.append("anchovy meat broth,")
        elif n == "두부":
            label.append("bean curd,")
        elif n == "참치":
            label.append("tuna,")
        elif n == "설탕":
            label.append("suga,")
            
    return label
    