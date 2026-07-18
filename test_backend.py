from backend.predictor import predict_pcos

sample = {
    "Age (yrs)": 24,
    "Weight (Kg)": 55,
    "Pregnant(Y/N)": 0,
    "No. of abortions": 0,
    "Weight gain(Y/N)": 0,
    "hair growth(Y/N)": 0,
    "Skin darkening (Y/N)": 0,
    "Hair loss(Y/N)": 0,
    "Pimples(Y/N)": 0,
    "Fast food (Y/N)": 0,
    "FSH/LH": 1.5,
    "Follicle No. (L)": 8,
    "Follicle No. (R)": 8,
    "Cycle(R/I)": 0,
    "Cycle length(days)": 28
}

prediction, probability = predict_pcos(sample)

print("Prediction :", prediction)
print("Probability :", probability)