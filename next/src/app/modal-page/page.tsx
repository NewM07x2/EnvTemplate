"use client"
import React, { useState, useEffect } from 'react';
import { createPortal } from "react-dom";
import Modal from "./Modal";

interface ModalModel {
  children: React.ReactElement | React.ReactElement[];
}

const ModalPortal = ({ children }: ModalModel) => {
  const [targetElement, setTargetElement] = useState<Element | null>(null);

  useEffect(() => {
    setTargetElement(document.querySelector(".container.modal-area"));
  }, []);

  if (!targetElement) return null;

  return createPortal(children, targetElement);
};

export default function ModalPage() {
  const [modalOpen, setModalOpen] = useState(false);

  const openModal = () => setModalOpen(true);
  const closeModal = () => setModalOpen(false);

  return (
    <>
      <p className="text-4xl">modalPage</p>
      <div className="container modal-area z-10" />

      <button type="button" onClick={openModal} className='bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded'>
        モーダルを表示する
      </button>
      
      <ModalPortal>
        <Modal handleCloseClick={closeModal} isOpen={modalOpen} />
      </ModalPortal>
    </>
  );
}