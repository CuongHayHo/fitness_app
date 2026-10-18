import 'dart:io' show Platform;

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';

/// Chữ một dòng tự cuộn ngang (marquee) khi dài hơn ô chứa; vừa ô thì đứng yên như `Text`.
/// Thay cho `Text(..., maxLines: 1, overflow: TextOverflow.ellipsis)` để người dùng đọc được
/// toàn bộ nội dung thay vì bị cắt thành "…". Chu kỳ: đứng 1,5 s → cuộn hết → đứng 1 s → về đầu.
class MarqueeText extends StatefulWidget {
  final String data;
  final TextStyle? style;
  final TextAlign? textAlign;

  /// Giữ tham số để thay thế trực tiếp cho `Text`; MarqueeText luôn hiển thị 1 dòng.
  final int? maxLines;
  final TextOverflow? overflow;

  /// Tốc độ cuộn (logical pixel / giây)
  final double velocity;

  const MarqueeText(
    this.data, {
    super.key,
    this.style,
    this.textAlign,
    this.maxLines,
    this.overflow,
    this.velocity = 35,
  });

  /// Trong `flutter test` không chạy hoạt ảnh vô hạn (tránh treo pumpAndSettle)
  static final bool _disabled =
      !kIsWeb && Platform.environment.containsKey('FLUTTER_TEST');

  @override
  State<MarqueeText> createState() => _MarqueeTextState();
}

class _MarqueeTextState extends State<MarqueeText> {
  final ScrollController _scroll = ScrollController();
  bool _running = false;

  @override
  void dispose() {
    _running = false;
    _scroll.dispose();
    super.dispose();
  }

  Future<void> _loop() async {
    if (_running) return;
    _running = true;
    while (mounted && _running) {
      await Future.delayed(const Duration(milliseconds: 1500));
      if (!mounted || !_running || !_scroll.hasClients) continue;
      final max = _scroll.position.maxScrollExtent;
      if (max <= 0) continue;
      await _scroll.animateTo(
        max,
        duration: Duration(milliseconds: (max / widget.velocity * 1000).round()),
        curve: Curves.linear,
      );
      await Future.delayed(const Duration(milliseconds: 1000));
      if (mounted && _scroll.hasClients) _scroll.jumpTo(0);
    }
  }

  @override
  Widget build(BuildContext context) {
    final style = DefaultTextStyle.of(context).style.merge(widget.style);
    return LayoutBuilder(
      builder: (context, constraints) {
        final painter = TextPainter(
          text: TextSpan(text: widget.data, style: style),
          maxLines: 1,
          textDirection: Directionality.of(context),
          textScaler: MediaQuery.textScalerOf(context),
        )..layout();
        final overflows =
            constraints.maxWidth.isFinite && painter.width > constraints.maxWidth;

        if (!overflows || MarqueeText._disabled) {
          _running = false;
          return Text(
            widget.data,
            style: widget.style,
            textAlign: widget.textAlign,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          );
        }

        if (!_running) {
          WidgetsBinding.instance.addPostFrameCallback((_) => _loop());
        }
        return SingleChildScrollView(
          controller: _scroll,
          scrollDirection: Axis.horizontal,
          physics: const NeverScrollableScrollPhysics(),
          child: Text(widget.data, style: widget.style, maxLines: 1, softWrap: false),
        );
      },
    );
  }
}
