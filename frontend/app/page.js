'use client'
import { Button } from "@nextui-org/react";
import { motion } from "framer-motion";
import Link from "next/link";

export default function Home() {
  return (
    <main className="light">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-100 to-purple-100"
      >
        <h1 className="text-4xl font-bold mb-6 text-gray-800">
          Welcome to Medical Assistant
        </h1>
        <p className="text-xl mb-8 text-center max-w-2xl px-4 text-gray-600">
          Get personalized medical advice through our interactive questionnaire.
        </p>
        <Link href="/questionnaire">
          <Button
            as={motion.button}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            color="primary"
            size="lg"
          >
            Try Now
          </Button>
        </Link>
      </motion.div>
    </main>
  );
}
