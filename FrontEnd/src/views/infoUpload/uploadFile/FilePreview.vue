<template>
    <div class="file-preview">
        <div v-if="file" class="file-preview__content">
            <!-- 为不同类型的文件添加预览功能 -->
            <div v-if="isDocumentFile" class="document-preview">
                <!-- 在此处实现文档文件的预览功能，例如使用 PDF.js 预览 PDF 文件 -->
            </div>
            <div v-else-if="isSpreadsheetFile" class="spreadsheet-preview">
                <!-- 在此处实现表格文件的预览功能，例如使用 SheetJS 预览 XLSX/XLS/CSV 文件 -->
            </div>
        </div>
        <div v-else class="file-preview__no-file">
            请选择文件进行预览
        </div>
    </div>
</template>
  
<script>
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
            const spreadsheetExtensions = ["xlsx", "xls", "csv"];
            return this.file && spreadsheetExtensions.includes(this.file.extension);
        },
    },
};
</script>
  
<style scoped>
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

.spreadsheet-preview {
    width: 100%;
    height: 100%;
}
</style>
  