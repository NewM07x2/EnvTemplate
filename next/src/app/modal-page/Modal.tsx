import React, { useEffect, useState } from "react";
import "./Modal.css";

interface ModalProps {
  handleCloseClick: () => void;
  isOpen: boolean;
}

const Modal = ({ handleCloseClick, isOpen }: ModalProps) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
    } else {
      const timer = setIsVisible(false);
    }
  }, [isOpen]);

  return (
    <div className={`modal ${isVisible ? 'visible' : ''}`}>
      <div className="modal__content flex flex-col items-center space-y-4">
        <p>モーダルを表示しました。</p>
        <button type="button" onClick={handleCloseClick} className='bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded'>
          閉じる
        </button>
      </div>
    </div>
  );
};

export default Modal;