<template>
    <div class="file-preview">
        <div v-if="file" class="file-preview__content">
            <button @click="previewFile" class="preview-button">预览文件</button>
            <div v-if="isDocumentFile" class="document-preview" ref="documentPreview">
                <!-- 使用 PDF.js 预览 PDF 文件 -->
            </div>
            <div v-else-if="isSpreadsheetFile" class="spreadsheet-preview" ref="spreadsheetPreview">
                <!-- 使用 SheetJS 预览 XLSX/XLS/CSV 文件 -->
            </div>
        </div>
        <div v-else class="file-preview__no-file">
            请选择文件进行预览
        </div>
    </div>
</template>
  
<script>
// 还是有bug，暂未启用！！！！

// import mammoth from "mammoth";
import { Document, Packer } from "docx";
import { ElMessage } from 'element-plus';
import { Message } from '@element-plus/icons-vue';
import PDFJS from 'pdfjs-dist/legacy/build/pdf.js'; // 引入 PDF.js
import * as XLSX from 'xlsx';
// import XLSX from "xlsx";

export default {
    props: {
        file: Object,
    },
    computed: {
        isDocumentFile() {
            const documentExtensions = ["pdf", "doc", "docx"];
            return this.file && documentExtensions.includes(this.file.extension);
        },
        isSpreadsheetFile() {
            const
                spreadsheetExtensions = ["xlsx", "xls", "csv"];
            return this.file && spreadsheetExtensions.includes(this.file.extension);
        },
    },
    watch: {
        file: {
            handler(newFile) {
                if (this.isDocumentFile) {
                    this.previewDocumentFile(newFile);
                } else if (this.isSpreadsheetFile) {
                    this.previewSpreadsheetFile(newFile);
                }
            },
            immediate: true,
        },
    },
    methods: {
        async previewDocumentFile(file) {
            if (file.extension === "pdf") {
                this.previewPdf(file); // 支持 PDF 预览
            } else if (file.extension === "doc") {
                // const docxFile = await this.convertDocToDocx(file);
                // this.previewDocx(docxFile);
                ElMessage.error("暂不支持doc文件预览");
            } else if (file.extension === "docx") {
                ElMessage.error("暂不支持docx文件预览");
                // this.previewDocx(file);
            }
        },
        // 添加预览 PDF 的方法
        async previewPdf(file) {
            const reader = new FileReader();
            reader.onload = async (event) => {
                const loadingTask = PDFJS.getDocument(event.target.result);
                const pdf = await loadingTask.promise;
                const numPages = pdf.numPages;            // 清空之前的预览内容
                this.$refs.documentPreview.innerHTML = "";

                // 循环添加 PDF 页面
                for (let i = 1; i <= numPages; i++) {
                    const page = await pdf.getPage(i);
                    const canvas = document.createElement("canvas");
                    const context = canvas.getContext("2d");
                    const viewport = page.getViewport({ scale: 1 });

                    canvas.width = viewport.width;
                    canvas.height = viewport.height;

                    await page.render({
                        canvasContext: context,
                        viewport: viewport,
                    }).promise;

                    this.$refs.documentPreview.appendChild(canvas);
                }
            };
            reader.readAsArrayBuffer(file);
        },
        //添加预览xls等文件的方法
        async previewSpreadsheetFile(file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const data = event.target.result;
                const workbook = XLSX.read(data, { type: "binary" });

                // 清空之前的预览内容
                this.$refs.spreadsheetPreview.innerHTML = "";

                // 遍历每个工作表并渲染它们
                workbook.SheetNames.forEach((sheetName) => {
                    const worksheet = workbook.Sheets[sheetName];
                    const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });                // 创建一个表格并设置相应的样式
                    const table = document.createElement("table");
                    table.style.borderCollapse = "collapse";
                    table.style.width = "100%";
                    table.style.marginBottom = "20px";

                    jsonData.forEach((row) => {
                        const tr = document.createElement("tr");

                        row.forEach((cell) => {
                            const td = document.createElement("td");
                            td.style.border = "1px solid #ddd";
                            td.style.padding = "8px";
                            td.textContent = cell;
                            tr.appendChild(td);
                        });

                        table.appendChild(tr);
                    });

                    // 添加表格到预览区域
                    this.$refs.spreadsheetPreview.appendChild(table);
                });
            };

            if (file.extension === "csv") {
                reader.readAsBinaryString(file);
            } else {
                reader.readAsArrayBuffer(file);
                reader.onload = () => {
                    const data = new Uint8Array(reader.result);
                    reader.readAsBinaryString(new Blob([data]));
                };
            }
        },
    },

};
</script>

<style style scoped >
.file-preview {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    padding: 20px;
    border-left: 1px solid #ebeef5;
    overflow-y: auto;
}

.file-preview__no-file {
    display: flex;
    flex-grow: 1;
    justify-content: center;
    align-items: center;
}

.document-preview {
    width: 100%;
    height: 100%;
    overflow-y: auto;
}

.spreadsheet-preview {
    width: 100%;
    height: 100%;
}
</style >  