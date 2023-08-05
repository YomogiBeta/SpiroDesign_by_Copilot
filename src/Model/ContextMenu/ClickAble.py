#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bridge_pyjs.PygameBridge import pygame
from bridge_pyjs.ABCBridge import ABC, abstractmethod

__author__ = 'Yomogiβ'
__version__ = '1.0.1'
__date__ = '2023/05/19 (Created: 2023/05/01 )'


class ClickAble(ABC):
    """クリック可能なオブジェクトのベースとなるクラスです。

    これを継承すると、pygameにてオブジェクトがclick ableになります。
    これはabstractクラスであり、継承して使う必要があります。
    """
    rect: pygame.Rect = None
    hoverd = False
    prepare_click = False

    def set_rect(self, rect: pygame.Rect) -> None:
        """クリック可能なオブジェクトの範囲を設定します。

        Args:
            rect (pygame.Rect):
                クリック可能なオブジェクトの範囲を示すRectオブジェクト
        """
        self.rect = rect

    @abstractmethod
    def hover_in(self) -> None:
        """マウスがオブジェクトに乗った時の処理を行います。"""
        pass

    @abstractmethod
    def hover_out(self) -> None:
        """マウスがオブジェクトから離れた時の処理を行います。"""
        pass

    @abstractmethod
    def click(self) -> None:
        """オブジェクトがクリックされた時の処理を行います。"""
        pass

    def check_hover_me(self, event: pygame.event.Event) -> None:
        """マウスがオブジェクトに乗っているかどうかを判定します。

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        if self.rect is not None:
            if self.rect.collidepoint(event.pos):
                if not self.hoverd:
                    self.hoverd = True
                    self.hover_in()
            else:
                if self.hoverd:
                    self.hoverd = False
                    self.hover_out()

    def check_down_me(self, event: pygame.event.Event) -> None:
        """オブジェクトにマウスダウンイベントが発生したかどうかの判定をします

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        if self.rect is not None:
            if self.rect.collidepoint(event.pos):
                self.prepare_click = True

    def check_click_me(self, event: pygame.event.Event) -> None:
        """オブジェクトがクリックされたかどうかを判定します。

        Args:
            event (pygame.event.Event):
                pygameのイベントオブジェクト
        """
        if self.rect is not None:
            if self.rect.collidepoint(event.pos) and self.prepare_click:
                self.click()
            elif self.prepare_click:
                self.prepare_click = False
