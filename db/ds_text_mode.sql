-- ds_text: режим страницы — текстовая (wysiwyg) или конструктор блоков.
-- text  — body хранит HTML из wysiwyg (поведение по умолчанию);
-- blocks — body хранит JSON конверта svcms.page_blocks (только блоки type=text).
ALTER TABLE ds_text
  ADD COLUMN mode ENUM('text','blocks') NOT NULL DEFAULT 'text' AFTER body;
