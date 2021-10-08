import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { ArtistMenuPage } from './artist-menu.page';
import { artistGraphicComponent } from './artist-graphic/artist-graphic.component';
import { ArtistFormComponent } from './artist-form/artist-form.component';

const routes: Routes = [
  {
    path: '',
    component: artistMenuPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  entryComponents: [ArtistFormComponent],
  declarations: [ArtistMenuPage, artistGraphicComponent, ArtistFormComponent],
})
export class ArtistMenuPageModule {}
