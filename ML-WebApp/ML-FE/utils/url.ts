export const PREDICTOR_URL =  process.env.NODE_ENV === 'development' ? process.env.PREDICTOR_API : `https://ml-dockerized.onrender.com/predict`