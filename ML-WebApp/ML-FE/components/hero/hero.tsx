"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import styles from "./hero.module.css";
import HeroDescription from "./hero-description";
import { setTimeout } from "timers";

const images = [
  // "https://images.pexels.com/photos/5768333/pexels-photo-5768333.jpeg", // Landscape Image 1
  // "https://images.pexels.com/photos/2553791/pexels-photo-2553791.jpeg", // Landscape Image 2
  // "https://images.pexels.com/photos/6813356/pexels-photo-6813356.jpeg",
  "/images/hero-1.jpg",
  "/images/hero-2.jpg",
  "/images/hero-3.jpg",
  "/images/hero-4.jpg",
];

export default function Hero() {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    let timeout: ReturnType<typeof setTimeout>;
    const interval = setInterval(() => {
      setIsVisible(false);

      timeout = setTimeout(() => {
        setCurrentImageIndex((prevIndex) =>
          prevIndex === images.length - 1 ? 0 : prevIndex + 1
        );
        setIsVisible(true);
      }, 3000);
      clearTimeout(timeout); // Match this to the CSS transition duration
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <section
      className={`bg-accent-content  relative flex flex-row   justify-between ${styles.wrapper}  rounded-lg mx-6`}
    >
      <div
        className={`flex items-center justify-start  ${styles.imageContainerDescription}`}
      >
        <HeroDescription />
      </div>
      <div className={`inset-0  ${styles.imageContainer} `}>
        {images.map((image, index) => (
          <Image
            priority
            key={index}
            alt={`hero-img-${index}`}
            src={image}
            fill
            sizes="50vh, 100vh"
            style={{
              objectFit: "cover",
            }}
            className={`${styles.imageContainerImg} ${
              index === currentImageIndex && isVisible
                ? styles.imageContainerImgVisible
                : ""
            }`}
          />
        ))}
      </div>
    </section>
  );
}
