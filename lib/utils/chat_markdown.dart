import 'package:flutter/material.dart';

/// Chuyển phần Markdown đơn giản mà Gemini hay trả về thành TextSpan để hiển thị gọn trong chat:
/// `**đậm**`, `*nghiêng*`, dòng bắt đầu bằng `* ` / `- ` thành gạch đầu dòng `•`,
/// tiêu đề `#`/`##` thành chữ đậm. Không phụ thuộc package ngoài.
TextSpan chatMarkdownSpan(String text, TextStyle baseStyle) {
  final spans = <InlineSpan>[];
  final lines = text.split('\n');
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    var lineStyle = baseStyle;

    // Gạch đầu dòng: giữ nguyên thụt lề, đổi "* " / "- " thành "• "
    final bullet = RegExp(r'^(\s*)[*-]\s+').firstMatch(line);
    if (bullet != null) {
      line = '${bullet.group(1)}• ${line.substring(bullet.end)}';
    }
    // Tiêu đề Markdown
    final heading = RegExp(r'^\s*#{1,6}\s+').firstMatch(line);
    if (heading != null) {
      line = line.substring(heading.end);
      lineStyle = baseStyle.copyWith(fontWeight: FontWeight.w700);
    }

    spans.addAll(_inlineSpans(line, lineStyle));
    if (i < lines.length - 1) spans.add(TextSpan(text: '\n', style: baseStyle));
  }
  return TextSpan(style: baseStyle, children: spans);
}

/// Tách `**đậm**` và `*nghiêng*` trong một dòng
List<InlineSpan> _inlineSpans(String line, TextStyle style) {
  final result = <InlineSpan>[];
  final pattern = RegExp(r'\*\*(.+?)\*\*|\*(\S(?:.*?\S)?)\*');
  var last = 0;
  for (final m in pattern.allMatches(line)) {
    if (m.start > last) result.add(TextSpan(text: line.substring(last, m.start), style: style));
    if (m.group(1) != null) {
      result.add(TextSpan(text: m.group(1), style: style.copyWith(fontWeight: FontWeight.w700)));
    } else {
      result.add(TextSpan(text: m.group(2), style: style.copyWith(fontStyle: FontStyle.italic)));
    }
    last = m.end;
  }
  if (last < line.length) result.add(TextSpan(text: line.substring(last), style: style));
  return result;
}
