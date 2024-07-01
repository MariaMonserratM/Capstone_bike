import Footer from "@/components/footer";
import Hero from "@/components/hero";
import TopBar from "@/components/top-bar";
import style from "./page.module.css";

export default function Home() {
  return (
    <div className={style.main}>
      <TopBar />

      <div className={style.content}>
        <Hero />
      </div>

      <Footer />
    </div>
  );
}
